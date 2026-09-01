"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowRight, Brain, Download, Eye, Layers, Scan, Shield, Volume2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { DEMO_DATA, isSupabaseConfigured } from "@/lib/demo-data";
import { useApp } from "@/components/providers";

const FEATURES = [
  { icon: Brain, title: "AI Machine Recognition", desc: "Point your camera at any machine for instant identification." },
  { icon: Layers, title: "AR Repair Guidance", desc: "Step-by-step overlays with animated component markers." },
  { icon: Volume2, title: "Voice-Controlled Workflow", desc: "Hands-free navigation with speech commands." },
  { icon: Shield, title: "Offline-First PWA", desc: "Works without connectivity and syncs when back online." },
];

const PRICING = [
  { name: "Starter", price: "$99", period: "/mo", features: ["5 technicians", "20 machines", "Basic AI", "Email support"] },
  { name: "Pro", price: "$499", period: "/mo", features: ["25 technicians", "Unlimited machines", "Full AI + AR", "Priority support"], popular: true },
  { name: "Enterprise", price: "Custom", period: "", features: ["Unlimited users", "Multi-factory", "Custom integrations", "Dedicated support"] },
];

const MACHINE_IMAGES = [
  "https://images.unsplash.com/photo-1565043666747-69f6646db940?w=800&q=80",
  "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&q=80",
  "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=800&q=80",
];

export default function LandingPage() {
  const router = useRouter();
  const { enterDemoMode } = useApp();
  const [imageIndex, setImageIndex] = useState(0);
  const [stats, setStats] = useState({ scanned: 127, repairs: 43 });
  const [deferredPrompt, setDeferredPrompt] = useState<{ prompt: () => Promise<void> } | null>(null);
  const [showInstall, setShowInstall] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => setImageIndex((index) => (index + 1) % MACHINE_IMAGES.length), 4000);
    const statsInterval = setInterval(() => {
      setStats((current) => ({
        scanned: current.scanned + Math.floor(Math.random() * 3),
        repairs: current.repairs + (Math.random() > 0.7 ? 1 : 0),
      }));
    }, 8000);

    const handler = (event: Event) => {
      event.preventDefault();
      setDeferredPrompt(event as unknown as { prompt: () => Promise<void> });
      setShowInstall(true);
    };

    window.addEventListener("beforeinstallprompt", handler);

    return () => {
      clearInterval(interval);
      clearInterval(statsInterval);
      window.removeEventListener("beforeinstallprompt", handler);
    };
  }, []);

  const installPwa = async () => {
    if (!deferredPrompt) return;
    await deferredPrompt.prompt();
    setShowInstall(false);
  };

  const handleTryDemo = () => {
    enterDemoMode();
    // Small delay to ensure cookie is set before navigation
    setTimeout(() => {
      router.replace("/scan?demo=1");
    }, 100);
  };

  const handleGetStarted = () => {
    if (!isSupabaseConfigured()) {
      handleTryDemo();
      return;
    }

    router.push("/signup");
  };

  return (
    <div className="min-h-screen industrial-gradient">
      <nav className="flex items-center justify-between border-b border-border/50 px-6 py-4">
        <div className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary font-bold text-primary-foreground">
            M
          </div>
          <span className="text-xl font-bold">
            Maint<span className="text-primary">AI</span>
          </span>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/login">
            <Button variant="ghost">Login</Button>
          </Link>
          <Button onClick={handleGetStarted}>Get Started</Button>
        </div>
      </nav>

      {showInstall && (
        <div className="flex items-center justify-between border-b border-primary/30 bg-primary/10 px-6 py-3">
          <span className="text-sm">Install MaintAI for offline access on your device</span>
          <Button size="sm" onClick={installPwa}>
            <Download className="mr-2 h-4 w-4" />
            Install App
          </Button>
        </div>
      )}

      <section className="mx-auto grid max-w-6xl gap-12 px-6 py-16 md:grid-cols-2 md:items-center md:py-24">
        <div>
          <Badge className="mb-4">AI-Powered Maintenance</Badge>
          <h1 className="mb-6 text-4xl font-bold leading-tight md:text-5xl">
            Industrial Maintenance, <span className="text-primary">Reimagined with AI</span>
          </h1>
          <p className="mb-8 text-lg text-muted-foreground">
            Scan, identify, and repair industrial equipment with AR guidance, voice control, and predictive maintenance in one installable PWA.
          </p>
          <div className="mb-8 flex flex-wrap gap-4">
            <div className="text-center">
              <p className="text-3xl font-bold text-primary">{stats.scanned}</p>
              <p className="text-xs text-muted-foreground">Machines scanned today</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-primary">{stats.repairs}</p>
              <p className="text-xs text-muted-foreground">Repairs completed</p>
            </div>
          </div>
          <div className="flex flex-wrap gap-3">
            <Button size="lg" className="orange-glow" onClick={handleGetStarted}>
              Get Started
              <ArrowRight className="h-4 w-4" />
            </Button>
            <Button size="lg" variant="outline" onClick={handleTryDemo}>
              Try Demo
            </Button>
          </div>
        </div>
        <div className="relative h-80 overflow-hidden rounded-2xl border border-border">
          {MACHINE_IMAGES.map((image, index) => (
            <img
              key={image}
              src={image}
              alt="Industrial machine"
              className={`absolute inset-0 h-full w-full object-cover transition-opacity duration-1000 ${index === imageIndex ? "opacity-100" : "opacity-0"}`}
            />
          ))}
          <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent" />
        </div>
      </section>

      <section className="bg-card/30 px-6 py-16">
        <div className="mx-auto grid max-w-6xl gap-6 md:grid-cols-2 lg:grid-cols-4">
          {FEATURES.map(({ icon: Icon, title, desc }) => (
            <Card key={title} className="border-border/50 transition-colors hover:border-primary/30">
              <CardHeader>
                <Icon className="mb-2 h-8 w-8 text-primary" />
                <CardTitle className="text-lg">{title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">{desc}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-4xl px-6 py-16 text-center">
        <h2 className="mb-8 text-2xl font-bold">See It In Action</h2>
        <div className="flex aspect-video items-center justify-center rounded-2xl border border-border bg-muted">
          <div className="text-center">
            <Scan className="mx-auto mb-4 h-16 w-16 text-primary" />
            <p className="text-muted-foreground">Worker scanning machine QR code with MaintAI</p>
            <Link href="/signup">
              <Button className="mt-4">Sign Up to Try It</Button>
            </Link>
          </div>
        </div>
      </section>

      <section className="bg-card/30 px-6 py-16">
        <h2 className="mb-12 text-center text-2xl font-bold">Pricing</h2>
        <div className="mx-auto grid max-w-5xl gap-6 md:grid-cols-3">
          {PRICING.map((tier) => (
            <Card key={tier.name} className={`relative ${tier.popular ? "border-primary orange-glow" : "border-border/50"}`}>
              {tier.popular && <Badge className="absolute -top-3 left-1/2 -translate-x-1/2">Most Popular</Badge>}
              <CardHeader className="text-center">
                <CardTitle>{tier.name}</CardTitle>
                <p className="text-3xl font-bold text-primary">
                  {tier.price}
                  <span className="text-sm text-muted-foreground">{tier.period}</span>
                </p>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-sm">
                  {tier.features.map((feature) => (
                    <li key={feature} className="flex items-center gap-2">
                      <Eye className="h-3 w-3 text-primary" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <Link href="/signup">
                  <Button className="mt-6 w-full" variant={tier.popular ? "default" : "outline"}>
                    Choose Plan
                  </Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <footer className="border-t border-border px-6 py-8 text-center text-sm text-muted-foreground">
        <p>MaintAI - Industrial Maintenance Assistant | {DEMO_DATA.machines.length} machines | Demo mode ready</p>
      </footer>
    </div>
  );
}
