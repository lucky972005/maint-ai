"use client";

import { useEffect, useRef } from "react";
import JsBarcode from "jsbarcode";

interface BarcodeGeneratorProps {
  value: string;
  width?: number;
  height?: number;
  displayValue?: boolean;
  className?: string;
  background?: string;
  lineColor?: string;
}

export function BarcodeGenerator({
  value,
  width = 2,
  height = 50,
  displayValue = true,
  className = "",
  background = "#ffffff",
  lineColor = "#000000",
}: BarcodeGeneratorProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (canvasRef.current && value) {
      try {
        JsBarcode(canvasRef.current, value, {
          width,
          height,
          displayValue,
          fontSize: 12,
          margin: 10,
          background,
          lineColor,
        });
      } catch (error) {
        console.error("Failed to generate barcode:", error);
      }
    }
  }, [value, width, height, displayValue, background, lineColor]);

  return (
    <div className={`inline-block ${className}`}>
      <canvas ref={canvasRef} />
    </div>
  );
}
