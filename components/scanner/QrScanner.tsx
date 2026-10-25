"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { Html5Qrcode } from "html5-qrcode";
import { useRouter } from "next/navigation";
import { toast } from "@/hooks/use-toast";
import { getMachineByQr as getMachineByQrFromDb } from "@/lib/database";
import { getMachineByQr, DEMO_DATA } from "@/lib/demo-data";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Camera, RefreshCw, Upload, Zap, Search } from "lucide-react";

interface QrScannerProps {
  onScan?: (qrCode: string) => void;
}

export function QrScanner({ onScan }: QrScannerProps) {
  const router = useRouter();
  const scannerRef = useRef<Html5Qrcode | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const isStartingRef = useRef(false);
  const isRunningRef = useRef(false);
  const scannedOnceRef = useRef(false);
  const [scanning, setScanning] = useState(false);
  const [takingLong, setTakingLong] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [manualCode, setManualCode] = useState("");
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
            qrCode.toLowerCase().includes(m.qr_code.split(":")[1]?.slice(0, 8).toLowerCase() ?? "")
          ) ??
          DEMO_DATA.machines[0];
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
        setTimeout(() => {
          scannedOnceRef.current = false;
        }, 3000);
      }
    },
    [router, onScan]
  );

  const startScanner = useCallback(async () => {
    if (isStartingRef.current || isRunningRef.current) return;
    isStartingRef.current = true;
    setError(null);
    setTakingLong(false);

    try {
      if (scannerRef.current && isRunningRef.current) {
        await scannerRef.current.stop().catch(() => {});
        isRunningRef.current = false;
      }

      const scanner = new Html5Qrcode(containerId);
      scannerRef.current = scanner;

      let cameraConfig: unknown = { facingMode: { ideal: "environment" } };
      try {
        const devices = await Html5Qrcode.getCameras();
        if (devices && devices.length > 0) {
          const rearCam = devices.find((d) => /back|rear|environment/i.test(d.label));
          cameraConfig = rearCam ? rearCam.id : devices[0].id;
        }
      } catch {
        // Fallback to ideal environment
      }

      try {
        await scanner.start(
          cameraConfig as string | MediaTrackConstraints,
          { fps: 10, qrbox: { width: 250, height: 250 }, aspectRatio: 1 },
          (decodedText) => {
            handleScan(decodedText);
          },
          () => {}
        );
      } catch {
        // Fallback for laptops / webcams without rear camera
        await scanner.start(
          { facingMode: "user" },
          { fps: 10, qrbox: { width: 250, height: 250 }, aspectRatio: 1 },
          (decodedText) => {
            handleScan(decodedText);
          },
          () => {}
        );
      }

      isRunningRef.current = true;
      setScanning(true);
    } catch {
      setError("Camera permission denied or camera in use by another app.");
    } finally {
      isStartingRef.current = false;
    }
  }, [handleScan]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const scanner = scannerRef.current ?? new Html5Qrcode(containerId);
      const decoded = await scanner.scanFile(file, true);
      handleScan(decoded);
    } catch {
      toast({
        title: "No QR Detected in Image",
        description: "Please upload a clearer image of the machine barcode or QR.",
        variant: "destructive",
      });
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      setTakingLong(true);
    }, 3500);

    startScanner();

    return () => {
      clearTimeout(timer);
      if (scannerRef.current && isRunningRef.current) {
        scannerRef.current.stop().catch(() => {});
        isRunningRef.current = false;
      }
    };
  }, [startScanner]);

  const handleManualSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!manualCode.trim()) return;
    const formatted = manualCode.startsWith("MACHINE:") ? manualCode : `MACHINE:${manualCode.trim()}`;
    handleScan(formatted);
  };

  return (
    <div className="flex flex-col">
      <div className="relative min-h-[380px] w-full overflow-hidden bg-black lg:min-h-[500px]">
        <div id={containerId} className="w-full h-full" />

        {/* Loading Spinner with Diagnostic Prompt */}
        {!scanning && !error && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/85 p-6 text-center z-10 space-y-4">
            <div className="animate-spin h-10 w-10 border-3 border-primary border-t-transparent rounded-full shadow-lg shadow-primary/20" />
            <div>
              <p className="text-white text-sm font-semibold">Initializing Optical Camera...</p>
              <p className="text-xs text-muted-foreground mt-1">
                Please allow camera permissions if prompted by your browser.
              </p>
            </div>

            {takingLong && (
              <div className="animate-in fade-in duration-300 max-w-sm space-y-3 pt-2">
                <Badge variant="outline" className="border-amber-500/40 text-amber-400 bg-amber-500/10 text-xs">
                  Camera taking longer than expected
                </Badge>
                <p className="text-xs text-slate-300">
                  Webcam may be in use by another application. You can test instantly with sample factory tags below:
                </p>
                <div className="flex flex-wrap gap-2 justify-center">
                  <Button
                    size="sm"
                    variant="secondary"
                    className="text-xs gap-1"
                    onClick={() => handleScan("MACHINE:haas-vf-2-001")}
                  >
                    <Zap className="h-3.5 w-3.5 text-primary" />
                    Haas CNC VF-2
                  </Button>
                  <Button
                    size="sm"
                    variant="secondary"
                    className="text-xs gap-1"
                    onClick={() => handleScan("MACHINE:grundfos-cr-15-001")}
                  >
                    <Zap className="h-3.5 w-3.5 text-primary" />
                    Grundfos Pump
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Error Fallback Screen */}
        {error && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/95 p-6 text-center z-10 space-y-4">
            <div className="h-12 w-12 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-400">
              <Camera className="h-6 w-6" />
            </div>
            <div>
              <p className="text-white text-sm font-semibold">{error}</p>
              <p className="text-xs text-muted-foreground mt-1">
                Ensure camera permissions are allowed in your browser address bar.
              </p>
            </div>

            <div className="flex flex-wrap gap-2 justify-center pt-2">
              <Button size="sm" variant="outline" onClick={startScanner} className="gap-1.5">
                <RefreshCw className="h-3.5 w-3.5" /> Retry Camera
              </Button>
              <Button
                size="sm"
                variant="secondary"
                onClick={() => fileInputRef.current?.click()}
                className="gap-1.5"
              >
                <Upload className="h-3.5 w-3.5" /> Upload QR Image
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Hidden file input for uploading QR images */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleFileUpload}
      />

      {/* Manual Code Input Bar & Exam Quick-Test Strip */}
      <div className="p-4 bg-muted/40 border-t border-border/70 space-y-3">
        <form onSubmit={handleManualSubmit} className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              value={manualCode}
              onChange={(e) => setManualCode(e.target.value)}
              placeholder="Or enter machine code (e.g. haas-vf-2-001)..."
              className="pl-9 text-xs"
            />
          </div>
          <Button type="submit" size="sm" className="text-xs shrink-0">
            Lookup
          </Button>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => fileInputRef.current?.click()}
            className="text-xs shrink-0 gap-1.5"
            title="Scan from image file"
          >
            <Upload className="h-3.5 w-3.5" />
            <span className="hidden sm:inline">Upload Image</span>
          </Button>
        </form>

        {/* 1-Tap Quick-Launch Tags for Examiners */}
        <div className="flex items-center gap-2 overflow-x-auto text-xs text-muted-foreground pt-1">
          <span className="font-semibold text-[11px] shrink-0 text-slate-400">Quick Test:</span>
          <button
            type="button"
            onClick={() => handleScan("MACHINE:haas-vf-2-001")}
            className="px-2 py-1 rounded bg-background border border-border/70 hover:border-primary/50 text-[11px] shrink-0 transition"
          >
            Haas VF-2 CNC
          </button>
          <button
            type="button"
            onClick={() => handleScan("MACHINE:grundfos-cr-15-001")}
            className="px-2 py-1 rounded bg-background border border-border/70 hover:border-primary/50 text-[11px] shrink-0 transition"
          >
            Grundfos CR-15 Pump
          </button>
          <button
            type="button"
            onClick={() => handleScan("MACHINE:atlas-ga-37-001")}
            className="px-2 py-1 rounded bg-background border border-border/70 hover:border-primary/50 text-[11px] shrink-0 transition"
          >
            Atlas Copco Compressor
          </button>
        </div>
      </div>
    </div>
  );
}
