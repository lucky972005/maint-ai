"use client";

import { useState, useEffect, useMemo } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { assignFaultReport } from "@/lib/database";
import { toast } from "@/hooks/use-toast";
import type { FaultReport, Profile, FaultSeverity } from "@/lib/types";
import {
  Calendar,
  Clock,
  UserCheck,
  UserPlus,
  Wrench,
} from "lucide-react";

interface AssignFaultModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  fault: FaultReport | null;
  technicians: Profile[];
  activeTaskCountByTech?: Record<string, number>;
  isReassign?: boolean;
  onAssigned?: (updatedFault: FaultReport) => void;
}

export function AssignFaultModal({
  open,
  onOpenChange,
  fault,
  technicians,
  activeTaskCountByTech = {},
  isReassign = false,
  onAssigned,
}: AssignFaultModalProps) {
  const [selectedTechnicianId, setSelectedTechnicianId] = useState<string>("");
  const [severity, setSeverity] = useState<FaultSeverity>("medium");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (open && fault) {
      setSelectedTechnicianId(fault.assigned_to || "");
      setSeverity((fault.severity as FaultSeverity) || "medium");
    }
  }, [open, fault]);

  const selectedTechnician = useMemo(
    () => technicians.find((t) => t.id === selectedTechnicianId),
    [technicians, selectedTechnicianId]
  );

  const getDueDateHours = (sev: FaultSeverity) => {
    switch (sev) {
      case "critical": return 4;
      case "high": return 24;
      case "medium": return 48;
      case "low": return 72;
    }
  };

  const calculatedDueDate = useMemo(() => {
    const hours = getDueDateHours(severity);
    return new Date(Date.now() + hours * 60 * 60 * 1000);
  }, [severity]);

  const handleAssign = async () => {
    if (!fault || !selectedTechnicianId) return;

    setSubmitting(true);
    try {
      const updatedFault = await assignFaultReport(fault.id, selectedTechnicianId, severity);
      toast({
        title: isReassign ? "Work Order Reassigned" : "Technician Assigned",
        description: `Dispatched to ${selectedTechnician?.full_name || "technician"}.`,
      });

      if (onAssigned) {
        onAssigned(updatedFault);
      }
      onOpenChange(false);
    } catch (error) {
      console.error("Failed to assign technician:", error);
      toast({
        title: "Assignment Failed",
        description: "Could not assign technician. Please try again.",
        variant: "destructive",
      });
    } finally {
      setSubmitting(false);
    }
  };

  if (!fault) return null;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <div className="flex items-center gap-2">
            <div className="rounded-lg bg-primary/20 p-2 text-primary">
              <UserPlus className="h-5 w-5" />
            </div>
            <div>
              <DialogTitle className="text-xl">
                {isReassign ? "Reassign Work Order" : "Assign Technician"}
              </DialogTitle>
              <DialogDescription>
                Assign {fault.machine?.name || "Equipment"} fault report to an on-duty technician.
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <div className="space-y-4 pt-2">
          {/* Fault Summary Card */}
          <div className="rounded-xl border border-border/80 bg-muted/40 p-3.5 space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Wrench className="h-4 w-4 text-primary" />
                <span className="font-semibold text-sm text-foreground">{fault.machine?.name || "Equipment"}</span>
                <span className="text-xs text-muted-foreground font-mono">({fault.machine?.model || fault.machine?.category})</span>
              </div>
              <Badge
                variant={
                  fault.severity === "critical"
                    ? "destructive"
                    : fault.severity === "high"
                    ? "warning"
                    : "outline"
                }
                className="text-[11px] uppercase tracking-wider"
              >
                {fault.severity || "medium"}
              </Badge>
            </div>
            <p className="text-xs text-muted-foreground leading-relaxed">
              {fault.description}
            </p>
            {fault.ai_diagnosis && (
              <div className="rounded-lg bg-background/70 border border-border/60 p-2 text-[11px] text-muted-foreground">
                <span className="font-semibold text-foreground">AI Insight: </span>
                {fault.ai_diagnosis}
              </div>
            )}
          </div>

          {/* Select Technician */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Select Technician <span className="text-rose-500">*</span>
            </label>
            <Select value={selectedTechnicianId} onValueChange={setSelectedTechnicianId}>
              <SelectTrigger>
                <SelectValue placeholder="Choose a qualified technician" />
              </SelectTrigger>
              <SelectContent>
                {technicians.map((tech) => {
                  const activeCount = activeTaskCountByTech[tech.id] ?? 0;
                  return (
                    <SelectItem key={tech.id} value={tech.id}>
                      <div className="flex items-center justify-between gap-3 w-full">
                        <span className="font-medium">{tech.full_name}</span>
                        <span
                          className={`text-[10px] px-1.5 py-0.5 rounded-full font-semibold ${
                            activeCount === 0
                              ? "bg-emerald-500/20 text-emerald-400"
                              : activeCount <= 2
                              ? "bg-amber-500/20 text-amber-400"
                              : "bg-rose-500/20 text-rose-400"
                          }`}
                        >
                          {activeCount} active task{activeCount === 1 ? "" : "s"}
                        </span>
                      </div>
                    </SelectItem>
                  );
                })}
              </SelectContent>
            </Select>

            {selectedTechnician && (
              <p className="text-[11px] text-muted-foreground flex items-center gap-1.5">
                <UserCheck className="h-3 w-3 text-emerald-400" />
                <span>Assigned to: <strong className="text-foreground">{selectedTechnician.full_name}</strong></span>
              </p>
            )}
          </div>

          {/* Urgency / Priority & Due Date preview */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Priority / SLA
              </label>
              <Select value={severity} onValueChange={(val) => setSeverity(val as FaultSeverity)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="critical">Critical (4h - Emergency)</SelectItem>
                  <SelectItem value="high">High (24h - Urgent)</SelectItem>
                  <SelectItem value="medium">Medium (48h - Standard)</SelectItem>
                  <SelectItem value="low">Low (72h - Routine)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="rounded-xl border border-border/80 bg-muted/30 p-3 flex flex-col justify-center text-xs">
              <div className="flex items-center gap-1 text-foreground font-medium">
                <Clock className="h-3.5 w-3.5 text-primary" />
                <span>Due in {getDueDateHours(severity)}h</span>
              </div>
              <p className="text-[11px] text-muted-foreground mt-0.5 flex items-center gap-1">
                <Calendar className="h-3 w-3" />
                {calculatedDueDate.toLocaleDateString()} {calculatedDueDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </div>
        </div>

        <DialogFooter className="gap-2 sm:gap-0 pt-2">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={submitting}>
            Cancel
          </Button>
          <Button
            onClick={handleAssign}
            disabled={!selectedTechnicianId || submitting}
            className="orange-glow bg-primary text-primary-foreground font-medium"
          >
            {submitting ? "Assigning..." : isReassign ? "Confirm Reassignment" : "Assign Technician"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
