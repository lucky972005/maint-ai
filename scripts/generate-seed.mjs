/**
 * Generate seed.sql from demo data.
 * Run: node scripts/generate-seed.mjs > supabase/seed.sql
 */
import { writeFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));

// Dynamic import demo data - we'll inline minimal seed for SQL
const factoryId = "f0000000-0000-4000-8000-000000000001";

const machines = [
  ["m00000001-0000-4000-8000-000000000001", "MACHINE:haas-vf-2-001", "CNC Machine", "CNC", "Haas VF-2", "Haas Automation"],
  ["m00000002-0000-4000-8000-000000000002", "MACHINE:grundfos-cr-15-001", "Water Pump", "Pump", "Grundfos CR-15", "Grundfos"],
  ["m00000003-0000-4000-8000-000000000003", "MACHINE:atlas-ga-37-001", "Air Compressor", "Compressor", "Atlas Copco GA-37", "Atlas Copco"],
  ["m00000004-0000-4000-8000-000000000004", "MACHINE:siemens-1le0102-001", "Electric Motor", "Motor", "Siemens 1LE0102", "Siemens"],
  ["m00000005-0000-4000-8000-000000000005", "MACHINE:cummins-c110d5-001", "Diesel Generator", "Generator", "Cummins C110D5", "Cummins"],
];

let sql = `-- MaintAI Seed Data
-- Create demo users via Supabase Auth first, then link profiles

INSERT INTO factories (id, name, location) VALUES
  ('${factoryId}', 'Apex Manufacturing Plant', 'Pune, Maharashtra, India')
ON CONFLICT (id) DO NOTHING;

-- Demo users (create in Supabase Auth with emails below, password: demo123456)
-- admin@demo.com, supervisor@demo.com, tech1@demo.com, tech2@demo.com, tech3@demo.com

`;

machines.forEach(([id, qr, name, cat, model, mfr]) => {
  sql += `INSERT INTO machines (id, qr_code, name, category, model, manufacturer, factory_id, location, status) VALUES
  ('${id}', '${qr}', '${name}', '${cat}', '${model}', '${mfr}', '${factoryId}', 'Bay A - Floor 1', 'operational')
ON CONFLICT (id) DO NOTHING;\n\n`;
});

sql += `-- Full demo dataset (20 machines, 120 procedures, 55 logs, 30 parts) ships in lib/demo-data.ts for offline demo mode.
-- Run the app without Supabase configured to use complete in-memory demo data.
`;

const outPath = join(__dirname, "..", "supabase", "seed.sql");
writeFileSync(outPath, sql);
console.log(`Wrote ${outPath}`);
