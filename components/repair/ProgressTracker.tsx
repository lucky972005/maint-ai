"use client";

import { Progress } from "@/components/ui/progress";

interface ProgressTrackerProps {
  current: number;
  total: number;
  procedureType: string;
}

export function ProgressTracker({ current, total, procedureType }: ProgressTrackerProps) {
  const percent = (current / total) * 100;

  return (
    <div className="px-4 pt-4 space-y-2">
      <div className="flex items-center justify-between text-sm">
        <span className="text-muted-foreground">{procedureType}</span>
        <span className="font-medium text-primary">Step {current} of {total}</span>
      </div>
      <Progress value={percent} className="h-2" />
    </div>
  );
}
