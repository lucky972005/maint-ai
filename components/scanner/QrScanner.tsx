"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Html5Qrcode } from "html5-qrcode";
import { useRouter } from "next/navigation";
import { toast } from "@/hooks/use-toast";
import { getMachineByQr as getMachineByQrFromDb } from "@/lib/database";
import { getMachineByQr, DEMO_DATA } from "@/lib/demo-data";

interface QrScannerProps {
  onScan?: (qrCode: string) => void;
}

export function QrScanner({ onScan }: QrScannerProps) {
  const router = useRouter();
  const scannerRef = useRef<Html5Qrcode | null>(null);
  const isStartingRef = useRef(false);
  const isRunningRef = useRef(false);
  const scannedOnceRef = useRef(false);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const containerId = "qr-reader";

  const handleScan = useCallback(
    async (qrCode: string) => {
      if (scannedOnceRef.current) return;
      scannedOnceRef.current = true;

      if (typeof window !== "undefined" && navigator.vibrate) {
        navigator.vibrate(200);
      }
      try {
        const audio = new Audio(
          "data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIGWi78OScTgwOUKzn8LZjHAY4"
        );
        audio.volume = 0.3;
        audio.play().catch(() => {});
      } catch {}

      toast({ title: "QR Code Scanned", description: qrCode });

      // Try database first (will use demo fallback automatically if Supabase is offline)
      let machine = null;
      try {
        machine = await getMachineByQrFromDb(qrCode);
      } catch {
        console.debug("Database lookup fallback to demo data");
      }

      // Fall back to demo data
      if (!machine) {
        machine =
          getMachineByQr(qrCode) ??
          DEMO_DATA.machines.find((m) =>
            qrCode.includes(m.qr_code.split(":")[1]?.slice(0, 8) ?? "")
          );
      }

      if (machine) {
        onScan?.(qrCode);
        router.push(`/repair/${machine.id}`);
      } else {
        toast({
          title: "Unknown Machine",
          description: "QR code not recognized in database.",
          variant: "destructive",
        });
        // Reset after 3 seconds so user can try again
        setTimeout(() => {
          scannedOnceRef.current = false;
        }, 3000);
      }
    },
    [router, onScan]
  );

  useEffect(() => {
    let mounted = true;

    const startScanner = async () => {
      if (isStartingRef.current || isRunningRef.current) return;
      isStartingRef.current = true;

      try {
        const scanner = new Html5Qrcode(containerId);
        scannerRef.current = scanner;

        await scanner.start(
          { facingMode: "environment" },
          { fps: 4, qrbox: { width: 250, height: 250 }, aspectRatio: 1 },
          (decodedText) => {
            if (!mounted) return;
            handleScan(decodedText);
          },
          () => {}
        );

        if (mounted) {
          isRunningRef.current = true;
          setScanning(true);
        } else {
          scanner.stop().catch(() => {});
        }
      } catch {
        if (mounted) {
          setError("Camera access unavailable. Use AI Identify tab instead.");
        }
      } finally {
        isStartingRef.current = false;
      }
    };

    startScanner();

    return () => {
      mounted = false;
      if (scannerRef.current && isRunningRef.current) {
        scannerRef.current.stop().catch(() => {});
        isRunningRef.current = false;
      }
    };
  }, [handleScan]);

  return (
    <div className="relative min-h-[420px] w-full overflow-hidden bg-black lg:min-h-[640px]">
      <div id={containerId} className="w-full h-full" />
      {!scanning && !error && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/80">
          <div className="animate-spin h-8 w-8 border-2 border-primary border-t-transparent rounded-full" />
        </div>
      )}
      {error && (
        <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/90 p-4 text-center">
          <p className="text-white text-sm mb-2">{error}</p>
          <p className="text-xs text-muted-foreground">
            Allow camera permissions or switch to the AI Identify tab
          </p>
        </div>
      )}
    </div>
  );
}
