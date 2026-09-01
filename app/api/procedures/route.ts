import { NextResponse } from "next/server";
import { getProceduresForMachine, getProcedureById } from "@/lib/database";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const machineId = searchParams.get("machineId");
    const id = searchParams.get("id");

    if (id) {
      const procedure = await getProcedureById(id);
      if (!procedure) {
        return NextResponse.json({ error: "Procedure not found" }, { status: 404 });
      }
      return NextResponse.json(procedure);
    }

    if (machineId) {
      const procedures = await getProceduresForMachine(machineId);
      return NextResponse.json(procedures);
    }

    return NextResponse.json({ error: "Missing machineId or id parameter" }, { status: 400 });
  } catch (error) {
    console.error("Error fetching procedures:", error);
    return NextResponse.json({ error: "Failed to fetch procedures" }, { status: 500 });
  }
}
