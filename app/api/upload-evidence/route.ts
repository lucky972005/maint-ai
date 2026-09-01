import { NextResponse } from "next/server";
import { uploadFile } from "@/lib/supabase/storage";
import { isSupabaseConfigured } from "@/lib/demo-data";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  try {
    const { file, fileName, logId } = await req.json();

    if (!isSupabaseConfigured()) {
      // Demo mode: return mock URL
      return NextResponse.json({
        url: `/uploads/demo/${fileName ?? "evidence.jpg"}`,
        id: crypto.randomUUID(),
        demo: true,
      });
    }

    const buffer = Buffer.from(file, "base64");
    const path = `evidence/${logId}/${Date.now()}-${fileName}`;

    const url = await uploadFile(path, buffer);

    return NextResponse.json({ url, id: path });
  } catch (error) {
    console.error("upload-evidence error:", error);
    return NextResponse.json({ error: "Upload failed" }, { status: 500 });
  }
}
