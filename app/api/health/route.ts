import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function GET() {
  const startTime = Date.now();
  const uptimeSeconds = Math.floor(process.uptime());
  const memory = process.memoryUsage();

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const isSupabaseConfigured =
    Boolean(supabaseUrl) &&
    !supabaseUrl?.includes("placeholder-project") &&
    Boolean(process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY);

  const aiProvider = process.env.AI_PROVIDER || "groq";
  const hasGroqKey = Boolean(process.env.GROQ_API_KEY);
  const hasGeminiKey = Boolean(process.env.GEMINI_API_KEY);
  const hasOpenAiKey = Boolean(process.env.OPENAI_API_KEY);

  const aiStatus = {
    provider: aiProvider,
    groqConfigured: hasGroqKey,
    geminiConfigured: hasGeminiKey,
    openaiConfigured: hasOpenAiKey,
    mode: (hasGroqKey || hasGeminiKey || hasOpenAiKey) ? "live" : "demo_fallback",
  };

  const responseTimeMs = Date.now() - startTime;

  return NextResponse.json(
    {
      status: "healthy",
      service: "maintai-assistant",
      version: process.env.npm_package_version || "0.1.0",
      timestamp: new Date().toISOString(),
      uptime: `${uptimeSeconds}s`,
      uptimeSeconds,
      environment: process.env.NODE_ENV || "development",
      checks: {
        database: {
          status: isSupabaseConfigured ? "configured" : "demo_mode",
          type: "supabase",
        },
        ai: aiStatus,
      },
      system: {
        nodeVersion: process.version,
        platform: process.platform,
        arch: process.arch,
        memoryUsageMb: {
          rss: Math.round((memory.rss / 1024 / 1024) * 100) / 100,
          heapTotal: Math.round((memory.heapTotal / 1024 / 1024) * 100) / 100,
          heapUsed: Math.round((memory.heapUsed / 1024 / 1024) * 100) / 100,
        },
      },
      latencyMs: responseTimeMs,
    },
    {
      status: 200,
      headers: {
        "Cache-Control": "no-store, no-cache, must-revalidate",
      },
    }
  );
}
