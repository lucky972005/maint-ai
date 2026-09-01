"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { ArMarker } from "@/lib/types";
import { drawOverlayFrame, hitTestMarker } from "@/lib/ar-overlay";
import { CameraView } from "./CameraView";

interface ArOverlayProps {
  markers: ArMarker[];
  fallbackImage?: string;
  onMarkerClick?: (index: number, marker: ArMarker) => void;
}

export function ArOverlay({ markers, fallbackImage, onMarkerClick }: ArOverlayProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [selectedIndex, setSelectedIndex] = useState<number | undefined>();
  const [expandedMarker, setExpandedMarker] = useState<ArMarker | null>(null);
  const pulseRef = useRef(0);
  const frameRef = useRef<number>();

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const { width, height } = container.getBoundingClientRect();
    canvas.width = width;
    canvas.height = height;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    pulseRef.current += 0.05;
    drawOverlayFrame(ctx, width, height, markers, pulseRef.current, selectedIndex);
    frameRef.current = requestAnimationFrame(draw);
  }, [markers, selectedIndex]);

  useEffect(() => {
    frameRef.current = requestAnimationFrame(draw);
    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current);
    };
  }, [draw]);

  const handleClick = (event: React.MouseEvent | React.TouchEvent) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const clientX = "touches" in event ? event.touches[0].clientX : event.clientX;
    const clientY = "touches" in event ? event.touches[0].clientY : event.clientY;
    const x = clientX - rect.left;
    const y = clientY - rect.top;

    const index = hitTestMarker(markers, canvas.width, canvas.height, x, y);
    if (index >= 0) {
      setSelectedIndex(index);
      setExpandedMarker(markers[index]);
      onMarkerClick?.(index, markers[index]);
    }
  };

  return (
    <div ref={containerRef} className="relative h-full w-full overflow-hidden">
      <CameraView showCaptureButton={false} className="absolute inset-0" fallbackImage={fallbackImage} />
      <canvas
        ref={canvasRef}
        className="absolute inset-0 h-full w-full cursor-pointer touch-none transition-opacity duration-300"
        onClick={handleClick}
        onTouchEnd={handleClick}
      />
      {expandedMarker && (
        <div className="absolute bottom-4 left-4 right-4 animate-in fade-in rounded-lg border border-primary/30 bg-card/90 p-4 backdrop-blur">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="font-semibold text-primary">{expandedMarker.label}</p>
              <p className="mt-1 text-xs text-muted-foreground">
                {expandedMarker.color === "red" && "Remove"}
                {expandedMarker.color === "green" && "Install"}
                {expandedMarker.color === "blue" && "Inspect"}
              </p>
            </div>
            <button
              type="button"
              onClick={() => {
                setExpandedMarker(null);
                setSelectedIndex(undefined);
              }}
              className="text-sm text-muted-foreground hover:text-foreground"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
