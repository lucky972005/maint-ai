"use client";

import { useEffect, useState, useCallback } from "react";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { getFaultsForTechnician, updateFaultStatus } from "@/lib/database";
import { useApp } from "@/components/providers";
import { toast } from "@/hooks/use-toast";
import { Clock, AlertTriangle, CheckCircle, PlayCircle, User } from "lucide-react";
import { formatDate } from "@/lib/utils";
import type { FaultReport } from "@/lib/types";

export default function InboxPage() {
  const { profile } = useApp();
  const [assignedFaults, setAssignedFaults] = useState<FaultReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState<string | null>(null);

  const loadInbox = useCallback(async () => {
    if (!profile?.id) return;

    try {
      const faults = await getFaultsForTechnician(profile.id);
      setAssignedFaults(faults);
    } catch (error) {
      console.error("Failed to load inbox:", error);
      toast({ title: "Error", description: "Failed to load inbox", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  }, [profile?.id]);

  useEffect(() => {
    loadInbox();
  }, [loadInbox]);

  const handleStatusChange = async (faultId: string, newStatus: "assigned" | "in_progress" | "resolved") => {
    setUpdating(faultId);
    try {
      await updateFaultStatus(faultId, newStatus);
      toast({ title: "Success", description: `Status updated to ${newStatus}` });
      loadInbox();
    } catch (error) {
      console.error("Failed to update status:", error);
      toast({ title: "Error", description: "Failed to update status", variant: "destructive" });
    } finally {
      setUpdating(null);
    }
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

  const getStatusColor = (status: string) => {
    switch (status) {
      case "assigned": return "bg-blue-500";
      case "in_progress": return "bg-purple-500";
      case "resolved": return "bg-green-500";
      default: return "bg-gray-500";
    }
  };

  const isOverdue = (dueDate: string | null) => {
    if (!dueDate) return false;
    return new Date(dueDate) < new Date();
  };

  const getTimeRemaining = (dueDate: string | null) => {
    if (!dueDate) return null;
    const now = new Date();
    const due = new Date(dueDate);
    const diff = due.getTime() - now.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    
    if (hours < 0) return `${Math.abs(hours)}h overdue`;
    if (hours < 24) return `${hours}h remaining`;
    const days = Math.floor(hours / 24);
    return `${days}d remaining`;
  };

  if (loading) {
    return (
      <AppShell title="Inbox">
        <div className="p-8 text-center">
          <p className="text-muted-foreground">Loading inbox...</p>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell title="Technician Inbox">
      <div className="p-4 space-y-6 max-w-7xl mx-auto">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">My Work Orders</h2>
            <p className="text-muted-foreground">View and manage assigned fault reports</p>
          </div>
          <div className="flex gap-2">
            <Badge variant="outline">{assignedFaults.filter(f => f.status === "assigned").length} Pending</Badge>
            <Badge variant="outline">{assignedFaults.filter(f => f.status === "in_progress").length} In Progress</Badge>
          </div>
        </div>

        <div className="grid gap-4">
          {assignedFaults.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center">
                <CheckCircle className="h-12 w-12 mx-auto mb-4 text-green-500" />
                <h3 className="text-lg font-semibold mb-2">No work orders</h3>
                <p className="text-muted-foreground">You don&apos;t have any assigned fault reports.</p>
              </CardContent>
            </Card>
          ) : (
            assignedFaults.map((fault) => (
              <Card key={fault.id} className={`border-border/70 ${isOverdue(fault.due_date) ? "border-red-500/50" : ""}`}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <CardTitle className="text-lg">{fault.machine?.name || "Unknown Machine"}</CardTitle>
                        <Badge className={getSeverityColor(fault.severity || "medium")}>
                          {fault.severity?.toUpperCase() || "MEDIUM"}
                        </Badge>
                        <Badge className={getStatusColor(fault.status || "assigned")}>
                          {fault.status?.replace("_", " ").toUpperCase() || "ASSIGNED"}
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {fault.machine?.category} • Assigned {formatDate(fault.assigned_at || "")}
                      </p>
                    </div>
                    {fault.due_date && (
                      <div className={`flex items-center gap-1 text-xs ${isOverdue(fault.due_date) ? "text-red-500" : "text-muted-foreground"}`}>
                        <Clock className="h-3 w-3" />
                        <span>{getTimeRemaining(fault.due_date)}</span>
                      </div>
                    )}
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <p className="text-sm">{fault.description}</p>
                    {fault.ai_diagnosis && (
                      <div className="bg-muted/50 p-3 rounded-lg">
                        <p className="text-xs font-semibold mb-1">AI Diagnosis:</p>
                        <p className="text-xs text-muted-foreground">{fault.ai_diagnosis}</p>
                      </div>
                    )}
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      {fault.assigned_to_profile && (
                        <div className="flex items-center gap-1">
                          <User className="h-3 w-3" />
                          <span>Assigned to: {fault.assigned_to_profile.full_name}</span>
                        </div>
                      )}
                      {fault.attachments && fault.attachments.length > 0 && (
                        <div className="flex items-center gap-1">
                          <AlertTriangle className="h-3 w-3" />
                          <span>{fault.attachments.length} attachment(s)</span>
                        </div>
                      )}
                    </div>
                    <div className="flex gap-2 pt-2">
                      {fault.status === "assigned" && (
                        <Button
                          size="sm"
                          onClick={() => handleStatusChange(fault.id, "in_progress")}
                          disabled={updating === fault.id}
                        >
                          <PlayCircle className="h-4 w-4 mr-2" />
                          {updating === fault.id ? "Starting..." : "Start Work"}
                        </Button>
                      )}
                      {fault.status === "in_progress" && (
                        <Button
                          size="sm"
                          onClick={() => handleStatusChange(fault.id, "resolved")}
                          disabled={updating === fault.id}
                        >
                          <CheckCircle className="h-4 w-4 mr-2" />
                          {updating === fault.id ? "Resolving..." : "Mark Resolved"}
                        </Button>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>
    </AppShell>
  );
}
