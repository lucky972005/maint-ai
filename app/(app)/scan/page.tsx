"use client";

import Link from "next/link";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AppShell } from "@/components/layout/app-shell";
import { QrScanner } from "@/components/scanner/QrScanner";
import { AiIdentifier } from "@/components/scanner/AiIdentifier";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DEMO_DATA } from "@/lib/demo-data";
import { Brain, Camera, ClipboardList, Scan, ShieldCheck } from "lucide-react";

const recentMachines = DEMO_DATA.machines.slice(0, 4);

export default function ScanPage() {
  return (
    <AppShell title="Scanner">
      <div className="grid gap-6 px-4 py-4 lg:grid-cols-[minmax(0,1fr)_320px] lg:px-8 lg:py-6">
        <div className="overflow-hidden rounded-[1.75rem] border border-border/70 bg-card/70 shadow-2xl shadow-black/20">
          <div className="border-b border-border/70 px-4 py-4 sm:px-6">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-lg font-semibold">Field capture</p>
                <p className="text-sm text-muted-foreground">
                  Scan a QR code or identify a machine from the camera feed.
                </p>
              </div>
              <Badge variant="success" className="px-3 py-1">
                Mobile and desktop ready
              </Badge>
            </div>
          </div>

          <Tabs defaultValue="qr" className="flex flex-col">
            <div className="border-b border-border/70 px-4 py-3 sm:px-6">
              <TabsList className="grid w-full grid-cols-2 rounded-2xl bg-muted/70 p-1">
                <TabsTrigger value="qr" className="gap-2 rounded-xl">
                  <Scan className="h-4 w-4" />
                  QR Scan
                </TabsTrigger>
                <TabsTrigger value="ai" className="gap-2 rounded-xl">
                  <Brain className="h-4 w-4" />
                  AI Identify
                </TabsTrigger>
              </TabsList>
            </div>
            <TabsContent value="qr" className="m-0">
              <QrScanner />
            </TabsContent>
            <TabsContent value="ai" className="m-0">
              <AiIdentifier />
            </TabsContent>
          </Tabs>
        </div>

        <div className="space-y-4">
          <Card className="border-primary/20 bg-gradient-to-br from-primary/15 via-card to-card">
            <CardHeader>
              <CardTitle className="text-base">Start a shift fast</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-muted-foreground">
              <div className="flex items-start gap-3 rounded-2xl border border-border/70 bg-background/60 p-3">
                <Camera className="mt-0.5 h-4 w-4 text-primary" />
                <p>Use QR scan for tagged equipment and AI Identify for legacy machines without labels.</p>
              </div>
              <div className="flex items-start gap-3 rounded-2xl border border-border/70 bg-background/60 p-3">
                <ShieldCheck className="mt-0.5 h-4 w-4 text-primary" />
                <p>Camera workflows stay usable on phones, tablets, laptops, and installed PWA sessions.</p>
              </div>
              <div className="flex items-start gap-3 rounded-2xl border border-border/70 bg-background/60 p-3">
                <ClipboardList className="mt-0.5 h-4 w-4 text-primary" />
                <p>Jump into a fault report if you discover a new issue during inspection.</p>
              </div>
              <Link href="/report">
                <Button className="w-full rounded-xl">Open fault report</Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="border-border/70">
            <CardHeader>
              <CardTitle className="text-base">Recently serviced machines</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {recentMachines.map((machine) => (
                <Link
                  key={machine.id}
                  href={`/repair/${machine.id}`}
                  className="flex items-center justify-between rounded-2xl border border-border/70 bg-background/60 px-4 py-3 transition hover:border-primary/30"
                >
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">{machine.name}</p>
                    <p className="truncate text-xs text-muted-foreground">
                      {machine.model} in {machine.location}
                    </p>
                  </div>
                  <Badge variant={machine.status === "operational" ? "success" : machine.status === "broken" ? "destructive" : "warning"}>
                    {machine.status}
                  </Badge>
                </Link>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
