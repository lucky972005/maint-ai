import { NextResponse } from "next/server";
import { getMachines, getMachineById, updateMachineStatus } from "@/lib/database";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get("id");

    if (id) {
      const machine = await getMachineById(id);
      if (!machine) {
        return NextResponse.json({ error: "Machine not found" }, { status: 404 });
      }
      return NextResponse.json(machine);
    }

    const machines = await getMachines();
    return NextResponse.json(machines);
  } catch (error) {
    console.error("Error fetching machines:", error);
    return NextResponse.json({ error: "Failed to fetch machines" }, { status: 500 });
  }
}

export async function PATCH(request: Request) {
  try {
    const body = await request.json();
    const { id, status } = body;

    if (!id || !status) {
      return NextResponse.json({ error: "Missing required fields" }, { status: 400 });
    }

    const machine = await updateMachineStatus(id, status);
    return NextResponse.json(machine);
  } catch (error) {
    console.error("Error updating machine:", error);
    return NextResponse.json({ error: "Failed to update machine" }, { status: 500 });
  }
}
