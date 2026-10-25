import { NextResponse } from "next/server";
import { createClient as createServerClient } from "@supabase/supabase-js";
import { DEMO_USERS } from "@/lib/demo-data";

export const dynamic = "force-dynamic";

export async function POST(req: Request) {
  try {
    const { email } = await req.json();
    const trimmedEmail = email?.trim().toLowerCase();

    if (!trimmedEmail) {
      return NextResponse.json(
        { error: "Email address is required." },
        { status: 400 }
      );
    }

    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

    const isConfigured = Boolean(
      supabaseUrl &&
        anonKey &&
        !supabaseUrl.includes("placeholder") &&
        !supabaseUrl.includes("your-")
    );

    let supabaseStatus: "connected" | "offline" | "unconfigured" = "unconfigured";
    let supabaseDetail = "";
    let emailSentViaSupabase = false;
    let existsInSupabase = false;
    let officialActionLink: string | null = null;
    let officialEmailOtp: string | null = null;
    let rateLimitNotice: string | null = null;

    const origin = req.headers.get("origin") || req.headers.get("referer") || "http://localhost:3000";
    const redirectUrl = `${origin}/reset-password`;

    // 1. Health check Supabase
    if (isConfigured && supabaseUrl) {
      try {
        const pingController = new AbortController();
        const pingTimeout = setTimeout(() => pingController.abort(), 3500);

        const pingRes = await fetch(`${supabaseUrl}/auth/v1/health`, {
          method: "GET",
          headers: { apikey: anonKey! },
          signal: pingController.signal,
        });
        clearTimeout(pingTimeout);

        if (pingRes.ok) {
          supabaseStatus = "connected";
        } else {
          supabaseStatus = "offline";
          supabaseDetail = `Supabase returned HTTP ${pingRes.status}`;
        }
      } catch (pingErr) {
        supabaseStatus = "offline";
        supabaseDetail = (pingErr as Error).message;
      }
    }

    // 2. If Supabase is connected, check user and generate official link
    if (supabaseStatus === "connected" && supabaseUrl && (serviceKey || anonKey)) {
      const adminClient = serviceKey
        ? createServerClient(supabaseUrl, serviceKey, {
            auth: { autoRefreshToken: false, persistSession: false },
          })
        : null;

      const publicClient = createServerClient(supabaseUrl, anonKey!);

      // Check if user exists in Supabase and generate official recovery link
      if (adminClient) {
        try {
          const { data, error } = await adminClient.auth.admin.generateLink({
            type: "recovery",
            email: trimmedEmail,
            options: { redirectTo: redirectUrl },
          });

          if (!error && data?.properties?.action_link) {
            existsInSupabase = true;
            officialActionLink = data.properties.action_link;
            officialEmailOtp = data.properties.email_otp ?? null;
          } else if (error && error.message.includes("User with this email not found")) {
            existsInSupabase = false;
          }
        } catch (adminErr) {
          console.warn("Supabase admin generateLink notice:", adminErr);
        }
      }

      // If user exists in Supabase, attempt actual email dispatch
      if (existsInSupabase) {
        try {
          const { error } = await publicClient.auth.resetPasswordForEmail(trimmedEmail, {
            redirectTo: redirectUrl,
          });

          if (error) {
            if (error.status === 429 || error.message.toLowerCase().includes("rate limit") || error.message.toLowerCase().includes("after")) {
              rateLimitNotice = error.message;
            } else {
              supabaseDetail = error.message;
            }
          } else {
            emailSentViaSupabase = true;
          }
        } catch (publicErr) {
          console.warn("Public client recover error:", publicErr);
        }
      }
    }

    // Check if email matches demo accounts
    const isDemoUser = DEMO_USERS.some((u) => u.email.toLowerCase() === trimmedEmail);

    // If neither in Supabase nor in demo accounts
    if (supabaseStatus === "connected" && !existsInSupabase && !isDemoUser) {
      return NextResponse.json(
        {
          success: false,
          notFound: true,
          error: `No registered account found for "${trimmedEmail}" in Supabase. Please check the spelling or create an account first.`,
        },
        { status: 404 }
      );
    }

    // Fallback OTP code for demo users or backup
    const fallbackOtp = officialEmailOtp || Math.floor(100000 + Math.random() * 900000).toString();

    return NextResponse.json({
      success: true,
      email: trimmedEmail,
      existsInSupabase,
      isDemoUser,
      emailSentViaSupabase,
      rateLimitNotice,
      officialActionLink,
      officialEmailOtp,
      supabaseStatus,
      supabaseDetail,
      supabaseUrl: supabaseUrl ? supabaseUrl.replace("https://", "") : null,
      otpCode: fallbackOtp,
      message: emailSentViaSupabase
        ? `Recovery email sent to ${trimmedEmail} via Supabase!`
        : rateLimitNotice
        ? `Supabase rate limit: ${rateLimitNotice}. Your official link is ready below.`
        : `Recovery access prepared for ${trimmedEmail}.`,
    });
  } catch (error) {
    console.error("Auth recover error:", error);
    return NextResponse.json(
      { error: (error as Error).message || "Internal server error" },
      { status: 500 }
    );
  }
}

export async function GET() {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  const isConfigured = Boolean(
    supabaseUrl &&
      anonKey &&
      !supabaseUrl.includes("placeholder") &&
      !supabaseUrl.includes("your-")
  );

  let status: "connected" | "offline" | "unconfigured" = "unconfigured";
  let detail = "";

  if (isConfigured && supabaseUrl) {
    try {
      const pingController = new AbortController();
      const pingTimeout = setTimeout(() => pingController.abort(), 3500);

      const res = await fetch(`${supabaseUrl}/auth/v1/health`, {
        method: "GET",
        headers: { apikey: anonKey! },
        signal: pingController.signal,
      });
      clearTimeout(pingTimeout);

      if (res.ok) {
        status = "connected";
        detail = "Supabase Auth service is active and responsive.";
      } else {
        status = "offline";
        detail = `Supabase returned HTTP ${res.status}`;
      }
    } catch (err) {
      status = "offline";
      detail = (err as Error).message;
    }
  }

  return NextResponse.json({
    isConfigured,
    status,
    detail,
    supabaseUrl: supabaseUrl ? supabaseUrl.replace("https://", "") : null,
  });
}
