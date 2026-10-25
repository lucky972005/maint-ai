"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/layout/app-shell";
import { KpiCards } from "@/components/dashboard/KpiCards";
import { FailureChart } from "@/components/dashboard/FailureChart";
import { DowntimeChart } from "@/components/dashboard/DowntimeChart";
import { TechnicianLeaderboard } from "@/components/dashboard/TechnicianLeaderboard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { DEMO_DATA, isFirebaseConfigured } from "@/lib/demo-data";
import {
  getMachines,
  getMaintenanceLogs,
  getFaultReports,
  getProfiles,
  getParts,
} from "@/lib/database";
import { useApp } from "@/components/providers";
import { Calendar, Download, Bell, UserCheck } from "lucide-react";
import { formatDate } from "@/lib/utils";
import Link from "next/link";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

type MaintenancePrediction = {
  procedure: string;
  urgency: "low" | "medium" | "high";
  days_until_due: number;
  reason: string;
};

const COLORS = ["#F97316", "#3B82F6", "#22C55E", "#EF4444", "#A855F7"];

export default function DashboardPage() {
  const { profile } = useApp();
  const [selectedMachineId, setSelectedMachineId] = useState<string>("");
  const [prediction, setPrediction] = useState<MaintenancePrediction[]>([]);
  const [predictionsLoading, setPredictionsLoading] = useState(false);
  const [showSchedule, setShowSchedule] = useState(false);
  const [loading, setLoading] = useState(true);
  const [useRealData, setUseRealData] = useState(false);
  
  const [machines, setMachines] = useState(DEMO_DATA.machines);
  const [logs, setLogs] = useState(DEMO_DATA.logs);
  const [faults, setFaults] = useState(DEMO_DATA.faults);
  const [profiles, setProfiles] = useState(DEMO_DATA.profiles);
  const [parts, setParts] = useState(DEMO_DATA.parts);

  const mergedLogs = useMemo(() => logs, [logs]);
  const mergedFaults = useMemo(() => faults, [faults]);

  const stats = useMemo(() => {
    const operational = machines.filter((m) => m.status === "operational").length;
    const total = machines.length;
    const thisMonth = mergedLogs.filter((l) => {
      const d = new Date(l.started_at);
      const now = new Date();
      return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear();
    });
    const completedLogs = mergedLogs.filter((l) => l.status === "completed" && l.duration_minutes);
    const avgTime = completedLogs.length > 0
      ? Math.round(completedLogs.reduce((s, l) => s + (l.duration_minutes ?? 0), 0) / completedLogs.length)
      : 0;
    const lowStock = parts.filter((p) => p.stock_quantity < p.min_stock_level);

    return {
      totalMachines: total,
      operationalPercent: total > 0 ? Math.round((operational / total) * 100) : 0,
      activeTechnicians: profiles.filter((p) => p.role === "technician").length,
      repairsThisMonth: thisMonth.length,
      avgRepairTime: avgTime,
      pendingFaults: mergedFaults.filter((f) => f.status === "open").length,
      lowStockParts: lowStock.length,
    };
  }, [machines, mergedLogs, parts, profiles, mergedFaults]);

  const failureData = useMemo(() => {
    const categories = new Map<string, number>();
    mergedFaults.forEach((fault) => {
      const category = fault.machine?.category ?? "Unknown";
      categories.set(category, (categories.get(category) ?? 0) + 1);
    });
    return Array.from(categories.entries()).map(([category, count]) => ({ category, count }));
  }, [mergedFaults]);

  const downtimeData = useMemo(() => {
    const days: { date: string; hours: number }[] = [];
    for (let i = 29; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      const dateStr = date.toISOString().split("T")[0];
      const dayLogs = mergedLogs.filter((log) => log.started_at.startsWith(dateStr));
      days.push({ date: dateStr, hours: dayLogs.length * 0.5 });
    }
    return days;
  }, [mergedLogs]);

  const leaderboard = useMemo(() => {
    const techs = profiles.filter((p) => p.role === "technician");
    return techs
      .map((tech) => ({
        name: tech.full_name,
        repairs: mergedLogs.filter((log) => log.technician_id === tech.id && log.status === "completed").length,
      }))
      .sort((a, b) => b.repairs - a.repairs);
  }, [profiles, mergedLogs]);

  const faultPie = failureData.map((f) => ({ name: f.category, value: f.count }));
  const topMachine = useMemo(() => {
    const counts = new Map<string, number>();
    logs.forEach((log) => counts.set(log.machine_id, (counts.get(log.machine_id) ?? 0) + 1));
    return machines
      .map((machine) => ({ machine, count: counts.get(machine.id) ?? 0 }))
      .sort((a, b) => b.count - a.count)[0]?.machine ?? machines[0];
  }, [logs, machines]);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      const firebaseConfigured = isFirebaseConfigured();
      setUseRealData(firebaseConfigured);

      if (firebaseConfigured) {
        try {
          const [machinesData, logsData, faultsData, profilesData, partsData] = await Promise.all([
            getMachines(),
            getMaintenanceLogs(100),
            getFaultReports(),
            getProfiles(),
            getParts(),
          ]);
          setMachines(machinesData);
          setLogs(logsData);
          setFaults(faultsData);
          setProfiles(profilesData);
          setParts(partsData);
        } catch (error) {
          console.error("Failed to load data from Firebase:", error);
          setUseRealData(false);
        }
      }
      setLoading(false);
    };

    loadData();
  }, []);

  useEffect(() => {
    const machineId = selectedMachineId || topMachine?.id;
    if (!machineId) return;

    let cancelled = false;
    setPredictionsLoading(true);

    fetch("/api/predict-maintenance", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ machineId }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (cancelled) return;
        setPrediction(Array.isArray(data.predictions) ? data.predictions : []);
      })
      .catch(() => {
        if (cancelled) return;
        setPrediction([
          { procedure: "Oil Change", urgency: "medium", days_until_due: 14, reason: "Standard maintenance interval approaching" },
          { procedure: "Motor Inspection", urgency: "low", days_until_due: 30, reason: "No recent inspection logged" },
        ]);
      })
      .finally(() => {
        if (!cancelled) setPredictionsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [selectedMachineId, topMachine?.id]);

  if (loading) {
    return (
      <AppShell title="Dashboard">
        <div className="p-8 text-center">
          <p className="text-muted-foreground">Loading dashboard...</p>
        </div>
      </AppShell>
    );
  }

  if (profile && profile.role === "technician") {
    return (
      <AppShell title="Dashboard">
        <div className="p-8 text-center">
          <p className="text-muted-foreground">Dashboard access requires supervisor or admin role.</p>
          <Link href="/scan"><Button className="mt-4">Go to Scanner</Button></Link>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell title="Dashboard">
      <div className="p-4 space-y-6 max-w-7xl mx-auto">
        {useRealData && (
          <div className="flex items-center justify-between p-3 bg-green-950/30 border border-green-800 rounded-lg">
            <p className="text-sm text-green-400">✓ Connected to Supabase database</p>
            <Badge variant="success">Live Data</Badge>
          </div>
        )}
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-lg font-semibold">Manager Overview</h2>
          <div className="flex flex-wrap gap-2">
            <Link href="/assignments">
              <Button size="sm" className="orange-glow gap-1.5 bg-primary text-primary-foreground font-medium">
                <UserCheck className="h-4 w-4" />
                Assign Work Orders ({stats.pendingFaults})
              </Button>
            </Link>
            <Button variant="outline" size="sm" onClick={() => setShowSchedule(true)}><Calendar className="h-4 w-4 mr-1" />Schedule Maintenance</Button>
            <Button variant="outline" size="sm"><Download className="h-4 w-4 mr-1" />Export PDF</Button>
          </div>
        </div>

        <KpiCards stats={stats} />

        <Card className="border-primary/20">
          <CardHeader className="flex flex-row items-center justify-between gap-4">
            <div>
              <CardTitle className="text-base">Predictive Maintenance</CardTitle>
              <p className="text-sm text-muted-foreground">Latest recommendations for {topMachine?.name ?? "selected machine"}</p>
            </div>
            <select
              className="h-10 rounded-md border border-input bg-background px-3 text-sm"
              value={selectedMachineId}
              onChange={(e) => setSelectedMachineId(e.target.value)}
            >
              {machines.map((machine) => (
                <option key={machine.id} value={machine.id}>{machine.name}</option>
              ))}
            </select>
          </CardHeader>
          <CardContent className="space-y-3">
            {predictionsLoading ? (
              <p className="text-sm text-muted-foreground">Analyzing maintenance history...</p>
            ) : prediction.length > 0 ? (
              prediction.slice(0, 3).map((item) => (
                <div key={`${item.procedure}-${item.days_until_due}`} className="flex items-center justify-between gap-3 rounded-lg border border-border bg-muted/30 p-3">
                  <div>
                    <p className="font-medium">{item.procedure}</p>
                    <p className="text-xs text-muted-foreground">{item.reason}</p>
                  </div>
                  <div className="text-right">
                    <Badge variant={item.urgency === "high" ? "destructive" : item.urgency === "medium" ? "warning" : "secondary"}>
                      {item.urgency}
                    </Badge>
                    <p className="text-xs text-muted-foreground mt-1">Due in {item.days_until_due} days</p>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-sm text-muted-foreground">No predictions available for this machine yet.</p>
            )}
          </CardContent>
        </Card>

        <div className="grid md:grid-cols-2 gap-4">
          <Card>
            <CardHeader><CardTitle className="text-base">Failure Frequency by Category</CardTitle></CardHeader>
            <CardContent><FailureChart data={failureData} /></CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-base">Downtime Trend (30 Days)</CardTitle></CardHeader>
            <CardContent><DowntimeChart data={downtimeData} /></CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-base">Common Faults</CardTitle></CardHeader>
            <CardContent>
              <div className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={faultPie} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} label>
                      {faultPie.map((_, i) => (
                        <Cell key={i} fill={COLORS[i % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={{ backgroundColor: "#1e293b", border: "1px solid #334155", borderRadius: "8px" }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-base">Technician Leaderboard</CardTitle></CardHeader>
            <CardContent><TechnicianLeaderboard data={leaderboard} /></CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader className="flex flex-row items-center gap-2">
            <Bell className="h-5 w-5 text-primary" />
            <CardTitle className="text-base">Live Alerts</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {mergedFaults.filter((f) => f.status === "open").slice(0, 5).map((f) => (
              <div key={f.id} className="flex items-center justify-between p-2 rounded-lg bg-muted/50 gap-2">
                <div className="min-w-0">
                  <p className="text-sm font-medium truncate">{f.machine?.name} — {f.description.slice(0, 50)}...</p>
                  <p className="text-xs text-muted-foreground">{formatDate(f.created_at ?? "")}</p>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <Badge variant="destructive">{f.severity}</Badge>
                  <Link href="/assignments">
                    <Button size="sm" variant="secondary" className="h-7 text-xs px-2.5">
                      Assign
                    </Button>
                  </Link>
                </div>
              </div>
            ))}
            {mergedLogs.filter((l) => l.status === "completed").slice(0, 3).map((l) => (
              <div key={l.id} className="flex items-center justify-between p-2 rounded-lg bg-green-950/30">
                <p className="text-sm">✅ {l.procedure?.procedure_type} completed on {l.machine?.name}</p>
                <span className="text-xs text-muted-foreground">{formatDate(l.started_at)}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <Dialog open={showSchedule} onOpenChange={setShowSchedule}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Schedule Maintenance</DialogTitle>
            <DialogDescription>
              Use the predictive recommendations to plan the next service window.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-3 text-sm">
            {prediction.slice(0, 3).map((item) => (
              <div key={item.procedure} className="flex items-center justify-between rounded-lg bg-muted/40 p-3">
                <div>
                  <p className="font-medium">{item.procedure}</p>
                  <p className="text-xs text-muted-foreground">{item.reason}</p>
                </div>
                <Badge variant={item.urgency === "high" ? "destructive" : item.urgency === "medium" ? "warning" : "secondary"}>
                  {item.days_until_due} days
                </Badge>
              </div>
            ))}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowSchedule(false)}>Close</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </AppShell>
  );
}
