import { createClient } from "@/lib/supabase/server";
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  const next = searchParams.get("next") ?? "/reset-password";

  if (code) {
    try {
      const supabase = await createClient();
      const { error } = await supabase.auth.exchangeCodeForSession(code);
      if (!error) {
        return NextResponse.redirect(`${origin}${next}`);
      }
      console.warn("Supabase auth code exchange error:", error.message);
    } catch (e) {
      console.error("Auth callback exception:", e);
    }
  }

  // Redirect to reset-password or requested route
  return NextResponse.redirect(`${origin}${next}`);
}
