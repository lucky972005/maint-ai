"use client";

import { useEffect, useRef, useState } from "react";
import { Camera, CameraOff } from "lucide-react";
import { Button } from "@/components/ui/button";

interface CameraViewProps {
  onCapture?: (dataUrl: string) => void;
  showCaptureButton?: boolean;
  className?: string;
  fallbackImage?: string;
}

export function CameraView({
  onCapture,
  showCaptureButton = true,
  className = "",
  fallbackImage,
}: CameraViewProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    let active = true;
    const videoEl = videoRef.current;

    if (typeof window !== "undefined" && !window.isSecureContext) {
      setError(true);
      return;
    }

    if (!navigator.mediaDevices?.getUserMedia) {
      setError(true);
      return;
    }

    const acquireCamera = async () => {
      try {
        return await navigator.mediaDevices.getUserMedia({
          video: { facingMode: { ideal: "environment" } },
          audio: false,
        });
      } catch {
        return await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });
      }
    };

    acquireCamera()
      .then((mediaStream) => {
        if (!active) {
          mediaStream.getTracks().forEach((t) => t.stop());
          return;
        }
        streamRef.current = mediaStream;
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
          videoRef.current.play().catch(() => {
            // Safe ignore if play request is aborted on quick tab switch
          });
        }
      })
      .catch(() => {
        if (active) setError(true);
      });

    return () => {
      active = false;
      if (videoEl) {
        videoEl.srcObject = null;
      }
      streamRef.current?.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    };
  }, []);

  const capture = () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext("2d");
    ctx?.drawImage(video, 0, 0);
    const dataUrl = canvas.toDataURL("image/jpeg", 0.8);
    onCapture?.(dataUrl);
  };

  if (error && fallbackImage) {
    return (
      <div className={`relative overflow-hidden bg-black ${className}`}>
        <img src={fallbackImage} alt="Machine" className="w-full h-full object-cover opacity-60" />
      </div>
    );
  }

  if (error) {
    return (
      <div className={`flex flex-col items-center justify-center bg-muted ${className}`}>
        <CameraOff className="h-12 w-12 text-muted-foreground mb-2" />
        <p className="text-sm text-muted-foreground text-center px-4">
          Camera unavailable. Open the app on HTTPS or localhost and allow camera permission.
        </p>
      </div>
    );
  }

  return (
    <div className={`relative overflow-hidden bg-black ${className}`}>
      <video ref={videoRef} autoPlay playsInline muted className="w-full h-full object-cover" />
      <canvas ref={canvasRef} className="hidden" />
      {showCaptureButton && (
        <div className="absolute bottom-4 left-0 right-0 flex justify-center">
          <Button onClick={capture} size="lg" className="rounded-full h-16 w-16 orange-glow">
            <Camera className="h-6 w-6" />
          </Button>
        </div>
      )}
    </div>
  );
}

export function getVideoElement(ref: React.RefObject<HTMLVideoElement | null>): HTMLVideoElement | null {
  return ref.current;
}
