import { NextResponse } from "next/server";
import { getMachines } from "@/lib/database";
import QRCode from "qrcode";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const machineId = searchParams.get("machineId");

    if (machineId) {
      // Generate QR code for a specific machine
      const machines = await getMachines();
      const machine = machines.find((m) => m.id === machineId);
      
      if (!machine) {
        return NextResponse.json({ error: "Machine not found" }, { status: 404 });
      }

      const qrCodeDataUrl = await QRCode.toDataURL(machine.qr_code, {
        width: 300,
        margin: 2,
        color: {
          dark: "#000000",
          light: "#FFFFFF",
        },
      });

      return NextResponse.json({
        machine,
        qrCode: qrCodeDataUrl,
      });
    }

    // Generate QR codes for all machines
    const machines = await getMachines();
    
    const qrCodes = await Promise.all(
      machines.map(async (machine) => {
        const qrCodeDataUrl = await QRCode.toDataURL(machine.qr_code, {
          width: 300,
          margin: 2,
          color: {
            dark: "#000000",
            light: "#FFFFFF",
          },
        });

        return {
          machine,
          qrCode: qrCodeDataUrl,
        };
      })
    );

    return NextResponse.json(qrCodes);
  } catch (error) {
    console.error("Error generating QR codes:", error);
    return NextResponse.json({ error: "Failed to generate QR codes" }, { status: 500 });
  }
}
