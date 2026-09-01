import { NextResponse } from "next/server";
import { generateJsonResponse, isAIConfigured } from "@/lib/ai";
import { DEMO_DATA } from "@/lib/demo-data";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  try {
    const { machineId } = await req.json();
    const machine = DEMO_DATA.machines.find((m) => m.id === machineId);
    const machineLogs = DEMO_DATA.logs.filter((l) => l.machine_id === machineId);

    if (isAIConfigured() && machine) {
      const result = await generateJsonResponse([
        {
          role: "user",
          content: `Analyze maintenance history for ${machine.name} (${machine.category}, ${machine.model}). Recent logs: ${machineLogs.length} in 90 days. Status: ${machine.status}. Predict next maintenance needs. Return JSON: {"predictions":[{"procedure":"string","urgency":"low|medium|high","days_until_due":number,"reason":"string"}],"overall_health":"good|fair|poor","recommendations":["string"]}`,
        },
      ]);

      return NextResponse.json(result);
    }

    // Demo predictions
    return NextResponse.json({
      predictions: [
        { procedure: "Oil Change", urgency: "medium", days_until_due: 14, reason: "Standard 90-day interval approaching" },
        { procedure: "Bearing Inspection", urgency: "low", days_until_due: 45, reason: "No recent bearing issues detected" },
        { procedure: "Belt Replacement", urgency: machine?.status === "maintenance" ? "high" : "low", days_until_due: 30, reason: "Based on operating hours estimate" },
      ],
      overall_health: machine?.status === "broken" ? "poor" : machine?.status === "maintenance" ? "fair" : "good",
      recommendations: [
        "Schedule preventive maintenance within 2 weeks",
        "Monitor vibration levels during operation",
        "Ensure spare belts are in stock",
      ],
    });
  } catch (error) {
    console.error("predict-maintenance error:", error);
    return NextResponse.json({ error: "Prediction failed" }, { status: 500 });
  }
}
