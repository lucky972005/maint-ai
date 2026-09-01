"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, Users, Wrench, Clock, AlertTriangle, Package } from "lucide-react";

interface KpiCardsProps {
  stats: {
    totalMachines: number;
    operationalPercent: number;
    activeTechnicians: number;
    repairsThisMonth: number;
    avgRepairTime: number;
    pendingFaults: number;
    lowStockParts: number;
  };
}

type StatKey = keyof KpiCardsProps["stats"];

interface KpiItem {
  key: StatKey;
  label: string;
  icon: typeof Activity;
  suffix?: string;
  subKey?: StatKey;
}

const kpis: KpiItem[] = [
  { key: "totalMachines", label: "Total Machines", icon: Activity, subKey: "operationalPercent" },
  { key: "activeTechnicians", label: "Active Technicians", icon: Users },
  { key: "repairsThisMonth", label: "Repairs This Month", icon: Wrench },
  { key: "avgRepairTime", label: "Avg Repair Time", icon: Clock, suffix: " min" },
  { key: "pendingFaults", label: "Pending Faults", icon: AlertTriangle },
  { key: "lowStockParts", label: "Low Stock Parts", icon: Package },
];

export function KpiCards({ stats }: KpiCardsProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      {kpis.map(({ key, label, icon: Icon, suffix, subKey }) => (
        <Card key={key} className="border-border/50">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-xs font-medium text-muted-foreground">{label}</CardTitle>
            <Icon className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {stats[key]}
              {subKey && (
                <span className="text-sm font-normal text-muted-foreground ml-1">
                  ({stats[subKey]}% op)
                </span>
              )}
              {suffix && (
                <span className="text-sm font-normal text-muted-foreground">{suffix}</span>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
