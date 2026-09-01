"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import {
  AlertTriangle,
  BookOpen,
  Boxes,
  History,
  LayoutDashboard,
  LogOut,
  Menu,
  MessageSquare,
  Package,
  QrCode,
  Radio,
  Scan,
  Search,
  TriangleAlert,
  User,
  Wifi,
  WifiOff,
  Wrench,
  X,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DEMO_DATA, getDashboardStats } from "@/lib/demo-data";
import { cn } from "@/lib/utils";
import { useApp } from "@/components/providers";

const navItems = [
  { href: "/scan", label: "Scanner", icon: Scan, description: "Scan QR codes and identify machines" },
  { href: "/history", label: "History", icon: History, description: "Review completed and active work" },
  { href: "/parts", label: "Parts", icon: Package, description: "Manage inventory and low-stock items" },
  { href: "/qr-codes", label: "QR Codes", icon: QrCode, description: "Generate and download machine QR codes" },
  { href: "/chat", label: "FixBot", icon: MessageSquare, description: "Ask the AI assistant for guidance" },
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard, description: "Track uptime, faults, and KPIs" },
  { href: "/assignments", label: "Assignments", icon: User, description: "Supervisor: assign work orders to technicians" },
  { href: "/inbox", label: "Inbox", icon: User, description: "Technician: view assigned work orders" },
];

const quickLinks = [
  { href: "/report", label: "Report fault", icon: TriangleAlert },
  { href: "/manuals", label: "Manual library", icon: BookOpen },
];

const alertMachines = DEMO_DATA.faults.filter((fault) => fault.status === "open").slice(0, 3);
const lowStockParts = DEMO_DATA.parts.filter((part) => part.stock_quantity < part.min_stock_level).slice(0, 4);
const recentMachines = DEMO_DATA.machines.slice(0, 5);
const dashboardStats = getDashboardStats();

type SearchItem = {
  href: string;
  label: string;
  description: string;
  section: string;
  icon: typeof Search;
};

function buildSearchItems(): SearchItem[] {
  const routeItems = [
    ...navItems.map((item) => ({
      href: item.href,
      label: item.label,
      description: item.description,
      section: "Workspace",
      icon: item.icon,
    })),
    ...quickLinks.map((item) => ({
      href: item.href,
      label: item.label,
      description: "Jump straight into a key workflow",
      section: "Quick actions",
      icon: item.icon,
    })),
  ];

  const machineItems = recentMachines.map((machine) => ({
    href: `/repair/${machine.id}`,
    label: machine.name,
    description: `${machine.model ?? machine.category} in ${machine.location ?? "the plant"}`,
    section: "Machines",
    icon: Wrench,
  }));

  const partItems = lowStockParts.map((part) => ({
    href: "/parts",
    label: part.name,
    description: `Stock ${part.stock_quantity} / min ${part.min_stock_level}`,
    section: "Inventory",
    icon: Boxes,
  }));

  return [...routeItems, ...machineItems, ...partItems];
}

function SearchPalette() {
  const router = useRouter();
  const pathname = usePathname();
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const searchItems = useMemo(buildSearchItems, []);

  const results = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) {
      return searchItems.slice(0, 6);
    }

    return searchItems
      .filter((item) =>
        [item.label, item.description, item.section].some((value) =>
          value.toLowerCase().includes(normalized)
        )
      )
      .slice(0, 8);
  }, [query, searchItems]);

  const handleNavigate = (href: string) => {
    setOpen(false);
    setQuery("");
    router.push(href);
  };

  return (
    <div className="relative w-full max-w-xl">
      <div className="relative">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <input
          value={query}
          onChange={(event) => {
            setQuery(event.target.value);
            setOpen(true);
          }}
          onFocus={() => setOpen(true)}
          onKeyDown={(event) => {
            if (event.key === "Escape") {
              setOpen(false);
              return;
            }

            if (event.key === "Enter" && results[0]) {
              event.preventDefault();
              handleNavigate(results[0].href);
            }
          }}
          placeholder="Search screens, machines, and inventory"
          className="h-11 w-full rounded-2xl border border-border bg-background/80 pl-10 pr-10 text-sm text-foreground outline-none transition focus:border-primary/50 focus:ring-2 focus:ring-primary/20"
        />
        {query && (
          <button
            type="button"
            onClick={() => {
              setQuery("");
              setOpen(false);
            }}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground transition hover:text-foreground"
            aria-label="Clear search"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      {open && (
        <div className="absolute left-0 right-0 top-[calc(100%+0.5rem)] z-50 rounded-2xl border border-border bg-card/95 p-2 shadow-2xl backdrop-blur">
          <div className="mb-2 flex items-center justify-between px-2 pt-1 text-xs text-muted-foreground">
            <span>{query ? "Best matches" : "Suggested jumps"}</span>
            <span>{pathname}</span>
          </div>
          {results.length > 0 ? (
            <div className="space-y-1">
              {results.map((item) => {
                const Icon = item.icon;
                return (
                  <button
                    key={`${item.section}-${item.href}-${item.label}`}
                    type="button"
                    onMouseDown={(event) => event.preventDefault()}
                    onClick={() => handleNavigate(item.href)}
                    className="flex w-full items-start gap-3 rounded-xl px-3 py-3 text-left transition hover:bg-muted/70"
                  >
                    <div className="mt-0.5 rounded-lg border border-border bg-background p-2">
                      <Icon className="h-4 w-4 text-primary" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-medium">{item.label}</p>
                      <p className="truncate text-xs text-muted-foreground">{item.description}</p>
                    </div>
                    <Badge variant="outline" className="ml-auto shrink-0">
                      {item.section}
                    </Badge>
                  </button>
                );
              })}
            </div>
          ) : (
            <div className="rounded-xl border border-dashed border-border px-4 py-8 text-center text-sm text-muted-foreground">
              No matches found. Try a machine, part, or page name.
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function DesktopSidebar() {
  const pathname = usePathname();
  const { profile } = useApp();

  const filteredNavItems = navItems.filter((item) => {
    if (item.href === "/assignments" && profile?.role === "technician") return false;
    if (item.href === "/inbox" && profile?.role === "supervisor") return false;
    if (item.href === "/inbox" && profile?.role === "admin") return false;
    return true;
  });

  return (
    <aside className="hidden lg:flex lg:w-72 lg:flex-col lg:border-r lg:border-border/70 lg:bg-card/70">
      <div className="sticky top-0 flex h-screen flex-col px-5 py-6">
        <Link href="/" className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-primary font-bold text-primary-foreground shadow-lg shadow-primary/20">
            M
          </div>
          <div>
            <p className="text-lg font-semibold">MaintAI</p>
            <p className="text-xs text-muted-foreground">Industrial service workspace</p>
          </div>
        </Link>

        <div className="mt-6">
          <SearchPalette />
        </div>

        <nav className="mt-6 space-y-2">
          {filteredNavItems.map(({ href, label, icon: Icon, description }) => {
            const active = pathname.startsWith(href);
            return (
              <Link
                key={href}
                href={href}
                className={cn(
                  "flex items-start gap-3 rounded-2xl border px-4 py-3 transition",
                  active
                    ? "border-primary/40 bg-primary/10 text-foreground shadow-lg shadow-primary/10"
                    : "border-transparent text-muted-foreground hover:border-border hover:bg-muted/70 hover:text-foreground"
                )}
              >
                <div className={cn("rounded-xl p-2", active ? "bg-primary text-primary-foreground" : "bg-muted")}>
                  <Icon className="h-4 w-4" />
                </div>
                <div className="min-w-0">
                  <p className="font-medium">{label}</p>
                  <p className="text-xs text-muted-foreground">{description}</p>
                </div>
              </Link>
            );
          })}
        </nav>

        <Card className="mt-6 border-primary/20 bg-gradient-to-br from-primary/15 via-card to-card">
          <CardHeader className="pb-3">
            <CardTitle className="text-base">Quick launch</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {quickLinks.map(({ href, label, icon: Icon }) => (
              <Link key={href} href={href}>
                <Button variant="outline" className="w-full justify-start rounded-xl">
                  <Icon className="h-4 w-4" />
                  {label}
                </Button>
              </Link>
            ))}
          </CardContent>
        </Card>

        <div className="mt-auto rounded-2xl border border-border/70 bg-background/70 p-4">
          <p className="text-sm font-medium">Shift snapshot</p>
          <div className="mt-3 grid grid-cols-2 gap-3 text-sm">
            <div>
              <p className="text-2xl font-semibold text-primary">{dashboardStats.pendingFaults}</p>
              <p className="text-muted-foreground">Open faults</p>
            </div>
            <div>
              <p className="text-2xl font-semibold text-primary">{dashboardStats.lowStockParts}</p>
              <p className="text-muted-foreground">Low stock</p>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}

function BottomNav() {
  const pathname = usePathname();
  const { profile } = useApp();

  const filteredNavItems = navItems.filter((item) => {
    if (item.href === "/assignments" && profile?.role === "technician") return false;
    if (item.href === "/inbox" && profile?.role === "supervisor") return false;
    if (item.href === "/inbox" && profile?.role === "admin") return false;
    return true;
  });

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 border-t border-border bg-card/95 backdrop-blur safe-bottom lg:hidden">
      <div className="flex items-center justify-around px-2 py-2">
        {filteredNavItems.map(({ href, label, icon: Icon }) => {
          const active = pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex min-w-[64px] flex-col items-center gap-1 rounded-lg px-3 py-1.5 transition-colors",
                active ? "text-primary" : "text-muted-foreground hover:text-foreground"
              )}
            >
              <Icon className={cn("h-5 w-5", active && "orange-glow")} />
              <span className="text-[10px] font-medium">{label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}

function AppHeader({ title, showStatus = true }: { title?: string; showStatus?: boolean }) {
  const { online, profile, demoMode } = useApp();
  const [mobileSearchOpen, setMobileSearchOpen] = useState(false);
  const router = useRouter();
  const roleLabel = profile?.role ? profile.role[0].toUpperCase() + profile.role.slice(1) : "Guest";

  const handleLogout = async () => {
    try {
      const { createClient } = await import("@/lib/supabase/client");
      const supabase = createClient();
      await supabase.auth.signOut();
      localStorage.removeItem("maintai_remember_me");
      router.push("/login");
    } catch (error) {
      console.error("Logout error:", error);
      router.push("/login");
    }
  };

  return (
    <header className="sticky top-0 z-30 border-b border-border/70 bg-background/85 backdrop-blur">
      <div className="safe-top px-4 py-4 lg:px-8">
        <div className="flex items-center gap-3 lg:hidden">
          <button
            type="button"
            onClick={() => setMobileSearchOpen((value) => !value)}
            className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-border bg-card text-foreground"
            aria-label="Toggle search"
          >
            <Menu className="h-4 w-4" />
          </button>
          <div className="min-w-0 flex-1">
            <p className="truncate text-lg font-semibold">{title ?? "Workspace"}</p>
            <p className="truncate text-xs text-muted-foreground">Apex Manufacturing Plant</p>
          </div>
          <div className="flex items-center gap-2">
            {demoMode && <Badge variant="warning">Demo</Badge>}
            {showStatus && (
              <Badge variant={online ? "success" : "destructive"} className="gap-1">
                {online ? <Wifi className="h-3 w-3" /> : <WifiOff className="h-3 w-3" />}
                {online ? "Online" : "Offline"}
              </Badge>
            )}
            <button
              type="button"
              onClick={handleLogout}
              className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-border bg-card text-foreground"
              aria-label="Logout"
            >
              <LogOut className="h-4 w-4" />
            </button>
          </div>
        </div>

        {mobileSearchOpen && (
          <div className="mt-3 lg:hidden">
            <SearchPalette />
          </div>
        )}

        <div className="hidden items-center justify-between gap-6 lg:flex">
          <div>
            <p className="text-2xl font-semibold">{title ?? "Workspace"}</p>
            <p className="text-sm text-muted-foreground">
              {profile?.full_name ?? "Guest operator"} - {roleLabel} access
            </p>
          </div>
          <div className="flex flex-1 items-center justify-end gap-3">
            <SearchPalette />
            {demoMode && <Badge variant="warning">Demo mode</Badge>}
            {showStatus && (
              <Badge variant={online ? "success" : "destructive"} className="gap-1 px-3 py-1.5">
                {online ? <Wifi className="h-3 w-3" /> : <WifiOff className="h-3 w-3" />}
                {online ? "Online sync" : "Offline queue"}
              </Badge>
            )}
            <button
              type="button"
              onClick={handleLogout}
              className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-border bg-card text-foreground"
              aria-label="Logout"
            >
              <LogOut className="h-4 w-4" />
            </button>
            <div className="flex items-center gap-3 rounded-2xl border border-border bg-card px-3 py-2">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/15 font-semibold text-primary">
                {(profile?.full_name ?? "M").slice(0, 1).toUpperCase()}
              </div>
              <div className="min-w-0">
                <p className="truncate text-sm font-medium">{profile?.full_name ?? "MaintAI demo"}</p>
                <p className="truncate text-xs text-muted-foreground">{profile?.email ?? "local workspace"}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function OfflineBanner() {
  const { online } = useApp();

  if (online) return null;

  return (
    <div className="border-b border-primary/30 bg-primary/15 px-4 py-2 text-center text-sm text-primary lg:px-8">
      Offline mode is active. New reports and logs will sync when the connection returns.
    </div>
  );
}

function WorkspaceRail() {
  return (
    <aside className="hidden xl:block xl:w-80 xl:border-l xl:border-border/70 xl:bg-card/60">
      <div className="sticky top-0 flex h-screen flex-col gap-4 overflow-y-auto px-5 py-6">
        <Card className="border-border/70">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-base">
              <Radio className="h-4 w-4 text-primary" />
              Live alerts
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {alertMachines.map((fault) => (
              <Link
                key={fault.id}
                href={`/repair/${fault.machine_id ?? ""}`}
                className="block rounded-xl border border-border/60 bg-background/60 p-3 transition hover:border-primary/30"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">{fault.machine?.name}</p>
                    <p className="mt-1 text-xs text-muted-foreground">{fault.description}</p>
                  </div>
                  <Badge variant={fault.severity === "critical" ? "destructive" : "warning"}>
                    {fault.severity}
                  </Badge>
                </div>
              </Link>
            ))}
          </CardContent>
        </Card>

        <Card className="border-border/70">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center gap-2 text-base">
              <AlertTriangle className="h-4 w-4 text-primary" />
              Restock queue
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {lowStockParts.map((part) => (
              <div key={part.id} className="rounded-xl border border-border/60 bg-background/60 p-3">
                <div className="flex items-center justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium">{part.name}</p>
                    <p className="text-xs text-muted-foreground">{part.part_number}</p>
                  </div>
                  <Badge variant="destructive">Stock {part.stock_quantity}</Badge>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </aside>
  );
}

export function AppShell({ children, title }: { children: React.ReactNode; title?: string }) {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="flex min-h-screen bg-[radial-gradient(circle_at_top_left,rgba(249,115,22,0.12),transparent_28%),linear-gradient(180deg,rgba(15,23,42,0.96),rgba(2,6,23,1))]">
        <DesktopSidebar />
        <div className="flex min-w-0 flex-1 flex-col">
          <AppHeader title={title} />
          <OfflineBanner />
          <main className="flex-1 pb-24 lg:pb-8">
            <div className="mx-auto w-full max-w-[1400px]">{children}</div>
          </main>
        </div>
        <WorkspaceRail />
      </div>
      <BottomNav />
    </div>
  );
}
