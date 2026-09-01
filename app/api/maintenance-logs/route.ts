import { NextResponse } from "next/server";
import { getMaintenanceLogs, createMaintenanceLog, updateMaintenanceLog } from "@/lib/database";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = searchParams.get("limit") ? parseInt(searchParams.get("limit")!) : undefined;

    const logs = await getMaintenanceLogs(limit);
    return NextResponse.json(logs);
  } catch (error) {
    console.error("Error fetching maintenance logs:", error);
    return NextResponse.json({ error: "Failed to fetch maintenance logs" }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const log = await createMaintenanceLog(body);
    return NextResponse.json(log);
  } catch (error) {
    console.error("Error creating maintenance log:", error);
    return NextResponse.json({ error: "Failed to create maintenance log" }, { status: 500 });
  }
}

export async function PATCH(request: Request) {
  try {
    const body = await request.json();
    const { id, ...updates } = body;

    if (!id) {
      return NextResponse.json({ error: "Missing log id" }, { status: 400 });
    }

    const log = await updateMaintenanceLog(id, updates);
    return NextResponse.json(log);
  } catch (error) {
    console.error("Error updating maintenance log:", error);
    return NextResponse.json({ error: "Failed to update maintenance log" }, { status: 500 });
  }
}
