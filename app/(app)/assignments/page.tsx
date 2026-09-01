"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { getUnassignedFaults, getTechnicians, assignFaultReport } from "@/lib/database";
import { useApp } from "@/components/providers";
import { toast } from "@/hooks/use-toast";
import { User, Clock, AlertTriangle, CheckCircle, Calendar } from "lucide-react";
import { formatDate } from "@/lib/utils";
import type { FaultReport, Profile } from "@/lib/types";

export default function AssignmentsPage() {
  const { profile } = useApp();
  const [unassignedFaults, setUnassignedFaults] = useState<FaultReport[]>([]);
  const [technicians, setTechnicians] = useState<Profile[]>([]);
  const [loading, setLoading] = useState(true);
  const [assignDialogOpen, setAssignDialogOpen] = useState(false);
  const [selectedFault, setSelectedFault] = useState<FaultReport | null>(null);
  const [selectedTechnician, setSelectedTechnician] = useState<string>("");
  const [assigning, setAssigning] = useState(false);

  const loadAssignmentData = async () => {
    try {
      const [faults, techs] = await Promise.all([
        getUnassignedFaults(),
        getTechnicians(),
      ]);
      setUnassignedFaults(faults);
      setTechnicians(techs);
    } catch (error) {
      console.error("Failed to load assignment data:", error);
      toast({ title: "Error", description: "Failed to load assignment data", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAssignmentData();
  }, []);

  const handleAssign = async () => {
    if (!selectedFault || !selectedTechnician) return;

    setAssigning(true);
    try {
      await assignFaultReport(selectedFault.id, selectedTechnician);
      toast({ title: "Success", description: "Fault assigned successfully" });
      setAssignDialogOpen(false);
      setSelectedFault(null);
      setSelectedTechnician("");
      loadAssignmentData();
    } catch (error) {
      console.error("Failed to assign fault:", error);
      toast({ title: "Error", description: "Failed to assign fault", variant: "destructive" });
    } finally {
      setAssigning(false);
    }
  };

  const openAssignDialog = (fault: FaultReport) => {
    setSelectedFault(fault);
    setSelectedTechnician("");
    setAssignDialogOpen(true);
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "critical": return "bg-red-500";
      case "high": return "bg-orange-500";
      case "medium": return "bg-yellow-500";
      case "low": return "bg-green-500";
      default: return "bg-gray-500";
    }
  };

  const getDueDateHours = (severity: string) => {
    switch (severity) {
      case "critical": return 4;
      case "high": return 24;
      case "medium": return 48;
      case "low": return 72;
      default: return 72;
    }
  };

  if (profile && profile.role === "technician") {
    return (
      <AppShell title="Assignments">
        <div className="p-8 text-center">
          <p className="text-muted-foreground">Assignment management requires supervisor or admin role.</p>
        </div>
      </AppShell>
    );
  }

  if (loading) {
    return (
      <AppShell title="Assignments">
        <div className="p-8 text-center">
          <p className="text-muted-foreground">Loading assignments...</p>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell title="Fault Assignments">
      <div className="p-4 space-y-6 max-w-7xl mx-auto">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Work Order Management</h2>
            <p className="text-muted-foreground">Assign fault reports to technicians and track progress</p>
          </div>
          <Badge variant="outline">{unassignedFaults.length} Unassigned</Badge>
        </div>

        <div className="grid gap-4">
          {unassignedFaults.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center">
                <CheckCircle className="h-12 w-12 mx-auto mb-4 text-green-500" />
                <h3 className="text-lg font-semibold mb-2">All caught up!</h3>
                <p className="text-muted-foreground">No unassigned fault reports at the moment.</p>
              </CardContent>
            </Card>
          ) : (
            unassignedFaults.map((fault) => (
              <Card key={fault.id} className="border-border/70">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <CardTitle className="text-lg">{fault.machine?.name || "Unknown Machine"}</CardTitle>
                        <Badge className={getSeverityColor(fault.severity || "medium")}>
                          {fault.severity?.toUpperCase() || "MEDIUM"}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {fault.machine?.category} • {formatDate(fault.created_at || "")}
                      </p>
                    </div>
                    <Button onClick={() => openAssignDialog(fault)}>
                      <User className="h-4 w-4 mr-2" />
                      Assign Technician
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <p className="text-sm">{fault.description}</p>
                    {fault.ai_diagnosis && (
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <p className="text-xs font-semibold mb-1">AI Diagnosis:</p>
                    <p className="text-xs text-muted-foreground">{fault.ai_diagnosis}</p>
                  </div>
                )}
                    <div className="flex items-center gap-4 text-xs text-muted-foreground">
                      <div className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        <span>Due within {getDueDateHours(fault.severity || "medium")}h</span>
                      </div>
                      {fault.attachments && fault.attachments.length > 0 && (
                        <div className="flex items-center gap-1">
                          <AlertTriangle className="h-3 w-3" />
                          <span>{fault.attachments.length} attachment(s)</span>
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        <Dialog open={assignDialogOpen} onOpenChange={setAssignDialogOpen}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Assign Fault Report</DialogTitle>
              <DialogDescription>
                Assign {selectedFault?.machine?.name} to a technician
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Select Technician</label>
                <Select value={selectedTechnician} onValueChange={setSelectedTechnician}>
                  <SelectTrigger>
                    <SelectValue placeholder="Choose a technician" />
                  </SelectTrigger>
                  <SelectContent>
                    {technicians.map((tech) => (
                      <SelectItem key={tech.id} value={tech.id}>
                        {tech.full_name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              {selectedFault && (
                <div className="bg-muted/50 p-3 rounded-lg space-y-2">
                  <div className="flex items-center gap-2 text-sm">
                    <Calendar className="h-4 w-4" />
                    <span>Due date: {new Date(Date.now() + getDueDateHours(selectedFault.severity || "medium") * 60 * 60 * 1000).toLocaleString()}</span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Based on severity: {selectedFault.severity?.toUpperCase() || "MEDIUM"}
                  </p>
                </div>
              )}
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setAssignDialogOpen(false)}>
                Cancel
              </Button>
              <Button onClick={handleAssign} disabled={!selectedTechnician || assigning}>
                {assigning ? "Assigning..." : "Assign"}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </AppShell>
  );
}
