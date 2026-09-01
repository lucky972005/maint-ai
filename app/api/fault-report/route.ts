import { NextResponse } from "next/server";
import { createFaultReport } from "@/lib/database";
import { isSupabaseConfigured } from "@/lib/demo-data";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  try {
    const payload = await req.json();

    if (!isSupabaseConfigured()) {
      return NextResponse.json({ ok: true, demo: true, id: crypto.randomUUID() });
    }

    const report = await createFaultReport(payload);
    return NextResponse.json({ ok: true, report });
  } catch (error) {
    console.error("fault-report error:", error);
    return NextResponse.json({ ok: false, error: "Fault report save failed" }, { status: 500 });
  }
}