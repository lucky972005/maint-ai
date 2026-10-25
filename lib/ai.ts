import OpenAI from "openai";

export type AIProvider = "openai" | "gemini" | "groq";

type TextMessage = {
  role: "system" | "user" | "assistant";
  content: string;
};

function getGeminiModel(): string {
  const envModel = process.env.GEMINI_MODEL;
  if (!envModel || envModel.includes("gemini-1.5") || envModel === "gemini-2.5-flash" || envModel === "gemini-2.5-flash-lite") {
    return "gemini-3.7-flash";
  }
  return envModel;
}

const OPENAI_MODEL = process.env.OPENAI_MODEL || "gpt-4o";
const GEMINI_MODEL = getGeminiModel();
const GROQ_MODEL = process.env.GROQ_MODEL || "llama-3.3-70b-versatile";

function getRequestedProvider(): AIProvider | "auto" {
  const provider = process.env.AI_PROVIDER?.toLowerCase();
  if (provider === "openai" || provider === "gemini" || provider === "groq") return provider;
  return "auto";
}

export function getAIProvider(): AIProvider | null {
  const requested = getRequestedProvider();
  const hasOpenAI = Boolean(process.env.OPENAI_API_KEY);
  const hasGemini = Boolean(process.env.GEMINI_API_KEY);
  const hasGroq = Boolean(process.env.GROQ_API_KEY);

  if (requested === "openai" && hasOpenAI) return "openai";
  if (requested === "gemini" && hasGemini) return "gemini";
  if (requested === "groq" && hasGroq) return "groq";
  if (requested === "auto") {
    if (hasGroq) return "groq";
    if (hasOpenAI) return "openai";
    if (hasGemini) return "gemini";
  }

  return null;
}

// Get vision provider separately - prefer Gemini (free) or OpenAI
export function getVisionProvider(): AIProvider | null {
  const hasOpenAI = Boolean(process.env.OPENAI_API_KEY);
  const hasGemini = Boolean(process.env.GEMINI_API_KEY);

  // Prefer Gemini for vision (free tier), fallback to OpenAI
  if (hasGemini) return "gemini";
  if (hasOpenAI) return "openai";

  return null;
}

export function isAIConfigured(): boolean {
  return getAIProvider() !== null;
}

function getOpenAIClient() {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    throw new Error("OPENAI_API_KEY is not configured");
  }
  return new OpenAI({ apiKey });
}

function normalizeMessages(messages: TextMessage[]) {
  const systemPrompt = messages.find((message) => message.role === "system")?.content ?? "";
  const chatMessages = messages.filter((message) => message.role !== "system");
  return { systemPrompt, chatMessages };
}

function extractTextFromGeminiResponse(response: unknown): string {
  const data = response as {
    candidates?: Array<{
      content?: { parts?: Array<{ text?: string }> };
    }>;
  };
  return data.candidates?.[0]?.content?.parts?.map((part) => part.text ?? "").join("") ?? "";
}

function extractJson(text: string): unknown {
  const trimmed = text.trim();
  if (!trimmed) return {};
  if (trimmed.startsWith("{") || trimmed.startsWith("[")) {
    return JSON.parse(trimmed);
  }

  const match = trimmed.match(/\{[\s\S]*\}/);
  if (match) {
    return JSON.parse(match[0]);
  }

  return {};
}

async function callOpenAIText(messages: TextMessage[], maxTokens = 800): Promise<string> {
  const openai = getOpenAIClient();
  const response = await openai.chat.completions.create({
    model: OPENAI_MODEL,
    messages,
    max_tokens: maxTokens,
  });
  return response.choices[0].message.content ?? "";
}

async function callGeminiText(messages: TextMessage[], maxOutputTokens = 800): Promise<string> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error("GEMINI_API_KEY is not configured");
  }

  const { systemPrompt, chatMessages } = normalizeMessages(messages);
  const contents = chatMessages.map((message) => ({
    role: message.role === "assistant" ? "model" : "user",
    parts: [{ text: message.content }],
  }));

  const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${apiKey}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      systemInstruction: systemPrompt ? { parts: [{ text: systemPrompt }] } : undefined,
      contents,
      generationConfig: { temperature: 0.2, maxOutputTokens },
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error("Gemini API error:", response.status, errorText);
    throw new Error(`Gemini request failed with status ${response.status}`);
  }

  const data = await response.json();
  return extractTextFromGeminiResponse(data);
}

async function callGroqText(messages: TextMessage[], maxTokens = 800): Promise<string> {
  const apiKey = process.env.GROQ_API_KEY;
  if (!apiKey) {
    throw new Error("GROQ_API_KEY is not configured");
  }

  const openai = new OpenAI({
    apiKey,
    baseURL: "https://api.groq.com/openai/v1",
    maxRetries: 0,
  });

  const response = await openai.chat.completions.create({
    model: GROQ_MODEL,
    messages,
    max_tokens: maxTokens,
  });

  return response.choices[0].message.content ?? "";
}

export async function generateTextResponse(messages: TextMessage[], maxTokens = 800): Promise<string> {
  const provider = getAIProvider();
  if (!provider) {
    throw new Error("No AI provider configured");
  }

  if (provider === "openai") {
    return callOpenAIText(messages, maxTokens);
  }

  if (provider === "groq") {
    return callGroqText(messages, maxTokens);
  }

  return callGeminiText(messages, maxTokens);
}

export async function generateJsonResponse(messages: TextMessage[], maxTokens = 800): Promise<Record<string, unknown>> {
  const text = await generateTextResponse(messages, maxTokens);
  return extractJson(text) as Record<string, unknown>;
}

export async function generateVisionJsonResponse(
  prompt: string,
  imageBase64?: string,
  mimeType = "image/jpeg",
  maxOutputTokens = 1500
): Promise<Record<string, unknown>> {
  const provider = getVisionProvider();
  if (!provider) {
    throw new Error("Vision requires OpenAI or Gemini API key (Groq doesn't support image analysis)");
  }

  if (provider === "openai") {
    const openai = getOpenAIClient();
    const response = await openai.chat.completions.create({
      model: OPENAI_MODEL,
      messages: [
        {
          role: "user",
          content: [
            { type: "text", text: prompt },
            ...(imageBase64 ? [{ type: "image_url" as const, image_url: { url: `data:${mimeType};base64,${imageBase64}` } }] : []),
          ],
        },
      ],
      response_format: { type: "json_object" },
      max_tokens: maxOutputTokens,
    });

    return extractJson(response.choices[0].message.content ?? "") as Record<string, unknown>;
  }

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error("GEMINI_API_KEY is not configured");
  }

  const parts: Array<{ text?: string; inlineData?: { mimeType: string; data: string } }> = [{ text: prompt }];
  if (imageBase64) {
    parts.push({ inlineData: { mimeType, data: imageBase64 } });
  }

  const candidateModels = Array.from(new Set([GEMINI_MODEL, "gemini-3.6-flash", "gemini-3.5-flash"]));
  let lastError: Error | null = null;

  for (const model of candidateModels) {
    try {
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ role: "user", parts }],
          generationConfig: { responseMimeType: "application/json", temperature: 0.1, maxOutputTokens },
        }),
      });

      if (!response.ok) {
        const errText = await response.text().catch(() => "");
        console.warn(`Gemini vision request with ${model} failed (${response.status}): ${errText}`);
        if (response.status === 503 || response.status === 429) {
          lastError = new Error(`Model ${model} status ${response.status}: ${errText}`);
          continue; // Try next fallback model
        }
        throw new Error(`Gemini vision request failed with status ${response.status}: ${errText}`);
      }

      const data = await response.json();
      return extractJson(extractTextFromGeminiResponse(data)) as Record<string, unknown>;
    } catch (err) {
      lastError = err instanceof Error ? err : new Error(String(err));
      console.warn(`Gemini vision error with model ${model}:`, lastError.message);
    }
  }

  throw lastError || new Error("All Gemini vision models failed");
}


