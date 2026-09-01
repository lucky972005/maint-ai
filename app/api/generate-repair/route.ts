import { NextResponse } from "next/server";
import { generateJsonResponse, isAIConfigured } from "@/lib/ai";
import { getMachineById, getProceduresForMachine } from "@/lib/demo-data";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  try {
    const { machineId, procedureType, faultDescription } = await req.json();
    const machine = getMachineById(machineId);
    const existing = getProceduresForMachine(machineId).find(
      (p) => p.procedure_type === procedureType
    );

    if (existing) {
      return NextResponse.json({ procedure: existing });
    }

    if (isAIConfigured()) {
      const procedure = await generateJsonResponse([
        {
          role: "user",
          content: `Generate a step-by-step repair procedure for ${procedureType} on ${machine?.name ?? "industrial machine"} (${machine?.model}). ${faultDescription ? `Fault: ${faultDescription}` : ""} Return JSON with: procedure_type, estimated_minutes, difficulty (easy|medium|hard), required_tools[], safety_warnings[], steps[{step, instruction, tool_needed, safety, ar_marker:{x,y,w,h,label,color}}]. Include 6-8 steps with AR markers as viewport percentages.`,
        },
      ]);
      return NextResponse.json({ procedure });
    }

    return NextResponse.json({ error: "Procedure not found" }, { status: 404 });
  } catch (error) {
    console.error("generate-repair error:", error);
    return NextResponse.json({ error: "Failed to generate repair procedure" }, { status: 500 });
  }
}
