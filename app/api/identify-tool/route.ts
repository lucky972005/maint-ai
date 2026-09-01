import { NextResponse } from "next/server";
import { generateVisionJsonResponse, isAIConfigured } from "@/lib/ai";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  try {
    const { image, expectedTool } = await req.json();

    if (isAIConfigured() && image) {
      const result = await generateVisionJsonResponse(
        `Identify the tool in this image. Expected tool: ${expectedTool}. Return JSON: {"detected":"string","confidence":0.0-1.0,"isCorrect":boolean,"alternative_guesses":["string"]}. Tools: screwdriver, wrench, pliers, hammer, drill, allen_key, multimeter, socket_set.`,
        image
      );
      const confidence = typeof result.confidence === "number" ? result.confidence : 0;
      const isCorrect = typeof result.isCorrect === "boolean" ? result.isCorrect : confidence > 0.8;
      return NextResponse.json({
        detected: result.detected ?? result.tool ?? "unknown",
        confidence,
        isCorrect,
        alternative_guesses: result.alternative_guesses ?? [],
      });
    }

    // Demo mode: accept expected tool with high confidence
    const normalized = expectedTool?.toLowerCase().replace(/\s/g, "_") ?? "";
    return NextResponse.json({
      detected: normalized,
      confidence: 0.95,
      isCorrect: true,
      alternative_guesses: [],
    });
  } catch (error) {
    console.error("identify-tool error:", error);
    return NextResponse.json({ detected: "unknown", confidence: 0, isCorrect: false }, { status: 200 });
  }
}
