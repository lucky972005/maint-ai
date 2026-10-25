"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Shield, Wrench, Users, AlertCircle, Sparkles, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useApp } from "@/components/providers";
import { toast } from "@/hooks/use-toast";
import { createClient } from "@/lib/supabase/client";
import { DEMO_USERS, isSupabaseConfigured } from "@/lib/demo-data";

const DEMO_ROLES = [
  {
    role: "admin" as const,
    title: "Admin",
    email: "admin@demo.com",
    name: "System Admin",
    icon: Shield,
    badgeVariant: "destructive" as const,
    description: "Manager dashboard, assignments, parts inventory & controls",
    defaultRoute: "/dashboard",
    color: "text-red-400 border-red-500/30 bg-red-500/10 hover:bg-red-500/20",
  },
  {
    role: "technician" as const,
    title: "Technician",
    email: "tech1@demo.com",
    name: "Raj Kumar",
    icon: Wrench,
    badgeVariant: "default" as const,
    description: "Camera scanner, AR repair guide, task inbox & certificate logs",
    defaultRoute: "/scan",
    color: "text-primary border-primary/30 bg-primary/10 hover:bg-primary/20",
  },
  {
    role: "supervisor" as const,
    title: "Supervisor",
    email: "supervisor@demo.com",
    name: "Supervisor Patel",
    icon: Users,
    badgeVariant: "secondary" as const,
    description: "Team oversight, technician assignments & shift dispatch",
    defaultRoute: "/assignments",
    color: "text-amber-400 border-amber-500/30 bg-amber-500/10 hover:bg-amber-500/20",
  },
];

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { enterDemoMode } = useApp();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const supabaseConfigured = isSupabaseConfigured();
  const supabase = createClient();

  useEffect(() => {
    const pEmail = searchParams.get("email");
    const pPwd = searchParams.get("prefill_pwd");
    const isReset = searchParams.get("reset_success");

    if (pEmail) setEmail(pEmail);
    if (pPwd) setPassword(pPwd);
    if (isReset) {
      toast({
        title: "Password Reset Completed",
        description: "Your new password is now active. Sign in below.",
      });
    }
  }, [searchParams]);

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);

    try {
      const trimmedEmail = email.trim().toLowerCase();
      let customUsers: any[] = [];
      if (typeof window !== "undefined") {
        try {
          customUsers = JSON.parse(localStorage.getItem("custom_registered_users") || "[]");
        } catch {
          customUsers = [];
        }
      }
      const allUsers = [...DEMO_USERS, ...customUsers];

      const matchedDemoUser = allUsers.find((u) => {
        if (u.email.toLowerCase() !== trimmedEmail) return false;
        if (typeof window !== "undefined") {
          const customPasswords = JSON.parse(localStorage.getItem("custom_user_passwords") || "{}");
          if (customPasswords[trimmedEmail]) {
            return password === customPasswords[trimmedEmail] || password === u.password;
          }
        }
        return u.password === password;
      });

      // If Supabase is not configured, authenticate against demo or custom accounts
      if (!supabaseConfigured) {
        if (matchedDemoUser) {
          const { password: _password, ...demoProfile } = matchedDemoUser;
          void _password;
          enterDemoMode(demoProfile);
          toast({
            title: `Welcome, ${demoProfile.full_name}`,
            description: `Signed in as ${demoProfile.role.toUpperCase()}`,
          });
          const targetRoute =
            demoProfile.role === "admin"
              ? "/dashboard"
              : demoProfile.role === "supervisor"
              ? "/assignments"
              : "/scan";
          setTimeout(() => {
            router.replace(`${targetRoute}?demo=1`);
          }, 100);
          return;
        }

        toast({
          title: "Supabase not configured in Vercel",
          description:
            "Please use one of the 1-Click Demo Logins below (Admin, Technician, or Supervisor) or enter admin@demo.com / demo123456.",
          variant: "destructive",
        });
        setLoading(false);
        return;
      }

      // Supabase is configured
      document.cookie = "maintai_demo=; path=/; max-age=0;";

      const timeoutPromise = new Promise<never>((_, reject) =>
        setTimeout(() => reject(new Error("Connection timeout. Please check your internet connection.")), 10000)
      );

      const { error } = await Promise.race([
        supabase.auth.signInWithPassword({ email: trimmedEmail, password }),
        timeoutPromise,
      ]);

      if (error) {
        // Fallback for demo users & locally registered users even if Supabase auth fails (e.g. rate limit, unconfirmed email)
        if (matchedDemoUser) {
          const { password: _password, ...demoProfile } = matchedDemoUser;
          void _password;
          enterDemoMode(demoProfile);
          toast({
            title: `Welcome, ${demoProfile.full_name}`,
            description: `Signed in as ${demoProfile.role.toUpperCase()}`,
          });
          const targetRoute =
            demoProfile.role === "admin"
              ? "/dashboard"
              : demoProfile.role === "supervisor"
              ? "/assignments"
              : "/scan";
          router.push(targetRoute);
          return;
        }
        throw error;
      }

      localStorage.setItem("maintai_remember_me", rememberMe.toString());
      router.push("/scan");
    } catch (error) {
      toast({
        title: "Login failed",
        description: error instanceof Error ? error.message : "Unknown error",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleRoleQuickLogin = (roleItem: typeof DEMO_ROLES[0]) => {
    const user = DEMO_USERS.find((u) => u.role === roleItem.role) ?? DEMO_USERS[0];
    const { password: _password, ...profile } = user;
    void _password;
    enterDemoMode(profile);
    toast({
      title: `Logged in as ${profile.full_name}`,
      description: `Active role: ${profile.role.toUpperCase()}`,
    });
    setTimeout(() => {
      router.replace(`${roleItem.defaultRoute}?demo=1`);
    }, 100);
  };

  const handleFillCredentials = (demoEmail: string) => {
    setEmail(demoEmail);
    setPassword("demo123456");
    toast({
      title: "Credentials filled",
      description: `${demoEmail} / demo123456`,
    });
  };

  return (
    <div className="flex min-h-screen items-center justify-center industrial-gradient p-4">
      <Card className="w-full max-w-lg border-border/50 shadow-2xl">
        <CardHeader className="text-center pb-4">
          <div className="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-2xl bg-primary font-bold text-primary-foreground shadow-lg shadow-primary/20">
            M
          </div>
          <CardTitle className="text-2xl">Welcome to MaintAI</CardTitle>
          <CardDescription>Industrial maintenance platform with AI vision & AR guidance</CardDescription>

          {!supabaseConfigured && (
            <div className="mt-3 flex items-start gap-2.5 rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-left text-xs text-amber-500">
              <AlertCircle className="h-4 w-4 shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-amber-400">Demo Mode Active (Cloud DB Unset)</p>
                <p className="text-amber-500/90 mt-0.5 leading-relaxed">
                  Supabase environment variables are not configured in Vercel settings. You can test all features immediately using the 1-Click Role Logins below.
                </p>
              </div>
            </div>
          )}
        </CardHeader>

        <CardContent className="space-y-6">
          {/* One-Click Role Logins Section */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                <Sparkles className="h-3.5 w-3.5 text-primary" />
                1-Click Demo Logins
              </span>
              <span className="text-[11px] text-muted-foreground">Select role to explore</span>
            </div>

            <div className="grid gap-2.5">
              {DEMO_ROLES.map((item) => {
                const Icon = item.icon;
                return (
                  <div
                    key={item.role}
                    className={`flex items-center justify-between rounded-xl border p-3 transition-all ${item.color}`}
                  >
                    <div className="flex items-start gap-3 min-w-0 pr-2">
                      <div className="rounded-lg p-2 bg-background/60 shadow-sm shrink-0">
                        <Icon className="h-4 w-4" />
                      </div>
                      <div className="min-w-0">
                        <div className="flex items-center gap-2">
                          <p className="text-sm font-semibold text-foreground truncate">{item.title}</p>
                          <span className="text-[11px] text-muted-foreground">({item.name})</span>
                        </div>
                        <p className="text-xs text-muted-foreground truncate">{item.description}</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-1.5 shrink-0">
                      <Button
                        type="button"
                        size="sm"
                        variant="secondary"
                        className="h-8 text-xs px-2.5 hidden sm:inline-flex"
                        onClick={() => handleFillCredentials(item.email)}
                        title="Fill form credentials"
                      >
                        Fill
                      </Button>
                      <Button
                        type="button"
                        size="sm"
                        className="h-8 text-xs font-semibold px-3 gap-1 shadow-sm"
                        onClick={() => handleRoleQuickLogin(item)}
                      >
                        Login <ArrowRight className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t border-border/60" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-card px-2 text-muted-foreground">Or sign in with email</span>
            </div>
          </div>

          {/* Standard Email / Password Form */}
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="admin@demo.com or tech1@demo.com"
                required
              />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password">Password</Label>
                <Link
                  href="/forgot-password"
                  className="text-xs text-primary font-medium hover:underline transition-colors"
                >
                  Forgot password?
                </Link>
              </div>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="demo123456"
                required
              />
              <p className="text-[11px] text-muted-foreground">Default demo password: demo123456</p>
            </div>
            <div className="flex items-center space-x-2">
              <input
                id="remember"
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
              />
              <Label htmlFor="remember" className="text-sm cursor-pointer text-muted-foreground">
                Remember me
              </Label>
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Signing in..." : "Sign In with Credentials"}
            </Button>
          </form>

          <p className="text-center text-sm text-muted-foreground pt-2 flex items-center justify-center gap-2">
            <Link href="/signup" className="text-primary hover:underline">
              Create account
            </Link>
            <span>•</span>
            <Link href="/forgot-password" className="text-primary hover:underline">
              Forgot password?
            </Link>
            <span>•</span>
            <Link href="/" className="text-primary hover:underline">
              Landing Page
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center industrial-gradient p-4">
          <div className="w-full max-w-lg rounded-2xl border border-border/50 bg-card p-8 shadow-2xl text-center">
            <div className="mx-auto mb-4 h-12 w-12 rounded-2xl bg-primary/20 animate-pulse" />
            <div className="h-6 w-48 bg-muted/40 rounded mx-auto mb-2 animate-pulse" />
            <div className="h-4 w-64 bg-muted/30 rounded mx-auto animate-pulse" />
          </div>
        </div>
      }
    >
      <LoginForm />
    </Suspense>
  );
}
