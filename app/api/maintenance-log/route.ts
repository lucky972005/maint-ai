import { NextResponse } from "next/server";
import { createMaintenanceLog } from "@/lib/database";
import { isSupabaseConfigured } from "@/lib/demo-data";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  try {
    const payload = await req.json();

    if (!isSupabaseConfigured()) {
      return NextResponse.json({ ok: true, demo: true, id: crypto.randomUUID() });
    }

    const log = await createMaintenanceLog(payload);
    return NextResponse.json({ ok: true, log });
  } catch (error) {
    console.error("maintenance-log error:", error);
    return NextResponse.json({ ok: false, error: "Maintenance log save failed" }, { status: 500 });
  }
}