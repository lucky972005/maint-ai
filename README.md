# MaintAI — Industrial Maintenance Assistant

AI-powered Progressive Web App for industrial maintenance teams. Scan QR codes, identify machines with AI vision, follow AR-guided repair steps with voice control, and manage spare parts — all offline-capable.

## Quick Start (Demo Mode)

Works immediately without any API keys:

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) and click **Try Demo**.

## Production Setup Guide

This guide will help you set up the full production version with real database, real industrial data, and AI integration.

### Step 1: Set Up Supabase Database

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com) and sign up
   - Create a new project (free tier is sufficient)
   - Wait for the project to be provisioned (2-3 minutes)

2. **Get Your Credentials**
   - Go to Project Settings → API
   - Copy:
     - Project URL (NEXT_PUBLIC_SUPABASE_URL)
     - anon public key (NEXT_PUBLIC_SUPABASE_ANON_KEY)
     - service_role key (SUPABASE_SERVICE_ROLE_KEY) - keep this secret!

3. **Run Database Migration**
   - Go to SQL Editor in Supabase dashboard
   - Copy and run the contents of `supabase/migrations/0001_init.sql`
   - This creates all tables, indexes, and Row Level Security policies

4. **Seed Real Industrial Data**
   - In SQL Editor, run `supabase/seed.sql`
   - This loads:
     - 3 factory locations
     - 20 real industrial machines with specifications
     - 35 real parts with inventory
     - 6 detailed repair procedures
     - Preventive maintenance schedules

5. **Create Demo Users**
   - Go to Authentication → Users
   - Create these users (password: demo123456):
     - admin@demo.com (Admin role)
     - supervisor@demo.com (Supervisor role)
     - tech1@demo.com (Technician role)
     - tech2@demo.com (Technician role)
     - tech3@demo.com (Technician role)

6. **Link Users to Profiles**
   - After creating users, run this in SQL Editor:
   ```sql
   INSERT INTO profiles (id, full_name, email, role, factory_id)
   SELECT 
     id,
     CASE email 
       WHEN 'admin@demo.com' THEN 'System Admin'
       WHEN 'supervisor@demo.com' THEN 'Supervisor Patel'
       WHEN 'tech1@demo.com' THEN 'Raj Kumar'
       WHEN 'tech2@demo.com' THEN 'Priya Singh'
       WHEN 'tech3@demo.com' THEN 'Ahmed Hassan'
     END,
     email,
     CASE email 
       WHEN 'admin@demo.com' THEN 'admin'
       WHEN 'supervisor@demo.com' THEN 'supervisor'
       ELSE 'technician'
     END,
     'f0000000-0000-4000-8000-000000000001'
   FROM auth.users
   WHERE email IN ('admin@demo.com', 'supervisor@demo.com', 'tech1@demo.com', 'tech2@demo.com', 'tech3@demo.com')
   ON CONFLICT (id) DO NOTHING;
   ```

### Step 2: Configure Environment Variables

1. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```

2. Fill in your values:
   ```env
   # Supabase
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

   # AI Provider (choose one)
   # Option 1: Gemini (Free tier available)
   GEMINI_API_KEY=your-gemini-api-key
   GEMINI_MODEL=gemini-1.5-flash
   AI_PROVIDER=gemini

   # Option 2: OpenAI (Paid)
   # OPENAI_API_KEY=sk-your-openai-key
   # OPENAI_MODEL=gpt-4o
   # AI_PROVIDER=openai

   # Option 3: Auto (tries OpenAI first, then Gemini)
   # AI_PROVIDER=auto
   ```

### Step 3: Set Up AI Provider

**Option A: Gemini (Recommended - Free Tier Available)**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add `GEMINI_API_KEY` to `.env.local`
4. Set `AI_PROVIDER=gemini`

**Option B: OpenAI (Paid)**
1. Go to [platform.openai.com](https://platform.openai.com/api-keys)
2. Create an API key
3. Add `OPENAI_API_KEY` to `.env.local`
4. Set `AI_PROVIDER=openai`

### Step 4: Set Up Storage Bucket (Optional)

For uploading maintenance evidence photos:

1. Go to Storage in Supabase dashboard
2. Create a new bucket: `maintenance-evidence`
3. Make it public
4. Add this policy in SQL Editor:
   ```sql
   INSERT INTO storage.buckets (id, name, public)
   VALUES ('maintenance-evidence', 'maintenance-evidence', true)
   ON CONFLICT (id) DO NOTHING;
   ```

### Step 5: Run Production Build

```bash
npm install
npm run build
npm start
```

The app will now:
- Connect to your real Supabase database
- Use real industrial machines and parts data
- Access real manufacturer manuals via URLs
- Use AI for machine identification and chat assistance
- Store all data persistently in the cloud

### Real Data Included

The seed data includes:

**20 Real Industrial Machines:**
- Haas VF-2SS CNC Vertical Machining Center
- Grundfos CR15-5 Centrifugal Pump
- Atlas Copco GA 37+ Rotary Screw Compressor
- Siemens 1LE0102 Three-Phase Induction Motor
- Cummins C110D5 Diesel Generator Set
- And 15 more with complete specifications

**35 Real Industrial Parts:**
- V-Belts, Bearings, Seals, Filters
- Electrical components (Fuses, Contactors, Relays)
- Hydraulic components
- With real part numbers and pricing

**6 Detailed Repair Procedures:**
- Oil Change (8 steps with AR markers)
- Belt Replacement (9 steps)
- Bearing Replacement (11 steps)
- Motor Inspection (8 steps)
- Electrical Wiring Check (9 steps)
- Emergency Shutdown (8 steps)

**Real Manufacturer Manual URLs:**
- Direct links to manufacturer documentation
- Haas, Grundfos, Atlas Copco, Siemens, Cummins, etc.

### Demo Login Accounts

| Email | Role | Password |
|-------|------|----------|
| admin@demo.com | Admin | demo123456 |
| supervisor@demo.com | Supervisor | demo123456 |
| tech1@demo.com | Technician | demo123456 |
| tech2@demo.com | Technician | demo123456 |
| tech3@demo.com | Technician | demo123456 |

One-click login buttons are available on the login page.

## Features

- **QR Scanner** — Scan machine QR codes (`MACHINE:haas-vf-2-001`) to jump to repair flow
- **AI Machine ID** — Camera-based identification with confidence scores
- **AR Repair Guide** — Canvas overlays with animated markers on live camera feed
- **Voice Control** — Hands-free step navigation (Next, Previous, Repeat, Safety, Help)
- **Tool Verification** — AI vision confirms correct tool before advancing
- **FixBot Chat** — Context-aware AI mechanic assistant
- **Work Order & Inspection Certificate** — 1-Tap enterprise ISO-9001 compliance certificate with canvas digital signature pad, audit QR stamp, and printable PDF export
- **Manager Dashboard** — KPIs, charts, technician leaderboard
- **Offline PWA** — IndexedDB caching + service worker (production builds)

## Production Setup

1. Configure Supabase and one AI provider as described above.
2. Build and deploy:

```bash
npm run build
npm start
```

## Install as PWA

On Android Chrome or desktop Chrome/Edge, use **Install App** from the landing page banner or browser menu. The app launches standalone at `/scan`.

## Tech Stack

- Next.js 14 (App Router) + TypeScript
- TailwindCSS + shadcn/ui (industrial dark theme, `#F97316` accent)
- Supabase (Auth, Postgres, Storage)
- OpenAI GPT-4o Vision or Gemini 1.5 Flash (optional, Gemini has a free tier)
- Dexie.js (IndexedDB), html5-qrcode, Recharts, next-pwa

## Project Structure

```
app/
  (public)/     Landing, login, signup
  (app)/        Scanner, repair, history, parts, chat, dashboard
  api/          AI vision, chat, upload, predictive maintenance
components/     Scanner, repair, dashboard, chat UI
lib/            Supabase, OpenAI, offline, voice, demo data
supabase/       SQL migrations + seed
```

## Notes

- Demo mode uses `lib/demo-data.ts` with 20 machines, 120 procedures, 55 maintenance logs, and 30 parts
- Free AI option: Gemini API free tier is the simplest no-cost path for the semester project
- Camera features require HTTPS or localhost
- Voice control requires browser Speech API support (Chrome recommended)
