# Supabase Setup Guide

This guide will help you set up Supabase for the MaintAI application and populate it with demo data.

## Prerequisites

- A Supabase account (free tier works)
- Node.js installed on your machine

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Choose a name (e.g., "maintai-demo")
4. Set a strong database password
5. Select a region closest to you
6. Click "Create new project"
7. Wait for the project to be provisioned (1-2 minutes)

## Step 2: Configure Environment Variables

1. Go to your Supabase project dashboard
2. Navigate to **Settings → API**
3. Copy the following values:
   - **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
   - **anon/public key** → `NEXT_PUBLIC_SUPABASE_ANON_KEY`

4. Update your `.env.local` file:
```bash
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## Step 3: Create Database Tables

Go to the **SQL Editor** in your Supabase dashboard and run the following SQL script:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

factories table
CREATE TABLE IF NOT EXISTS factories (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  location TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Profiles table
CREATE TABLE IF NOT EXISTS profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  full_name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('technician', 'supervisor', 'admin')),
  factory_id UUID REFERENCES factories(id),
  avatar_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Machines table
CREATE TABLE IF NOT EXISTS machines (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  qr_code TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  model TEXT,
  manufacturer TEXT,
  serial_number TEXT,
  location TEXT,
  factory_id UUID REFERENCES factories(id),
  installed_date DATE,
  image_url TEXT,
  manual_url TEXT,
  specs JSONB,
  status TEXT NOT NULL CHECK (status IN ('operational', 'maintenance', 'broken')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Parts table
CREATE TABLE IF NOT EXISTS parts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  part_number TEXT UNIQUE NOT NULL,
  category TEXT,
  stock_quantity INTEGER NOT NULL DEFAULT 0,
  min_stock_level INTEGER NOT NULL DEFAULT 0,
  unit_price DECIMAL(10,2),
  image_url TEXT,
  compatible_machines UUID[]
);

-- Repair procedures table
CREATE TABLE IF NOT EXISTS repair_procedures (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  machine_id UUID REFERENCES machines(id),
  procedure_type TEXT NOT NULL,
  estimated_minutes INTEGER,
  difficulty TEXT CHECK (difficulty IN ('easy', 'medium', 'hard')),
  steps JSONB NOT NULL,
  required_tools TEXT[],
  safety_warnings TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Maintenance logs table
CREATE TABLE IF NOT EXISTS maintenance_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  machine_id UUID REFERENCES machines(id),
  technician_id UUID REFERENCES profiles(id),
  procedure_id UUID REFERENCES repair_procedures(id),
  started_at TIMESTAMP WITH TIME ZONE NOT NULL,
  completed_at TIMESTAMP WITH TIME ZONE,
  duration_minutes INTEGER,
  status TEXT CHECK (status IN ('in_progress', 'completed', 'abandoned')),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Fault reports table
CREATE TABLE IF NOT EXISTS fault_reports (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  machine_id UUID REFERENCES machines(id),
  reported_by UUID REFERENCES profiles(id),
  description TEXT NOT NULL,
  severity TEXT CHECK (severity IN ('low', 'medium', 'high', 'critical')),
  ai_diagnosis TEXT,
  status TEXT CHECK (status IN ('open', 'assigned', 'resolved')),
  attachments TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_machines_qr_code ON machines(qr_code);
CREATE INDEX IF NOT EXISTS idx_machines_factory_id ON machines(factory_id);
CREATE INDEX IF NOT EXISTS idx_procedures_machine_id ON repair_procedures(machine_id);
CREATE INDEX IF NOT EXISTS idx_logs_machine_id ON maintenance_logs(machine_id);
CREATE INDEX IF NOT EXISTS idx_logs_technician_id ON maintenance_logs(technician_id);
CREATE INDEX IF NOT EXISTS idx_faults_machine_id ON fault_reports(machine_id);
```

## Step 4: Enable Authentication

1. Go to **Authentication → Providers**
2. Enable **Email** provider
3. In **Authentication → URL Configuration**, set:
   - Site URL: `http://localhost:3000`
   - Redirect URLs: `http://localhost:3000/auth/callback`

## Step 5: Enable Storage (Optional)

For file uploads (evidence photos):

1. Go to **Storage**
2. Create a new bucket named `evidence`
3. Make it **Public**
4. Add the following policy (in **Storage → Policies**):

```sql
-- Allow authenticated users to upload
CREATE POLICY "Authenticated users can upload"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'evidence');

-- Allow public read access
CREATE POLICY "Public can read evidence"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'evidence');
```

## Step 6: Seed Demo Data

Before running the seeding script, you need to either:

**Option A: Disable RLS temporarily (easier)**
Run this in your Supabase SQL Editor:
```sql
-- Disable RLS for all tables
ALTER TABLE factories ENABLE ROW LEVEL SECURITY;
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE machines ENABLE ROW LEVEL SECURITY;
ALTER TABLE parts ENABLE ROW LEVEL SECURITY;
ALTER TABLE repair_procedures ENABLE ROW LEVEL SECURITY;
ALTER TABLE maintenance_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE fault_reports ENABLE ROW LEVEL SECURITY;

-- Allow public access for seeding
CREATE POLICY "Enable seeding" ON factories FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable seeding" ON profiles FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable seeding" ON machines FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable seeding" ON parts FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable seeding" ON repair_procedures FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable seeding" ON maintenance_logs FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable seeding" ON fault_reports FOR ALL USING (true) WITH CHECK (true);
```

**Option B: Use service role key (more secure)**
1. Go to **Settings → API** in Supabase dashboard
2. Copy the **service_role** secret key (not the anon key)
3. Add to `.env.local`:
```bash
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

Then run the seeding script:

```bash
# Install tsx if not already installed
npm install -D tsx

# Run the seeding script
npx tsx scripts/seed-supabase.ts
```

This will populate your database with:
- 1 factory
- 5 demo users (profiles)
- 20 machines
- 50+ parts
- 100+ repair procedures

## Step 7: Create Supabase Auth Users

The seeding script creates profiles in the database, but you need to create the actual auth users manually:

1. Go to **Authentication → Users**
2. Click "Add user" for each demo account:

**Demo User Credentials:**
- `admin@demo.com` / `demo123456` (Admin role)
- `supervisor@demo.com` / `demo123456` (Supervisor role)  
- `tech1@demo.com` / `demo123456` (Technician role)
- `tech2@demo.com` / `demo123456` (Technician role)
- `tech3@demo.com` / `demo123456` (Technician role)

For each user:
- Enter email and password
- Enable "Auto confirm user"
- Click "Create user"

## Step 8: Test the Application

1. Start the dev server:
```bash
npm run dev
```

2. Go to http://localhost:3000
3. Click "Login" and use any demo account
4. You should now see the live Supabase data!

## Troubleshooting

**"Missing Supabase configuration" error:**
- Make sure your `.env.local` has the correct Supabase URL and anon key
- Restart the dev server after updating `.env.local`

**"Table does not exist" error:**
- Run the SQL script from Step 3 in your Supabase SQL Editor
- Make sure all tables are created successfully

**Seeding script fails:**
- Check that your Supabase project is active
- Verify your API keys are correct
- Ensure all required tables exist

**Authentication not working:**
- Make sure Email provider is enabled
- Check redirect URLs match your local dev URL
- Try creating auth users manually as described in Step 7

## Demo Mode vs Live Mode

The app automatically detects if Supabase is configured:
- **Without Supabase**: Uses demo mode with local data
- **With Supabase**: Uses live database with real authentication

You can switch between modes by adding/removing the Supabase environment variables.
