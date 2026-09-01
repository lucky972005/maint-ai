import { type NextRequest, NextResponse } from "next/server";
import { DEMO_COOKIE } from "@/lib/demo-session";
import { createClient } from "@/lib/supabase/server";

const PROTECTED_ROUTES = ["/scan", "/identify", "/repair", "/manuals", "/history", "/parts", "/chat", "/report", "/dashboard"];
const AUTH_ROUTES = ["/login", "/signup"];

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const supabase = await createClient();
  const { data: { session } } = await supabase.auth.getSession();
  const isAuthenticated = !!session;
  const isDemoSession = request.cookies.get(DEMO_COOKIE)?.value === "1" || request.nextUrl.searchParams.get("demo") === "1";

  if (PROTECTED_ROUTES.some((r) => pathname.startsWith(r)) && !isAuthenticated && !isDemoSession) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (AUTH_ROUTES.includes(pathname) && (isAuthenticated || isDemoSession)) {
    return NextResponse.redirect(new URL("/scan", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|icons|manifest|sw|workbox|api).*)",
  ],
};
