import { NextResponse } from "next/server";
import { generateVisionJsonResponse, isAIConfigured } from "@/lib/ai";
import { DEMO_DATA } from "@/lib/demo-data";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  try {
    const { image } = await req.json();

    if (isAIConfigured() && image) {
      const parsed = await generateVisionJsonResponse(
        `Identify the industrial machine in this image. Return JSON with format: {"matches":[{"name":"string","model":"string","category":"string","confidence":0.0-1.0}]}. Return top 3 matches from common industrial equipment: CNC, pumps, compressors, motors, generators, conveyors, presses, lathes, welders, boilers, chillers, forklifts, PLCs, transformers.`,
        image
      );
      const matches = (((parsed.matches as Array<{ name: string; model: string; confidence: number }> | undefined) ?? [])).slice(0, 3).map(
        (m: { name: string; model: string; confidence: number }, i: number) => {
          const machine = DEMO_DATA.machines.find(
            (dm) =>
              dm.name.toLowerCase().includes(m.name?.toLowerCase()?.split(" ")[0] ?? "") ||
              dm.model?.toLowerCase().includes(m.model?.toLowerCase()?.split(" ")[0] ?? "")
          ) ?? DEMO_DATA.machines[i % DEMO_DATA.machines.length];

          return {
            id: machine.id,
            name: m.name ?? machine.name,
            model: m.model ?? machine.model,
            confidence: m.confidence ?? 0.85 - i * 0.1,
            image_url: machine.images?.[0] || machine.image_url,
          };
        }
      );

      return NextResponse.json({ matches });
    }

    // Demo fallback without OpenAI
    const demoMatches = DEMO_DATA.machines.slice(0, 3).map((m, i) => ({
      id: m.id,
      name: m.name,
      model: m.model,
      confidence: 0.92 - i * 0.08,
      image_url: m.images?.[0] || m.image_url,
    }));

    return NextResponse.json({ matches: demoMatches });
  } catch (error) {
    console.error("identify-machine error:", error);
    return NextResponse.json(
      { matches: DEMO_DATA.machines.slice(0, 3).map((m, i) => ({ id: m.id, name: m.name, model: m.model, confidence: 0.85 - i * 0.1, image_url: m.images?.[0] || m.image_url })) },
      { status: 200 }
    );
  }
}
