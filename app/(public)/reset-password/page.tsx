"use client";

import { Suspense, useEffect, useState, useMemo } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { ShieldCheck, Eye, EyeOff, ArrowRight, CheckCircle2, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { toast } from "@/hooks/use-toast";
import { createClient } from "@/lib/supabase/client";
import { isSupabaseConfigured, DEMO_USERS } from "@/lib/demo-data";

function ResetPasswordContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const supabaseConfigured = isSupabaseConfigured();
  const supabase = createClient();

  // Load target email from URL params, Supabase auth session, or sessionStorage
  useEffect(() => {
    const urlEmail = searchParams.get("email");
    if (urlEmail) {
      setEmail(urlEmail.trim().toLowerCase());
      return;
    }

    if (supabaseConfigured) {
      supabase.auth.getUser().then(({ data }) => {
        if (data?.user?.email) {
          setEmail(data.user.email.toLowerCase());
        }
      });
    }

    if (typeof window !== "undefined") {
      const stored = sessionStorage.getItem("maintai_pwd_reset");
      if (stored) {
        try {
          const parsed = JSON.parse(stored);
          if (parsed.email) setEmail(parsed.email.toLowerCase());
        } catch {
          /* ignore json error */
        }
      }
    }
  }, [searchParams, supabaseConfigured, supabase.auth]);

  // Password criteria evaluations
  const checks = useMemo(() => {
    return {
      hasMinLength: password.length >= 6,
      hasNumber: /\d/.test(password),
      hasLetter: /[a-zA-Z]/.test(password),
      isMatched: password.length > 0 && password === confirmPassword,
    };
  }, [password, confirmPassword]);

  const strengthScore = useMemo(() => {
    let score = 0;
    if (checks.hasMinLength) score += 25;
    if (checks.hasNumber) score += 25;
    if (checks.hasLetter) score += 25;
    if (password.length >= 10 || /[^a-zA-Z0-9]/.test(password)) score += 25;
    return score;
  }, [checks, password]);

  const strengthLabel = useMemo(() => {
    if (strengthScore <= 25) return { label: "Weak", color: "bg-red-500", text: "text-red-400" };
    if (strengthScore <= 50) return { label: "Fair", color: "bg-amber-500", text: "text-amber-400" };
    if (strengthScore <= 75) return { label: "Good", color: "bg-blue-500", text: "text-blue-400" };
    return { label: "Strong", color: "bg-emerald-500", text: "text-emerald-400" };
  }, [strengthScore]);

  const handleResetPassword = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!email) {
      toast({
        title: "Missing account reference",
        description: "Please restart the password reset request.",
        variant: "destructive",
      });
      router.push("/forgot-password");
      return;
    }

    if (!checks.hasMinLength) {
      toast({
        title: "Password too short",
        description: "Password must be at least 6 characters.",
        variant: "destructive",
      });
      return;
    }

    if (password !== confirmPassword) {
      toast({
        title: "Passwords do not match",
        description: "Please verify both password entries match exactly.",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);

    try {
      const normalizedEmail = email.trim().toLowerCase();

      // 1. Update in Supabase if configured & active session
      if (supabaseConfigured) {
        try {
          const { error } = await supabase.auth.updateUser({ password });
          if (error) {
            console.warn("Supabase updateUser notice:", error.message);
          }
        } catch (sbErr) {
          console.warn("Supabase auth error:", sbErr);
        }
      }

      // 2. Persist updated custom password locally for demo and offline accounts
      if (typeof window !== "undefined") {
        const storedCustom = JSON.parse(localStorage.getItem("custom_user_passwords") || "{}");
        storedCustom[normalizedEmail] = password;
        localStorage.setItem("custom_user_passwords", JSON.stringify(storedCustom));

        // Update in-memory DEMO_USERS instance if matching
        const demoUser = DEMO_USERS.find((u) => u.email.toLowerCase() === normalizedEmail);
        if (demoUser) {
          demoUser.password = password;
        }

        // Clean up reset session token
        sessionStorage.removeItem("maintai_pwd_reset");
      }

      setSuccess(true);
      toast({
        title: "Password Updated Successfully",
        description: `New password is now active for ${normalizedEmail}`,
      });
    } catch (err) {
      toast({
        title: "Failed to update password",
        description: err instanceof Error ? err.message : "An unexpected error occurred.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleNavigateToLogin = () => {
    router.push(
      `/login?email=${encodeURIComponent(email)}&prefill_pwd=${encodeURIComponent(password)}&reset_success=1`
    );
  };

  return (
    <div className="flex min-h-screen items-center justify-center industrial-gradient p-4">
      <Card className="w-full max-w-lg border-border/50 shadow-2xl">
        <CardHeader className="text-center pb-4">
          <div className="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-2xl bg-primary font-bold text-primary-foreground shadow-lg shadow-primary/20">
            <ShieldCheck className="h-6 w-6" />
          </div>
          <CardTitle className="text-2xl font-bold">
            {success ? "Password Updated" : "Set New Password"}
          </CardTitle>
          <CardDescription>
            {success
              ? "Your new credentials are saved and ready to use"
              : `Create a strong, secure password for ${email || "your account"}`}
          </CardDescription>

          {email && !success && (
            <div className="mt-2 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs text-primary font-medium mx-auto">
              <span>Account:</span>
              <strong className="text-foreground">{email}</strong>
            </div>
          )}
        </CardHeader>

        <CardContent className="space-y-6">
          {!success ? (
            <form onSubmit={handleResetPassword} className="space-y-5">
              {/* New Password */}
              <div className="space-y-2">
                <Label htmlFor="new-password">New Password</Label>
                <div className="relative">
                  <Input
                    id="new-password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter new password"
                    className="pr-10"
                    required
                    autoFocus
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    tabIndex={-1}
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              {/* Password Strength Indicator */}
              {password && (
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">Strength:</span>
                    <span className={`font-semibold ${strengthLabel.text}`}>{strengthLabel.label}</span>
                  </div>
                  <Progress value={strengthScore} className="h-1.5" />
                </div>
              )}

              {/* Confirm New Password */}
              <div className="space-y-2">
                <Label htmlFor="confirm-password">Confirm New Password</Label>
                <div className="relative">
                  <Input
                    id="confirm-password"
                    type={showConfirmPassword ? "text" : "password"}
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter new password"
                    className="pr-10"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                    tabIndex={-1}
                  >
                    {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              {/* Validation Checklist */}
              <div className="rounded-xl border border-border/60 bg-card/60 p-3.5 space-y-2 text-xs">
                <p className="font-semibold text-muted-foreground uppercase tracking-wider text-[11px]">
                  Password Requirements
                </p>
                <div className="grid grid-cols-2 gap-2">
                  <div className={`flex items-center gap-1.5 ${checks.hasMinLength ? "text-emerald-400" : "text-muted-foreground"}`}>
                    <CheckCircle2 className={`h-3.5 w-3.5 ${checks.hasMinLength ? "text-emerald-400" : "opacity-30"}`} />
                    <span>6+ characters</span>
                  </div>
                  <div className={`flex items-center gap-1.5 ${checks.hasNumber ? "text-emerald-400" : "text-muted-foreground"}`}>
                    <CheckCircle2 className={`h-3.5 w-3.5 ${checks.hasNumber ? "text-emerald-400" : "opacity-30"}`} />
                    <span>At least 1 number</span>
                  </div>
                  <div className={`flex items-center gap-1.5 ${checks.hasLetter ? "text-emerald-400" : "text-muted-foreground"}`}>
                    <CheckCircle2 className={`h-3.5 w-3.5 ${checks.hasLetter ? "text-emerald-400" : "opacity-30"}`} />
                    <span>Contains letters</span>
                  </div>
                  <div className={`flex items-center gap-1.5 ${checks.isMatched ? "text-emerald-400" : "text-muted-foreground"}`}>
                    <CheckCircle2 className={`h-3.5 w-3.5 ${checks.isMatched ? "text-emerald-400" : "opacity-30"}`} />
                    <span>Passwords match</span>
                  </div>
                </div>
              </div>

              <Button
                type="submit"
                className="w-full gap-2 font-semibold shadow-md shadow-primary/20"
                disabled={loading || !checks.hasMinLength || !checks.isMatched}
              >
                {loading ? "Updating Password..." : "Save New Password"}
                <ArrowRight className="h-4 w-4" />
              </Button>
            </form>
          ) : (
            /* Success confirmation screen */
            <div className="space-y-5 text-center">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
                <CheckCircle2 className="h-8 w-8" />
              </div>

              <div className="space-y-1">
                <h3 className="text-lg font-bold text-foreground">Password Changed Successfully</h3>
                <p className="text-xs text-muted-foreground">
                  Your new password is now active for <strong className="text-foreground">{email}</strong>.
                </p>
              </div>

              <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-3.5 text-xs text-emerald-400 text-left flex items-start gap-2.5">
                <Sparkles className="h-4 w-4 shrink-0 mt-0.5 text-emerald-300" />
                <div>
                  <p className="font-semibold text-emerald-300">Ready to Sign In</p>
                  <p className="text-emerald-400/90 mt-0.5">
                    Click below to return to the sign-in page with your updated credentials automatically loaded.
                  </p>
                </div>
              </div>

              <Button
                type="button"
                className="w-full gap-2 font-semibold shadow-md shadow-primary/20"
                onClick={handleNavigateToLogin}
              >
                Sign In with New Password <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          )}

          <div className="pt-2 text-center border-t border-border/50">
            <Link
              href="/login"
              className="text-xs text-muted-foreground hover:text-foreground transition-colors"
            >
              Cancel and return to Sign In
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function ResetPasswordPage() {
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
      <ResetPasswordContent />
    </Suspense>
  );
}
