import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDuration(minutes: number): string {
  if (minutes < 60) return `${minutes}m`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m > 0 ? `${h}h ${m}m` : `${h}h`;
}

export function formatDate(date: string | Date | null | undefined): string {
  try {
    if (!date) {
      return new Date().toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
    }
    const d = new Date(date);
    if (isNaN(d.getTime())) {
      return new Date().toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
    }
    return d.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch {
    return new Date().toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
  }
}

export function slugify(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}
