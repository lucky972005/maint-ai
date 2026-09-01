import type { ArMarker } from "./types";

export type MarkerColor = ArMarker["color"];

const COLOR_MAP: Record<MarkerColor, string> = {
  red: "#EF4444",
  green: "#22C55E",
  blue: "#3B82F6",
};

export interface DrawMarkerOptions {
  ctx: CanvasRenderingContext2D;
  marker: ArMarker;
  canvasWidth: number;
  canvasHeight: number;
  pulsePhase: number;
  selected?: boolean;
}

export function percentToPixels(
  percent: number,
  dimension: number
): number {
  return (percent / 100) * dimension;
}

export function drawMarker({
  ctx,
  marker,
  canvasWidth,
  canvasHeight,
  pulsePhase,
  selected = false,
}: DrawMarkerOptions): void {
  const x = percentToPixels(marker.x, canvasWidth);
  const y = percentToPixels(marker.y, canvasHeight);
  const w = percentToPixels(marker.w, canvasWidth);
  const h = percentToPixels(marker.h, canvasHeight);
  const color = COLOR_MAP[marker.color];
  const pulse = 0.5 + 0.5 * Math.sin(pulsePhase);

  ctx.save();

  // Highlight box
  ctx.strokeStyle = color;
  ctx.lineWidth = selected ? 3 : 2;
  ctx.globalAlpha = 0.6 + pulse * 0.4;
  ctx.setLineDash([6, 4]);
  ctx.strokeRect(x, y, w, h);
  ctx.setLineDash([]);

  // Pulsing corner brackets
  const bracketLen = Math.min(w, h) * 0.3;
  ctx.globalAlpha = 1;
  ctx.lineWidth = 3;
  ctx.strokeStyle = color;

  // Top-left
  ctx.beginPath();
  ctx.moveTo(x, y + bracketLen);
  ctx.lineTo(x, y);
  ctx.lineTo(x + bracketLen, y);
  ctx.stroke();

  // Top-right
  ctx.beginPath();
  ctx.moveTo(x + w - bracketLen, y);
  ctx.lineTo(x + w, y);
  ctx.lineTo(x + w, y + bracketLen);
  ctx.stroke();

  // Bottom-left
  ctx.beginPath();
  ctx.moveTo(x, y + h - bracketLen);
  ctx.lineTo(x, y + h);
  ctx.lineTo(x + bracketLen, y + h);
  ctx.stroke();

  // Bottom-right
  ctx.beginPath();
  ctx.moveTo(x + w - bracketLen, y + h);
  ctx.lineTo(x + w, y + h);
  ctx.lineTo(x + w, y + h - bracketLen);
  ctx.stroke();

  // Animated arrow pointing to center
  const centerX = x + w / 2;
  const arrowOffset = 30 + pulse * 10;
  const arrowY = y - arrowOffset;

  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(centerX, arrowY + 20);
  ctx.lineTo(centerX - 12, arrowY);
  ctx.lineTo(centerX + 12, arrowY);
  ctx.closePath();
  ctx.fill();

  // Label badge
  const labelPadding = 8;
  ctx.font = "bold 14px system-ui, sans-serif";
  const textWidth = ctx.measureText(marker.label).width;
  const badgeW = textWidth + labelPadding * 2;
  const badgeH = 28;
  const badgeX = centerX - badgeW / 2;
  const badgeY = arrowY - badgeH - 8;

  ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
  ctx.beginPath();
  ctx.roundRect(badgeX, badgeY, badgeW, badgeH, 6);
  ctx.fill();

  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.stroke();

  ctx.fillStyle = "#FFFFFF";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(marker.label, centerX, badgeY + badgeH / 2);

  ctx.restore();
}

export function drawOverlayFrame(
  ctx: CanvasRenderingContext2D,
  width: number,
  height: number,
  markers: ArMarker[],
  pulsePhase: number,
  selectedIndex?: number
): void {
  ctx.clearRect(0, 0, width, height);
  markers.forEach((marker, index) => {
    drawMarker({
      ctx,
      marker,
      canvasWidth: width,
      canvasHeight: height,
      pulsePhase,
      selected: index === selectedIndex,
    });
  });
}

export function hitTestMarker(
  markers: ArMarker[],
  canvasWidth: number,
  canvasHeight: number,
  clickX: number,
  clickY: number
): number {
  for (let i = markers.length - 1; i >= 0; i--) {
    const m = markers[i];
    const x = percentToPixels(m.x, canvasWidth);
    const y = percentToPixels(m.y, canvasHeight);
    const w = percentToPixels(m.w, canvasWidth);
    const h = percentToPixels(m.h, canvasHeight);
    if (clickX >= x && clickX <= x + w && clickY >= y && clickY <= y + h) {
      return i;
    }
  }
  return -1;
}
