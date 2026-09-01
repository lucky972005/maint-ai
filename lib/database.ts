import { createClient } from "./supabase/client";
import {
  DEMO_DATA,
  isSupabaseConfigured,
  getMachineById as getDemoMachineById,
  getMachineByQr as getDemoMachineByQr,
  getProceduresForMachine as getDemoProcedures,
  getProcedureById as getDemoProcedureById,
  getDashboardStats as getDemoDashboardStats,
  getFailureByCategory as getDemoFailureByCategory,
  getDowntimeTrend as getDemoDowntimeTrend,
  getTechnicianLeaderboard as getDemoTechnicianLeaderboard,
} from "./demo-data";
import type {
  Machine,
  Profile,
  RepairProcedure,
  MaintenanceLog,
  Part,
  FaultReport,
  Factory,
  FaultSeverity,
} from "./types";

const supabase = createClient();

export async function getMachines(): Promise<Machine[]> {
  if (!isSupabaseConfigured()) {
    return DEMO_DATA.machines;
  }
  try {
    const { data, error } = await supabase.from("machines").select("*");
    if (error) throw error;
    return data && data.length > 0 ? data : DEMO_DATA.machines;
  } catch (error) {
    console.warn("Supabase getMachines failed, using demo data:", error);
    return DEMO_DATA.machines;
  }
}

export async function getMachineById(id: string): Promise<Machine | null> {
  if (!isSupabaseConfigured()) {
    return getDemoMachineById(id) ?? null;
  }
  try {
    const { data, error } = await supabase.from("machines").select("*").eq("id", id).single();
    if (error) throw error;
    return data ?? getDemoMachineById(id) ?? null;
  } catch (error) {
    console.warn("Supabase getMachineById failed, using demo data:", error);
    return getDemoMachineById(id) ?? null;
  }
}

export async function getMachineByQr(qrCode: string): Promise<Machine | null> {
  if (!isSupabaseConfigured()) {
    const exact = getDemoMachineByQr(qrCode);
    if (exact) return exact;
    const fuzzy = DEMO_DATA.machines.find((m) =>
      qrCode.includes(m.qr_code.split(":")[1]?.slice(0, 8) ?? "")
    );
    return fuzzy ?? null;
  }
  try {
    const { data, error } = await supabase.from("machines").select("*").eq("qr_code", qrCode).single();
    if (error) throw error;
    return data;
  } catch {
    const exact = getDemoMachineByQr(qrCode);
    if (exact) return exact;
    return DEMO_DATA.machines.find((m) =>
      qrCode.includes(m.qr_code.split(":")[1]?.slice(0, 8) ?? "")
    ) ?? null;
  }
}

export async function getProceduresForMachine(machineId: string): Promise<RepairProcedure[]> {
  if (!isSupabaseConfigured()) {
    return getDemoProcedures(machineId);
  }
  try {
    const { data, error } = await supabase.from("repair_procedures").select("*").eq("machine_id", machineId);
    if (error) throw error;
    return data && data.length > 0 ? data : getDemoProcedures(machineId);
  } catch {
    return getDemoProcedures(machineId);
  }
}

export async function getProcedureById(id: string): Promise<RepairProcedure | null> {
  if (!isSupabaseConfigured()) {
    return getDemoProcedureById(id);
  }
  try {
    const { data, error } = await supabase.from("repair_procedures").select("*").eq("id", id).single();
    if (error) throw error;
    return data ?? getDemoProcedureById(id);
  } catch {
    return getDemoProcedureById(id);
  }
}

export async function getParts(): Promise<Part[]> {
  if (!isSupabaseConfigured()) {
    return DEMO_DATA.parts;
  }
  try {
    const { data, error } = await supabase.from("parts").select("*");
    if (error) throw error;
    return data && data.length > 0 ? data : DEMO_DATA.parts;
  } catch {
    return DEMO_DATA.parts;
  }
}

export async function getLowStockParts(): Promise<Part[]> {
  if (!isSupabaseConfigured()) {
    return DEMO_DATA.parts.filter((p) => p.stock_quantity < p.min_stock_level);
  }
  try {
    const { data, error } = await supabase.from("parts").select("*").lte("stock_quantity", "min_stock_level");
    if (error) throw error;
    return data || [];
  } catch {
    return DEMO_DATA.parts.filter((p) => p.stock_quantity < p.min_stock_level);
  }
}

export async function getMaintenanceLogs(limit = 50): Promise<MaintenanceLog[]> {
  if (!isSupabaseConfigured()) {
    return DEMO_DATA.logs.slice(0, limit);
  }
  try {
    const { data, error } = await supabase
      .from("maintenance_logs")
      .select("*")
      .order("created_at", { ascending: false })
      .limit(limit);
    if (error) throw error;
    return data && data.length > 0 ? data : DEMO_DATA.logs.slice(0, limit);
  } catch {
    return DEMO_DATA.logs.slice(0, limit);
  }
}

export async function createMaintenanceLog(
  log: Omit<MaintenanceLog, "id" | "created_at">
): Promise<MaintenanceLog> {
  if (!isSupabaseConfigured()) {
    const newLog: MaintenanceLog = {
      ...log,
      id: crypto.randomUUID(),
      created_at: new Date().toISOString(),
    };
    DEMO_DATA.logs.unshift(newLog);
    return newLog;
  }
  try {
    const { data, error } = await supabase.from("maintenance_logs").insert(log).select().single();
    if (error) throw error;
    return data;
  } catch {
    const newLog: MaintenanceLog = {
      ...log,
      id: crypto.randomUUID(),
      created_at: new Date().toISOString(),
    };
    DEMO_DATA.logs.unshift(newLog);
    return newLog;
  }
}

export async function updateMaintenanceLog(
  id: string,
  updates: Partial<Omit<MaintenanceLog, "id">>
): Promise<MaintenanceLog> {
  if (!isSupabaseConfigured()) {
    const existing = DEMO_DATA.logs.find((l) => l.id === id);
    if (existing) {
      Object.assign(existing, updates);
      return existing;
    }
    return { ...updates, id, created_at: new Date().toISOString() } as MaintenanceLog;
  }
  try {
    const { data, error } = await supabase.from("maintenance_logs").update(updates).eq("id", id).select().single();
    if (error) throw error;
    return data;
  } catch {
    const existing = DEMO_DATA.logs.find((l) => l.id === id);
    if (existing) {
      Object.assign(existing, updates);
      return existing;
    }
    return { ...updates, id, created_at: new Date().toISOString() } as MaintenanceLog;
  }
}

export async function getFaultReports(): Promise<FaultReport[]> {
  if (!isSupabaseConfigured()) {
    return DEMO_DATA.faults;
  }
  try {
    const { data, error } = await supabase
      .from("fault_reports")
      .select(`
        *,
        machine:machines(*),
        assigned_to_profile:profiles!fault_reports_assigned_to_fkey(*)
      `)
      .order("created_at", { ascending: false });
    if (error) throw error;
    return data && data.length > 0 ? data : DEMO_DATA.faults;
  } catch {
    return DEMO_DATA.faults;
  }
}

export async function createFaultReport(
  report: Omit<FaultReport, "id" | "created_at">
): Promise<FaultReport> {
  if (!isSupabaseConfigured()) {
    const newReport: FaultReport = {
      ...report,
      id: crypto.randomUUID(),
      created_at: new Date().toISOString(),
      machine: DEMO_DATA.machines.find((m) => m.id === report.machine_id),
      assigned_to_profile: DEMO_DATA.profiles.find((p) => p.id === report.assigned_to),
    };
    DEMO_DATA.faults.unshift(newReport);
    return newReport;
  }
  try {
    const { data, error } = await supabase.from("fault_reports").insert(report).select().single();
    if (error) throw error;
    return data;
  } catch {
    const newReport: FaultReport = {
      ...report,
      id: crypto.randomUUID(),
      created_at: new Date().toISOString(),
      machine: DEMO_DATA.machines.find((m) => m.id === report.machine_id),
      assigned_to_profile: DEMO_DATA.profiles.find((p) => p.id === report.assigned_to),
    };
    DEMO_DATA.faults.unshift(newReport);
    return newReport;
  }
}

export async function updateFaultReport(
  id: string,
  updates: Partial<Omit<FaultReport, "id">>
): Promise<FaultReport> {
  if (!isSupabaseConfigured()) {
    const existing = DEMO_DATA.faults.find((f) => f.id === id);
    if (existing) {
      Object.assign(existing, updates);
      return existing;
    }
    return { ...updates, id, created_at: new Date().toISOString() } as FaultReport;
  }
  try {
    const { data, error } = await supabase.from("fault_reports").update(updates).eq("id", id).select().single();
    if (error) throw error;
    return data;
  } catch {
    const existing = DEMO_DATA.faults.find((f) => f.id === id);
    if (existing) {
      Object.assign(existing, updates);
      return existing;
    }
    return { ...updates, id, created_at: new Date().toISOString() } as FaultReport;
  }
}

export async function assignFaultReport(
  faultId: string,
  technicianId: string,
  severity?: FaultSeverity
): Promise<FaultReport> {
  let faultSeverity = severity;
  if (!faultSeverity) {
    const fault = await getFaultReportById(faultId);
    faultSeverity = fault?.severity || "medium";
  }
  
  const dueDate = calculateDueDateBySeverity(faultSeverity);

  if (!isSupabaseConfigured()) {
    const fault = DEMO_DATA.faults.find((f) => f.id === faultId);
    const tech = DEMO_DATA.profiles.find((p) => p.id === technicianId);
    if (fault) {
      fault.assigned_to = technicianId;
      fault.assigned_to_profile = tech;
      fault.status = "assigned";
      fault.assigned_at = new Date().toISOString();
      fault.due_date = dueDate;
      return fault;
    }
  }

  try {
    const { data, error } = await supabase
      .from("fault_reports")
      .update({
        assigned_to: technicianId,
        status: "assigned",
        assigned_at: new Date().toISOString(),
        due_date: dueDate,
      })
      .eq("id", faultId)
      .select(`
        *,
        machine:machines(*),
        assigned_to_profile:profiles!fault_reports_assigned_to_fkey(*)
      `)
      .single();
    
    if (error) throw error;
    return data;
  } catch {
    const fault = DEMO_DATA.faults.find((f) => f.id === faultId);
    const tech = DEMO_DATA.profiles.find((p) => p.id === technicianId);
    if (fault) {
      fault.assigned_to = technicianId;
      fault.assigned_to_profile = tech;
      fault.status = "assigned";
      fault.assigned_at = new Date().toISOString();
      fault.due_date = dueDate;
      return fault;
    }
    throw new Error("Fault not found");
  }
}

export async function getFaultReportById(id: string): Promise<FaultReport | null> {
  if (!isSupabaseConfigured()) {
    return DEMO_DATA.faults.find((f) => f.id === id) ?? null;
  }
  try {
    const { data, error } = await supabase
      .from("fault_reports")
      .select("*")
      .eq("id", id)
      .single();
    if (error) throw error;
    return data;
  } catch {
    return DEMO_DATA.faults.find((f) => f.id === id) ?? null;
  }
}

export async function getFaultsForTechnician(technicianId: string): Promise<FaultReport[]> {
  if (!isSupabaseConfigured()) {
    return DEMO_DATA.faults.filter((f) => f.assigned_to === technicianId);
  }
  try {
    const { data, error } = await supabase
      .from("fault_reports")
      .select(`
        *,
        machine:machines(*),
        assigned_to_profile:profiles!fault_reports_assigned_to_fkey(*)
      `)
      .eq("assigned_to", technicianId)
      .order("created_at", { ascending: false });
    
    if (error) throw error;
    return data && data.length > 0 ? data : DEMO_DATA.faults.filter((f) => f.assigned_to === technicianId);
  } catch {
    return DEMO_DATA.faults.filter((f) => f.assigned_to === technicianId);
  }
}

export async function getUnassignedFaults(): Promise<FaultReport[]> {
  if (!isSupabaseConfigured()) {
    return DEMO_DATA.faults.filter((f) => !f.assigned_to && f.status === "open");
  }
  try {
    const { data, error } = await supabase
      .from("fault_reports")
      .select(`
        *,
        machine:machines(*),
        assigned_to_profile:profiles!fault_reports_assigned_to_fkey(*)
      `)
      .is("assigned_to", null)
      .eq("status", "open")
      .order("created_at", { ascending: false });
    
    if (error) throw error;
    return data && data.length > 0 ? data : DEMO_DATA.faults.filter((f) => !f.assigned_to && f.status === "open");
  } catch {
    return DEMO_DATA.faults.filter((f) => !f.assigned_to && f.status === "open");
  }
}

export async function updateFaultStatus(
  faultId: string,
  status: "open" | "assigned" | "in_progress" | "resolved"
): Promise<FaultReport> {
  if (!isSupabaseConfigured()) {
    const fault = DEMO_DATA.faults.find((f) => f.id === faultId);
    if (fault) {
      fault.status = status;
      return fault;
    }
  }
  try {
    const { data, error } = await supabase
      .from("fault_reports")
      .update({ status })
      .eq("id", faultId)
      .select(`
        *,
        machine:machines(*),
        assigned_to_profile:profiles!fault_reports_assigned_to_fkey(*)
      `)
      .single();
    
    if (error) throw error;
    return data;
  } catch {
    const fault = DEMO_DATA.faults.find((f) => f.id === faultId);
    if (fault) {
      fault.status = status;
      return fault;
    }
    throw new Error("Fault not found");
  }
}

export async function getTechnicians(): Promise<Profile[]> {
  if (!isSupabaseConfigured()) {
    return DEMO_DATA.profiles.filter((p) => p.role === "technician");
  }
  try {
    const { data, error } = await supabase
      .from("profiles")
      .select("*")
      .eq("role", "technician");
    
    if (error) throw error;
    return data && data.length > 0 ? data : DEMO_DATA.profiles.filter((p) => p.role === "technician");
  } catch {
    return DEMO_DATA.profiles.filter((p) => p.role === "technician");
  }
}

function calculateDueDateBySeverity(severity: FaultSeverity): string {
  const hours = {
    critical: 4,
    high: 24,
    medium: 48,
    low: 72,
  };
  
  const date = new Date();
  date.setHours(date.getHours() + hours[severity]);
  return date.toISOString();
}

export async function getFactory(): Promise<Factory | null> {
  return DEMO_DATA.factory;
}

export async function getProfiles(): Promise<Profile[]> {
  if (!isSupabaseConfigured()) {
    return DEMO_DATA.profiles;
  }
  try {
    const { data, error } = await supabase.from("profiles").select("*");
    if (error) throw error;
    return data && data.length > 0 ? data : DEMO_DATA.profiles;
  } catch {
    return DEMO_DATA.profiles;
  }
}

export async function getProfileById(id: string): Promise<Profile | null> {
  if (!isSupabaseConfigured()) {
    return DEMO_DATA.profiles.find((p) => p.id === id) ?? null;
  }
  try {
    const { data, error } = await supabase.from("profiles").select("*").eq("id", id).single();
    if (error) throw error;
    return data ?? DEMO_DATA.profiles.find((p) => p.id === id) ?? null;
  } catch {
    return DEMO_DATA.profiles.find((p) => p.id === id) ?? null;
  }
}

export async function getFactoryById(id?: string): Promise<Factory | null> {
  if (id && DEMO_DATA.factory.id === id) return DEMO_DATA.factory;
  return DEMO_DATA.factory;
}

export async function updateMachineStatus(
  id: string,
  status: Machine["status"]
): Promise<Machine> {
  if (!isSupabaseConfigured()) {
    const machine = DEMO_DATA.machines.find((m) => m.id === id);
    if (machine) {
      machine.status = status;
      return machine;
    }
  }
  try {
    const { error } = await supabase.from("machines").update({ status }).eq("id", id);
    if (error) throw error;
    const machine = await getMachineById(id);
    if (!machine) throw new Error("Machine not found");
    return machine;
  } catch {
    const machine = DEMO_DATA.machines.find((m) => m.id === id);
    if (machine) {
      machine.status = status;
      return machine;
    }
    throw new Error("Machine not found");
  }
}

export async function updateMachine(
  id: string,
  updates: Partial<Omit<Machine, "id">>
): Promise<Machine> {
  if (!isSupabaseConfigured()) {
    const machine = DEMO_DATA.machines.find((m) => m.id === id);
    if (machine) {
      Object.assign(machine, updates);
      return machine;
    }
  }
  try {
    const { data, error } = await supabase
      .from("machines")
      .update(updates)
      .eq("id", id)
      .select()
      .single();
    if (error) throw error;
    return data;
  } catch {
    const machine = DEMO_DATA.machines.find((m) => m.id === id);
    if (machine) {
      Object.assign(machine, updates);
      return machine;
    }
    throw new Error("Machine not found");
  }
}

export async function updatePart(
  id: string,
  updates: Partial<Omit<Part, "id">>
): Promise<Part> {
  if (!isSupabaseConfigured()) {
    const part = DEMO_DATA.parts.find((p) => p.id === id);
    if (part) {
      Object.assign(part, updates);
      return part;
    }
  }
  try {
    const { data, error } = await supabase
      .from("parts")
      .update(updates)
      .eq("id", id)
      .select()
      .single();
    if (error) throw error;
    return data;
  } catch {
    const part = DEMO_DATA.parts.find((p) => p.id === id);
    if (part) {
      Object.assign(part, updates);
      return part;
    }
    throw new Error("Part not found");
  }
}

export async function updatePartStock(id: string, quantity: number): Promise<Part> {
  if (!isSupabaseConfigured()) {
    const part = DEMO_DATA.parts.find((p) => p.id === id);
    if (part) {
      part.stock_quantity = quantity;
      return part;
    }
  }
  try {
    const { error } = await supabase.from("parts").update({ stock_quantity: quantity }).eq("id", id);
    if (error) throw error;
    const parts = await getParts();
    const part = parts.find((p) => p.id === id);
    if (!part) throw new Error("Part not found");
    return part;
  } catch {
    const part = DEMO_DATA.parts.find((p) => p.id === id);
    if (part) {
      part.stock_quantity = quantity;
      return part;
    }
    throw new Error("Part not found");
  }
}

export async function getDashboardStats() {
  if (!isSupabaseConfigured()) {
    return getDemoDashboardStats();
  }
  try {
    const [machines, logs, parts, faults] = await Promise.all([
      getMachines(),
      getMaintenanceLogs(100),
      getParts(),
      getFaultReports(),
    ]);

    const operational = machines.filter((m) => m.status === "operational").length;
    const total = machines.length;
    const thisMonth = logs.filter((l) => {
      const d = new Date(l.started_at);
      const now = new Date();
      return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear();
    });
    const completedLogs = logs.filter((l) => l.status === "completed" && l.duration_minutes);
    const avgTime =
      completedLogs.length > 0
        ? Math.round(
            completedLogs.reduce((s, l) => s + (l.duration_minutes ?? 0), 0) / completedLogs.length
          )
        : 0;
    const lowStock = parts.filter((p) => p.stock_quantity < p.min_stock_level);
    const activeTechnicians = await getProfiles().then((profiles) =>
      profiles.filter((p) => p.role === "technician").length
    );

    return {
      totalMachines: total,
      operationalPercent: total > 0 ? Math.round((operational / total) * 100) : 0,
      activeTechnicians,
      repairsThisMonth: thisMonth.length,
      avgRepairTime: avgTime,
      pendingFaults: faults.filter((f) => f.status === "open").length,
      lowStockParts: lowStock.length,
      lowStockItems: lowStock,
    };
  } catch {
    return getDemoDashboardStats();
  }
}

export async function getFailureByCategory() {
  if (!isSupabaseConfigured()) {
    return getDemoFailureByCategory();
  }
  try {
    const faults = await getFaultReports();

    const categories = new Map<string, number>();
    faults.forEach((f) => {
      const cat = f.machine?.category ?? "Unknown";
      categories.set(cat, (categories.get(cat) ?? 0) + 1);
    });
    return Array.from(categories.entries()).map(([category, count]) => ({ category, count }));
  } catch {
    return getDemoFailureByCategory();
  }
}

export async function getDowntimeTrend() {
  if (!isSupabaseConfigured()) {
    return getDemoDowntimeTrend();
  }
  try {
    const logs = await getMaintenanceLogs(100);
    const days: { date: string; hours: number }[] = [];

    for (let i = 29; i >= 0; i--) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().split("T")[0];
      const dayLogs = logs.filter((l) => l.started_at.startsWith(dateStr));
      days.push({
        date: dateStr,
        hours: dayLogs.length * 0.5 + Math.random() * 2,
      });
    }
    return days;
  } catch {
    return getDemoDowntimeTrend();
  }
}

export async function getTechnicianLeaderboard() {
  if (!isSupabaseConfigured()) {
    return getDemoTechnicianLeaderboard();
  }
  try {
    const [profiles, logs] = await Promise.all([getProfiles(), getMaintenanceLogs(200)]);

    const techs = profiles.filter((p) => p.role === "technician");
    return techs
      .map((t) => ({
        name: t.full_name,
        repairs: logs.filter((l) => l.technician_id === t.id && l.status === "completed").length,
      }))
      .sort((a, b) => b.repairs - a.repairs);
  } catch {
    return getDemoTechnicianLeaderboard();
  }
}
