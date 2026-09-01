/**
 * Firebase Database Seeding Script
 * Run this script to populate your Firebase Firestore with demo data
 * 
 * Usage:
 * 1. Ensure your .env.local has Firebase configuration
 * 2. Run: npx tsx scripts/seed-firebase.ts
 */

import { initializeApp, getApps, FirebaseApp } from "firebase/app";
import { getFirestore, Firestore, collection, doc, setDoc, writeBatch } from "firebase/firestore";

// Firebase configuration from environment variables
const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
  measurementId: process.env.NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID,
};

// Initialize Firebase
let app: FirebaseApp;
if (!getApps().length) {
  app = initializeApp(firebaseConfig);
} else {
  app = getApps()[0];
}

const db: Firestore = getFirestore(app);

// Demo data
const DEMO_FACTORY = {
  id: "f0000000-0000-4000-8000-000000000001",
  name: "Apex Manufacturing Plant",
  location: "Pune, Maharashtra, India",
  created_at: new Date().toISOString(),
};

const DEMO_PROFILES = [
  {
    id: "u0000000-0000-4000-8000-000000000001",
    full_name: "Rajesh Kumar",
    email: "admin@demo.com",
    role: "admin",
    factory_id: DEMO_FACTORY.id,
    avatar_url: null,
    created_at: new Date().toISOString(),
  },
  {
    id: "u0000000-0000-4000-8000-000000000002",
    full_name: "Sunita Sharma",
    email: "supervisor@demo.com",
    role: "supervisor",
    factory_id: DEMO_FACTORY.id,
    avatar_url: null,
    created_at: new Date().toISOString(),
  },
  {
    id: "u0000000-0000-4000-8000-000000000003",
    full_name: "Vikram Patel",
    email: "tech1@demo.com",
    role: "technician",
    factory_id: DEMO_FACTORY.id,
    avatar_url: null,
    created_at: new Date().toISOString(),
  },
  {
    id: "u0000000-0000-4000-8000-000000000004",
    full_name: "Priya Singh",
    email: "tech2@demo.com",
    role: "technician",
    factory_id: DEMO_FACTORY.id,
    avatar_url: null,
    created_at: new Date().toISOString(),
  },
  {
    id: "u0000000-0000-4000-8000-000000000005",
    full_name: "Ahmed Hassan",
    email: "tech3@demo.com",
    role: "technician",
    factory_id: DEMO_FACTORY.id,
    avatar_url: null,
    created_at: new Date().toISOString(),
  },
];

const MACHINE_DEFS = [
  { name: "CNC Machine", model: "Haas VF-2", category: "CNC", manufacturer: "Haas Automation", qr: "MACHINE:haas-vf-2-001" },
  { name: "Water Pump", model: "Grundfos CR-15", category: "Pump", manufacturer: "Grundfos", qr: "MACHINE:grundfos-cr-15-001" },
  { name: "Air Compressor", model: "Atlas Copco GA-37", category: "Compressor", manufacturer: "Atlas Copco", qr: "MACHINE:atlas-ga-37-001" },
  { name: "Electric Motor", model: "Siemens 1LE0102", category: "Motor", manufacturer: "Siemens", qr: "MACHINE:siemens-1le0102-001" },
  { name: "Diesel Generator", model: "Cummins C110D5", category: "Generator", manufacturer: "Cummins", qr: "MACHINE:cummins-c110d5-001" },
  { name: "Conveyor Belt", model: "Flexco 1900", category: "Conveyor", manufacturer: "Flexco", qr: "MACHINE:flexco-1900-001" },
  { name: "Hydraulic Press", model: "Schuler PH-400", category: "Press", manufacturer: "Schuler", qr: "MACHINE:schuler-ph-400-001" },
  { name: "Lathe Machine", model: "Hindustan H-22", category: "CNC", manufacturer: "Hindustan", qr: "MACHINE:hindustan-h-22-001" },
  { name: "Welding Machine", model: "Lincoln Power Wave S350", category: "Welder", manufacturer: "Lincoln Electric", qr: "MACHINE:lincoln-s350-001" },
  { name: "Milling Machine", model: "Bridgeport Series 1", category: "CNC", manufacturer: "Bridgeport", qr: "MACHINE:bridgeport-s1-001" },
  { name: "Boiler System", model: "Cleaver-Brooks CB-200", category: "Boiler", manufacturer: "Cleaver-Brooks", qr: "MACHINE:cleaver-cb200-001" },
  { name: "Cooling Tower", model: "Baltimore Aircoil VTL", category: "Cooling", manufacturer: "Baltimore Aircoil", qr: "MACHINE:bac-vtl-001" },
  { name: "Chiller Unit", model: "Trane RTAC-140", category: "Chiller", manufacturer: "Trane", qr: "MACHINE:trane-rtac140-001" },
  { name: "Forklift", model: "Toyota 8FGCU25", category: "Forklift", manufacturer: "Toyota", qr: "MACHINE:toyota-8fgcu25-001" },
  { name: "Industrial Fan", model: "Greenheck CUE-220", category: "Fan", manufacturer: "Greenheck", qr: "MACHINE:greenheck-cue220-001" },
  { name: "Pump Motor Assembly", model: "PM-4500", category: "Motor", manufacturer: "Apex OEM", qr: "MACHINE:pump-motor-4500-001" },
  { name: "Pneumatic Cylinder", model: "Festo DSBC-50", category: "Pneumatic", manufacturer: "Festo", qr: "MACHINE:festo-dsbc50-001" },
  { name: "Servo Drive", model: "Mitsubishi MR-J4", category: "Drive", manufacturer: "Mitsubishi", qr: "MACHINE:mitsubishi-mrj4-001" },
  { name: "PLC Control Panel", model: "Siemens S7-1500", category: "Control", manufacturer: "Siemens", qr: "MACHINE:siemens-s71500-001" },
  { name: "Transformer", model: "ABB 500kVA", category: "Electrical", manufacturer: "ABB", qr: "MACHINE:abb-500kva-001" },
];

const LOCATIONS = [
  "Bay A - Floor 1",
  "Bay B - Floor 1",
  "Bay C - Floor 2",
  "Warehouse Zone 3",
  "Production Line 4",
  "Utility Room",
  "Maintenance Shop",
];

const PARTS_DEFS = [
  { name: "Hydraulic Oil", part_number: "OIL-HYD-001", stock: 50, min: 10, price: 45.00 },
  { name: "V-Belt (Type A)", part_number: "BELT-A-001", stock: 30, min: 8, price: 12.50 },
  { name: "Ball Bearing 6205", part_number: "BRG-6205", stock: 100, min: 20, price: 8.75 },
  { name: "Air Filter", part_number: "FLT-AIR-001", stock: 25, min: 5, price: 18.00 },
  { name: "Pressure Switch", part_number: "SW-PRS-001", stock: 15, min: 3, price: 35.00 },
  { name: "Motor Capacitor", part_number: "CAP-MTR-001", stock: 40, min: 10, price: 6.50 },
  { name: "Seal Kit (Pump)", part_number: "SK-PMP-001", stock: 20, min: 5, price: 28.00 },
  { name: "Thermocouple", part_number: "THM-001", stock: 60, min: 15, price: 14.00 },
  { name: "Relay 12V", part_number: "RLY-12V-001", stock: 80, min: 20, price: 5.25 },
  { name: "Circuit Breaker 20A", part_number: "CB-20A-001", stock: 35, min: 8, price: 22.00 },
];

const PROCEDURE_TYPES = [
  "Oil Change",
  "Belt Replacement",
  "Bearing Replacement",
  "Motor Inspection",
  "Electrical Wiring Check",
  "Filter Replacement",
  "Calibration",
  "Safety Inspection",
];

const STEP_TEMPLATES: Record<string, string[]> = {
  "Oil Change": [
    "Power off the machine and engage lockout/tagout procedures",
    "Locate the oil drain plug on the {unit}",
    "Place drain pan beneath the drain plug",
    "Remove drain plug using wrench and allow oil to fully drain",
    "Replace drain plug and torque to specification",
    "Remove old oil filter and install new filter",
    "Refill with manufacturer-specified oil grade",
    "Run machine briefly and check for leaks",
    "Record oil type and quantity in maintenance log",
  ],
  "Belt Replacement": [
    "De-energize the machine and verify zero energy state",
    "Remove belt guard panels using screwdriver",
    "Release belt tension using adjustment bolt",
    "Inspect pulleys for wear or damage",
    "Remove worn belt from pulley system",
    "Install new belt ensuring proper alignment",
    "Adjust tension to manufacturer specification",
    "Reinstall belt guards securely",
    "Test run and verify belt tracking",
  ],
  "Bearing Replacement": [
    "Lock out machine and confirm isolation",
    "Remove access panels to expose bearing housing",
    "Mark shaft position before disassembly",
    "Remove retaining ring and pull bearing with puller",
    "Clean bearing seat and inspect for scoring",
    "Apply appropriate grease to new bearing",
    "Press new bearing into housing using arbor press",
    "Reassemble components in reverse order",
    "Verify free rotation before energizing",
  ],
  "Motor Inspection": [
    "Verify lockout/tagout is in place",
    "Visual inspect motor housing for cracks or burn marks",
    "Check motor mounting bolts for tightness",
    "Measure insulation resistance with multimeter",
    "Inspect cooling fan and ventilation ports",
    "Check shaft alignment with coupling",
    "Listen for abnormal noise during brief test run",
    "Record all measurements in inspection log",
  ],
  "Electrical Wiring Check": [
    "De-energize all circuits and verify with multimeter",
    "Open electrical panel using appropriate PPE",
    "Inspect wire terminations for looseness or corrosion",
    "Check wire insulation for heat damage or fraying",
    "Test ground connections for continuity",
    "Verify proper wire gauge for current load",
    "Check for proper labeling of circuits",
    "Close panel and restore power with supervision",
  ],
  "Filter Replacement": [
    "Shut down system and relieve pressure",
    "Locate filter housing and prepare drain container",
    "Remove filter housing cover or cartridge",
    "Inspect old filter for contamination patterns",
    "Clean filter housing interior",
    "Install new filter with proper orientation",
    "Replace gaskets if worn or damaged",
    "Reassemble housing and check for leaks",
    "Restart system and monitor pressure readings",
  ],
  "Calibration": [
    "Verify calibration tools are certified and within date",
    "Allow equipment to reach operating temperature",
    "Connect calibration device according to manual",
    "Record current readings before adjustment",
    "Adjust to meet specification using control interface",
    "Verify reading at multiple test points",
    "Document calibration values and date",
    "Apply calibration tag with next due date",
  ],
  "Safety Inspection": [
    "Review equipment safety manual checklist",
    "Check all emergency stop functionality",
    "Inspect safety guards and interlocks",
    "Verify warning labels are visible and intact",
    "Test safety sensors and limit switches",
    "Check for proper grounding of equipment",
    "Inspect PPE availability and condition",
    "Document findings and required corrective actions",
  ],
};

// Helper function to generate random ID
function generateId(prefix: string): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 9);
  return `${prefix}${timestamp}${random}`;
}

// Helper function to get random item from array
function getRandomItem<T>(array: T[]): T {
  return array[Math.floor(Math.random() * array.length)];
}

// Generate machines
function generateMachines() {
  return MACHINE_DEFS.map((def, index) => ({
    id: generateId("m"),
    qr_code: def.qr,
    name: def.name,
    model: def.model,
    manufacturer: def.manufacturer,
    category: def.category,
    location: LOCATIONS[index % LOCATIONS.length],
    status: getRandomItem(["operational", "operational", "operational", "maintenance", "broken"]),
    image_url: null,
    created_at: new Date(Date.now() - Math.random() * 90 * 24 * 60 * 60 * 1000).toISOString(),
  }));
}

// Generate parts
function generateParts() {
  return PARTS_DEFS.map((def) => ({
    id: generateId("p"),
    name: def.name,
    part_number: def.part_number,
    stock_quantity: def.stock,
    min_stock_level: def.min,
    unit_price: def.price,
  }));
}

// Generate repair procedures for each machine
function generateProcedures(machines: any[]) {
  const procedures: any[] = [];
  
  machines.forEach((machine) => {
    const numProcedures = Math.floor(Math.random() * 3) + 2; // 2-4 procedures per machine
    
    for (let i = 0; i < numProcedures; i++) {
      const procedureType = getRandomItem(PROCEDURE_TYPES);
      const steps = STEP_TEMPLATES[procedureType] || STEP_TEMPLATES["Safety Inspection"];
      
      procedures.push({
        id: generateId("rp"),
        machine_id: machine.id,
        procedure_type: procedureType,
        estimated_minutes: Math.floor(Math.random() * 60) + 15,
        difficulty: getRandomItem(["easy", "medium", "medium", "hard"]),
        steps: steps.map((instruction, idx) => ({
          step: idx + 1,
          instruction: instruction.replace("{unit}", machine.name.toLowerCase()),
          tool_needed: getRandomItem(["Wrench Set", "Screwdriver", "Multimeter", "Pliers", "Torque Wrench", "None"]),
          safety: getRandomItem([
            "Wear appropriate PPE",
            "Ensure machine is locked out",
            "Check for hot surfaces",
            "Use proper lifting techniques",
            "Verify electrical isolation",
          ]),
          ar_marker: {
            x: Math.random() * 100,
            y: Math.random() * 100,
            w: Math.random() * 30 + 10,
            h: Math.random() * 30 + 10,
            label: `Step ${idx + 1}`,
            color: getRandomItem(["red", "green", "blue"]),
          },
          requires_tool_verification: Math.random() > 0.5,
          is_dangerous: procedureType === "Electrical Wiring Check" || procedureType === "Bearing Replacement",
        })),
        created_at: new Date(Date.now() - Math.random() * 60 * 24 * 60 * 60 * 1000).toISOString(),
      });
    }
  });
  
  return procedures;
}

// Main seeding function
async function seedDatabase() {
  console.log("🌱 Starting Firebase database seeding...\n");
  
  try {
    // Seed Factory
    console.log("📁 Seeding factory...");
    await setDoc(doc(db, "factories", DEMO_FACTORY.id), DEMO_FACTORY);
    console.log("✅ Factory seeded\n");
    
    // Seed Profiles
    console.log("👤 Seeding profiles...");
    const profilesBatch = writeBatch(db);
    DEMO_PROFILES.forEach((profile) => {
      profilesBatch.set(doc(db, "profiles", profile.id), profile);
    });
    await profilesBatch.commit();
    console.log(`✅ ${DEMO_PROFILES.length} profiles seeded\n`);
    
    // Seed Machines
    console.log("🔧 Seeding machines...");
    const machines = generateMachines();
    const machinesBatch = writeBatch(db);
    machines.forEach((machine) => {
      machinesBatch.set(doc(db, "machines", machine.id), machine);
    });
    await machinesBatch.commit();
    console.log(`✅ ${machines.length} machines seeded\n`);
    
    // Seed Parts
    console.log("📦 Seeding parts...");
    const parts = generateParts();
    const partsBatch = writeBatch(db);
    parts.forEach((part) => {
      partsBatch.set(doc(db, "parts", part.id), part);
    });
    await partsBatch.commit();
    console.log(`✅ ${parts.length} parts seeded\n`);
    
    // Seed Repair Procedures
    console.log("📋 Seeding repair procedures...");
    const procedures = generateProcedures(machines);
    const proceduresBatch = writeBatch(db);
    procedures.forEach((procedure) => {
      proceduresBatch.set(doc(db, "repairProcedures", procedure.id), procedure);
    });
    await proceduresBatch.commit();
    console.log(`✅ ${procedures.length} repair procedures seeded\n`);
    
    console.log("🎉 Database seeding completed successfully!");
    console.log("\n📊 Summary:");
    console.log(`   - 1 Factory`);
    console.log(`   - ${DEMO_PROFILES.length} Profiles`);
    console.log(`   - ${machines.length} Machines`);
    console.log(`   - ${parts.length} Parts`);
    console.log(`   - ${procedures.length} Repair Procedures`);
    console.log("\n🔐 Demo Accounts:");
    console.log("   - admin@demo.com (Admin)");
    console.log("   - supervisor@demo.com (Supervisor)");
    console.log("   - tech1@demo.com (Technician)");
    console.log("   - tech2@demo.com (Technician)");
    console.log("   - tech3@demo.com (Technician)");
    console.log("\n⚠️  Note: You'll need to create these users in Firebase Authentication");
    console.log("   with password: demo123456");
    
  } catch (error) {
    console.error("❌ Error seeding database:", error);
    process.exit(1);
  }
}

// Run the seeding
seedDatabase().then(() => {
  console.log("\n✨ Done!");
  process.exit(0);
});
