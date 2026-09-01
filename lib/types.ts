export type UserRole = "technician" | "supervisor" | "admin";
export type MachineStatus = "operational" | "maintenance" | "broken";
export type ProcedureDifficulty = "easy" | "medium" | "hard";
export type LogStatus = "in_progress" | "completed" | "abandoned";
export type FaultSeverity = "low" | "medium" | "high" | "critical";
export type FaultStatus = "open" | "assigned" | "in_progress" | "resolved";

export interface ArMarker {
  x: number;
  y: number;
  w: number;
  h: number;
  label: string;
  color: "red" | "green" | "blue";
}

export interface RepairStep {
  step: number;
  instruction: string;
  tool_needed: string;
  safety: string;
  ar_marker: ArMarker;
  requires_tool_verification?: boolean;
  is_dangerous?: boolean;
}

export interface Factory {
  id: string;
  name: string;
  location: string | null;
  created_at?: string;
}

export interface Profile {
  id: string;
  full_name: string;
  email: string;
  role: UserRole;
  factory_id: string | null;
  avatar_url: string | null;
  created_at?: string;
}

export interface Machine {
  id: string;
  qr_code: string;
  name: string;
  category: string;
  model: string | null;
  manufacturer: string | null;
  serial_number: string | null;
  location: string | null;
  factory_id: string | null;
  installed_date: string | null;
  image_url: string | null;
  images: string[] | null;
  thumbnail_url: string | null;
  primary_image_index: number | null;
  manual_url: string | null;
  specs: Record<string, unknown> | null;
  status: MachineStatus;
  created_at?: string;
}

export interface RepairProcedure {
  id: string;
  machine_id: string;
  procedure_type: string;
  estimated_minutes: number | null;
  difficulty: ProcedureDifficulty | null;
  steps: RepairStep[];
  required_tools: string[];
  safety_warnings: string[];
  created_at?: string;
}

export interface MaintenanceLog {
  id: string;
  machine_id: string;
  technician_id: string | null;
  procedure_id: string | null;
  started_at: string;
  completed_at: string | null;
  duration_minutes: number | null;
  status: LogStatus | null;
  notes: string | null;
  created_at?: string;
  machine?: Machine;
  procedure?: RepairProcedure;
  technician?: Profile;
}

export interface Part {
  id: string;
  name: string;
  part_number: string;
  category: string | null;
  stock_quantity: number;
  min_stock_level: number;
  unit_price: number | null;
  image_url: string | null;
  images: string[] | null;
  thumbnail_url: string | null;
  primary_image_index: number | null;
  compatible_machines: string[] | null;
  supplier?: string;
  lead_time_days?: number;
  description?: string;
}

export interface FaultReport {
  id: string;
  machine_id: string | null;
  reported_by: string | null;
  assigned_to: string | null;
  description: string;
  severity: FaultSeverity | null;
  ai_diagnosis: string | null;
  ai_detection_results: Record<string, unknown> | null;
  status: FaultStatus | null;
  attachments: string[] | null;
  assigned_at: string | null;
  due_date: string | null;
  created_at?: string;
  machine?: Machine;
  assigned_to_profile?: Profile;
}

export const PROCEDURE_TYPES = [
  "Oil Change",
  "Belt Replacement",
  "Bearing Replacement",
  "Motor Inspection",
  "Electrical Wiring Check",
  "Emergency Shutdown",
] as const;

export const TOOLS = [
  "screwdriver",
  "wrench",
  "pliers",
  "hammer",
  "drill",
  "allen_key",
  "multimeter",
  "socket_set",
] as const;

export type ToolName = (typeof TOOLS)[number];
