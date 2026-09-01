"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import type { LucideIcon } from "lucide-react";
import {
  AlertTriangle,
  BookOpen,
  Gauge,
  Package,
  Plug,
  RefreshCw,
  ShieldAlert,
  Wrench,
  Zap,
} from "lucide-react";
import { AppShell } from "@/components/layout/app-shell";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import type { Machine, RepairProcedure } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { getMachineById as getMachineByIdFromDb, getProceduresForMachine as getProceduresForMachineFromDb, updateMachine } from "@/lib/database";
import { getMachineById, getProceduresForMachine } from "@/lib/demo-data";
import { ImageManager } from "@/components/image-manager";

const PROCEDURE_ICONS: Record<string, LucideIcon> = {
  "Oil Change": Wrench,
  "Belt Replacement": Gauge,
  "Bearing Replacement": RefreshCw,
  "Motor Inspection": Zap,
  "Electrical Wiring Check": Plug,
  "Emergency Shutdown": ShieldAlert,
};

export default function RepairPage() {
  const params = useParams();
  const router = useRouter();
  const machineId = params.machineId as string;
  const [machine, setMachine] = useState<Machine | null>(null);
  const [procedures, setProcedures] = useState<RepairProcedure[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  useEffect(() => {
    async function loadData() {
      try {
        // Try database first
        const machineData = await getMachineByIdFromDb(machineId);
        const proceduresData = await getProceduresForMachineFromDb(machineId);
        
        if (machineData) {
          setMachine(machineData);
          setProcedures(proceduresData);
        } else {
          // Fall back to demo data
          const demoMachine = getMachineById(machineId);
          setMachine(demoMachine ?? null);
          setProcedures(getProceduresForMachine(machineId));
        }
      } catch {
        console.log("Database lookup failed, using demo data");
        const demoMachine = getMachineById(machineId);
        setMachine(demoMachine ?? null);
        setProcedures(getProceduresForMachine(machineId));
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [machineId]);

  if (loading) {
    return (
      <AppShell title="Repair">
        <div className="flex items-center justify-center p-8">
          <div className="animate-spin h-8 w-8 border-2 border-primary border-t-transparent rounded-full" />
        </div>
      </AppShell>
    );
  }

  if (!machine) {
    return (
      <AppShell title="Not Found">
        <div className="p-8 text-center">
          <p className="text-muted-foreground">Machine not found</p>
          <Link href="/scan">
            <Button className="mt-4">Back to Scanner</Button>
          </Link>
        </div>
      </AppShell>
    );
  }

  const startProcedure = (procedureId: string) => {
    router.push(`/repair/${machineId}/step/1?procedure=${procedureId}`);
  };

  return (
    <AppShell title="Repair">
      <div className="space-y-4 px-4 py-4 lg:px-8 lg:py-6">
        <Card className="overflow-hidden border-primary/20">
          <div className="relative h-48 bg-muted lg:h-64">
            {((machine.images && machine.images.length > 0) || machine.image_url) ? (
              <>
                <img 
                  src={machine.images?.[currentImageIndex] || machine.image_url || ""} 
                  alt={`${machine.name} - Image ${currentImageIndex + 1}`} 
                  className="h-full w-full object-cover opacity-70" 
                />
                {machine.images && machine.images.length > 1 && (
                  <>
                    <button
                      onClick={() => setCurrentImageIndex((prev) => (prev - 1 + machine.images!.length) % machine.images!.length)}
                      className="absolute left-2 top-1/2 -translate-y-1/2 p-2 bg-black/50 hover:bg-black/70 rounded-full text-white transition"
                    >
                      ←
                    </button>
                    <button
                      onClick={() => setCurrentImageIndex((prev) => (prev + 1) % machine.images!.length)}
                      className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-black/50 hover:bg-black/70 rounded-full text-white transition"
                    >
                      →
                    </button>
                    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-1">
                      {machine.images.map((_, i) => (
                        <button
                          key={i}
                          onClick={() => setCurrentImageIndex(i)}
                          className={`w-2 h-2 rounded-full transition ${i === currentImageIndex ? 'bg-white' : 'bg-white/50'}`}
                        />
                      ))}
                    </div>
                  </>
                )}
              </>
            ) : (
              <div className="flex items-center justify-center h-full text-muted-foreground">
                No images available
              </div>
            )}
            <div className="absolute inset-0 bg-gradient-to-t from-card via-card/50 to-transparent" />
            <div className="absolute bottom-4 left-4 right-4">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <h2 className="text-2xl font-bold">{machine.name}</h2>
                  <p className="text-sm text-muted-foreground">{machine.model} - {machine.manufacturer}</p>
                  <p className="mt-1 text-xs text-muted-foreground">{machine.location}</p>
                </div>
                <Badge
                  variant={
                    machine.status === "operational"
                      ? "success"
                      : machine.status === "broken"
                        ? "destructive"
                        : "warning"
                  }
                >
                  {machine.status}
                </Badge>
              </div>
            </div>
          </div>
        </Card>

        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">Maintenance Procedures</h3>
          <ImageManager
            entityType="machine"
            entityId={machineId}
            existingImages={machine.images || []}
            onImagesUpdate={async (newImages) => {
              if (machine) {
                try {
                  await updateMachine(machineId, { images: newImages });
                  setMachine({ ...machine, images: newImages });
                } catch (error) {
                  console.error("Failed to update machine images:", error);
                }
              }
            }}
          />
        </div>

        <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          {procedures.map((procedure) => {
            const Icon = PROCEDURE_ICONS[procedure.procedure_type] ?? Wrench;
            return (
              <Button
                key={procedure.id}
                variant="outline"
                className="h-auto flex-col items-start gap-3 rounded-2xl border-border/70 px-5 py-5 text-left hover:border-primary hover:bg-primary/5"
                onClick={() => startProcedure(procedure.id)}
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/15 text-primary">
                  <Icon className="h-5 w-5" />
                </div>
                <div>
                  <span className="block text-sm font-medium">{procedure.procedure_type}</span>
                  <span className="text-xs text-muted-foreground">
                    {procedure.estimated_minutes} min - {procedure.difficulty}
                  </span>
                </div>
              </Button>
            );
          })}
        </div>

        <div className="grid gap-2 pt-2 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)_minmax(0,1fr)]">
          <Link href={`/report?machineId=${machineId}`}>
            <Button variant="destructive" className="w-full">
              <AlertTriangle className="h-4 w-4" />
              Report New Fault
            </Button>
          </Link>
          <Link href={`/manuals/${machineId}`}>
            <Button variant="outline" className="w-full">
              <BookOpen className="h-4 w-4" />
              View Manual
            </Button>
          </Link>
          <Link href={`/parts?machine=${machineId}`}>
            <Button variant="outline" className="w-full">
              <Package className="h-4 w-4" />
              Spare Parts
            </Button>
          </Link>
        </div>
      </div>
    </AppShell>
  );
}
