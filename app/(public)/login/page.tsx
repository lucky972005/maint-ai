"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useApp } from "@/components/providers";
import { toast } from "@/hooks/use-toast";
import { createClient } from "@/lib/supabase/client";
import { isSupabaseConfigured } from "@/lib/demo-data";

export default function LoginPage() {
  const router = useRouter();
  const { enterDemoMode } = useApp();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const supabase = createClient();

  const handleLogin = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);

    try {
      if (!isSupabaseConfigured()) {
        toast({ 
          title: "Supabase not configured", 
          description: "Please configure Supabase in .env.local or use Demo mode below",
          variant: "destructive" 
        });
        setLoading(false);
        return;
      }

      // Clear demo mode cookie when logging in with Supabase
      document.cookie = "maintai_demo=; path=/; max-age=0;";

      // Add timeout to prevent hanging
      const timeoutPromise = new Promise<never>((_, reject) => 
        setTimeout(() => reject(new Error("Connection timeout. Please check your internet connection.")), 10000)
      );

      const { error } = await Promise.race([
        supabase.auth.signInWithPassword({ email, password }),
        timeoutPromise
      ]);

      if (error) throw error;

      // Save remember me preference
      localStorage.setItem("maintai_remember_me", rememberMe.toString());

      // If remember me is not checked, the session will be temporary
      // The providers will handle clearing it on next load
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

  const handleDemo = () => {
    enterDemoMode();
    // Small delay to ensure cookie is set before navigation
    setTimeout(() => {
      router.replace("/scan?demo=1");
    }, 100);
  };

  return (
    <div className="flex min-h-screen items-center justify-center industrial-gradient p-4">
      <Card className="w-full max-w-md border-border/50">
        <CardHeader className="text-center">
          <div className="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-lg bg-primary font-bold text-primary-foreground">
            M
          </div>
          <CardTitle>Welcome Back</CardTitle>
          <CardDescription>Sign in to MaintAI</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="admin@demo.com"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="demo123456"
                required
              />
            </div>
            <div className="flex items-center space-x-2">
              <input
                id="remember"
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
              />
              <Label htmlFor="remember" className="text-sm cursor-pointer">
                Remember me
              </Label>
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Signing in..." : "Sign In"}
            </Button>
          </form>

          <Button type="button" variant="outline" className="w-full" onClick={handleDemo}>
            Try Demo (no account needed)
          </Button>

          <p className="text-center text-sm text-muted-foreground">
            <Link href="/signup" className="text-primary hover:underline">
              Create account
            </Link>
            {" | "}
            <button
              type="button"
              className="text-primary hover:underline"
              onClick={() =>
                toast({ title: "Password reset", description: "Check your email for reset link" })
              }
            >
              Forgot password?
            </button>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
