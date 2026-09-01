import { NextResponse } from "next/server";
import { getFaultsForTechnician, updateFaultStatus } from "@/lib/database";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const technicianId = searchParams.get("technicianId");

    if (!technicianId) {
      return NextResponse.json({ error: "Missing technicianId" }, { status: 400 });
    }

    const faults = await getFaultsForTechnician(technicianId);
    return NextResponse.json(faults);
  } catch (error) {
    console.error("Error fetching technician inbox:", error);
    return NextResponse.json({ error: "Failed to fetch technician inbox" }, { status: 500 });
  }
}

export async function PATCH(request: Request) {
  try {
    const body = await request.json();
    const { faultId, status } = body;

    if (!faultId || !status) {
      return NextResponse.json({ error: "Missing faultId or status" }, { status: 400 });
    }

    const updatedFault = await updateFaultStatus(faultId, status);
    return NextResponse.json(updatedFault);
  } catch (error) {
    console.error("Error updating fault status:", error);
    return NextResponse.json({ error: "Failed to update fault status" }, { status: 500 });
  }
}
