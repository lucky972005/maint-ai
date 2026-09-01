import {
  DEMO_DATA,
  isFirebaseConfigured,
  getMachineById as getDemoMachineById,
  getMachineByQr as getDemoMachineByQr,
  getProceduresForMachine as getDemoProcedures,
  getProcedureById as getDemoProcedureById,
  getDashboardStats as getDemoDashboardStats,
  getFailureByCategory as getDemoFailureByCategory,
  getDowntimeTrend as getDemoDowntimeTrend,
  getTechnicianLeaderboard as getDemoTechnicianLeaderboard,
} from "./demo-data";
import * as db from "./database";
import type {
  Machine,
  RepairProcedure,
  Part,
  MaintenanceLog,
  FaultReport,
  Profile,
} from "./types";

function hasLiveBackend(): boolean {
  return isFirebaseConfigured();
}

export async function getMachines(): Promise<Machine[]> {
  if (hasLiveBackend()) {
    try {
      const machines = await db.getMachines();
      if (machines.length > 0) return machines;
    } catch (error) {
      console.error("Firebase getMachines failed, using demo:", error);
    }
  }
  return DEMO_DATA.machines;
}

export async function getMachineById(id: string): Promise<Machine | null> {
  if (hasLiveBackend()) {
    try {
      const machine = await db.getMachineById(id);
      if (machine) return machine;
    } catch (error) {
      console.error("Firebase getMachineById failed:", error);
    }
  }
  return getDemoMachineById(id) ?? null;
}

export async function getMachineByQr(qrCode: string): Promise<Machine | null> {
  if (hasLiveBackend()) {
    try {
      const machine = await db.getMachineByQr(qrCode);
      if (machine) return machine;
    } catch (error) {
      console.error("Firebase getMachineByQr failed:", error);
    }
  }
  const exact = getDemoMachineByQr(qrCode);
  if (exact) return exact;
  const fuzzy = DEMO_DATA.machines.find((m) =>
    qrCode.includes(m.qr_code.split(":")[1]?.slice(0, 8) ?? "")
  );
  return fuzzy ?? null;
}

export async function getProceduresForMachine(machineId: string): Promise<RepairProcedure[]> {
  if (hasLiveBackend()) {
    try {
      const procedures = await db.getProceduresForMachine(machineId);
      if (procedures.length > 0) return procedures;
    } catch (error) {
      console.error("Firebase getProcedures failed:", error);
    }
  }
  return getDemoProcedures(machineId);
}

export async function getProcedureById(id: string): Promise<RepairProcedure | null> {
  if (hasLiveBackend()) {
    try {
      const procedure = await db.getProcedureById(id);
      if (procedure) return procedure;
    } catch (error) {
      console.error("Firebase getProcedureById failed:", error);
    }
  }
  return getDemoProcedureById(id) ?? null;
}

export async function getParts(): Promise<Part[]> {
  if (hasLiveBackend()) {
    try {
      const parts = await db.getParts();
      if (parts.length > 0) return parts;
    } catch (error) {
      console.error("Firebase getParts failed:", error);
    }
  }
  return DEMO_DATA.parts;
}

export async function getMaintenanceLogs(limit = 50): Promise<MaintenanceLog[]> {
  if (hasLiveBackend()) {
    try {
      const logs = await db.getMaintenanceLogs(limit);
      if (logs.length > 0) return logs;
    } catch (error) {
      console.error("Firebase getMaintenanceLogs failed:", error);
    }
  }
  return DEMO_DATA.logs.slice(0, limit);
}

export async function getFaultReports(): Promise<FaultReport[]> {
  if (hasLiveBackend()) {
    try {
      const faults = await db.getFaultReports();
      if (faults.length > 0) return faults;
    } catch (error) {
      console.error("Firebase getFaultReports failed:", error);
    }
  }
  return DEMO_DATA.faults;
}

export async function getProfiles(): Promise<Profile[]> {
  if (hasLiveBackend()) {
    try {
      const profiles = await db.getProfiles();
      if (profiles.length > 0) return profiles;
    } catch (error) {
      console.error("Firebase getProfiles failed:", error);
    }
  }
  return DEMO_DATA.profiles;
}

export async function getDashboardStats() {
  if (hasLiveBackend()) {
    try {
      return await db.getDashboardStats();
    } catch (error) {
      console.error("Firebase dashboard stats failed:", error);
    }
  }
  return getDemoDashboardStats();
}

export async function getFailureByCategory() {
  if (hasLiveBackend()) {
    try {
      return await db.getFailureByCategory();
    } catch (error) {
      console.error("Firebase failure stats failed:", error);
    }
  }
  return getDemoFailureByCategory();
}

export async function getDowntimeTrend() {
  if (hasLiveBackend()) {
    try {
      return await db.getDowntimeTrend();
    } catch (error) {
      console.error("Firebase downtime trend failed:", error);
    }
  }
  return getDemoDowntimeTrend();
}

export async function getTechnicianLeaderboard() {
  if (hasLiveBackend()) {
    try {
      return await db.getTechnicianLeaderboard();
    } catch (error) {
      console.error("Firebase leaderboard failed:", error);
    }
  }
  return getDemoTechnicianLeaderboard();
}

export async function updatePartStock(id: string, quantity: number): Promise<Part> {
  if (hasLiveBackend()) {
    return db.updatePartStock(id, quantity);
  }
  const part = DEMO_DATA.parts.find((p) => p.id === id);
  if (!part) throw new Error("Part not found");
  part.stock_quantity = quantity;
  return part;
}
