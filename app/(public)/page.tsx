"use client";

import { useEffect, useState, useMemo } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Activity,
  ArrowRight,
  Brain,
  Check,
  CheckCircle2,
  Download,
  HardHat,
  Layers,
  Mic,
  Package,
  Play,
  Scan,
  Shield,
  Sparkles,
  UserCheck,
  Volume2,
  Wrench,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { DEMO_DATA, isSupabaseConfigured } from "@/lib/demo-data";
import { useApp } from "@/components/providers";

const SHOWCASE_MACHINES = [
  {
    name: "Haas VF-2 CNC Milling Machine",
    category: "CNC Machining Center",
    location: "Bay A - Floor 1",
    image: "/machines/cnc-machine.jpg",
    status: "operational",
    telemetry: { vibration: "1.4 mm/s", temp: "42°C", pressure: "6.2 bar" },
    activeProcedure: "Spindle Bearing Inspection",
    marker: "Bearing Housing #02",
  },
  {
    name: "Atlas Copco GA-37 Compressor",
    category: "Rotary Screw Compressor",
    location: "Utility Room 03",
    image: "/machines/air-compressor.jpeg",
    status: "operational",
    telemetry: { vibration: "2.1 mm/s", temp: "78°C", pressure: "8.5 bar" },
    activeProcedure: "Air Filter & Oil Separator Service",
    marker: "Filter Cartridge Bay",
  },
  {
    name: "Schuler PH-400 Hydraulic Press",
    category: "High-Tonnage Stamping Press",
    location: "Production Line 04",
    image: "/machines/hydraulic-press.jpg",
    status: "maintenance",
    telemetry: { vibration: "3.2 mm/s", temp: "65°C", pressure: "220 bar" },
    activeProcedure: "Hydraulic Seal Replacement",
    marker: "Main Ram Cylinder Seal",
  },
];

const PLATFORM_CAPABILITIES = [
  {
    icon: Brain,
    badge: "Computer Vision",
    title: "Neural Machine Recognition",
    desc: "Instant camera and QR detection matches machine models, serial tags, and manufacturer specs in sub-200ms.",
    highlight: "98.4% model match accuracy",
  },
  {
    icon: Layers,
    badge: "Spatial AR",
    title: "Augmented Reality Step Guidance",
    desc: "Interactive 3D overlays pinpoint drain plugs, tension bolts, and filter ports directly over the live camera stream.",
    highlight: "Lockout/Tagout safety verification",
  },
  {
    icon: Mic,
    badge: "Hands-Free Voice",
    title: "Voice-Controlled Navigation",
    desc: "Technicians navigate complex procedures hands-free with speech commands while keeping both hands on industrial tools.",
    highlight: "Speech-to-text notes & step skips",
  },
  {
    icon: Package,
    badge: "Smart Inventory",
    title: "Spare Parts & Barcode Tracking",
    desc: "Automated stock thresholds, on-demand Code128 bin labels, and 1-click purchase requisitions for critical components.",
    highlight: "Auto-decrement on procedure completion",
  },
  {
    icon: UserCheck,
    badge: "Operations Command",
    title: "Supervisor Work Order Dispatch",
    desc: "Role-based dispatch interface allows admins and supervisors to assign tasks, monitor live SLAs, and balance shift workloads.",
    highlight: "Real-time technician queue visibility",
  },
  {
    icon: Shield,
    badge: "High Resilience",
    title: "Offline-First Industrial PWA",
    desc: "Engineered for deep concrete factory floors and shielded basements. Operates with zero connectivity and syncs upon reconnection.",
    highlight: "Local IndexedDB + background sync",
  },
];

const WORKFLOW_STEPS = [
  {
    step: "01",
    title: "Scan & Identify",
    subtitle: "Optical or QR detection",
    desc: "Point any smartphone or tablet camera at the machine. MaintAI identifies model, OEM service history, and pending work orders.",
    icon: Scan,
    accent: "from-blue-500/20 to-blue-500/5",
  },
  {
    step: "02",
    title: "Execute AR Procedure",
    subtitle: "Spatial overlays & voice control",
    desc: "Follow animated AR component markers, safety warnings, and tool checklists. Navigate steps using voice commands without touching the screen.",
    icon: Wrench,
    accent: "from-primary/20 to-primary/5",
  },
  {
    step: "03",
    title: "Procure & Auto-Log",
    subtitle: "Parts decrement & supervisor signoff",
    desc: "Spare parts are automatically decremented, compliance certificates are minted, and maintenance logs are synced across the plant.",
    icon: CheckCircle2,
    accent: "from-emerald-500/20 to-emerald-500/5",
  },
];

export default function LandingPage() {
  const router = useRouter();
  const { enterDemoMode } = useApp();
  const [machineIndex, setMachineIndex] = useState(0);
  const [stats, setStats] = useState({ scanned: 1428, repairs: 684, uptime: 99.8 });
  const [deferredPrompt, setDeferredPrompt] = useState<{ prompt: () => Promise<void> } | null>(null);
  const [showInstall, setShowInstall] = useState(false);
  const [activeRoleView, setActiveRoleView] = useState<"technician" | "supervisor">("technician");

  const currentMachine = useMemo(() => SHOWCASE_MACHINES[machineIndex], [machineIndex]);

  useEffect(() => {
    const machineTimer = setInterval(() => {
      setMachineIndex((prev) => (prev + 1) % SHOWCASE_MACHINES.length);
    }, 5000);

    const statsTimer = setInterval(() => {
      setStats((prev) => ({
        scanned: prev.scanned + Math.floor(Math.random() * 2),
        repairs: prev.repairs + (Math.random() > 0.8 ? 1 : 0),
        uptime: 99.8,
      }));
    }, 6000);

    const promptHandler = (event: Event) => {
      event.preventDefault();
      setDeferredPrompt(event as unknown as { prompt: () => Promise<void> });
      setShowInstall(true);
    };

    window.addEventListener("beforeinstallprompt", promptHandler);

    return () => {
      clearInterval(machineTimer);
      clearInterval(statsTimer);
      window.removeEventListener("beforeinstallprompt", promptHandler);
    };
  }, []);

  const installPwa = async () => {
    if (!deferredPrompt) return;
    await deferredPrompt.prompt();
    setShowInstall(false);
  };

  const handleTryDemo = (initialRole: "technician" | "supervisor" | "admin" = "technician") => {
    const targetUser = DEMO_DATA.users.find((u) => u.role === initialRole);
    if (targetUser) {
      const { password: _p, ...profile } = targetUser;
      void _p;
      enterDemoMode(profile);
    } else {
      enterDemoMode();
    }

    setTimeout(() => {
      if (initialRole === "supervisor" || initialRole === "admin") {
        router.replace("/assignments?demo=1");
      } else {
        router.replace("/scan?demo=1");
      }
    }, 120);
  };

  const handleGetStarted = () => {
    if (!isSupabaseConfigured()) {
      handleTryDemo("technician");
      return;
    }
    router.push("/signup");
  };

  return (
    <div className="min-h-screen industrial-gradient text-foreground selection:bg-primary selection:text-white">
      {/* Top Navbar */}
      <nav className="sticky top-0 z-50 border-b border-border/70 bg-background/85 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3.5 sm:px-6 lg:px-8">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary font-black text-primary-foreground shadow-lg shadow-primary/25 transition group-hover:scale-105">
              M
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-bold tracking-tight text-foreground">
                Maint<span className="text-primary">AI</span>
              </span>
              <span className="text-[10px] font-mono tracking-wider text-muted-foreground uppercase">
                Field Maintenance OS
              </span>
            </div>
          </Link>

          {/* Center Links */}
          <div className="hidden md:flex items-center gap-6 text-sm font-medium text-muted-foreground">
            <a href="#features" className="hover:text-foreground transition">Capabilities</a>
            <a href="#workflow" className="hover:text-foreground transition">AR Workflow</a>
            <a href="#roles" className="hover:text-foreground transition">Team Dispatch</a>
            <a href="#telemetry" className="hover:text-foreground transition">Machine Health</a>
          </div>

          {/* Right Actions */}
          <div className="flex items-center gap-2.5">
            <Link href="/login">
              <Button variant="ghost" size="sm" className="text-xs font-medium hover:text-foreground">
                Sign In
              </Button>
            </Link>
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleTryDemo("technician")}
              className="text-xs font-medium border-primary/40 text-primary hover:bg-primary/10 hidden sm:inline-flex"
            >
              Quick Demo
            </Button>
            <Button
              size="sm"
              onClick={handleGetStarted}
              className="orange-glow text-xs font-semibold bg-primary text-primary-foreground gap-1.5"
            >
              <span>Get Started</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          </div>
        </div>
      </nav>

      {/* PWA Install Notification Ribbon */}
      {showInstall && (
        <div className="border-b border-primary/30 bg-primary/15 px-4 py-2.5 text-center text-xs backdrop-blur-md">
          <div className="mx-auto flex max-w-7xl items-center justify-between">
            <span className="flex items-center gap-2 font-medium text-foreground">
              <Download className="h-4 w-4 text-primary animate-bounce" />
              <span>Install MaintAI PWA for offline zero-latency shop floor operation</span>
            </span>
            <Button size="sm" onClick={installPwa} className="h-7 text-xs bg-primary text-white">
              Install App
            </Button>
          </div>
        </div>
      )}

      {/* HERO SECTION */}
      <section className="relative overflow-hidden pt-12 pb-16 sm:pt-20 sm:pb-24 lg:pt-24 lg:pb-32">
        {/* Subtle background glow spheres */}
        <div className="pointer-events-none absolute -top-40 left-1/2 -translate-x-1/2 h-96 w-[800px] rounded-full bg-primary/10 blur-3xl opacity-70" />
        <div className="pointer-events-none absolute top-1/2 -right-40 h-80 w-80 rounded-full bg-amber-500/10 blur-3xl" />

        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-12 lg:grid-cols-12 lg:items-center">
            {/* Left Column: Headline & Value Proposition */}
            <div className="space-y-6 lg:col-span-7">
              {/* Status Pill */}
              <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-3.5 py-1 text-xs font-medium text-primary backdrop-blur-sm">
                <span className="h-2 w-2 rounded-full bg-primary animate-pulse" />
                <span className="font-mono uppercase tracking-wider text-[11px]">Industrial AI 2.0 • Offline Ready</span>
              </div>

              {/* Main Headline */}
              <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl leading-[1.1]">
                Zero Machine Downtime.{" "}
                <span className="bg-gradient-to-r from-primary via-orange-400 to-amber-300 bg-clip-text text-transparent">
                  Intelligent Field Guidance.
                </span>
              </h1>

              {/* Subheading */}
              <p className="max-w-2xl text-base text-muted-foreground sm:text-lg leading-relaxed">
                Empower maintenance technicians with real-time neural equipment recognition, spatial AR repair overlays, hands-free voice commands, and automated supervisor work order dispatch.
              </p>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center gap-3 pt-2">
                <Button
                  size="lg"
                  className="orange-glow gap-2 bg-primary text-primary-foreground font-semibold px-6"
                  onClick={() => handleTryDemo("technician")}
                >
                  <Play className="h-4 w-4 fill-current" />
                  <span>Launch Live Demo</span>
                </Button>
                <Button
                  size="lg"
                  variant="outline"
                  className="gap-2 border-border/80 bg-card/60 backdrop-blur-sm hover:border-primary/50 px-6 font-medium"
                  onClick={() => handleTryDemo("supervisor")}
                >
                  <UserCheck className="h-4 w-4 text-primary" />
                  <span>Supervisor Console</span>
                </Button>
              </div>

              {/* Feature Checklist */}
              <div className="grid grid-cols-2 gap-2.5 pt-3 text-xs text-muted-foreground sm:grid-cols-3">
                <div className="flex items-center gap-1.5">
                  <Check className="h-3.5 w-3.5 text-primary" />
                  <span>Sub-200ms AI Vision</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Check className="h-3.5 w-3.5 text-primary" />
                  <span>Hands-Free Speech</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Check className="h-3.5 w-3.5 text-primary" />
                  <span>PWA Offline IndexedDB</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Check className="h-3.5 w-3.5 text-primary" />
                  <span>Parts Barcode Labels</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Check className="h-3.5 w-3.5 text-primary" />
                  <span>Lockout/Tagout Safety</span>
                </div>
                <div className="flex items-center gap-1.5">
                  <Check className="h-3.5 w-3.5 text-primary" />
                  <span>Instant Shift Dispatch</span>
                </div>
              </div>
            </div>

            {/* Right Column: Interactive AR Terminal Simulator */}
            <div className="lg:col-span-5">
              <div className="relative mx-auto max-w-md lg:max-w-none">
                {/* Glow ring */}
                <div className="absolute -inset-1 rounded-3xl bg-gradient-to-r from-primary/30 to-amber-500/20 blur-xl opacity-80" />

                {/* Main Console Frame */}
                <div className="relative rounded-2xl border border-primary/40 bg-card/90 shadow-2xl backdrop-blur-md overflow-hidden">
                  {/* Console Title Bar */}
                  <div className="flex items-center justify-between border-b border-border/80 bg-background/90 px-4 py-2.5">
                    <div className="flex items-center gap-2">
                      <div className="h-2.5 w-2.5 rounded-full bg-rose-500/80" />
                      <div className="h-2.5 w-2.5 rounded-full bg-amber-500/80" />
                      <div className="h-2.5 w-2.5 rounded-full bg-emerald-500/80" />
                      <span className="text-[11px] font-mono text-muted-foreground ml-1">
                        MAINT-AR // HUD v2.4
                      </span>
                    </div>
                    <Badge variant="outline" className="gap-1 text-[10px] font-mono text-emerald-400 border-emerald-500/30 bg-emerald-500/10">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping" />
                      FEED LIVE
                    </Badge>
                  </div>

                  {/* Viewport with Machine Photo & Simulated AR HUD */}
                  <div className="relative aspect-[4/3] w-full overflow-hidden bg-black">
                    <img
                      src={currentMachine.image}
                      alt={currentMachine.name}
                      className="h-full w-full object-cover transition-all duration-700 opacity-80"
                    />

                    {/* Animated Scanning Line */}
                    <div className="scan-line absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-primary to-transparent shadow-[0_0_12px_rgba(249,115,22,0.8)]" />

                    {/* Dark gradient overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-transparent" />

                    {/* Top Overlay: Machine Name & Confidence */}
                    <div className="absolute left-3 top-3 right-3 flex items-start justify-between gap-2">
                      <div className="rounded-lg bg-black/70 px-2.5 py-1.5 backdrop-blur-md border border-white/10">
                        <p className="text-[10px] font-mono text-primary uppercase font-bold tracking-wider">
                          Identified Machine
                        </p>
                        <p className="text-xs font-semibold text-white truncate max-w-[190px]">
                          {currentMachine.name}
                        </p>
                      </div>

                      <div className="rounded-lg bg-black/70 px-2 py-1 text-right backdrop-blur-md border border-white/10">
                        <span className="text-[10px] font-mono text-emerald-400 font-bold">98.6%</span>
                        <p className="text-[9px] text-muted-foreground font-mono">Neural Match</p>
                      </div>
                    </div>

                    {/* Simulated AR Target Marker */}
                    <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none">
                      <div className="relative flex items-center justify-center">
                        <div className="h-16 w-16 rounded-full border-2 border-dashed border-primary animate-spin" style={{ animationDuration: "12s" }} />
                        <div className="absolute h-8 w-8 rounded-full border border-primary/80 animate-ping" />
                        <div className="h-3 w-3 rounded-full bg-primary" />
                        <div className="absolute -top-7 whitespace-nowrap rounded bg-primary px-1.5 py-0.5 text-[9px] font-bold text-black uppercase tracking-wider">
                          {currentMachine.marker}
                        </div>
                      </div>
                    </div>

                    {/* Bottom HUD: Live Step Guidance */}
                    <div className="absolute bottom-3 left-3 right-3 space-y-2">
                      <div className="rounded-xl border border-primary/30 bg-black/80 p-2.5 backdrop-blur-md space-y-1">
                        <div className="flex items-center justify-between text-[10px]">
                          <span className="font-semibold text-primary uppercase tracking-wider">
                            Active Procedure
                          </span>
                          <span className="text-muted-foreground font-mono">Step 2 / 5</span>
                        </div>
                        <p className="text-xs font-medium text-white truncate">
                          {currentMachine.activeProcedure}
                        </p>
                        <div className="flex items-center gap-2 pt-1 text-[10px] text-muted-foreground font-mono">
                          <span className="text-amber-400">Vib: {currentMachine.telemetry.vibration}</span>
                          <span>•</span>
                          <span>Temp: {currentMachine.telemetry.temp}</span>
                          <span>•</span>
                          <span>P: {currentMachine.telemetry.pressure}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Machine Carousel Selector */}
                  <div className="flex items-center justify-between border-t border-border/80 bg-background/90 px-3 py-2 text-xs">
                    <span className="text-muted-foreground text-[11px]">Simulate equipment switch:</span>
                    <div className="flex gap-1.5">
                      {SHOWCASE_MACHINES.map((m, idx) => (
                        <button
                          key={m.name}
                          onClick={() => setMachineIndex(idx)}
                          className={`rounded px-2 py-0.5 text-[10px] font-mono transition ${
                            idx === machineIndex
                              ? "bg-primary text-black font-bold"
                              : "bg-muted text-muted-foreground hover:text-white"
                          }`}
                        >
                          0{idx + 1}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* KPI METRIC STRIP */}
      <section className="border-y border-border/80 bg-card/40 py-8 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 gap-6 md:grid-cols-4 text-center">
            <div className="space-y-1 border-r border-border/60 last:border-r-0">
              <p className="text-3xl font-extrabold text-primary sm:text-4xl">{stats.scanned.toLocaleString()}+</p>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Equipment Scanned</p>
            </div>
            <div className="space-y-1 border-r border-border/60 last:border-r-0">
              <p className="text-3xl font-extrabold text-foreground sm:text-4xl">{stats.repairs.toLocaleString()}+</p>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Procedures Completed</p>
            </div>
            <div className="space-y-1 border-r border-border/60 last:border-r-0">
              <p className="text-3xl font-extrabold text-primary sm:text-4xl">42%</p>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Reduction in MTTR</p>
            </div>
            <div className="space-y-1">
              <p className="text-3xl font-extrabold text-emerald-400 sm:text-4xl">{stats.uptime}%</p>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Target Plant Uptime</p>
            </div>
          </div>
        </div>
      </section>

      {/* CORE CAPABILITIES GRID */}
      <section id="features" className="py-20 sm:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 space-y-12">
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <Badge variant="outline" className="border-primary/40 text-primary text-xs uppercase tracking-wider">
              Comprehensive Platform
            </Badge>
            <h2 className="text-3xl font-extrabold text-foreground sm:text-4xl tracking-tight">
              Engineered for the Modern Industrial Shop Floor
            </h2>
            <p className="text-sm text-muted-foreground sm:text-base">
              Every tool a plant needs to detect faults early, execute standardized repairs, and track mission-critical spare parts.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {PLATFORM_CAPABILITIES.map(({ icon: Icon, badge, title, desc, highlight }) => (
              <Card
                key={title}
                className="group relative flex flex-col justify-between overflow-hidden border-border/80 bg-card/60 p-6 transition-all duration-300 hover:border-primary/50 hover:bg-card/90 hover:shadow-xl hover:shadow-primary/5"
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/15 text-primary transition duration-300 group-hover:scale-110 group-hover:bg-primary group-hover:text-black">
                      <Icon className="h-6 w-6" />
                    </div>
                    <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground font-semibold">
                      {badge}
                    </span>
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-foreground group-hover:text-primary transition">
                      {title}
                    </h3>
                    <p className="mt-2 text-xs text-muted-foreground leading-relaxed">
                      {desc}
                    </p>
                  </div>
                </div>

                <div className="mt-6 border-t border-border/60 pt-3 text-[11px] font-medium text-primary flex items-center gap-1.5">
                  <Sparkles className="h-3 w-3" />
                  <span>{highlight}</span>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* 3-STEP AR WORKFLOW SECTION */}
      <section id="workflow" className="border-y border-border/80 bg-card/30 py-20 sm:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 space-y-12">
          <div className="text-center max-w-2xl mx-auto space-y-3">
            <Badge variant="outline" className="border-primary/40 text-primary text-xs uppercase tracking-wider">
              Field Execution
            </Badge>
            <h2 className="text-3xl font-extrabold text-foreground sm:text-4xl tracking-tight">
              From Machine Scan to Work Sign-off in 3 Steps
            </h2>
            <p className="text-sm text-muted-foreground">
              Eliminate paper manuals, outdated checklists, and incorrect part picks.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-3">
            {WORKFLOW_STEPS.map((s) => {
              const StepIcon = s.icon;
              return (
                <div
                  key={s.step}
                  className="relative rounded-2xl border border-border/80 bg-gradient-to-b from-card to-background p-6 space-y-4 hover:border-primary/40 transition"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-3xl font-black text-primary/40">
                      {s.step}
                    </span>
                    <div className="rounded-xl bg-primary/10 p-2.5 text-primary">
                      <StepIcon className="h-5 w-5" />
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-bold text-foreground">{s.title}</h3>
                    <p className="text-xs font-medium text-primary mt-0.5">{s.subtitle}</p>
                    <p className="text-xs text-muted-foreground mt-2 leading-relaxed">{s.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ROLE PERSPECTIVES: TECHNICIAN VS SUPERVISOR */}
      <section id="roles" className="py-20 sm:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 space-y-10">
          <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
            <div>
              <Badge variant="outline" className="border-primary/40 text-primary text-xs uppercase tracking-wider">
                Built For The Whole Plant
              </Badge>
              <h2 className="mt-2 text-3xl font-extrabold text-foreground sm:text-4xl tracking-tight">
                Designed for Technicians. Built for Supervisors.
              </h2>
            </div>

            {/* Toggle buttons */}
            <div className="flex items-center rounded-xl border border-border/80 bg-background/80 p-1">
              <button
                onClick={() => setActiveRoleView("technician")}
                className={`flex items-center gap-1.5 rounded-lg px-4 py-2 text-xs font-semibold transition ${
                  activeRoleView === "technician"
                    ? "bg-primary text-primary-foreground shadow-md"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <HardHat className="h-4 w-4" />
                <span>Field Technicians</span>
              </button>
              <button
                onClick={() => setActiveRoleView("supervisor")}
                className={`flex items-center gap-1.5 rounded-lg px-4 py-2 text-xs font-semibold transition ${
                  activeRoleView === "supervisor"
                    ? "bg-primary text-primary-foreground shadow-md"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                <UserCheck className="h-4 w-4" />
                <span>Supervisors & Admins</span>
              </button>
            </div>
          </div>

          {/* Role Showcase Content */}
          <div className="grid gap-6 lg:grid-cols-2 lg:items-center">
            {activeRoleView === "technician" ? (
              <>
                <div className="space-y-4">
                  <div className="rounded-xl border border-border/80 bg-card/60 p-5 space-y-3">
                    <div className="flex items-center gap-2.5 text-primary font-semibold text-sm">
                      <Wrench className="h-4 w-4" />
                      <span>AR Assisted Step-by-Step Execution</span>
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      Color-coded AR overlays show exactly where to connect tools, adjust bolts, and inspect seals, with mandatory tool verifications.
                    </p>
                  </div>

                  <div className="rounded-xl border border-border/80 bg-card/60 p-5 space-y-3">
                    <div className="flex items-center gap-2.5 text-primary font-semibold text-sm">
                      <Volume2 className="h-4 w-4" />
                      <span>Hands-Free Speech Navigation</span>
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      Voice recognition allows technicians to advance steps, log observations, and replay safety warnings hands-free.
                    </p>
                  </div>

                  <div className="rounded-xl border border-border/80 bg-card/60 p-5 space-y-3">
                    <div className="flex items-center gap-2.5 text-primary font-semibold text-sm">
                      <CheckCircle2 className="h-4 w-4" />
                      <span>Personal Inbox & Task Queues</span>
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      Technicians see dispatched work orders sorted by urgency with SLA countdowns and 1-click links directly into machine guides.
                    </p>
                  </div>

                  <Button
                    size="sm"
                    className="orange-glow gap-1.5 text-xs bg-primary text-primary-foreground"
                    onClick={() => handleTryDemo("technician")}
                  >
                    <span>Test Technician Flow in Demo</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Button>
                </div>

                <div className="rounded-2xl border border-border/80 bg-card/80 p-6 space-y-4">
                  <h4 className="text-sm font-bold uppercase tracking-wider text-muted-foreground">
                    Technician Experience Highlights
                  </h4>
                  <div className="space-y-2.5 text-xs">
                    <div className="flex items-center justify-between rounded-lg bg-background/60 p-3 border border-border/60">
                      <span>Machine Identification</span>
                      <Badge variant="outline" className="text-[11px] text-emerald-400">QR / AI Vision</Badge>
                    </div>
                    <div className="flex items-center justify-between rounded-lg bg-background/60 p-3 border border-border/60">
                      <span>Offline Capability</span>
                      <Badge variant="outline" className="text-[11px] text-emerald-400">Full PWA Cache</Badge>
                    </div>
                    <div className="flex items-center justify-between rounded-lg bg-background/60 p-3 border border-border/60">
                      <span>Manuals & Documentation</span>
                      <Badge variant="outline" className="text-[11px] text-emerald-400">Interactive PDF Viewer</Badge>
                    </div>
                    <div className="flex items-center justify-between rounded-lg bg-background/60 p-3 border border-border/60">
                      <span>Conversational AI Assistant</span>
                      <Badge variant="outline" className="text-[11px] text-emerald-400">FixBot Chat</Badge>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <>
                <div className="space-y-4">
                  <div className="rounded-xl border border-border/80 bg-card/60 p-5 space-y-3">
                    <div className="flex items-center gap-2.5 text-primary font-semibold text-sm">
                      <UserCheck className="h-4 w-4" />
                      <span>Work Order Dispatch & Technician Rosters</span>
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      Assign maintenance procedures or custom work orders directly to technicians with automatic SLA calculation and workload balancing.
                    </p>
                  </div>

                  <div className="rounded-xl border border-border/80 bg-card/60 p-5 space-y-3">
                    <div className="flex items-center gap-2.5 text-primary font-semibold text-sm">
                      <Package className="h-4 w-4" />
                      <span>Parts Buffer & Procurement Queues</span>
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      Monitor low-stock alerts, print Code128 warehouse bin labels, and generate purchase orders with one click.
                    </p>
                  </div>

                  <div className="rounded-xl border border-border/80 bg-card/60 p-5 space-y-3">
                    <div className="flex items-center gap-2.5 text-primary font-semibold text-sm">
                      <Activity className="h-4 w-4" />
                      <span>Factory Telemetry & Uptime Analytics</span>
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed">
                      Track mean time to repair (MTTR), failure category distributions, 30-day downtime trends, and technician leaderboards.
                    </p>
                  </div>

                  <Button
                    size="sm"
                    className="orange-glow gap-1.5 text-xs bg-primary text-primary-foreground"
                    onClick={() => handleTryDemo("supervisor")}
                  >
                    <span>Test Supervisor Console in Demo</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Button>
                </div>

                <div className="rounded-2xl border border-border/80 bg-card/80 p-6 space-y-4">
                  <h4 className="text-sm font-bold uppercase tracking-wider text-muted-foreground">
                    Management Control Highlights
                  </h4>
                  <div className="space-y-2.5 text-xs">
                    <div className="flex items-center justify-between rounded-lg bg-background/60 p-3 border border-border/60">
                      <span>Dispatch Authority</span>
                      <Badge variant="outline" className="text-[11px] text-primary">Admin & Supervisor</Badge>
                    </div>
                    <div className="flex items-center justify-between rounded-lg bg-background/60 p-3 border border-border/60">
                      <span>Restock Queue Workflow</span>
                      <Badge variant="outline" className="text-[11px] text-primary">Automated PO Generator</Badge>
                    </div>
                    <div className="flex items-center justify-between rounded-lg bg-background/60 p-3 border border-border/60">
                      <span>Shift Reassignment</span>
                      <Badge variant="outline" className="text-[11px] text-primary">1-Click Handover</Badge>
                    </div>
                    <div className="flex items-center justify-between rounded-lg bg-background/60 p-3 border border-border/60">
                      <span>Audit & History</span>
                      <Badge variant="outline" className="text-[11px] text-primary">Verifiable Service Logs</Badge>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </section>

      {/* BOTTOM CONVERSION CTA BANNER */}
      <section className="py-16 sm:py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="relative overflow-hidden rounded-3xl border border-primary/40 bg-gradient-to-br from-primary/20 via-card to-background p-8 sm:p-12 lg:p-16 shadow-2xl text-center space-y-6">
            <div className="inline-flex items-center gap-2 rounded-full border border-primary/40 bg-primary/10 px-3.5 py-1 text-xs font-semibold text-primary">
              <Sparkles className="h-3.5 w-3.5" />
              <span>Ready for Immediate Deployment</span>
            </div>

            <h2 className="mx-auto max-w-2xl text-3xl font-extrabold tracking-tight sm:text-4xl text-foreground">
              Modernize Your Industrial Maintenance Today
            </h2>

            <p className="mx-auto max-w-xl text-sm sm:text-base text-muted-foreground">
              Test full AR guidance, computer vision identification, spare parts inventory, and work order dispatch in our interactive demo.
            </p>

            <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
              <Button
                size="lg"
                className="orange-glow gap-2 bg-primary text-primary-foreground font-semibold px-8"
                onClick={() => handleTryDemo("technician")}
              >
                <span>Launch Interactive Demo</span>
                <ArrowRight className="h-4 w-4" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                onClick={handleGetStarted}
                className="border-border/80 bg-background/60 hover:border-primary/50 px-8"
              >
                Create Account
              </Button>
            </div>

            <p className="text-[11px] text-muted-foreground pt-2">
              Includes preloaded machine catalog • No credit card required • Instant browser access
            </p>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t border-border/80 bg-background/80 py-10 text-xs text-muted-foreground">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-primary font-bold text-black text-xs">
              M
            </div>
            <span className="font-semibold text-foreground">
              MaintAI Industrial Maintenance Operating System
            </span>
          </div>

          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
              System Status: Operational
            </span>
            <span>•</span>
            <span>{DEMO_DATA.machines.length} Equipment Units</span>
            <span>•</span>
            <span>{DEMO_DATA.parts.length} Spare Part SKUs</span>
          </div>

          <p>© {new Date().getFullYear()} MaintAI. Enterprise Industrial Maintenance.</p>
        </div>
      </footer>
    </div>
  );
}
