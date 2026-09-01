"use client";

import { useState } from "react";
import { CameraView } from "./CameraView";
import { Button } from "@/components/ui/button";
import { CheckCircle2, XCircle, Loader2, RotateCcw } from "lucide-react";

interface ToolDetectorProps {
  expectedTool: string;
  onVerified: () => void;
  onSkip?: () => void;
}

export function ToolDetector({ expectedTool, onVerified, onSkip }: ToolDetectorProps) {
  const [status, setStatus] = useState<"idle" | "checking" | "success" | "fail">("idle");
  const [detected, setDetected] = useState<string>("");

  const verifyTool = async (dataUrl: string) => {
    setStatus("checking");
    try {
      const base64 = dataUrl.split(",")[1];
      const res = await fetch("/api/identify-tool", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64, expectedTool }),
      });
      const data = await res.json();

      setDetected(data.detected ?? data.tool ?? "unknown");

      if (data.isCorrect || data.confidence > 0.8) {
        setStatus("success");
        setTimeout(onVerified, 1500);
      } else {
        setStatus("fail");
      }
    } catch {
      setStatus("fail");
    }
  };

  return (
    <div className="space-y-4">
      <div className="text-center">
        <p className="text-lg font-medium">Show me the <span className="text-primary">{expectedTool.replace(/_/g, " ")}</span></p>
        <p className="text-sm text-muted-foreground mt-1">Hold tool up to camera and tap capture</p>
      </div>

      <div className="relative h-64 rounded-lg overflow-hidden border border-border">
        <CameraView onCapture={verifyTool} className="h-full" />
        {status === "checking" && (
          <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
            <Loader2 className="h-8 w-8 text-primary animate-spin" />
          </div>
        )}
      </div>

      {status === "success" && (
        <div className="flex items-center justify-center gap-2 text-green-500">
          <CheckCircle2 className="h-6 w-6" />
          <span className="font-medium">Correct tool! Proceeding...</span>
        </div>
      )}

      {status === "fail" && (
        <div className="space-y-3">
          <div className="flex items-center justify-center gap-2 text-destructive">
            <XCircle className="h-6 w-6" />
            <span>Wrong tool. Detected: {detected}. Please use {expectedTool.replace(/_/g, " ")}</span>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" className="flex-1" onClick={() => setStatus("idle")}>
              <RotateCcw className="h-4 w-4 mr-2" /> Retry
            </Button>
            {onSkip && (
              <Button variant="ghost" className="flex-1" onClick={onSkip}>Skip</Button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
