import type {
  ArMarker,
  Factory,
  Machine,
  Part,
  Profile,
  RepairProcedure,
  RepairStep,
  MaintenanceLog,
  FaultReport,
} from "./types";
import { PROCEDURE_TYPES, TOOLS } from "./types";

// Static UUIDs for demo data to ensure server/client consistency
const STATIC_UUIDS = [
  "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4C5d",
  "b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e",
  "c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f",
  "d4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a",
  "e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b",
  "f6a7b8c9-d0e1-4f2a-3b4c-5d6e7f8a9b0c",
  "a7b8c9d0-e1f2-4a3b-4c5d-6e7f8a9b0c1d",
  "b8c9d0e1-f2a3-4b4c-5d6e-7f8a9b0c1d2e",
  "c9d0e1f2-a3b4-4c5d-6e7f-8a9b0c1d2e3f",
  "d0e1f2a3-b4c5-4d6e-7f8a-9b0c1d2e3f4a",
  "e1f2a3b4-c5d6-4e7f-8a9b-0c1d2e3f4a5b",
  "f2a3b4c5-d6e7-4f8a-9b0c-1d2e3f4a5b6c",
  "a3b4c5d6-e7f8-4a9b-0c1d-2e3f4a5b6c7d",
  "b4c5d6e7-f8a9-4b0c-1d2e-3f4a5b6c7d8e",
  "c5d6e7f8-a9b0-4c1d-2e3f-4a5b6c7d8e9f",
  "d6e7f8a9-b0c1-4d2e-3f4a-5b6c7d8e9f0a",
  "e7f8a9b0-c1d2-4e3f-4a5b-6c7d8e9f0a1b",
  "f8a9b0c1-d2e3-4f4a-5b6c-7d8e9f0a1b2c",
  "a9b0c1d2-e3f4-4a5b-6c7d-8e9f0a1b2c3d",
  "b0c1d2e3-f4a5-4b6c-7d8e-9f0a1b2c3d4e",
  "c1d2e3f4-a5b6-4c7d-8e9f-0a1b2c3d4e5f",
  "d2e3f4a5-b6c7-4d8e-9f0a-1b2c3d4e5f6a",
  "e3f4a5b6-c7d8-4e9f-0a1b-2c3d4e5f6a7b",
  "f4a5b6c7-d8e9-4f0a-1b2c-3d4e5f6a7b8c",
  "a5b6c7d8-e9f0-4a1b-2c3d-4e5f6a7b8c9d",
  "b6c7d8e9-f0a1-4b2c-3d4e-5f6a7b8c9d0e",
  "c7d8e9f0-a1b2-4c3d-4e5f-6a7b8c9d0e1f",
  "d8e9f0a1-b2c3-4d4e-5f6a-7b8c9d0e1f2a",
  "e9f0a1b2-c3d4-4e5f-6a7b-8c9d0e1f2a3b",
  "f0a1b2c3-d4e5-4f6a-7b8c-9d0e1f2a3b4c",
];

let uuidIndex = 0;
function randomUUID(): string {
  return STATIC_UUIDS[uuidIndex++ % STATIC_UUIDS.length];
}

export const DEMO_FACTORY: Factory = {
  id: "f0000000-0000-4000-8000-000000000001",
  name: "Apex Manufacturing Plant",
  location: "Pune, Maharashtra, India",
};

export const DEMO_USERS: (Profile & { password: string })[] = [
  {
    id: "u0000000-0000-4000-8000-000000000001",
    full_name: "System Admin",
    email: "admin@demo.com",
    role: "admin",
    factory_id: DEMO_FACTORY.id,
    avatar_url: null,
    password: "demo123456",
  },
  {
    id: "u0000000-0000-4000-8000-000000000002",
    full_name: "Supervisor Patel",
    email: "supervisor@demo.com",
    role: "supervisor",
    factory_id: DEMO_FACTORY.id,
    avatar_url: null,
    password: "demo123456",
  },
  {
    id: "u0000000-0000-4000-8000-000000000003",
    full_name: "Raj Kumar",
    email: "tech1@demo.com",
    role: "technician",
    factory_id: DEMO_FACTORY.id,
    avatar_url: null,
    password: "demo123456",
  },
  {
    id: "u0000000-0000-4000-8000-000000000004",
    full_name: "Priya Singh",
    email: "tech2@demo.com",
    role: "technician",
    factory_id: DEMO_FACTORY.id,
    avatar_url: null,
    password: "demo123456",
  },
  {
    id: "u0000000-0000-4000-8000-000000000005",
    full_name: "Ahmed Hassan",
    email: "tech3@demo.com",
    role: "technician",
    factory_id: DEMO_FACTORY.id,
    avatar_url: null,
    password: "demo123456",
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
    "Verify ground connections are secure",
    "Test circuit breakers and fuses for proper rating",
    "Tighten all terminal connections to spec",
    "Close panel and restore power gradually",
    "Monitor for abnormal readings post-restoration",
  ],
  "Emergency Shutdown": [
    "Identify the emergency stop button location",
    "Press E-STOP button firmly until latched",
    "Verify all motion has ceased on the {unit}",
    "Turn main disconnect switch to OFF position",
    "Apply lockout/tagout devices to all energy sources",
    "Verify zero energy state with testing equipment",
    "Post warning signs at control stations",
    "Notify supervisor of emergency shutdown reason",
  ],
};

const AR_LABELS = [
  "Drain Plug",
  "Oil Filter",
  "Fill Port",
  "Belt Guard",
  "Tension Bolt",
  "Pulley A",
  "Bearing Housing",
  "Retaining Ring",
  "Motor Terminal",
  "Ground Wire",
  "E-STOP Button",
  "Main Disconnect",
];

function uuid(): string {
  return randomUUID();
}

function randomTool(index: number): string {
  return TOOLS[index % TOOLS.length];
}

function generateArMarker(stepIndex: number, label: string): ArMarker {
  const colors: ArMarker["color"][] = ["red", "green", "blue"];
  return {
    x: 15 + (stepIndex * 7) % 60,
    y: 20 + (stepIndex * 11) % 50,
    w: 12 + (stepIndex % 3) * 2,
    h: 8 + (stepIndex % 2) * 3,
    label,
    color: colors[stepIndex % 3],
  };
}

function generateSteps(procedureType: string, machineName: string): RepairStep[] {
  const templates = STEP_TEMPLATES[procedureType] || STEP_TEMPLATES["Oil Change"];
  return templates.map((template, i) => ({
    step: i + 1,
    instruction: template.replace("{unit}", machineName),
    tool_needed: randomTool(i + procedureType.length),
    safety: i === 0 || i % 3 === 0
      ? "Ensure lockout/tagout is applied before proceeding. Wear appropriate PPE."
      : "Keep hands clear of moving parts. Verify machine is de-energized.",
    ar_marker: generateArMarker(i, AR_LABELS[i % AR_LABELS.length]),
    requires_tool_verification: i > 0 && i % 2 === 0,
    is_dangerous: procedureType === "Emergency Shutdown" || i % 3 === 2,
  }));
}

const MACHINE_IMAGES_MAP: Record<string, string[]> = {
  "CNC Machine": ["/machines/cnc-machine.jpg"],
  "Water Pump": ["/machines/water-pump.jpg"],
  "Air Compressor": ["/machines/air-compressor.jpeg"],
  "Electric Motor": ["/machines/electric-motor.jpg"],
  "Diesel Generator": ["/machines/diesel-generator.jpg"],
  "Conveyor Belt": ["/machines/conveyor-belt.jpg"],
  "Hydraulic Press": ["/machines/hydraulic-press.jpg"],
  "Lathe Machine": ["/machines/lathe-machine.jpg", "/machines/cnc-machine.jpg"],
  "Welding Machine": ["/machines/welding-machine.jpg"],
  "Milling Machine": ["/machines/milling-machine.jpg"],
  "Boiler System": ["/machines/boiler-system.jpg"],
  "Cooling Tower": ["/machines/cooling-tower.jpg"],
  "Chiller Unit": ["/machines/chiller-unit.jpg"],
  "Forklift": ["/machines/forklift.jpg"],
  "Industrial Fan": ["/machines/industrial-fan.png"],
  "Pump Motor Assembly": ["/machines/pump-motor.jpg", "/machines/electric-motor.jpg"],
  "Pneumatic Cylinder": ["/machines/pneumatic-cylinder.jpg"],
  "Servo Drive": ["/machines/servo-drive.png"],
  "PLC Control Panel": ["/machines/plc-panel.jpg"],
  "Transformer": ["/machines/transformer.jpg"],
};

const PART_DEFS = [
  { name: "V-Belt A68", category: "Mechanical", supplier: "Gates Industrial", lead_time_days: 2, price: 45.00, image: "/parts/v-belt-a68.jpg", description: "Heavy-duty wrapped classical V-belt for industrial drive transmissions." },
  { name: "Oil Filter OF-200", category: "Consumable", supplier: "Donaldson Filtration", lead_time_days: 1, price: 28.50, image: "/parts/oil-filter-of-200.jpg", description: "High-efficiency spin-on hydraulic and lubricant oil filter element." },
  { name: "Ball Bearing 6205", category: "Mechanical", supplier: "SKF Bearings", lead_time_days: 3, price: 35.00, image: "/parts/ball-bearing-6205.jpg", description: "Deep groove single-row chrome steel ball bearing (25x52x15mm)." },
  { name: "Gasket Set GS-100", category: "Consumable", supplier: "Flexitallic Gaskets", lead_time_days: 2, price: 42.00, image: "/parts/gasket-set-gs-100.jpg", description: "Universal graphite & PTFE flange gasket replacement kit." },
  { name: "Hydraulic Seal HS-45", category: "Hydraulic", supplier: "Parker Hannifin", lead_time_days: 4, price: 125.00, image: "/parts/hydraulic-seal-hs-45.jpg", description: "High-pressure polyurethane rod/piston U-cup seal (45mm ID)." },
  { name: "Motor Coupling MC-12", category: "Mechanical", supplier: "Lovejoy Couplings", lead_time_days: 3, price: 89.00, image: "/parts/motor-coupling-mc-12.jpg", description: "Jaw-type flexible shaft elastomer coupling hub with spider insert." },
  { name: "Drive Belt DB-900", category: "Mechanical", supplier: "Continental ContiTech", lead_time_days: 2, price: 52.00, image: "/parts/drive-belt-db-900.jpg", description: "Synchronous toothed timing belt with high tensile fiberglass cords." },
  { name: "Air Filter AF-300", category: "Pneumatic", supplier: "Festo Pneumatics", lead_time_days: 1, price: 42.00, image: "/parts/air-filter-af-300.jpg", description: "Sintered bronze 5-micron compressed air particulate filter regulator." },
  { name: "Coolant Pump CP-55", category: "Hydraulic", supplier: "Grundfos Direct", lead_time_days: 5, price: 245.00, image: "/parts/coolant-pump-cp-55.jpg", description: "Submerged coolant & cutting fluid circulation pump (55 L/min)." },
  { name: "Fuse 32A", category: "Electrical", supplier: "Bussmann / Eaton", lead_time_days: 1, price: 18.00, image: "/parts/fuse-32a.jpg", description: "Industrial ceramic high-breaking capacity cartridge fuse (32A 500V)." },
  { name: "Contactor LC1D25", category: "Electrical", supplier: "Schneider Electric", lead_time_days: 2, price: 65.00, image: "/parts/contactor-lc1d25.jpg", description: "3-Pole 25A motor control magnetic AC contactor 24V coil." },
  { name: "Relay 24V DC", category: "Electrical", supplier: "Omron Automation", lead_time_days: 2, price: 22.00, image: "/parts/relay-24v-dc.jpg", description: "Miniature plug-in electromagnetic control relay with LED indicator." },
  { name: "Pressure Switch PS-100", category: "Pneumatic", supplier: "Danfoss Controls", lead_time_days: 3, price: 78.00, image: "/parts/pressure-switch-ps-100.jpg", description: "Adjustable range differential pressure switch 0-10 bar." },
  { name: "Temperature Sensor TS-200", category: "Electrical", supplier: "Endress+Hauser", lead_time_days: 3, price: 95.00, image: "/parts/temperature-sensor-ts-200.jpg", description: "PT100 RTD mineral-insulated probe sensor with terminal head." },
  { name: "Lubrication Grease LG-500", category: "Consumable", supplier: "Mobil Industrial", lead_time_days: 1, price: 35.00, image: "/parts/lubrication-grease-lg-500.jpg", description: "NLGI 2 extreme-pressure synthetic lithium complex grease (500g cartridge)." },
  { name: "Chain Link CL-38", category: "Mechanical", supplier: "Tsubaki Chain", lead_time_days: 2, price: 28.00, image: "/parts/chain-link-cl-38.jpg", description: "ANSI #40 master connecting roller chain link with spring clip." },
  { name: "Sprocket SP-24", category: "Mechanical", supplier: "Martin Sprocket", lead_time_days: 3, price: 55.00, image: "/parts/sprocket-sp-24.jpg", description: "24-Tooth hardened carbon steel roller chain sprocket (B-hub)." },
  { name: "Pulley PL-6", category: "Mechanical", supplier: "TB Wood's", lead_time_days: 3, price: 42.00, image: "/parts/pulley-pl-6.jpg", description: "6-inch cast iron single-groove A-section V-belt sheave pulley." },
  { name: "Shaft Seal SS-30", category: "Mechanical", supplier: "Timken Seals", lead_time_days: 2, price: 38.00, image: "/parts/shaft-seal-ss-30.jpg", description: "Rotary double-lip oil shaft seal with garter spring (30mm)." },
  { name: "O-Ring Kit OR-50", category: "Consumable", supplier: "Parker O-Rings", lead_time_days: 1, price: 45.00, image: "/parts/o-ring-kit-or-50.jpg", description: "386-Piece NBR 70 Shore A metric O-ring assortment case." },
  { name: "Terminal Block TB-12", category: "Electrical", supplier: "Phoenix Contact", lead_time_days: 2, price: 12.00, image: "/parts/terminal-block-tb-12.jpg", description: "DIN-rail feed-through spring cage terminal blocks (pack of 10)." },
  { name: "Cable Gland CG-25", category: "Electrical", supplier: "LAPP Group", lead_time_days: 2, price: 8.50, image: "/parts/cable-gland-cg-25.jpg", description: "Nickel-plated brass IP68 waterproof strain relief cable gland (M25)." },
  { name: "Limit Switch LS-10", category: "Electrical", supplier: "Honeywell Sensing", lead_time_days: 3, price: 32.00, image: "/parts/limit-switch-ls-10.jpg", description: "Heavy-duty roller lever enclosed position limit switch (1NO/1NC)." },
  { name: "Proximity Sensor PR-18", category: "Electrical", supplier: "IFM Efector", lead_time_days: 3, price: 85.00, image: "/parts/proximity-sensor-pr-18.jpg", description: "M18 Inductive proximity switch PNP normally open (8mm sensing)." },
  { name: "Encoder EN-1024", category: "Electrical", supplier: "Sick Sensor Intelligence", lead_time_days: 4, price: 185.00, image: "/parts/encoder-en-1024.jpg", description: "1024 PPR incremental optical rotary encoder with HTL output." },
  { name: "Servo Cable SC-5M", category: "Electrical", supplier: "Igus Motion Plastics", lead_time_days: 2, price: 120.00, image: "/parts/servo-cable-sc-5m.jpg", description: "5-Meter high-flex shielded power & feedback servo drive cable." },
  { name: "PLC Module IM-16", category: "Electrical", supplier: "Siemens Automation", lead_time_days: 4, price: 450.00, image: "/parts/plc-module-im-16.jpg", description: "16-Channel 24V DC digital input slice module for S7 system." },
  { name: "Transformer Fuse TF-63", category: "Electrical", supplier: "ABB Electrification", lead_time_days: 3, price: 25.00, image: "/parts/transformer-fuse-tf-63.jpg", description: "63A 12kV medium voltage current-limiting back-up fuse link." },
  { name: "Cooling Fan CF-120", category: "Mechanical", supplier: "ebm-papst", lead_time_days: 2, price: 68.00, image: "/parts/cooling-fan-cf-120.jpg", description: "120mm ball-bearing 230V AC cabinet ventilation exhaust fan." },
  { name: "Heating Element HE-3kW", category: "Electrical", supplier: "Watlow Thermal", lead_time_days: 4, price: 95.00, image: "/parts/heating-element-he-3kw.jpg", description: "3kW 415V Incoloy screw-plug industrial immersion heating element." },
  { name: "Welding Wire 0.8mm", category: "Consumable", supplier: "ESAB Welding", lead_time_days: 2, price: 28.00, image: "/parts/welding-wire-08mm.jpg", description: "0.8mm ER70S-6 copper-coated solid MIG welding wire (15kg spool)." },
  { name: "Welding Gas Cylinder", category: "Consumable", supplier: "Linde Gas", lead_time_days: 3, price: 180.00, image: "/parts/welding-gas-cylinder.jpg", description: "50L high-pressure Argon/CO2 shielding gas cylinder (200 bar)." },
  { name: "Cutting Tool Insert", category: "Consumable", supplier: "Sandvik Coromant", lead_time_days: 2, price: 15.00, image: "/parts/cutting-tool-insert.jpg", description: "TiAlN coated carbide indexable milling insert for steel & alloys." },
  { name: "End Mill 10mm", category: "Consumable", supplier: "Kennametal", lead_time_days: 2, price: 35.00, image: "/parts/end-mill-10mm.jpg", description: "10mm 4-flute solid carbide high-performance CNC end mill." },
  { name: "Forklift Tire 23x9-10", category: "Mechanical", supplier: "Continental Industrial", lead_time_days: 4, price: 285.00, image: "/parts/forklift-tire-23x9-10.jpg", description: "23x9-10 resilient solid rubber non-marking forklift drive tire." },
  { name: "Hydraulic Fluid 20L", category: "Consumable", supplier: "Shell Industrial", lead_time_days: 1, price: 145.00, image: "/parts/hydraulic-fluid-20l.jpg", description: "ISO VG 46 premium anti-wear hydraulic oil (20 Liter pail)." },
];

export function generateDemoMachines(): Machine[] {
  return MACHINE_DEFS.map((def, i) => {
    const images = MACHINE_IMAGES_MAP[def.name] || [
      "https://images.unsplash.com/photo-1581092335397-9583fe92d232?w=800&auto=format&fit=crop&q=80",
    ];

    return {
      id: uuid(),
      qr_code: def.qr,
      name: def.name,
      category: def.category,
      model: def.model,
      manufacturer: def.manufacturer,
      serial_number: `SN-${String(10000 + i).padStart(6, "0")}`,
      location: LOCATIONS[i % LOCATIONS.length],
      factory_id: DEMO_FACTORY.id,
      installed_date: `20${15 + (i % 8)}-${String((i % 12) + 1).padStart(2, "0")}-15`,
      image_url: images[0] || null,
      images: images.length > 0 ? images : null,
      thumbnail_url: images[0] || null,
      primary_image_index: 0,
      manual_url: `/manuals/${uuid()}`,
      specs: { power: `${5 + i}kW`, voltage: "415V", weight: `${100 + i * 50}kg` },
      status: i % 7 === 0 ? "maintenance" : i % 11 === 0 ? "broken" : "operational",
    };
  });
}

export function generateDemoProcedures(machines: Machine[]): RepairProcedure[] {
  const procedures: RepairProcedure[] = [];
  let procIndex = 0;

  for (const machine of machines) {
    for (const procedureType of PROCEDURE_TYPES) {
      procIndex++;
      const steps = generateSteps(procedureType, machine.name);
      procedures.push({
        id: uuid(),
        machine_id: machine.id,
        procedure_type: procedureType,
        estimated_minutes: 20 + (procIndex % 5) * 15,
        difficulty: procIndex % 3 === 0 ? "hard" : procIndex % 2 === 0 ? "medium" : "easy",
        steps,
        required_tools: Array.from(new Set(steps.map((s) => s.tool_needed))),
        safety_warnings: [
          "Always follow lockout/tagout procedures",
          "Wear safety glasses and gloves",
          "Never bypass safety interlocks",
        ],
      });
    }
  }
  return procedures;
}

export function generateDemoParts(machines: Machine[] = []): Part[] {
  return PART_DEFS.map((def, i) => {
    const images = [def.image];
    const compatible =
      machines.length > 0
        ? [machines[i % machines.length].id, machines[(i + 3) % machines.length].id]
        : [];

    return {
      id: uuid(),
      name: def.name,
      part_number: `PN-${String(1000 + i).padStart(5, "0")}`,
      category: def.category,
      stock_quantity: i % 4 === 0 ? 2 : i % 3 === 0 ? 4 : 15 + ((i * 3) % 40),
      min_stock_level: 5,
      unit_price: def.price ?? (12.5 + i * 7.25),
      image_url: images[0] || null,
      images: images.length > 0 ? images : null,
      thumbnail_url: images[0] || null,
      primary_image_index: 0,
      supplier: def.supplier,
      lead_time_days: def.lead_time_days,
      description: def.description,
      compatible_machines: compatible,
    };
  });
}

export function generateDemoLogs(
  machines: Machine[],
  procedures: RepairProcedure[],
  technicians: Profile[]
): MaintenanceLog[] {
  const logs: MaintenanceLog[] = [];
  const techProfiles = technicians.filter((t) => t.role === "technician");
  const now = Date.now();

  for (let i = 0; i < 55; i++) {
    const machine = machines[i % machines.length];
    const machineProcs = procedures.filter((p) => p.machine_id === machine.id);
    const procedure = machineProcs[i % machineProcs.length];
    const tech = techProfiles[i % techProfiles.length];
    const daysAgo = Math.floor(Math.random() * 90);
    const started = new Date(now - daysAgo * 86400000 - Math.random() * 86400000);
    const duration = 15 + Math.floor(Math.random() * 90);
    const completed = new Date(started.getTime() + duration * 60000);
    const status = i % 8 === 0 ? "in_progress" : i % 12 === 0 ? "abandoned" : "completed";

    logs.push({
      id: uuid(),
      machine_id: machine.id,
      technician_id: tech.id,
      procedure_id: procedure?.id ?? null,
      started_at: started.toISOString(),
      completed_at: status === "completed" ? completed.toISOString() : null,
      duration_minutes: status === "completed" ? duration : null,
      status,
      notes: status === "completed" ? "Routine maintenance completed successfully." : null,
      machine,
      procedure,
      technician: tech,
    });
  }
  return logs.sort(
    (a, b) => new Date(b.started_at).getTime() - new Date(a.started_at).getTime()
  );
}

export function generateDemoFaults(machines: Machine[], reporters: Profile[]): FaultReport[] {
  const severities: FaultReport["severity"][] = ["low", "medium", "high", "critical"];
  const statuses: FaultReport["status"][] = ["open", "assigned", "in_progress", "resolved"];
  const descriptions = [
    "Unusual vibration detected during operation",
    "Oil leak observed near pump housing",
    "Motor overheating after 2 hours runtime",
    "Emergency stop triggered unexpectedly",
    "Abnormal noise from bearing assembly",
    "Conveyor belt slipping under load",
    "PLC communication error on HMI",
    "Pressure drop below minimum threshold",
  ];

  return descriptions.map((desc, i) => {
    const status = statuses[i % statuses.length];
    const severity = severities[i % severities.length];
    const isAssigned = status === "assigned" || status === "in_progress" || status === "resolved";
    
    // Calculate due date based on severity
    const hoursMap: Record<string, number> = { critical: 4, high: 24, medium: 48, low: 72 };
    const hours = severity ? (hoursMap[severity] || 48) : 48;
    const dueDate = new Date(Date.now() + hours * 60 * 60 * 1000);
    
    return {
      id: uuid(),
      machine_id: machines[i % machines.length].id,
      reported_by: reporters[i % reporters.length].id,
      assigned_to: isAssigned ? reporters[(i + 1) % reporters.length].id : null,
      description: desc,
      severity: severity,
      ai_diagnosis: null,
      ai_detection_results: null,
      status: status,
      attachments: [],
      assigned_at: isAssigned ? new Date(Date.now() - i * 3600000).toISOString() : null,
      due_date: isAssigned ? dueDate.toISOString() : null,
      created_at: new Date(Date.now() - i * 86400000 * 2).toISOString(),
      machine: machines[i % machines.length],
    };
  });
}

const machines = generateDemoMachines();
const procedures = generateDemoProcedures(machines);
const parts = generateDemoParts(machines);
const profiles = DEMO_USERS.map(({ password, ...p }) => {
  void password;
  return p;
});
const logs = generateDemoLogs(machines, procedures, profiles);
const faults = generateDemoFaults(machines, profiles);

export const DEMO_DATA = {
  factory: DEMO_FACTORY,
  users: DEMO_USERS,
  profiles,
  machines,
  procedures,
  parts,
  logs,
  faults,
};

export function getMachineById(id: string): Machine | null {
  return DEMO_DATA.machines.find((m) => m.id === id) || null;
}

export function getMachineByQr(qrCode: string): Machine | null {
  return DEMO_DATA.machines.find(
    (m) => m.qr_code === qrCode || m.qr_code.endsWith(qrCode.replace("MACHINE:", ""))
  ) || null;
}

export function getProceduresForMachine(machineId: string): RepairProcedure[] {
  return DEMO_DATA.procedures.filter((p) => p.machine_id === machineId);
}

export function getProcedureById(id: string): RepairProcedure | null {
  return DEMO_DATA.procedures.find((p) => p.id === id) || null;
}

export function isSupabaseConfigured(): boolean {
  return Boolean(
    process.env.NEXT_PUBLIC_SUPABASE_URL &&
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY &&
      !process.env.NEXT_PUBLIC_SUPABASE_URL.includes("placeholder") &&
      !process.env.NEXT_PUBLIC_SUPABASE_URL.includes("your-")
  );
}

export function isFirebaseConfigured(): boolean {
  return Boolean(
    process.env.NEXT_PUBLIC_FIREBASE_API_KEY &&
      process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID &&
      !process.env.NEXT_PUBLIC_FIREBASE_API_KEY.includes("your-") &&
      !process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID.includes("your-")
  );
}

export function getDashboardStats() {
  const operational = DEMO_DATA.machines.filter((m) => m.status === "operational").length;
  const total = DEMO_DATA.machines.length;
  const thisMonth = DEMO_DATA.logs.filter((l) => {
    const d = new Date(l.started_at);
    const now = new Date();
    return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear();
  });
  const completedLogs = DEMO_DATA.logs.filter((l) => l.status === "completed" && l.duration_minutes);
  const avgTime =
    completedLogs.length > 0
      ? Math.round(
          completedLogs.reduce((s, l) => s + (l.duration_minutes ?? 0), 0) / completedLogs.length
        )
      : 0;
  const lowStock = DEMO_DATA.parts.filter((p) => p.stock_quantity < p.min_stock_level);

  return {
    totalMachines: total,
    operationalPercent: Math.round((operational / total) * 100),
    activeTechnicians: DEMO_DATA.profiles.filter((p) => p.role === "technician").length,
    repairsThisMonth: thisMonth.length,
    avgRepairTime: avgTime,
    pendingFaults: DEMO_DATA.faults.filter((f) => f.status === "open").length,
    lowStockParts: lowStock.length,
    lowStockItems: lowStock,
  };
}

export function getFailureByCategory() {
  const categories = new Map<string, number>();
  DEMO_DATA.faults.forEach((f) => {
    const cat = f.machine?.category ?? "Unknown";
    categories.set(cat, (categories.get(cat) ?? 0) + 1);
  });
  return Array.from(categories.entries()).map(([category, count]) => ({ category, count }));
}

export function getDowntimeTrend() {
  const days: { date: string; hours: number }[] = [];
  for (let i = 29; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const dateStr = d.toISOString().split("T")[0];
    const dayLogs = DEMO_DATA.logs.filter((l) => l.started_at.startsWith(dateStr));
    days.push({ date: dateStr, hours: dayLogs.length * 0.5 + Math.random() * 2 });
  }
  return days;
}

export function getTechnicianLeaderboard() {
  const techs = DEMO_DATA.profiles.filter((p) => p.role === "technician");
  return techs
    .map((t) => ({
      name: t.full_name,
      repairs: DEMO_DATA.logs.filter((l) => l.technician_id === t.id && l.status === "completed").length,
    }))
    .sort((a, b) => b.repairs - a.repairs);
}
