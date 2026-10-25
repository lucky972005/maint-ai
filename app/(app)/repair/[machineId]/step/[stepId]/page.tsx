"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { AppShell } from "@/components/layout/app-shell";
import { StepGuide } from "@/components/repair/StepGuide";
import { getMachineById, getProcedureById, getProceduresForMachine, DEMO_DATA } from "@/lib/demo-data";
import { Button } from "@/components/ui/button";
import { CheckCircle2 } from "lucide-react";
import { useApp } from "@/components/providers";
import { cacheMaintenanceLog, queueForSync } from "@/lib/offline";
import { WorkOrderCertificateModal } from "@/components/certificate/WorkOrderCertificateModal";
import type { MaintenanceLog } from "@/lib/types";

export default function RepairStepPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const { profile } = useApp();
  const machineId = params.machineId as string;
  const stepId = parseInt(params.stepId as string, 10);
  const procedureId = searchParams.get("procedure");

  const machine =
    getMachineById(machineId) ??
    DEMO_DATA.machines.find(
      (m) =>
        m.qr_code.toLowerCase().includes(machineId.toLowerCase()) ||
        m.name.toLowerCase().replace(/[^a-z0-9]/g, "-").includes(machineId.toLowerCase())
    ) ??
    DEMO_DATA.machines[0];

  const procedure =
    (procedureId ? getProcedureById(procedureId) : null) ??
    getProceduresForMachine(machine.id)[0] ??
    DEMO_DATA.procedures[0];

  const [completionLogged, setCompletionLogged] = useState(false);
  const [showCertificate, setShowCertificate] = useState(false);
  const [createdLog, setCreatedLog] = useState<MaintenanceLog | null>(null);

  const currentIndex = useMemo(() => Math.max(0, stepId - 1), [stepId]);

  useEffect(() => {
    const isComplete = procedure && currentIndex >= procedure.steps.length;
    if (!isComplete || !machine || !procedure || createdLog) return;

    let existingLog: MaintenanceLog | null = null;
    if (typeof window !== "undefined") {
      try {
        const stored = window.localStorage.getItem("maintai_saved_logs");
        if (stored) {
          const list: MaintenanceLog[] = JSON.parse(stored);
          existingLog = list.find((l) => l.machine_id === machine.id && l.procedure_id === procedure.id) || null;
        }
      } catch {}
    }

    const log: MaintenanceLog = existingLog || {
      id: `wo-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`,
      machine_id: machine.id,
      technician_id: profile?.id ?? DEMO_DATA.profiles.find((p) => p.role === "technician")?.id ?? "tech-demo",
      procedure_id: procedure.id,
      started_at: new Date(Date.now() - (procedure.estimated_minutes ?? 30) * 60000).toISOString(),
      completed_at: new Date().toISOString(),
      duration_minutes: procedure.estimated_minutes ?? 30,
      status: "completed" as const,
      notes: `${procedure.procedure_type} on ${machine.name} completed successfully via guided AR inspection.`,
      machine,
      procedure,
      technician: profile ?? DEMO_DATA.profiles.find((p) => p.role === "technician"),
    };

    setCreatedLog(log);
    setCompletionLogged(true);

    // Save to all persistence layers: IndexedDB, localStorage, and in-memory DEMO_DATA
    cacheMaintenanceLog(log).catch(console.error);

    // Also notify server in the background (non-blocking)
    fetch("/api/maintenance-log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(log),
    }).catch(() => {
      queueForSync("maintenance_log", log).catch(() => {});
    });
  }, [createdLog, currentIndex, machine, machineId, profile, procedure]);

  if (!machine || !procedure) {
    return (
      <AppShell title="Repair Step">
        <div className="p-8 text-center">
          <p className="text-muted-foreground">Procedure not found</p>
          <Link href={`/repair/${machineId}`}><Button className="mt-4">Back</Button></Link>
        </div>
      </AppShell>
    );
  }

  const steps = procedure.steps;
  const isComplete = currentIndex >= steps.length;

  if (isComplete) {
    return (
      <AppShell title="Complete">
        <div className="p-8 text-center space-y-5 max-w-lg mx-auto">
          <div className="relative mx-auto w-20 h-20 flex items-center justify-center rounded-full bg-emerald-500/10 border border-emerald-500/20">
            <CheckCircle2 className="h-12 w-12 text-emerald-500 animate-in zoom-in-50 duration-300" />
          </div>
          <div>
            <h2 className="text-2xl font-bold">Repair Complete!</h2>
            <p className="text-muted-foreground mt-1">
              {procedure.procedure_type} on <span className="text-foreground font-semibold">{machine.name}</span> finished successfully.
            </p>
          </div>

          {/* Certificate Action Card */}
          <div className="p-4 rounded-xl border border-emerald-500/30 bg-emerald-500/5 text-left space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                  Compliance Ready
                </span>
              </div>
              <span className="text-[11px] text-muted-foreground">ISO-9001 Protocol</span>
            </div>
            <p className="text-xs text-muted-foreground">
              Official work order record generated with digital signature pad and audit QR stamp.
            </p>
            <Button
              onClick={() => setShowCertificate(true)}
              className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold gap-2 shadow-lg shadow-emerald-900/20"
            >
              📄 View & Sign Work Order Certificate
            </Button>
          </div>

          <div className="flex flex-wrap gap-2 justify-center pt-2">
            <Link href={`/repair/${machineId}`}>
              <Button variant="outline">Back to Machine</Button>
            </Link>
            <Link href="/history">
              <Button variant="outline" className="gap-1.5 border-emerald-500/40 text-emerald-400 hover:bg-emerald-500/10">
                📋 View in History
              </Button>
            </Link>
            <Link href="/scan">
              <Button>Scan Next Machine</Button>
            </Link>
          </div>
        </div>

        <WorkOrderCertificateModal
          open={showCertificate}
          onOpenChange={setShowCertificate}
          machine={machine}
          procedure={procedure}
          log={createdLog}
          technician={profile ?? createdLog?.technician}
          completedAt={createdLog?.completed_at ?? new Date().toISOString()}
        />
      </AppShell>
    );
  }

  const navigate = (newStep: number) => {
    router.push(`/repair/${machineId}/step/${newStep}?procedure=${procedureId}`);
  };

  return (
    <AppShell title={procedure.procedure_type}>
      <StepGuide
        machine={machine}
        steps={steps}
        currentStep={currentIndex}
        procedureType={procedure.procedure_type}
        onNext={() => navigate(stepId + 1)}
        onPrevious={() => navigate(Math.max(1, stepId - 1))}
        onSkip={() => navigate(stepId + 1)}
        onComplete={() => navigate(steps.length + 1)}
      />
    </AppShell>
  );
}
