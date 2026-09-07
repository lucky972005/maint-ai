import { NextResponse } from "next/server";
import { generateVisionJsonResponse, isAIConfigured } from "@/lib/ai";
import { getMachines, getProceduresForMachine } from "@/lib/database";
import type { Machine } from "@/lib/types";

export const dynamic = "force-dynamic";

interface AiMatchItem {
  id?: string;
  name?: string;
  model?: string;
  category?: string;
  confidence?: number;
  reasoning?: string;
  detected_features?: string[];
}

export async function POST(req: Request) {
  try {
    const { image, mimeType = "image/jpeg" } = await req.json();

    if (!image) {
      return NextResponse.json({ error: "Image data is required" }, { status: 400 });
    }

    // 1. Fetch real machines from database
    const allMachines = await getMachines();
    if (!allMachines || allMachines.length === 0) {
      return NextResponse.json({ error: "No machines found in database", matches: [] }, { status: 404 });
    }

    if (isAIConfigured()) {
      // 2. Prepare database catalog summary for the AI vision prompt
      const catalog = allMachines.map((m) => ({
        id: m.id,
        name: m.name,
        model: m.model,
        category: m.category,
        manufacturer: m.manufacturer,
        location: m.location,
        serial_number: m.serial_number,
        specs: m.specs,
      }));

      const prompt = `You are an expert industrial machinery vision AI.
Examine this image of an industrial machine or equipment carefully.
Compare what you observe in the image against our registered database of machines:

REGISTERED MACHINES DATABASE:
${JSON.stringify(catalog, null, 2)}

INSTRUCTIONS:
1. Identify the visual characteristics, mechanical parts, shape, hoses, pump casings, cylinders, motors, radiators, forks, screens, enclosures, or manufacturer badges in the photo.
2. Determine which machine(s) in the registered database catalog best match what is shown in the image.
3. Select up to 3 candidate matches from the database catalog, sorted by highest confidence.
4. Assign a realistic confidence score (0.0 to 1.0):
   - 0.85 - 0.99: Strong visual evidence matches the exact machine type/model.
   - 0.65 - 0.84: Equipment category or general appearance matches well.
   - Below 0.65: Low visual confidence or partial match.
5. Provide a clear reasoning explaining specifically what visual cues matched (e.g., "Vertical multistage pump casing and Grundfos motor flange identified", "Counterbalance forklift chassis with vertical mast and forks observed").
6. List key detected visual features.

Return ONLY a valid JSON object with this exact structure:
{
  "identified_type": "string describing what equipment is visible in the photo",
  "matches": [
    {
      "id": "exact-machine-id-from-database",
      "confidence": 0.95,
      "reasoning": "Clear explanation of visual match",
      "detected_features": ["feature 1", "feature 2"]
    }
  ]
}`;

      const parsed = await generateVisionJsonResponse(prompt, image, mimeType, 1500);

      const rawMatches: AiMatchItem[] = Array.isArray(parsed.matches)
        ? (parsed.matches as AiMatchItem[])
        : [];

      // 3. Match AI output to actual database machine records
      const resolvedMatches: Array<{
        machine: Machine;
        confidence: number;
        reasoning: string;
        detected_features: string[];
      }> = [];

      const matchedIds = new Set<string>();

      for (const item of rawMatches) {
        if (!item) continue;

        // Try exact ID match first
        let machine = allMachines.find((m) => m.id === item.id);

        // Fallback: match by name or model if ID was altered by AI
        if (!machine && (item.name || item.model)) {
          const searchName = (item.name || "").toLowerCase();
          const searchModel = (item.model || "").toLowerCase();
          machine = allMachines.find((m) => {
            const mName = m.name.toLowerCase();
            const mModel = (m.model || "").toLowerCase();
            return (
              (searchModel && (mModel.includes(searchModel) || searchModel.includes(mModel))) ||
              (searchName && (mName.includes(searchName) || searchName.includes(mName)))
            );
          });
        }

        if (machine && !matchedIds.has(machine.id)) {
          matchedIds.add(machine.id);
          const confidence = typeof item.confidence === "number" ? Math.min(Math.max(item.confidence, 0.1), 0.99) : 0.85;
          resolvedMatches.push({
            machine,
            confidence,
            reasoning: item.reasoning || `Matched as ${machine.name} (${machine.model}) based on visual characteristics.`,
            detected_features: Array.isArray(item.detected_features) ? item.detected_features : [],
          });
        }
      }

      // If matches were found, load their repair procedures menu and return
      if (resolvedMatches.length > 0) {
        const matchesWithMenu = await Promise.all(
          resolvedMatches.map(async ({ machine, confidence, reasoning, detected_features }) => {
            const procedures = await getProceduresForMachine(machine.id);
            return {
              id: machine.id,
              name: machine.name,
              model: machine.model,
              category: machine.category,
              manufacturer: machine.manufacturer,
              location: machine.location,
              status: machine.status,
              serial_number: machine.serial_number,
              specs: machine.specs,
              confidence,
              reasoning,
              detected_features,
              image_url: machine.images?.[0] || machine.image_url,
              procedures: procedures.map((p) => ({
                id: p.id,
                procedure_type: p.procedure_type,
                estimated_minutes: p.estimated_minutes,
                difficulty: p.difficulty,
                steps_count: p.steps?.length || 0,
              })),
            };
          })
        );

        // Filter out low confidence noise (e.g. blank images, non-machine photos)
        const confidentMatches = matchesWithMenu.filter((m) => m.confidence >= 0.35);

        if (confidentMatches.length > 0) {
          return NextResponse.json({
            identified_type: parsed.identified_type || "Industrial Machinery",
            matches: confidentMatches,
          });
        }
      }
    }

    // 4. Fallback if AI was unavailable or no confident match returned
    return NextResponse.json({
      identified_type: "Unidentified Machine",
      matches: [],
      message: "No registered machine confidently matched the image. Please try taking a clearer photo showing the front panel, nameplate, or entire machine body.",
    });

  } catch (error) {
    console.error("identify-machine error:", error);
    return NextResponse.json(
      {
        error: "Failed to identify machine from image",
        details: error instanceof Error ? error.message : "Unknown error",
        matches: [],
      },
      { status: 500 }
    );
  }
}
