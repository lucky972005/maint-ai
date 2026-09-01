"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/layout/app-shell";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DEMO_DATA, isFirebaseConfigured } from "@/lib/demo-data";
import { getMaintenanceLogs } from "@/lib/database";
import { formatDate, formatDuration } from "@/lib/utils";
import { useApp } from "@/components/providers";
import { ClipboardCheck, Download, FileCheck, Filter, TimerReset, Wrench } from "lucide-react";
import { getCachedMaintenanceLogs } from "@/lib/offline";
import { WorkOrderCertificateModal } from "@/components/certificate/WorkOrderCertificateModal";
import type { MaintenanceLog } from "@/lib/types";

export default function HistoryPage() {
  const { profile } = useApp();
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [myRepairs, setMyRepairs] = useState(false);
  const [selectedLog, setSelectedLog] = useState<string | null>(null);
  const [certificateLog, setCertificateLog] = useState<MaintenanceLog | null>(null);
  const [showCertModal, setShowCertModal] = useState(false);
  const [logs, setLogs] = useState<MaintenanceLog[]>(DEMO_DATA.logs);
  const [loading, setLoading] = useState(true);
  const [useRealData, setUseRealData] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      const firebaseConfigured = isFirebaseConfigured();
      setUseRealData(firebaseConfigured);

      if (firebaseConfigured) {
        try {
          const logsData = await getMaintenanceLogs(200);
          setLogs(logsData);
        } catch (error) {
          console.error("Failed to load logs from Firebase:", error);
        }
      } else {
        const cached = await getCachedMaintenanceLogs();
        if (cached.length > 0) {
          setLogs(cached);
        }
      }
      setLoading(false);
    };

    loadData();
  }, []);

  const allLogs = useMemo(() => {
    return logs.sort(
      (a, b) => new Date(b.started_at).getTime() - new Date(a.started_at).getTime()
    );
  }, [logs]);

  const filtered = useMemo(() => {
    return allLogs.filter((log) => {
      if (myRepairs && profile && log.technician_id !== profile.id) return false;
      if (statusFilter !== "all" && log.status !== statusFilter) return false;
      if (search) {
        const query = search.toLowerCase();
        return (
          log.machine?.name.toLowerCase().includes(query) ||
          log.procedure?.procedure_type.toLowerCase().includes(query) ||
          log.technician?.full_name.toLowerCase().includes(query)
        );
      }
      return true;
    });
  }, [allLogs, myRepairs, profile, search, statusFilter]);

  const metrics = useMemo(() => {
    const completed = filtered.filter((log) => log.status === "completed");
    const avgDuration =
      completed.length > 0
        ? Math.round(
            completed.reduce((total, log) => total + (log.duration_minutes ?? 0), 0) / completed.length
          )
        : 0;

    return {
      total: filtered.length,
      completed: completed.length,
      inProgress: filtered.filter((log) => log.status === "in_progress").length,
      avgDuration,
    };
  }, [filtered]);

  const exportCsv = () => {
    const headers = ["Date", "Machine", "Procedure", "Technician", "Duration", "Status"];
    const rows = filtered.map((log) => [
      formatDate(log.started_at),
      log.machine?.name ?? "",
      log.procedure?.procedure_type ?? "",
      log.technician?.full_name ?? "",
      log.duration_minutes ? formatDuration(log.duration_minutes) : "-",
      log.status ?? "",
    ]);
    const csv = [headers, ...rows].map((row) => row.join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "maintenance-history.csv";
    anchor.click();
    URL.revokeObjectURL(url);
  };

  const selected = filtered.find((log) => log.id === selectedLog);

  if (loading) {
    return (
      <AppShell title="History">
        <div className="p-8 text-center">
          <p className="text-muted-foreground">Loading maintenance history...</p>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell title="History">
      <div className="space-y-6 px-4 py-4 lg:px-8 lg:py-6">
        {useRealData && (
          <div className="flex items-center justify-between p-3 bg-green-950/30 border border-green-800 rounded-lg">
            <p className="text-sm text-green-400">✓ Connected to Supabase database</p>
            <Badge variant="success">Live Data</Badge>
          </div>
        )}
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <Card className="border-border/70">
            <CardContent className="flex items-center gap-4 p-5">
              <div className="rounded-2xl bg-primary/15 p-3 text-primary">
                <ClipboardCheck className="h-5 w-5" />
              </div>
              <div>
                <p className="text-2xl font-semibold">{metrics.total}</p>
                <p className="text-sm text-muted-foreground">Visible work logs</p>
              </div>
            </CardContent>
          </Card>
          <Card className="border-border/70">
            <CardContent className="flex items-center gap-4 p-5">
              <div className="rounded-2xl bg-green-500/15 p-3 text-green-400">
                <Wrench className="h-5 w-5" />
              </div>
              <div>
                <p className="text-2xl font-semibold">{metrics.completed}</p>
                <p className="text-sm text-muted-foreground">Completed procedures</p>
              </div>
            </CardContent>
          </Card>
          <Card className="border-border/70">
            <CardContent className="flex items-center gap-4 p-5">
              <div className="rounded-2xl bg-yellow-500/15 p-3 text-yellow-400">
                <Filter className="h-5 w-5" />
              </div>
              <div>
                <p className="text-2xl font-semibold">{metrics.inProgress}</p>
                <p className="text-sm text-muted-foreground">Still in progress</p>
              </div>
            </CardContent>
          </Card>
          <Card className="border-border/70">
            <CardContent className="flex items-center gap-4 p-5">
              <div className="rounded-2xl bg-blue-500/15 p-3 text-blue-400">
                <TimerReset className="h-5 w-5" />
              </div>
              <div>
                <p className="text-2xl font-semibold">{metrics.avgDuration}m</p>
                <p className="text-sm text-muted-foreground">Average duration</p>
              </div>
            </CardContent>
          </Card>
        </div>

        <Card className="border-border/70">
          <CardHeader className="gap-4">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <CardTitle className="text-lg">Repair log explorer</CardTitle>
                <p className="text-sm text-muted-foreground">
                  Filter work by technician, status, machine, or procedure.
                </p>
              </div>
              <Button variant="outline" size="sm" onClick={exportCsv}>
                <Download className="h-4 w-4" />
                Export CSV
              </Button>
            </div>
            <div className="flex flex-col gap-3 lg:flex-row">
              <Input
                placeholder="Search machine, procedure, or technician"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                className="flex-1"
              />
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger className="w-full lg:w-[180px]">
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All status</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                  <SelectItem value="in_progress">In progress</SelectItem>
                  <SelectItem value="abandoned">Abandoned</SelectItem>
                </SelectContent>
              </Select>
              <Button
                variant={myRepairs ? "default" : "outline"}
                onClick={() => setMyRepairs((current) => !current)}
                className="lg:w-auto"
              >
                {myRepairs ? "Showing my repairs" : "Only my repairs"}
              </Button>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3 md:hidden">
              {filtered.slice(0, 30).map((log) => (
                <button
                  key={log.id}
                  type="button"
                  onClick={() => setSelectedLog(log.id === selectedLog ? null : log.id)}
                  className="w-full rounded-2xl border border-border/70 bg-background/60 p-4 text-left transition hover:border-primary/30"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0">
                      <p className="truncate font-medium">{log.machine?.name}</p>
                      <p className="truncate text-sm text-muted-foreground">{log.procedure?.procedure_type}</p>
                    </div>
                    <Badge
                      variant={
                        log.status === "completed"
                          ? "success"
                          : log.status === "in_progress"
                            ? "warning"
                            : "secondary"
                      }
                    >
                      {log.status}
                    </Badge>
                  </div>
                  <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
                    <span>{formatDate(log.started_at)}</span>
                    <span>{log.technician?.full_name ?? "Unassigned"}</span>
                    <span>{log.duration_minutes ? formatDuration(log.duration_minutes) : "-"}</span>
                  </div>
                </button>
              ))}
            </div>

            <div className="hidden overflow-hidden rounded-2xl border border-border/70 md:block">
              <table className="w-full text-sm">
                <thead className="bg-muted/60">
                  <tr>
                    <th className="p-3 text-left font-medium">Date</th>
                    <th className="p-3 text-left font-medium">Machine</th>
                    <th className="p-3 text-left font-medium">Procedure</th>
                    <th className="p-3 text-left font-medium">Technician</th>
                    <th className="p-3 text-left font-medium">Duration</th>
                    <th className="p-3 text-left font-medium">Status</th>
                    <th className="p-3 text-right font-medium">Certificate</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.slice(0, 50).map((log) => (
                    <tr
                      key={log.id}
                      className="cursor-pointer border-t border-border/70 transition hover:bg-muted/40"
                      onClick={() => setSelectedLog(log.id === selectedLog ? null : log.id)}
                    >
                      <td className="p-3">{formatDate(log.started_at)}</td>
                      <td className="p-3 font-medium">{log.machine?.name}</td>
                      <td className="p-3">{log.procedure?.procedure_type}</td>
                      <td className="p-3 text-muted-foreground">{log.technician?.full_name ?? "Assigned Tech"}</td>
                      <td className="p-3">{log.duration_minutes ? formatDuration(log.duration_minutes) : "-"}</td>
                      <td className="p-3">
                        <Badge
                          variant={
                            log.status === "completed"
                              ? "success"
                              : log.status === "in_progress"
                                ? "warning"
                                : "secondary"
                          }
                        >
                          {log.status}
                        </Badge>
                      </td>
                      <td className="p-3 text-right">
                        <Button
                          size="sm"
                          variant="ghost"
                          className="h-8 text-xs gap-1 text-emerald-400 hover:text-emerald-300 hover:bg-emerald-950/40"
                          onClick={(e) => {
                            e.stopPropagation();
                            setCertificateLog(log);
                            setShowCertModal(true);
                          }}
                        >
                          <FileCheck className="h-3.5 w-3.5" />
                          View
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {selected && (
              <Card className="border-emerald-500/30 bg-emerald-950/10">
                <CardContent className="grid gap-4 p-5 lg:grid-cols-[minmax(0,1fr)_auto]">
                  <div>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline" className="bg-emerald-500/10 text-emerald-400 border-emerald-500/30">
                        Selected Service Record
                      </Badge>
                      <span className="text-xs font-mono text-muted-foreground">ID: {selected.id.slice(0, 8)}</span>
                    </div>
                    <h3 className="mt-2 text-lg font-bold">
                      {selected.machine?.name} • {selected.procedure?.procedure_type}
                    </h3>
                    <p className="mt-2 text-sm text-muted-foreground">
                      {selected.notes ?? "Maintenance and calibration executed under certified safety protocols."}
                    </p>
                    <div className="mt-4 flex flex-wrap items-center gap-2">
                      <Badge variant="outline">{selected.technician?.full_name ?? "Raj Kumar"}</Badge>
                      <Badge variant="outline">{formatDate(selected.started_at)}</Badge>
                      <Badge variant="outline">
                        {selected.duration_minutes ? formatDuration(selected.duration_minutes) : "35m"}
                      </Badge>
                      <Button
                        size="sm"
                        onClick={() => {
                          setCertificateLog(selected);
                          setShowCertModal(true);
                        }}
                        className="bg-emerald-600 hover:bg-emerald-700 text-white gap-1.5 shadow-sm text-xs ml-auto"
                      >
                        <FileCheck className="h-4 w-4" />
                        Generate Inspection Certificate
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </CardContent>
        </Card>

        {certificateLog && (
          <WorkOrderCertificateModal
            open={showCertModal}
            onOpenChange={setShowCertModal}
            machine={certificateLog.machine ?? null}
            procedure={certificateLog.procedure ?? null}
            log={certificateLog}
            technician={certificateLog.technician ?? null}
            completedAt={certificateLog.completed_at ?? certificateLog.started_at}
          />
        )}
      </div>
    </AppShell>
  );
}
