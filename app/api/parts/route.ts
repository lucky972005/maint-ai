import { NextResponse } from "next/server";
import { getParts, getLowStockParts, updatePartStock } from "@/lib/database";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const lowStock = searchParams.get("lowStock") === "true";

    if (lowStock) {
      const parts = await getLowStockParts();
      return NextResponse.json(parts);
    }

    const parts = await getParts();
    return NextResponse.json(parts);
  } catch (error) {
    console.error("Error fetching parts:", error);
    return NextResponse.json({ error: "Failed to fetch parts" }, { status: 500 });
  }
}

export async function PATCH(request: Request) {
  try {
    const body = await request.json();
    const { id, quantity } = body;

    if (!id || quantity === undefined) {
      return NextResponse.json({ error: "Missing required fields" }, { status: 400 });
    }

    const part = await updatePartStock(id, quantity);
    return NextResponse.json(part);
  } catch (error) {
    console.error("Error updating part:", error);
    return NextResponse.json({ error: "Failed to update part" }, { status: 500 });
  }
}
