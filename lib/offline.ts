import Dexie, { type Table } from "dexie";
import type { FaultReport, Machine, RepairProcedure, Profile, MaintenanceLog } from "./types";
import { DEMO_DATA } from "./demo-data";

export interface CachedManual {
  id: string;
  machineId: string;
  name: string;
  blob: Blob;
  cachedAt: number;
}

export interface SyncQueueItem {
  id?: number;
  type: "maintenance_log" | "fault_report" | "evidence";
  payload: unknown;
  createdAt: number;
  retries: number;
}

export interface CachedFaultReport extends FaultReport {
  source: "demo" | "sync-queue";
}

class MaintenanceDB extends Dexie {
  machines!: Table<Machine, string>;
  procedures!: Table<RepairProcedure, string>;
  profile!: Table<Profile, string>;
  manuals!: Table<CachedManual, string>;
  syncQueue!: Table<SyncQueueItem, number>;
  maintenanceLogs!: Table<MaintenanceLog, string>;
  faultReports!: Table<CachedFaultReport, string>;

  constructor() {
    super("IndustrialMaintenanceDB");
    this.version(1).stores({
      machines: "id, qr_code, factory_id, category",
      procedures: "id, machine_id, procedure_type",
      profile: "id",
      manuals: "id, machineId",
      syncQueue: "++id, type, createdAt",
      maintenanceLogs: "id, machine_id, technician_id, status",
      faultReports: "id, machine_id, reported_by, status",
    });
    this.version(2).stores({
      machines: "id, qr_code, factory_id, category",
      procedures: "id, machine_id, procedure_type",
      profile: "id",
      manuals: "id, machineId",
      syncQueue: "++id, type, createdAt",
      maintenanceLogs: "id, machine_id, technician_id, status, started_at, completed_at",
      faultReports: "id, machine_id, reported_by, status, created_at",
    });
  }
}

let db: MaintenanceDB | null = null;

export function getDB(): MaintenanceDB {
  if (typeof window === "undefined") {
    throw new Error("IndexedDB is only available in the browser");
  }
  if (!db) {
    db = new MaintenanceDB();
  }
  return db;
}

export async function cacheMachines(machines: Machine[]): Promise<void> {
  const database = getDB();
  await database.machines.bulkPut(machines);
}

export async function cacheProcedures(procedures: RepairProcedure[]): Promise<void> {
  const database = getDB();
  await database.procedures.bulkPut(procedures);
}

export async function cacheProfile(profile: Profile): Promise<void> {
  const database = getDB();
  await database.profile.put(profile);
}

export async function getCachedMachine(id: string): Promise<Machine | undefined> {
  return getDB().machines.get(id);
}

export async function getCachedMachineByQr(qrCode: string): Promise<Machine | undefined> {
  return getDB().machines.where("qr_code").equals(qrCode).first();
}

export async function getCachedProcedures(machineId: string): Promise<RepairProcedure[]> {
  return getDB().procedures.where("machine_id").equals(machineId).toArray();
}

export async function getCachedProfile(): Promise<Profile | undefined> {
  return getDB().profile.toCollection().first();
}

export async function cacheManual(id: string, machineId: string, name: string, blob: Blob): Promise<void> {
  await getDB().manuals.put({ id, machineId, name, blob, cachedAt: Date.now() });
}

export async function getCachedManual(id: string): Promise<CachedManual | undefined> {
  return getDB().manuals.get(id);
}

export async function queueForSync(
  type: SyncQueueItem["type"],
  payload: unknown
): Promise<void> {
  await getDB().syncQueue.add({
    type,
    payload,
    createdAt: Date.now(),
    retries: 0,
  });
}

export async function cacheFaultReport(
  report: FaultReport,
  source: CachedFaultReport["source"] = "demo"
): Promise<void> {
  await getDB().faultReports.put({ ...report, source });
}

export async function getCachedFaultReports(): Promise<CachedFaultReport[]> {
  try {
    const list = await getDB().faultReports.toArray();
    return list.sort(
      (a, b) => new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime()
    );
  } catch (err) {
    console.warn("getCachedFaultReports error:", err);
    return [];
  }
}

export async function cacheMaintenanceLog(log: MaintenanceLog): Promise<void> {
  try {
    await getDB().maintenanceLogs.put(log);
  } catch (e) {
    console.warn("IndexedDB cache error:", e);
  }
  // Store in DEMO_DATA so in-memory pages have it immediately
  if (!DEMO_DATA.logs.some((l) => l.id === log.id)) {
    DEMO_DATA.logs.unshift(log);
  }
  // Also store in localStorage as client fallback
  if (typeof window !== "undefined") {
    try {
      const stored = JSON.parse(window.localStorage.getItem("maintai_saved_logs") || "[]");
      if (!stored.some((item: MaintenanceLog) => item.id === log.id)) {
        window.localStorage.setItem("maintai_saved_logs", JSON.stringify([log, ...stored]));
      }
    } catch {}
  }
}

export async function getCachedMaintenanceLogs(): Promise<MaintenanceLog[]> {
  try {
    let dbLogs: MaintenanceLog[] = [];
    try {
      dbLogs = await getDB().maintenanceLogs.toArray();
    } catch (e) {
      console.warn("IndexedDB toArray read error:", e);
    }
    let localLogs: MaintenanceLog[] = [];
    if (typeof window !== "undefined") {
      try {
        localLogs = JSON.parse(window.localStorage.getItem("maintai_saved_logs") || "[]");
      } catch {}
    }
    const map = new Map<string, MaintenanceLog>();
    dbLogs.forEach((l) => map.set(l.id, l));
    localLogs.forEach((l) => map.set(l.id, l));
    return Array.from(map.values()).sort(
      (a, b) => new Date(b.completed_at || b.started_at).getTime() - new Date(a.completed_at || a.started_at).getTime()
    );
  } catch {
    return [];
  }
}

export async function getSyncQueue(): Promise<SyncQueueItem[]> {
  return getDB().syncQueue.orderBy("createdAt").toArray();
}

export async function removeSyncItem(id: number): Promise<void> {
  await getDB().syncQueue.delete(id);
}

export async function processSyncQueue(
  syncFn: (item: SyncQueueItem) => Promise<boolean>
): Promise<number> {
  const items = await getSyncQueue();
  let synced = 0;
  for (const item of items) {
    if (item.id === undefined) continue;
    try {
      const success = await syncFn(item);
      if (success) {
        await removeSyncItem(item.id);
        synced++;
      }
    } catch {
      await getDB().syncQueue.update(item.id, { retries: item.retries + 1 });
    }
  }
  return synced;
}

export function isOnline(): boolean {
  return typeof navigator !== "undefined" ? navigator.onLine : true;
}

export async function hydrateOfflineCache(
  machines: Machine[],
  procedures: RepairProcedure[],
  profile?: Profile
): Promise<void> {
  await cacheMachines(machines);
  await cacheProcedures(procedures);
  if (profile) await cacheProfile(profile);
}
