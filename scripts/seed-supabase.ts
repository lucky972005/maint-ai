/**
 * Supabase Database Seeding Script
 * Run this script to populate your Supabase database with demo data
 *
 * Usage:
 * 1. Ensure your .env.local has Supabase configuration
 * 2. Run: npx tsx scripts/seed-supabase.ts
 */

import { config } from "dotenv";
import { createClient } from "@supabase/supabase-js";
import { randomUUID } from "crypto";
import { DEMO_DATA, DEMO_USERS } from "../lib/demo-data";
import { PROCEDURE_TYPES, TOOLS } from "../lib/types";
import type { Machine, RepairStep } from "../lib/types";

// Load environment variables from .env.local
config({ path: ".env.local" });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error("Missing Supabase configuration in .env.local");
  console.error("Required: NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY");
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

// Helper functions for generating procedure data
const STEP_TEMPLATES: Record<string, string[]> = {
  "Oil Change": [
    "Drain old oil from {unit} using drain plug",
    "Remove and replace oil filter",
    "Refill with recommended oil grade",
    "Check for leaks around drain plug",
    "Verify oil level with dipstick",
  ],
  "Belt Replacement": [
    "Loosen tension bolts on {unit}",
    "Remove worn belt carefully",
    "Clean pulleys and check for wear",
    "Install new belt with proper tension",
    "Test belt alignment and operation",
  ],
  "Bearing Replacement": [
    "Disconnect power to {unit}",
    "Remove housing covers to access bearing",
    "Extract old bearing using puller",
    "Clean bearing seat and inspect shaft",
    "Install new bearing with proper tools",
    "Reassemble and test operation",
  ],
  "Motor Inspection": [
    "Verify {unit} is de-energized and locked out",
    "Inspect motor windings for damage",
    "Check bearings and lubrication",
    "Test electrical connections",
    "Measure insulation resistance",
    "Inspect cooling fan and ventilation ports",
  ],
  "Electrical Wiring Check": [
    "De-energize all circuits and verify with multimeter",
    "Open electrical panel using appropriate PPE",
    "Inspect wire terminations for looseness or corrosion",
    "Check wire insulation for heat damage or fraying",
    "Verify ground connections are secure",
    "Tighten all terminal connections to spec",
  ],
  "Emergency Shutdown": [
    "Identify the emergency stop button location",
    "Press E-STOP button firmly until latched",
    "Verify all motion has ceased on the {unit}",
    "Turn main disconnect switch to OFF position",
    "Apply lockout/tagout devices to all energy sources",
  ],
};

const AR_LABELS = [
  "Drain Plug", "Oil Filter", "Fill Port", "Belt Guard", "Tension Bolt",
  "Pulley A", "Bearing Housing", "Retaining Ring", "Motor Terminal", "Ground Wire",
  "E-STOP Button", "Main Disconnect",
];

function generateArMarker(stepIndex: number, label: string) {
  const colors: ("red" | "green" | "blue")[] = ["red", "green", "blue"];
  return {
    x: 15 + (stepIndex * 7) % 60,
    y: 20 + (stepIndex * 5) % 40,
    w: 10 + (stepIndex % 3) * 5,
    h: 8 + (stepIndex % 2) * 4,
    label,
    color: colors[stepIndex % 3],
  };
}

function generateSteps(procedureType: string, machineName: string): RepairStep[] {
  const templates = STEP_TEMPLATES[procedureType] || STEP_TEMPLATES["Oil Change"];
  return templates.map((template, i) => ({
    step: i + 1,
    instruction: template.replace("{unit}", machineName),
    tool_needed: TOOLS[i % TOOLS.length],
    safety: i === 0 || i % 3 === 0
      ? "Ensure lockout/tagout is applied before proceeding. Wear appropriate PPE."
      : "Keep hands clear of moving parts. Verify machine is de-energized.",
    ar_marker: generateArMarker(i, AR_LABELS[i % AR_LABELS.length]),
    requires_tool_verification: i > 0 && i % 2 === 0,
    is_dangerous: procedureType === "Emergency Shutdown" || i % 3 === 2,
  }));
}

async function seedDatabase() {
  console.log("🌱 Starting Supabase database seeding...\n");

  try {
    // Clear existing data first (in reverse order of dependencies)
    console.log("🗑️ Clearing existing data...");
    await supabase.from("repair_procedures").delete().neq("id", "00000000-0000-0000-0000-000000000000");
    await supabase.from("fault_reports").delete().neq("id", "00000000-0000-0000-0000-000000000000");
    await supabase.from("maintenance_logs").delete().neq("id", "00000000-0000-0000-0000-000000000000");
    await supabase.from("parts").delete().neq("id", "00000000-0000-0000-0000-000000000000");
    
    // Delete machines by QR codes since foreign keys may prevent direct delete
    const { data: existingMachines } = await supabase.from("machines").select("qr_code");
    if (existingMachines) {
      for (const machine of existingMachines) {
        await supabase.from("machines").delete().eq("qr_code", machine.qr_code);
      }
    }
    
    // Skip profile deletion - profiles reference Supabase auth users
    // Users should sign up through the app to create profiles
    await supabase.from("factories").delete().neq("id", "00000000-0000-0000-0000-000000000000");
    console.log("✅ Existing data cleared\n");
    // 1. Seed Factory
    console.log("📦 Seeding factory...");
    const { data: factoryData, error: factoryError } = await supabase
      .from("factories")
      .upsert({
        id: "f0000000-0000-4000-8000-000000000001",
        name: "Demo Factory",
        location: "Industrial Zone A",
      })
      .select()
      .single();

    if (factoryError) {
      console.error("Error seeding factory:", factoryError);
    } else {
      console.log("✅ Factory seeded successfully");
    }

    // 2. Seed Machines
    console.log("\n🔧 Seeding machines...");
    const seededMachines: Machine[] = [];
    for (const machine of DEMO_DATA.machines) {
      const { data, error: machineError } = await supabase
        .from("machines")
        .insert(machine)
        .select()
        .single();

      if (machineError) {
        console.error(`Error seeding machine ${machine.name}:`, machineError);
      } else {
        console.log(`✅ Machine seeded: ${machine.name}`);
        seededMachines.push(data);
      }
    }

    // 4. Seed Parts
    console.log("\n⚙️ Seeding parts...");
    for (const part of DEMO_DATA.parts) {
      const { error: partError } = await supabase
        .from("parts")
        .upsert(part, { onConflict: "id" });

      if (partError) {
        console.error(`Error seeding part ${part.name}:`, partError);
      } else {
        console.log(`✅ Part seeded: ${part.name}`);
      }
    }

    // 5. Seed Repair Procedures (using actual seeded machine IDs)
    console.log("\n📋 Seeding repair procedures...");
    let procIndex = 0;
    for (const machine of seededMachines) {
      for (const procedureType of PROCEDURE_TYPES) {
        procIndex++;
        const steps = generateSteps(procedureType, machine.name);
        const procedure = {
          id: randomUUID(),
          machine_id: machine.id,
          procedure_type: procedureType,
          estimated_minutes: 20 + (procIndex % 5) * 15,
          difficulty: ["easy", "medium", "hard"][procIndex % 3] as "easy" | "medium" | "hard",
          steps,
          required_tools: TOOLS.slice(0, 3 + (procIndex % 4)),
          safety_warnings: ["Wear PPE", "Lockout/Tagout"].slice(0, 1 + (procIndex % 2)),
        };

        const { error: procedureError } = await supabase
          .from("repair_procedures")
          .upsert(procedure, { onConflict: "id" });

        if (procedureError) {
          console.error(`Error seeding procedure ${procedureType} for ${machine.name}:`, procedureError);
        } else {
          console.log(`✅ Procedure seeded: ${procedureType} for ${machine.name}`);
        }
      }
    }

    console.log("\n🎉 Database seeding completed successfully!");
    console.log("\n📊 Summary:");
    console.log(`   - 1 Factory`);
    console.log(`   - ${seededMachines.length} Machines`);
    console.log(`   - ${DEMO_DATA.parts.length} Parts`);
    console.log(`   - ${seededMachines.length * PROCEDURE_TYPES.length} Repair procedures`);
    console.log("\n� Note: User profiles must be created through the app signup process");
    console.log("   since they reference Supabase auth users.");

  } catch (error) {
    console.error("❌ Seeding failed:", error);
    process.exit(1);
  }
}

seedDatabase();
