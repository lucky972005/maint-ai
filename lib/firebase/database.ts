import {
  collection,
  doc,
  getDoc,
  getDocs,
  addDoc,
  updateDoc,
  setDoc,
  query,
  where,
  orderBy,
  limit,
  DocumentData,
  QueryDocumentSnapshot,
} from "firebase/firestore";
import { db } from "../firebase";
import type {
  Machine,
  Profile,
  RepairProcedure,
  MaintenanceLog,
  Part,
  FaultReport,
  Factory,
} from "../types";

function docToType<T>(snapshot: QueryDocumentSnapshot<DocumentData>): T {
  return { id: snapshot.id, ...snapshot.data() } as T;
}

// Machines
export async function getMachines(): Promise<Machine[]> {
  const machinesRef = collection(db, "machines");
  const q = query(machinesRef, orderBy("created_at", "desc"));
  const snapshot = await getDocs(q);
  return snapshot.docs.map(docToType<Machine>);
}

export async function getMachineById(id: string): Promise<Machine | null> {
  const docRef = doc(db, "machines", id);
  const snapshot = await getDoc(docRef);
  return snapshot.exists() ? docToType<Machine>(snapshot as QueryDocumentSnapshot<DocumentData>) : null;
}

export async function getMachineByQr(qrCode: string): Promise<Machine | null> {
  const machinesRef = collection(db, "machines");
  const q = query(machinesRef, where("qr_code", "==", qrCode));
  const snapshot = await getDocs(q);
  return snapshot.empty ? null : docToType<Machine>(snapshot.docs[0]);
}

export async function updateMachineStatus(id: string, status: Machine["status"]): Promise<void> {
  await updateDoc(doc(db, "machines", id), { status });
}

// Procedures
export async function getProceduresForMachine(machineId: string): Promise<RepairProcedure[]> {
  const proceduresRef = collection(db, "repairProcedures");
  const q = query(proceduresRef, where("machine_id", "==", machineId));
  const snapshot = await getDocs(q);
  return snapshot.docs
    .map(docToType<RepairProcedure>)
    .sort((a, b) => (b.created_at ?? "").localeCompare(a.created_at ?? ""));
}

export async function getProcedureById(id: string): Promise<RepairProcedure | null> {
  const docRef = doc(db, "repairProcedures", id);
  const snapshot = await getDoc(docRef);
  return snapshot.exists() ? docToType<RepairProcedure>(snapshot as QueryDocumentSnapshot<DocumentData>) : null;
}

// Parts
export async function getParts(): Promise<Part[]> {
  const partsRef = collection(db, "parts");
  const q = query(partsRef, orderBy("name"));
  const snapshot = await getDocs(q);
  return snapshot.docs.map(docToType<Part>);
}

export async function getLowStockParts(): Promise<Part[]> {
  const parts = await getParts();
  return parts.filter((part) => part.stock_quantity < part.min_stock_level);
}

export async function updatePartStock(id: string, quantity: number): Promise<void> {
  await updateDoc(doc(db, "parts", id), { stock_quantity: quantity });
}

// Maintenance Logs
export async function getMaintenanceLogs(limitCount = 50): Promise<MaintenanceLog[]> {
  const logsRef = collection(db, "maintenanceLogs");
  const q = query(logsRef, orderBy("started_at", "desc"), limit(limitCount));
  const snapshot = await getDocs(q);
  return snapshot.docs.map(docToType<MaintenanceLog>);
}

export async function createMaintenanceLog(log: Omit<MaintenanceLog, "id">): Promise<string> {
  const logsRef = collection(db, "maintenanceLogs");
  const docRef = await addDoc(logsRef, log);
  return docRef.id;
}

export async function updateMaintenanceLog(
  id: string,
  updates: Partial<Omit<MaintenanceLog, "id">>
): Promise<MaintenanceLog> {
  const docRef = doc(db, "maintenanceLogs", id);
  await updateDoc(docRef, updates);
  const snapshot = await getDoc(docRef);
  if (!snapshot.exists()) throw new Error("Maintenance log not found");
  return docToType<MaintenanceLog>(snapshot as QueryDocumentSnapshot<DocumentData>);
}

// Fault Reports
export async function getFaultReports(): Promise<FaultReport[]> {
  const faultsRef = collection(db, "faultReports");
  const q = query(faultsRef, orderBy("created_at", "desc"));
  const snapshot = await getDocs(q);
  return snapshot.docs.map(docToType<FaultReport>);
}

export async function createFaultReport(fault: Omit<FaultReport, "id" | "created_at">): Promise<string> {
  const faultsRef = collection(db, "faultReports");
  const docRef = await addDoc(faultsRef, {
    ...fault,
    created_at: new Date().toISOString(),
  });
  return docRef.id;
}

export async function updateFaultReport(
  id: string,
  updates: Partial<Omit<FaultReport, "id">>
): Promise<FaultReport> {
  const docRef = doc(db, "faultReports", id);
  await updateDoc(docRef, updates);
  const snapshot = await getDoc(docRef);
  if (!snapshot.exists()) throw new Error("Fault report not found");
  return docToType<FaultReport>(snapshot as QueryDocumentSnapshot<DocumentData>);
}

// Profiles
export async function getProfiles(): Promise<Profile[]> {
  const profilesRef = collection(db, "profiles");
  const snapshot = await getDocs(profilesRef);
  return snapshot.docs.map(docToType<Profile>);
}

export async function getProfileById(id: string): Promise<Profile | null> {
  const docRef = doc(db, "profiles", id);
  const snapshot = await getDoc(docRef);
  return snapshot.exists() ? docToType<Profile>(snapshot as QueryDocumentSnapshot<DocumentData>) : null;
}

export async function getProfileByEmail(email: string): Promise<Profile | null> {
  const profilesRef = collection(db, "profiles");
  const q = query(profilesRef, where("email", "==", email));
  const snapshot = await getDocs(q);
  return snapshot.empty ? null : docToType<Profile>(snapshot.docs[0]);
}

export async function createProfile(profile: Profile): Promise<void> {
  const docRef = doc(db, "profiles", profile.id);
  await setDoc(docRef, profile);
}

export async function updateProfile(id: string, data: Partial<Profile>): Promise<void> {
  const docRef = doc(db, "profiles", id);
  await updateDoc(docRef, data);
}

// Factory
export async function getFactoryById(id: string): Promise<Factory | null> {
  const docRef = doc(db, "factories", id);
  const snapshot = await getDoc(docRef);
  return snapshot.exists() ? docToType<Factory>(snapshot as QueryDocumentSnapshot<DocumentData>) : null;
}
