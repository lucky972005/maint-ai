import type { Profile } from "./types";
import { DEMO_USERS } from "./demo-data";

export const DEMO_COOKIE = "maintai_demo";

export function getDemoUserByEmail(email: string): Profile | undefined {
  const user = DEMO_USERS.find((u) => u.email.toLowerCase() === email.trim().toLowerCase());
  if (!user) return undefined;
  const { password: _password, ...profile } = user;
  void _password;
  return profile;
}

export function getDemoUserByRole(role: "admin" | "technician" | "supervisor"): Profile | undefined {
  const user = DEMO_USERS.find((u) => u.role === role);
  if (!user) return undefined;
  const { password: _password, ...profile } = user;
  void _password;
  return profile;
}

export function getDefaultDemoProfile(): Profile {
  const user = DEMO_USERS.find((u) => u.role === "technician") ?? DEMO_USERS[0];
  const { password: _password, ...profile } = user;
  void _password;
  return profile;
}

export function startDemoSession(profile?: Profile): Profile {
  const demoProfile = profile ?? getDefaultDemoProfile();
  if (typeof window !== "undefined") {
    localStorage.setItem("demo_profile", JSON.stringify(demoProfile));
    document.cookie = `${DEMO_COOKIE}=1; path=/; max-age=${60 * 60 * 24 * 7}; SameSite=Lax`;
  }
  return demoProfile;
}

export function clearDemoSession(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem("demo_profile");
    document.cookie = `${DEMO_COOKIE}=; path=/; max-age=0; SameSite=Lax`;
  }
}

export function isDemoCookieSet(cookieHeader: string | null): boolean {
  if (!cookieHeader) return false;
  return cookieHeader.split(";").some((c) => c.trim().startsWith(`${DEMO_COOKIE}=1`));
}
