import { NextResponse } from "next/server";
import { getFaultReports, createFaultReport, updateFaultReport } from "@/lib/database";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const faults = await getFaultReports();
    return NextResponse.json(faults);
  } catch (error) {
    console.error("Error fetching fault reports:", error);
    return NextResponse.json({ error: "Failed to fetch fault reports" }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const fault = await createFaultReport(body);
    return NextResponse.json(fault);
  } catch (error) {
    console.error("Error creating fault report:", error);
    return NextResponse.json({ error: "Failed to create fault report" }, { status: 500 });
  }
}

export async function PATCH(request: Request) {
  try {
    const body = await request.json();
    const { id, ...updates } = body;

    if (!id) {
      return NextResponse.json({ error: "Missing fault id" }, { status: 400 });
    }

    const fault = await updateFaultReport(id, updates);
    return NextResponse.json(fault);
  } catch (error) {
    console.error("Error updating fault report:", error);
    return NextResponse.json({ error: "Failed to update fault report" }, { status: 500 });
  }
}
