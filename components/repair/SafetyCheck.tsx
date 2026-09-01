"use client";

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { AlertTriangle } from "lucide-react";

interface SafetyCheckProps {
  open: boolean;
  warnings: string[];
  onConfirm: () => void;
  onCancel: () => void;
}

export function SafetyCheck({ open, warnings, onConfirm, onCancel }: SafetyCheckProps) {
  return (
    <Dialog open={open} onOpenChange={(v) => !v && onCancel()}>
      <DialogContent className="border-destructive/50">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-destructive">
            <AlertTriangle className="h-5 w-5" />
            Safety Checkpoint
          </DialogTitle>
          <DialogDescription>
            Review these safety warnings before proceeding. Say &quot;Confirm safety&quot; or tap the button.
          </DialogDescription>
        </DialogHeader>
        <ul className="space-y-2 my-4">
          {warnings.map((w, i) => (
            <li key={i} className="flex items-start gap-2 text-sm">
              <AlertTriangle className="h-4 w-4 text-destructive shrink-0 mt-0.5" />
              {w}
            </li>
          ))}
        </ul>
        <DialogFooter>
          <Button variant="outline" onClick={onCancel}>Cancel</Button>
          <Button onClick={onConfirm} className="bg-destructive hover:bg-destructive/90">
            I Understand
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
