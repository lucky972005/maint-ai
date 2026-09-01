import { NextResponse } from "next/server";
import { assignFaultReport, getUnassignedFaults, getTechnicians } from "@/lib/database";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const [unassignedFaults, technicians] = await Promise.all([
      getUnassignedFaults(),
      getTechnicians(),
    ]);
    
    return NextResponse.json({
      unassignedFaults,
      technicians,
    });
  } catch (error) {
    console.error("Error fetching assignment data:", error);
    return NextResponse.json({ error: "Failed to fetch assignment data" }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { faultId, technicianId } = body;

    if (!faultId || !technicianId) {
      return NextResponse.json({ error: "Missing faultId or technicianId" }, { status: 400 });
    }

    const assignedFault = await assignFaultReport(faultId, technicianId);
    return NextResponse.json(assignedFault);
  } catch (error) {
    console.error("Error assigning fault report:", error);
    return NextResponse.json({ error: "Failed to assign fault report" }, { status: 500 });
  }
}
