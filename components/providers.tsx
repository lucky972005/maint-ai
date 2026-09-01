"use client";

import { createContext, useContext, useEffect, useRef, useState, type ReactNode } from "react";
import type { Profile } from "@/lib/types";
import { DEMO_DATA, isSupabaseConfigured } from "@/lib/demo-data";
import { startDemoSession } from "@/lib/demo-session";
import { hydrateOfflineCache, isOnline, processSyncQueue, type SyncQueueItem } from "@/lib/offline";
import { toast } from "@/hooks/use-toast";
import { createClient } from "@/lib/supabase/client";

interface AppContextValue {
  profile: Profile | null;
  setProfile: (p: Profile | null) => void;
  online: boolean;
  demoMode: boolean;
  enterDemoMode: () => void;
}

const AppContext = createContext<AppContextValue>({
  profile: null,
  setProfile: () => {},
  online: true,
  demoMode: true,
  enterDemoMode: () => {},
});

export function useApp() {
  return useContext(AppContext);
}

function isDemoSessionActive(): boolean {
  if (!isSupabaseConfigured()) return true;
  if (typeof document === "undefined") return false;
  return document.cookie.split(";").some((c) => c.trim() === "maintai_demo=1");
}

export function Providers({ children }: { children: ReactNode }) {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [online, setOnline] = useState(true);
  const [demoMode, setDemoMode] = useState(() => isDemoSessionActive());
  const syncRunning = useRef(false);
  const supabase = createClient();

  const enterDemoMode = () => {
    const demoProfile = startDemoSession();
    setDemoMode(true);
    setProfile(demoProfile);
    hydrateOfflineCache(DEMO_DATA.machines, DEMO_DATA.procedures).catch(console.error);
  };

  useEffect(() => {
    setOnline(isOnline());
    const onOnline = () => setOnline(true);
    const onOffline = () => setOnline(false);
    window.addEventListener("online", onOnline);
    window.addEventListener("offline", onOffline);
    return () => {
      window.removeEventListener("online", onOnline);
      window.removeEventListener("offline", onOffline);
    };
  }, []);

  useEffect(() => {
    const loadProfile = async () => {
      if (demoMode) {
        const stored = localStorage.getItem("demo_profile");
        if (stored) {
          setProfile(JSON.parse(stored));
        }
        hydrateOfflineCache(DEMO_DATA.machines, DEMO_DATA.procedures).catch(console.error);
        return;
      }

      // Only restore session if user checked "remember me"
      const rememberMe = localStorage.getItem("maintai_remember_me") === "true";
      if (!rememberMe) {
        // Clear any existing session if remember me was not checked
        await supabase.auth.signOut();
        return;
      }

      try {
        const { data: { session } } = await supabase.auth.getSession();
        if (session) {
          const { data: userProfile } = await supabase
            .from("profiles")
            .select("*")
            .eq("id", session.user.id)
            .single();
          if (userProfile) {
            setProfile(userProfile);
          }
        }
      } catch (error) {
        console.error("Failed to load profile:", error);
      }
    };

    loadProfile();
  }, [demoMode, supabase]);

  useEffect(() => {
    if (demoMode) return;

    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      if (!session) {
        setProfile(null);
        return;
      }

      try {
        const { data: userProfile } = await supabase
          .from("profiles")
          .select("*")
          .eq("id", session.user.id)
          .single();
        
        if (userProfile) {
          setProfile(userProfile);
        } else {
          setProfile({
            id: session.user.id,
            full_name: session.user.user_metadata.full_name || session.user.email?.split("@")[0] || "Technician",
            email: session.user.email || "",
            role: session.user.user_metadata.role || "technician",
            factory_id: "f0000000-0000-4000-8000-000000000001",
            avatar_url: null,
          });
        }
      } catch (error) {
        console.error("Auth state change error:", error);
      }
    });

    return () => subscription.unsubscribe();
  }, [demoMode, supabase]);

  useEffect(() => {
    const syncQueuedChanges = async () => {
      if (syncRunning.current) return;
      if (!online) return;
      syncRunning.current = true;

      try {
        const synced = await processSyncQueue(async (item: SyncQueueItem) => {
          if (item.type === "fault_report") {
            const response = await fetch("/api/fault-report", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(item.payload),
            });
            return response.ok;
          }

          if (item.type === "maintenance_log") {
            const response = await fetch("/api/maintenance-log", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(item.payload),
            });
            return response.ok;
          }

          if (item.type === "evidence") {
            const response = await fetch("/api/upload-evidence", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(item.payload),
            });
            return response.ok;
          }

          return false;
        });

        if (synced > 0) {
          toast({ title: "Offline changes synced", description: `${synced} queued item${synced === 1 ? "" : "s"} uploaded.` });
        }
      } finally {
        syncRunning.current = false;
      }
    };

    syncQueuedChanges().catch(() => {});
  }, [online]);

  return (
    <AppContext.Provider value={{ profile, setProfile, online, demoMode, enterDemoMode }}>
      {children}
    </AppContext.Provider>
  );
}
