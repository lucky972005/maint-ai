-- Industrial Maintenance Assistant Schema
-- Run in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS factories (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  location text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name text NOT NULL,
  email text NOT NULL UNIQUE,
  role text NOT NULL CHECK (role IN ('technician','supervisor','admin')),
  factory_id uuid REFERENCES factories(id),
  avatar_url text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS machines (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  qr_code text UNIQUE NOT NULL,
  name text NOT NULL,
  category text NOT NULL,
  model text,
  manufacturer text,
  serial_number text,
  location text,
  factory_id uuid REFERENCES factories(id),
  installed_date date,
  image_url text,
  manual_url text,
  specs jsonb,
  status text DEFAULT 'operational' CHECK (status IN ('operational','maintenance','broken')),
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS repair_procedures (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  machine_id uuid REFERENCES machines(id) ON DELETE CASCADE,
  procedure_type text NOT NULL,
  estimated_minutes int,
  difficulty text CHECK (difficulty IN ('easy','medium','hard')),
  steps jsonb NOT NULL,
  required_tools text[],
  safety_warnings text[],
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS maintenance_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  machine_id uuid REFERENCES machines(id),
  technician_id uuid REFERENCES profiles(id),
  procedure_id uuid REFERENCES repair_procedures(id),
  started_at timestamptz NOT NULL,
  completed_at timestamptz,
  duration_minutes int,
  status text CHECK (status IN ('in_progress','completed','abandoned')),
  notes text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS maintenance_evidence (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  log_id uuid REFERENCES maintenance_logs(id) ON DELETE CASCADE,
  type text CHECK (type IN ('before','after','video','voice_note')),
  file_url text NOT NULL,
  uploaded_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS parts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  part_number text UNIQUE,
  category text,
  stock_quantity int DEFAULT 0,
  min_stock_level int DEFAULT 5,
  unit_price decimal(10,2),
  image_url text,
  compatible_machines text[]
);

CREATE TABLE IF NOT EXISTS parts_used (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  log_id uuid REFERENCES maintenance_logs(id),
  part_id uuid REFERENCES parts(id),
  quantity int NOT NULL,
  used_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fault_reports (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  machine_id uuid REFERENCES machines(id),
  reported_by uuid REFERENCES profiles(id),
  assigned_to uuid REFERENCES profiles(id),
  description text NOT NULL,
  severity text CHECK (severity IN ('low','medium','high','critical')),
  ai_diagnosis text,
  status text DEFAULT 'open' CHECK (status IN ('open','assigned','in_progress','resolved')),
  attachments text[],
  assigned_at timestamptz,
  due_date timestamptz,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS preventive_schedules (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  machine_id uuid REFERENCES machines(id),
  procedure_id uuid REFERENCES repair_procedures(id),
  next_due_date date NOT NULL,
  frequency_days int,
  notified boolean DEFAULT false
);

-- Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE machines ENABLE ROW LEVEL SECURITY;
ALTER TABLE maintenance_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE fault_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE parts ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users see own factory machines" ON machines;
CREATE POLICY "Users see own factory machines" ON machines
  FOR SELECT USING (
    factory_id IN (SELECT factory_id FROM profiles WHERE id = auth.uid())
    OR EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
  );

DROP POLICY IF EXISTS "Users see own profile" ON profiles;
CREATE POLICY "Users see own profile" ON profiles
  FOR SELECT USING (id = auth.uid() OR EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role IN ('admin','supervisor')));

DROP POLICY IF EXISTS "Technicians manage own logs" ON maintenance_logs;
CREATE POLICY "Technicians manage own logs" ON maintenance_logs
  FOR ALL USING (
    technician_id = auth.uid()
    OR EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role IN ('admin','supervisor'))
  );

DROP POLICY IF EXISTS "Factory fault reports" ON fault_reports;
CREATE POLICY "Factory fault reports" ON fault_reports
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM machines m
      JOIN profiles p ON p.factory_id = m.factory_id
      WHERE m.id = fault_reports.machine_id AND p.id = auth.uid()
    )
    OR EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
  );

DROP POLICY IF EXISTS "All users read parts" ON parts;
CREATE POLICY "All users read parts" ON parts FOR SELECT USING (true);

-- Storage bucket (run separately in Supabase dashboard or via API)
-- INSERT INTO storage.buckets (id, name, public) VALUES ('maintenance-evidence', 'maintenance-evidence', true);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_machines_qr ON machines(qr_code);
CREATE INDEX IF NOT EXISTS idx_machines_factory ON machines(factory_id);
CREATE INDEX IF NOT EXISTS idx_logs_machine ON maintenance_logs(machine_id);
CREATE INDEX IF NOT EXISTS idx_logs_technician ON maintenance_logs(technician_id);
CREATE INDEX IF NOT EXISTS idx_procedures_machine ON repair_procedures(machine_id);
