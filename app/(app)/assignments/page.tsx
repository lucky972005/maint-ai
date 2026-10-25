"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import Link from "next/link";
import { AppShell } from "@/components/layout/app-shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  getFaultReports,
  getTechnicians,
  getMachines,
  updateFaultStatus,
} from "@/lib/database";
import { useApp } from "@/components/providers";
import { toast } from "@/hooks/use-toast";
import { formatDate } from "@/lib/utils";
import type { FaultReport, Profile, Machine, FaultSeverity } from "@/lib/types";
import { CreateWorkOrderModal } from "@/components/assignments/CreateWorkOrderModal";
import { AssignFaultModal } from "@/components/assignments/AssignFaultModal";
import {
  AlertTriangle,
  ArrowRight,
  Calendar,
  CheckCircle,
  Clock,
  ExternalLink,
  Filter,
  HardHat,
  Inbox,
  Plus,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
  User,
  UserCheck,
  UserPlus,
  Users,
  Wrench,
  X,
} from "lucide-react";

export default function AssignmentsPage() {
  const { profile, switchDemoRole } = useApp();
  const [allFaults, setAllFaults] = useState<FaultReport[]>([]);
  const [technicians, setTechnicians] = useState<Profile[]>([]);
  const [machines, setMachines] = useState<Machine[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters & Tabs
  const [activeTab, setActiveTab] = useState<string>("unassigned");
  const [searchQuery, setSearchQuery] = useState("");
  const [severityFilter, setSeverityFilter] = useState<string>("all");

  // Modals state
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [assignModalOpen, setAssignModalOpen] = useState(false);
  const [selectedFault, setSelectedFault] = useState<FaultReport | null>(null);
  const [isReassigning, setIsReassigning] = useState(false);
  const [targetTechForDirectCreate, setTargetTechForDirectCreate] = useState<string>("");

  const isSupervisorOrAdmin = profile?.role === "admin" || profile?.role === "supervisor";

  const loadData = useCallback(async () => {
    try {
      const [faultsData, techsData, machinesData] = await Promise.all([
        getFaultReports(),
        getTechnicians(),
        getMachines(),
      ]);
      setAllFaults(faultsData);
      setTechnicians(techsData);
      setMachines(machinesData);
    } catch (error) {
      console.error("Failed to load assignments data:", error);
      toast({
        title: "Error",
        description: "Failed to load assignment data.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Derived lists
  const unassignedFaults = useMemo(
    () => allFaults.filter((f) => !f.assigned_to && f.status === "open"),
    [allFaults]
  );

  const activeDispatchedFaults = useMemo(
    () => allFaults.filter((f) => f.assigned_to && (f.status === "assigned" || f.status === "in_progress")),
    [allFaults]
  );

  const completedFaults = useMemo(
    () => allFaults.filter((f) => f.status === "resolved"),
    [allFaults]
  );

  // Active task counts per technician
  const activeTaskCountByTech = useMemo(() => {
    const counts: Record<string, number> = {};
    technicians.forEach((t) => {
      counts[t.id] = 0;
    });
    activeDispatchedFaults.forEach((f) => {
      if (f.assigned_to) {
        counts[f.assigned_to] = (counts[f.assigned_to] || 0) + 1;
      }
    });
    return counts;
  }, [technicians, activeDispatchedFaults]);

  // Filtered unassigned
  const filteredUnassigned = useMemo(() => {
    return unassignedFaults.filter((f) => {
      if (severityFilter !== "all" && f.severity !== severityFilter) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const mName = f.machine?.name.toLowerCase() ?? "";
        const desc = f.description.toLowerCase();
        return mName.includes(q) || desc.includes(q);
      }
      return true;
    });
  }, [unassignedFaults, severityFilter, searchQuery]);

  // Filtered active dispatched
  const filteredActive = useMemo(() => {
    return activeDispatchedFaults.filter((f) => {
      if (severityFilter !== "all" && f.severity !== severityFilter) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const mName = f.machine?.name.toLowerCase() ?? "";
        const desc = f.description.toLowerCase();
        const techName = f.assigned_to_profile?.full_name.toLowerCase() ?? "";
        return mName.includes(q) || desc.includes(q) || techName.includes(q);
      }
      return true;
    });
  }, [activeDispatchedFaults, severityFilter, searchQuery]);

  const openAssignModal = (fault: FaultReport, isReassign = false) => {
    setSelectedFault(fault);
    setIsReassigning(isReassign);
    setAssignModalOpen(true);
  };

  const openCreateForTech = (techId: string) => {
    setTargetTechForDirectCreate(techId);
    setCreateModalOpen(true);
  };

  const getSeverityBadge = (severity: string | null) => {
    switch (severity) {
      case "critical":
        return <Badge variant="destructive" className="uppercase font-semibold">Critical</Badge>;
      case "high":
        return <Badge variant="warning" className="bg-amber-500 text-black uppercase font-semibold">High</Badge>;
      case "medium":
        return <Badge variant="outline" className="border-blue-500/50 text-blue-400 uppercase font-semibold">Medium</Badge>;
      case "low":
        return <Badge variant="outline" className="border-emerald-500/50 text-emerald-400 uppercase font-semibold">Low</Badge>;
      default:
        return <Badge variant="outline">Standard</Badge>;
    }
  };

  const getDueDateLabel = (dueDateStr: string | null) => {
    if (!dueDateStr) return "SLA pending";
    const now = new Date();
    const due = new Date(dueDateStr);
    const diffHours = Math.round((due.getTime() - now.getTime()) / (1000 * 60 * 60));

    if (diffHours < 0) {
      return <span className="text-rose-400 font-semibold">{Math.abs(diffHours)}h overdue</span>;
    }
    if (diffHours <= 4) {
      return <span className="text-amber-400 font-semibold">{diffHours}h remaining</span>;
    }
    return <span>Due in {diffHours}h</span>;
  };

  // If user is a technician
  if (profile && profile.role === "technician") {
    return (
      <AppShell title="Assignments">
        <div className="p-6 max-w-2xl mx-auto space-y-6 text-center">
          <Card className="border-border/80 bg-card/60 p-8">
            <div className="rounded-full bg-primary/15 p-4 w-16 h-16 mx-auto flex items-center justify-center text-primary mb-4">
              <HardHat className="h-8 w-8" />
            </div>
            <h2 className="text-xl font-bold text-foreground">Technician Access View</h2>
            <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
              Work orders and maintenance tasks are dispatched by <strong>Supervisors</strong> and <strong>Administrators</strong>. You can view, start, and resolve tasks assigned directly to you in your technician inbox.
            </p>
            <div className="mt-6 flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link href="/inbox">
                <Button className="orange-glow gap-2 bg-primary text-primary-foreground">
                  <Inbox className="h-4 w-4" />
                  <span>Go to My Assigned Inbox</span>
                </Button>
              </Link>
              <Button
                variant="outline"
                onClick={() => switchDemoRole("supervisor")}
                className="gap-2"
              >
                <ShieldCheck className="h-4 w-4 text-amber-400" />
                <span>Switch to Supervisor Role (Demo)</span>
              </Button>
            </div>
          </Card>
        </div>
      </AppShell>
    );
  }

  if (loading) {
    return (
      <AppShell title="Work Order Dispatch">
        <div className="flex h-96 flex-col items-center justify-center space-y-3">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
          <p className="text-sm text-muted-foreground animate-pulse">Loading work orders and technician rosters...</p>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell title="Work Order Dispatch">
      <div className="space-y-6 px-4 py-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Top Header & Direct Dispatch CTA */}
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
                Work Order Dispatch
              </h1>
              <Badge variant="secondary" className="gap-1 text-xs font-semibold bg-primary/15 text-primary border-primary/30">
                <ShieldCheck className="h-3.5 w-3.5" />
                {profile?.role === "admin" ? "Admin Authorization" : "Supervisor Dispatch"}
              </Badge>
            </div>
            <p className="mt-1 text-sm text-muted-foreground">
              Dispatch maintenance procedures and fault reports to technicians, manage shift assignments, and balance team workloads.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <Button
              variant="outline"
              size="sm"
              onClick={loadData}
              className="gap-1.5 text-xs"
              title="Refresh assignments"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Refresh</span>
            </Button>

            <Button
              size="sm"
              onClick={() => {
                setTargetTechForDirectCreate("");
                setCreateModalOpen(true);
              }}
              className="orange-glow gap-1.5 bg-primary text-primary-foreground font-semibold"
            >
              <Plus className="h-4 w-4" />
              <span>Create & Assign Work Order</span>
            </Button>
          </div>
        </div>

        {/* KPI Stat Cards */}
        <div className="grid grid-cols-2 gap-3 sm:gap-4 lg:grid-cols-4">
          <Card
            className={`cursor-pointer transition-all border-border/80 hover:border-amber-500/60 hover:bg-amber-500/5 ${
              activeTab === "unassigned" ? "ring-2 ring-amber-500/60 bg-amber-500/10" : ""
            }`}
            onClick={() => setActiveTab("unassigned")}
          >
            <CardContent className="p-4 sm:p-5">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-amber-400 uppercase tracking-wider">Unassigned Queue</p>
                <div className="rounded-lg bg-amber-500/15 p-2 text-amber-400">
                  <AlertTriangle className="h-4 w-4" />
                </div>
              </div>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-bold tracking-tight text-amber-400 sm:text-3xl">
                  {unassignedFaults.length}
                </span>
                <span className="text-xs text-amber-400/80">awaiting tech</span>
              </div>
              <p className="mt-1 text-[11px] text-muted-foreground">Requires technician dispatch</p>
            </CardContent>
          </Card>

          <Card
            className={`cursor-pointer transition-all border-border/80 hover:border-blue-500/60 hover:bg-blue-500/5 ${
              activeTab === "active" ? "ring-2 ring-blue-500/60 bg-blue-500/10" : ""
            }`}
            onClick={() => setActiveTab("active")}
          >
            <CardContent className="p-4 sm:p-5">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-blue-400 uppercase tracking-wider">Active Dispatched</p>
                <div className="rounded-lg bg-blue-500/15 p-2 text-blue-400">
                  <Clock className="h-4 w-4" />
                </div>
              </div>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
                  {activeDispatchedFaults.length}
                </span>
                <span className="text-xs text-muted-foreground">in progress</span>
              </div>
              <p className="mt-1 text-[11px] text-muted-foreground">Assigned & actively executing</p>
            </CardContent>
          </Card>

          <Card
            className={`cursor-pointer transition-all border-border/80 hover:border-primary/60 hover:bg-primary/5 ${
              activeTab === "technicians" ? "ring-2 ring-primary/60 bg-primary/10" : ""
            }`}
            onClick={() => setActiveTab("technicians")}
          >
            <CardContent className="p-4 sm:p-5">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-primary uppercase tracking-wider">Technician Roster</p>
                <div className="rounded-lg bg-primary/15 p-2 text-primary">
                  <Users className="h-4 w-4" />
                </div>
              </div>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
                  {technicians.length}
                </span>
                <span className="text-xs text-muted-foreground">on shift</span>
              </div>
              <p className="mt-1 text-[11px] text-muted-foreground">Available maintenance engineers</p>
            </CardContent>
          </Card>

          <Card
            className={`cursor-pointer transition-all border-border/80 hover:border-emerald-500/60 hover:bg-emerald-500/5 ${
              activeTab === "completed" ? "ring-2 ring-emerald-500/60 bg-emerald-500/10" : ""
            }`}
            onClick={() => setActiveTab("completed")}
          >
            <CardContent className="p-4 sm:p-5">
              <div className="flex items-center justify-between">
                <p className="text-xs font-medium text-emerald-400 uppercase tracking-wider">Resolved</p>
                <div className="rounded-lg bg-emerald-500/15 p-2 text-emerald-400">
                  <CheckCircle className="h-4 w-4" />
                </div>
              </div>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-bold tracking-tight text-foreground sm:text-3xl">
                  {completedFaults.length}
                </span>
                <span className="text-xs text-muted-foreground">closed</span>
              </div>
              <p className="mt-1 text-[11px] text-muted-foreground">Completed work orders</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Tab Navigation & Filters Toolbar */}
        <div className="space-y-4">
          <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between rounded-xl border border-border/80 bg-card/60 p-3.5 backdrop-blur-sm">
            {/* Tabs List */}
            <div className="flex flex-wrap items-center gap-1.5">
              <button
                type="button"
                onClick={() => setActiveTab("unassigned")}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition flex items-center gap-2 ${
                  activeTab === "unassigned"
                    ? "bg-amber-500 text-black shadow-sm"
                    : "bg-muted/60 text-muted-foreground hover:bg-muted hover:text-foreground"
                }`}
              >
                <span>Unassigned Queue</span>
                {unassignedFaults.length > 0 && (
                  <span className="rounded-full bg-black/20 px-1.5 py-0.2 text-[10px] font-bold">
                    {unassignedFaults.length}
                  </span>
                )}
              </button>

              <button
                type="button"
                onClick={() => setActiveTab("active")}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition flex items-center gap-2 ${
                  activeTab === "active"
                    ? "bg-blue-600 text-white shadow-sm"
                    : "bg-muted/60 text-muted-foreground hover:bg-muted hover:text-foreground"
                }`}
              >
                <span>Active Dispatched</span>
                <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px]">
                  {activeDispatchedFaults.length}
                </span>
              </button>

              <button
                type="button"
                onClick={() => setActiveTab("technicians")}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition flex items-center gap-2 ${
                  activeTab === "technicians"
                    ? "bg-primary text-primary-foreground shadow-sm"
                    : "bg-muted/60 text-muted-foreground hover:bg-muted hover:text-foreground"
                }`}
              >
                <span>Technician Roster</span>
                <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px]">
                  {technicians.length}
                </span>
              </button>

              <button
                type="button"
                onClick={() => setActiveTab("completed")}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition flex items-center gap-2 ${
                  activeTab === "completed"
                    ? "bg-emerald-600 text-white shadow-sm"
                    : "bg-muted/60 text-muted-foreground hover:bg-muted hover:text-foreground"
                }`}
              >
                <span>Completed Logs</span>
                <span className="rounded-full bg-white/20 px-1.5 py-0.2 text-[10px]">
                  {completedFaults.length}
                </span>
              </button>
            </div>

            {/* Search and Priority Filter */}
            <div className="flex flex-wrap items-center gap-2">
              <div className="relative min-w-[200px] flex-1 sm:flex-none">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
                <Input
                  placeholder="Search by equipment, task, or tech..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-8 h-8 text-xs bg-background/80"
                />
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery("")}
                    className="absolute right-2.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  >
                    <X className="h-3 w-3" />
                  </button>
                )}
              </div>

              <Select value={severityFilter} onValueChange={setSeverityFilter}>
                <SelectTrigger className="w-[130px] h-8 text-xs bg-background/80">
                  <SelectValue placeholder="Priority" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Priorities</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="low">Low</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* TAB 1: UNASSIGNED QUEUE */}
          {activeTab === "unassigned" && (
            <div className="space-y-3">
              {filteredUnassigned.length === 0 ? (
                <Card className="border-border/80 bg-card/40 p-10 text-center">
                  <div className="flex flex-col items-center justify-center space-y-3">
                    <div className="rounded-full bg-emerald-500/10 p-3 text-emerald-400">
                      <CheckCircle className="h-8 w-8" />
                    </div>
                    <h3 className="text-base font-semibold text-foreground">Unassigned Queue Empty</h3>
                    <p className="max-w-md text-xs text-muted-foreground">
                      No open work orders are currently awaiting assignment. Create a new work order or check active dispatched tasks.
                    </p>
                    <Button
                      size="sm"
                      onClick={() => setCreateModalOpen(true)}
                      className="orange-glow gap-1.5 mt-2"
                    >
                      <Plus className="h-4 w-4" />
                      Create Work Order
                    </Button>
                  </div>
                </Card>
              ) : (
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {filteredUnassigned.map((fault) => (
                    <Card
                      key={fault.id}
                      className="flex flex-col justify-between border-border/80 bg-card/70 hover:border-amber-500/50 transition shadow-sm"
                    >
                      <CardHeader className="p-4 pb-2 space-y-2">
                        <div className="flex items-start justify-between gap-2">
                          <div className="min-w-0">
                            <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground">
                              {fault.machine?.category || "Equipment"}
                            </span>
                            <h3 className="font-semibold text-sm text-foreground truncate" title={fault.machine?.name}>
                              {fault.machine?.name || "Equipment"}
                            </h3>
                          </div>
                          {getSeverityBadge(fault.severity)}
                        </div>
                        <p className="text-xs text-muted-foreground line-clamp-2">
                          {fault.description}
                        </p>
                      </CardHeader>

                      <CardContent className="p-4 pt-2 space-y-3">
                        {fault.ai_diagnosis && (
                          <div className="rounded-md bg-muted/50 border border-border/60 p-2 text-[11px] text-muted-foreground">
                            <span className="font-semibold text-foreground">Diagnosis: </span>
                            <span className="line-clamp-2">{fault.ai_diagnosis}</span>
                          </div>
                        )}

                        <div className="flex items-center justify-between text-xs text-muted-foreground border-t border-border/60 pt-2">
                          <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            <span>{getDueDateLabel(fault.due_date)}</span>
                          </div>
                          <span>{formatDate(fault.created_at || "")}</span>
                        </div>

                        <Button
                          size="sm"
                          className="w-full orange-glow gap-1.5 bg-primary text-primary-foreground font-medium"
                          onClick={() => openAssignModal(fault)}
                        >
                          <UserPlus className="h-4 w-4" />
                          <span>Assign Technician</span>
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB 2: ACTIVE DISPATCHED TASKS */}
          {activeTab === "active" && (
            <div className="space-y-3">
              {filteredActive.length === 0 ? (
                <Card className="border-border/80 bg-card/40 p-10 text-center">
                  <div className="flex flex-col items-center justify-center space-y-2">
                    <Clock className="h-8 w-8 text-muted-foreground opacity-50" />
                    <h3 className="text-base font-semibold text-foreground">No Active Dispatched Tasks</h3>
                    <p className="text-xs text-muted-foreground">
                      No tasks are currently assigned or in progress matching your filters.
                    </p>
                  </div>
                </Card>
              ) : (
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {filteredActive.map((fault) => {
                    const tech = fault.assigned_to_profile || technicians.find((t) => t.id === fault.assigned_to);
                    const isInProgress = fault.status === "in_progress";

                    return (
                      <Card
                        key={fault.id}
                        className="flex flex-col justify-between border-border/80 bg-card/70 hover:border-blue-500/50 transition shadow-sm"
                      >
                        <CardHeader className="p-4 pb-2 space-y-2">
                          <div className="flex items-start justify-between gap-2">
                            <div>
                              <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground">
                                {fault.machine?.category}
                              </span>
                              <h3 className="font-semibold text-sm text-foreground truncate" title={fault.machine?.name}>
                                {fault.machine?.name}
                              </h3>
                            </div>
                            <div className="flex items-center gap-1.5">
                              {getSeverityBadge(fault.severity)}
                              <Badge
                                className={
                                  isInProgress
                                    ? "bg-purple-600 text-white font-semibold text-[10px]"
                                    : "bg-blue-600 text-white font-semibold text-[10px]"
                                }
                              >
                                {isInProgress ? "IN PROGRESS" : "ASSIGNED"}
                              </Badge>
                            </div>
                          </div>
                          <p className="text-xs text-muted-foreground line-clamp-2">
                            {fault.description}
                          </p>
                        </CardHeader>

                        <CardContent className="p-4 pt-2 space-y-3">
                          {/* Technician Card */}
                          <div className="flex items-center justify-between rounded-lg border border-border/70 bg-muted/40 p-2.5">
                            <div className="flex items-center gap-2">
                              <div className="h-7 w-7 rounded-full bg-primary/20 text-primary flex items-center justify-center text-xs font-bold">
                                {tech?.full_name ? tech.full_name.charAt(0) : "T"}
                              </div>
                              <div>
                                <p className="text-xs font-medium text-foreground">{tech?.full_name || "Assigned Technician"}</p>
                                <p className="text-[10px] text-muted-foreground">{tech?.email}</p>
                              </div>
                            </div>
                            <span className="text-[10px] text-muted-foreground">
                              {fault.assigned_at ? `Assigned ${formatDate(fault.assigned_at)}` : ""}
                            </span>
                          </div>

                          <div className="flex items-center justify-between text-xs text-muted-foreground">
                            <div className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              <span>{getDueDateLabel(fault.due_date)}</span>
                            </div>
                            {fault.machine_id && (
                              <Link
                                href={`/repair/${fault.machine_id}`}
                                className="text-xs text-primary hover:underline flex items-center gap-1"
                              >
                                <span>Machine flow</span>
                                <ExternalLink className="h-3 w-3" />
                              </Link>
                            )}
                          </div>

                          <div className="flex items-center gap-2 pt-1 border-t border-border/60">
                            <Button
                              size="sm"
                              variant="outline"
                              className="flex-1 text-xs gap-1"
                              onClick={() => openAssignModal(fault, true)}
                            >
                              <UserCheck className="h-3.5 w-3.5" />
                              <span>Reassign</span>
                            </Button>
                          </div>
                        </CardContent>
                      </Card>
                    );
                  })}
                </div>
              )}
            </div>
          )}

          {/* TAB 3: TECHNICIAN WORKLOAD ROSTER */}
          {activeTab === "technicians" && (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {technicians.map((tech) => {
                const activeCount = activeTaskCountByTech[tech.id] ?? 0;
                const assignedTasks = activeDispatchedFaults.filter((f) => f.assigned_to === tech.id);
                const workloadStatus =
                  activeCount === 0
                    ? { label: "Available", color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" }
                    : activeCount <= 2
                    ? { label: "Balanced", color: "bg-blue-500/20 text-blue-400 border-blue-500/30" }
                    : { label: "High Workload", color: "bg-rose-500/20 text-rose-400 border-rose-500/30" };

                return (
                  <Card key={tech.id} className="border-border/80 bg-card/70 flex flex-col justify-between">
                    <CardHeader className="p-4 pb-3">
                      <div className="flex items-start justify-between gap-3">
                        <div className="flex items-center gap-3">
                          <div className="h-10 w-10 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold text-sm">
                            {tech.full_name ? tech.full_name.charAt(0) : "T"}
                          </div>
                          <div>
                            <h3 className="font-semibold text-sm text-foreground">{tech.full_name}</h3>
                            <p className="text-xs text-muted-foreground">{tech.email}</p>
                          </div>
                        </div>
                        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${workloadStatus.color}`}>
                          {workloadStatus.label}
                        </span>
                      </div>
                    </CardHeader>

                    <CardContent className="p-4 pt-0 space-y-3">
                      <div className="rounded-lg border border-border/70 bg-muted/30 p-2.5 flex items-center justify-between text-xs">
                        <span className="text-muted-foreground">Active Work Orders:</span>
                        <span className="font-bold text-foreground">{activeCount} tasks</span>
                      </div>

                      {assignedTasks.length > 0 ? (
                        <div className="space-y-1.5">
                          <p className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">
                            Assigned queue:
                          </p>
                          {assignedTasks.slice(0, 3).map((task) => (
                            <div
                              key={task.id}
                              className="rounded-md border border-border/60 bg-background/50 p-2 text-xs flex items-center justify-between gap-2"
                            >
                              <span className="truncate font-medium text-foreground">{task.machine?.name || "Equipment"}</span>
                              {getSeverityBadge(task.severity)}
                            </div>
                          ))}
                          {assignedTasks.length > 3 && (
                            <p className="text-[10px] text-muted-foreground text-center">
                              +{assignedTasks.length - 3} more task(s)
                            </p>
                          )}
                        </div>
                      ) : (
                        <p className="text-xs text-muted-foreground italic py-1">
                          No active assignments. Ready for dispatch.
                        </p>
                      )}

                      <Button
                        size="sm"
                        className="w-full text-xs gap-1.5 orange-glow bg-primary text-primary-foreground"
                        onClick={() => openCreateForTech(tech.id)}
                      >
                        <UserPlus className="h-3.5 w-3.5" />
                        <span>Assign Direct Work</span>
                      </Button>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}

          {/* TAB 4: COMPLETED LOGS */}
          {activeTab === "completed" && (
            <div className="space-y-3">
              {completedFaults.length === 0 ? (
                <Card className="border-border/80 bg-card/40 p-10 text-center">
                  <p className="text-xs text-muted-foreground">No resolved work orders in the current cycle.</p>
                </Card>
              ) : (
                <div className="overflow-x-auto rounded-xl border border-border/80 bg-card/60">
                  <table className="w-full text-left text-xs">
                    <thead className="border-b border-border/80 bg-muted/40 text-[11px] uppercase tracking-wider text-muted-foreground font-semibold">
                      <tr>
                        <th className="py-3 pl-4 pr-3">Equipment</th>
                        <th className="px-3 py-3">Work Summary</th>
                        <th className="px-3 py-3">Completed By</th>
                        <th className="px-3 py-3">Priority</th>
                        <th className="py-3 pl-3 pr-4 text-right">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-border/60">
                      {completedFaults.map((fault) => (
                        <tr key={fault.id} className="hover:bg-muted/20">
                          <td className="py-2.5 pl-4 pr-3 font-medium text-foreground">
                            {fault.machine?.name || "Equipment"}
                          </td>
                          <td className="px-3 py-2.5 text-muted-foreground max-w-xs truncate">
                            {fault.description}
                          </td>
                          <td className="px-3 py-2.5 text-foreground font-medium">
                            {fault.assigned_to_profile?.full_name || "Maintenance Tech"}
                          </td>
                          <td className="px-3 py-2.5">
                            {getSeverityBadge(fault.severity)}
                          </td>
                          <td className="py-2.5 pl-3 pr-4 text-right">
                            <Badge variant="success" className="bg-emerald-600 text-white font-semibold">
                              RESOLVED
                            </Badge>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Create Work Order Modal */}
        <CreateWorkOrderModal
          open={createModalOpen}
          onOpenChange={setCreateModalOpen}
          machines={machines}
          technicians={technicians}
          initialTechnicianId={targetTechForDirectCreate}
          activeTaskCountByTech={activeTaskCountByTech}
          onWorkOrderCreated={() => {
            loadData();
          }}
        />

        {/* Assign / Reassign Fault Modal */}
        <AssignFaultModal
          open={assignModalOpen}
          onOpenChange={setAssignModalOpen}
          fault={selectedFault}
          technicians={technicians}
          activeTaskCountByTech={activeTaskCountByTech}
          isReassign={isReassigning}
          onAssigned={() => {
            loadData();
          }}
        />
      </div>
    </AppShell>
  );
}
