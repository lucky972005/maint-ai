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
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useApp } from "@/components/providers";
import { createFaultReport, getProceduresForMachine } from "@/lib/database";
import { toast } from "@/hooks/use-toast";
import type { Machine, Profile, FaultReport, FaultSeverity, RepairProcedure } from "@/lib/types";
import {
  Calendar,
  Clock,
  HardHat,
  Send,
  UserCheck,
} from "lucide-react";

interface CreateWorkOrderModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  machines: Machine[];
  technicians: Profile[];
  initialMachineId?: string;
  initialProcedureName?: string;
  initialTechnicianId?: string;
  activeTaskCountByTech?: Record<string, number>;
  onWorkOrderCreated?: (newReport: FaultReport) => void;
}

export function CreateWorkOrderModal({
  open,
  onOpenChange,
  machines,
  technicians,
  initialMachineId = "",
  initialProcedureName = "",
  initialTechnicianId = "",
  activeTaskCountByTech = {},
  onWorkOrderCreated,
}: CreateWorkOrderModalProps) {
  const { profile } = useApp();
  const [selectedMachineId, setSelectedMachineId] = useState(initialMachineId);
  const [taskTitle, setTaskTitle] = useState(initialProcedureName);
  const [selectedTechnicianId, setSelectedTechnicianId] = useState(initialTechnicianId);
  const [severity, setSeverity] = useState<FaultSeverity>("medium");
  const [instructions, setInstructions] = useState("");
  const [procedures, setProcedures] = useState<RepairProcedure[]>([]);
  const [submitting, setSubmitting] = useState(false);

  // Sync initial props
  useEffect(() => {
    if (open) {
      if (initialMachineId) setSelectedMachineId(initialMachineId);
      if (initialProcedureName) setTaskTitle(initialProcedureName);
      if (initialTechnicianId) setSelectedTechnicianId(initialTechnicianId);
    }
  }, [open, initialMachineId, initialProcedureName, initialTechnicianId]);

  // Load procedures when machine changes
  useEffect(() => {
    if (selectedMachineId) {
      getProceduresForMachine(selectedMachineId)
        .then((data) => setProcedures(data))
        .catch(() => setProcedures([]));
    } else {
      setProcedures([]);
    }
  }, [selectedMachineId]);

  const selectedMachine = useMemo(
    () => machines.find((m) => m.id === selectedMachineId),
    [machines, selectedMachineId]
  );

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
    const date = new Date(Date.now() + hours * 60 * 60 * 1000);
    return date;
  }, [severity]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedMachineId || !taskTitle.trim() || !selectedTechnicianId) {
      toast({
        title: "Missing Information",
        description: "Please select a machine, enter task title, and assign a technician.",
        variant: "destructive",
      });
      return;
    }

    setSubmitting(true);
    try {
      const fullDescription = instructions.trim()
        ? `${taskTitle.trim()} - Instructions: ${instructions.trim()}`
        : taskTitle.trim();

      const newWorkOrder = await createFaultReport({
        machine_id: selectedMachineId,
        reported_by: profile?.id ?? null,
        assigned_to: selectedTechnicianId,
        description: fullDescription,
        severity,
        status: "assigned",
        assigned_at: new Date().toISOString(),
        due_date: calculatedDueDate.toISOString(),
        ai_diagnosis: `Dispatched by ${profile?.role?.toUpperCase() || "SUPERVISOR"} (${profile?.full_name || "Manager"})`,
        ai_detection_results: null,
        attachments: [],
      });

      toast({
        title: "Work Order Assigned",
        description: `Dispatched "${taskTitle}" to ${selectedTechnician?.full_name || "technician"}.`,
      });

      if (onWorkOrderCreated) {
        onWorkOrderCreated(newWorkOrder);
      }

      onOpenChange(false);
      // Reset form
      setTaskTitle("");
      setInstructions("");
    } catch (error) {
      console.error("Failed to create work order assignment:", error);
      toast({
        title: "Assignment Failed",
        description: "Could not create work order. Please try again.",
        variant: "destructive",
      });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <div className="flex items-center gap-2">
            <div className="rounded-lg bg-primary/20 p-2 text-primary">
              <HardHat className="h-5 w-5" />
            </div>
            <div>
              <DialogTitle className="text-xl">Dispatch Work Order</DialogTitle>
              <DialogDescription>
                Assign preventive maintenance, inspection, or repairs directly to a technician.
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4 pt-2">
          {/* Machine Selection */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Equipment / Machine <span className="text-rose-500">*</span>
            </label>
            <Select value={selectedMachineId} onValueChange={setSelectedMachineId}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select target equipment" />
              </SelectTrigger>
              <SelectContent className="max-h-60">
                {machines.map((machine) => (
                  <SelectItem key={machine.id} value={machine.id}>
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{machine.name}</span>
                      <span className="text-xs text-muted-foreground font-mono">({machine.model || machine.category})</span>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {selectedMachine && (
              <p className="text-[11px] text-muted-foreground">
                Location: {selectedMachine.location || "Main Plant Floor"} • Status: {selectedMachine.status}
              </p>
            )}
          </div>

          {/* Quick Procedure Select or Custom Title */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Work Order / Procedure <span className="text-rose-500">*</span>
              </label>
              {procedures.length > 0 && (
                <span className="text-[11px] text-primary">
                  {procedures.length} procedure templates available
                </span>
              )}
            </div>

            {procedures.length > 0 && (
              <div className="mb-2 flex flex-wrap gap-1.5">
                {procedures.map((proc) => (
                  <button
                    key={proc.id}
                    type="button"
                    onClick={() => {
                      setTaskTitle(proc.procedure_type);
                      if (proc.difficulty === "hard") setSeverity("high");
                      else if (proc.difficulty === "medium") setSeverity("medium");
                      else setSeverity("low");
                    }}
                    className={`rounded-md border px-2.5 py-1 text-xs transition ${
                      taskTitle === proc.procedure_type
                        ? "border-primary bg-primary/15 text-primary font-semibold"
                        : "border-border/80 bg-muted/40 text-muted-foreground hover:bg-muted hover:text-foreground"
                    }`}
                  >
                    {proc.procedure_type} ({proc.estimated_minutes}m)
                  </button>
                ))}
              </div>
            )}

            <Input
              placeholder="e.g., Oil Change & Filter Replacement, Belt Alignment Inspection"
              value={taskTitle}
              onChange={(e) => setTaskTitle(e.target.value)}
              required
            />
          </div>

          {/* Technician Selection with Workload Indicators */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Assign to Technician <span className="text-rose-500">*</span>
              </label>
              <span className="text-[11px] text-muted-foreground">
                Current active workloads shown below
              </span>
            </div>

            <Select value={selectedTechnicianId} onValueChange={setSelectedTechnicianId}>
              <SelectTrigger className="w-full">
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
                <span>Selected: <strong className="text-foreground">{selectedTechnician.full_name}</strong> ({selectedTechnician.email})</span>
              </p>
            )}
          </div>

          {/* Severity & SLA Preview */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Priority / Urgency
              </label>
              <Select value={severity} onValueChange={(val) => setSeverity(val as FaultSeverity)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="critical">Critical (4h - Machine Down)</SelectItem>
                  <SelectItem value="high">High (24h - High Risk)</SelectItem>
                  <SelectItem value="medium">Medium (48h - Standard)</SelectItem>
                  <SelectItem value="low">Low (72h - Routine)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="rounded-xl border border-border/80 bg-muted/30 p-3 flex flex-col justify-center">
              <div className="flex items-center gap-1.5 text-xs font-medium text-foreground">
                <Clock className="h-3.5 w-3.5 text-primary" />
                <span>Target SLA: Within {getDueDateHours(severity)} Hours</span>
              </div>
              <p className="text-[11px] text-muted-foreground mt-0.5 flex items-center gap-1">
                <Calendar className="h-3 w-3" />
                Due: {calculatedDueDate.toLocaleDateString()} at {calculatedDueDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </div>

          {/* Dispatch Instructions & Notes */}
          <div className="space-y-1.5">
            <label className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Instructions & Safety Notes (Optional)
            </label>
            <Textarea
              placeholder="e.g., Follow Lockout/Tagout protocol. Required tools: 14mm socket, grease gun. Check vibration post-service."
              value={instructions}
              onChange={(e) => setInstructions(e.target.value)}
              rows={3}
              className="resize-none"
            />
          </div>

          <DialogFooter className="gap-2 sm:gap-0 pt-2">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)} disabled={submitting}>
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={!selectedMachineId || !taskTitle.trim() || !selectedTechnicianId || submitting}
              className="orange-glow gap-1.5 bg-primary text-primary-foreground font-medium"
            >
              <Send className="h-4 w-4" />
              <span>{submitting ? "Dispatching..." : "Dispatch Work Order"}</span>
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
