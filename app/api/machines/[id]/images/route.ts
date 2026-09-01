import { NextResponse } from "next/server";
import { updateMachine } from "@/lib/database";
import { uploadFile } from "@/lib/supabase/storage";
import { isSupabaseConfigured } from "@/lib/demo-data";

export const dynamic = "force-dynamic";

export async function POST(
  req: Request,
  { params }: { params: { id: string } }
) {
  try {
    const { images, setPrimaryIndex } = await req.json();
    const machineId = params.id;

    if (!images || !Array.isArray(images)) {
      return NextResponse.json({ error: "Images array is required" }, { status: 400 });
    }

    if (!isSupabaseConfigured()) {
      // Demo mode: return mock URLs
      const mockUrls = images.map((img: { name: string }) => 
        `/uploads/demo/machines/${machineId}/${img.name || "image.jpg"}`
      );
      return NextResponse.json({ 
        success: true, 
        urls: mockUrls,
        thumbnail_url: mockUrls[0] || null,
        demo: true 
      });
    }

    // Upload each image
    const uploadedUrls: string[] = [];
    for (let i = 0; i < images.length; i++) {
      const image = images[i];
      if (image.data) {
        const buffer = Buffer.from(image.data, "base64");
        const path = `machines/${machineId}/${Date.now()}-${image.name || `image-${i}.jpg`}`;
        const url = await uploadFile(path, buffer);
        uploadedUrls.push(url);
      }
    }

    // Update machine with new images
    const updateData: Record<string, unknown> = {
      images: uploadedUrls,
      thumbnail_url: uploadedUrls[0] || null,
    };

    if (typeof setPrimaryIndex === "number" && setPrimaryIndex >= 0) {
      updateData.primary_image_index = setPrimaryIndex;
    }

    await updateMachine(machineId, updateData);

    return NextResponse.json({ 
      success: true, 
      urls: uploadedUrls,
      thumbnail_url: uploadedUrls[0] || null
    });

  } catch (error) {
    console.error("Machine image upload error:", error);
    return NextResponse.json({ error: "Failed to upload images" }, { status: 500 });
  }
}
