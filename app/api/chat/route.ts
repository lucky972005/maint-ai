import { NextResponse } from "next/server";
import { generateTextResponse, isAIConfigured } from "@/lib/ai";

export const dynamic = "force-dynamic";

interface FixBotResult {
  message: string;
  suggestions: string[];
}

function getStructuredIndustrialResponse(query: string, machineContext?: string): FixBotResult {
  const q = query.toLowerCase().trim();
  const machine = machineContext ? machineContext.trim() : "";
  const machinePrefix = machine ? `Regarding your **${machine}**:\n\n` : "";

  // A. EXPLICIT "TALK NORMALLY" / CASUAL CHAT REQUEST
  if (
    q.includes("talk normal") ||
    q.includes("talk normally") ||
    q.includes("speak normal") ||
    q.includes("speak normally") ||
    q.includes("talk like a human") ||
    q.includes("speak like a human") ||
    q.includes("talk like normal") ||
    q.includes("chat normally") ||
    q.includes("can you talk normally") ||
    q.includes("can we talk normally") ||
    q.includes("talk casual") ||
    q.includes("talk casually") ||
    q.includes("act normal")
  ) {
    return {
      message:
        `**Yes, absolutely!** I can chat with you just like a normal colleague or friend. We definitely don't have to talk in rigid 5-step Lockout/Tagout manuals every time!\n\n` +
        `I can do both seamlessly:\n` +
        `- **Casual & Normal Conversation:** We can talk about how your shift is going, discuss everyday shop floor situations, share maintenance tips, or just have a friendly chat.\n` +
        `- **Deep Engineering Specs & Repairs:** Whenever an actual machine breaks down and you need exact torque specs (Nm), 3-phase wiring color codes, vibration tolerances, or LOTO procedures, I've got you covered with authoritative precision.\n\n` +
        `So, how are things going with you today? What's on your mind?`,
      suggestions: [
        "How are you doing today?",
        "What can you do?",
        "Tell me about MaintAI",
      ],
    };
  }

  // B. GREETINGS & CASUAL HELLOS
  const isGreetingOnly =
    q === "hi" ||
    q === "hello" ||
    q === "hey" ||
    q === "yo" ||
    q === "sup" ||
    q === "howdy" ||
    q === "greetings" ||
    q === "hi there" ||
    q === "hello there" ||
    q === "hey there" ||
    q === "hi fixbot" ||
    q === "hello fixbot" ||
    q === "hey fixbot" ||
    q === "good morning" ||
    q === "good afternoon" ||
    q === "good evening";

  if (isGreetingOnly) {
    const greetingMachine = machine ? ` I see you're checked into **${machine}**.` : "";
    return {
      message:
        `Hey there! Great to see you.${greetingMachine} I'm FixBot, your plant maintenance copilot.\n\n` +
        `I'm here to make your shift smoother—whether you want to chat normally, brainstorm an equipment question, look up torque specs and wiring diagrams, or check spare parts in inventory.\n\n` +
        `How's your day going, and what can I help you with today?`,
      suggestions: [
        "What can you do?",
        "Why is my motor overheating?",
        "What's the torque spec?",
      ],
    };
  }

  // C. "HOW ARE YOU" / STATUS INQUIRIES
  if (
    q.includes("how are you") ||
    q.includes("how r u") ||
    q.includes("how are u") ||
    q.includes("how's it going") ||
    q.includes("hows it going") ||
    q.includes("how is it going") ||
    q.includes("how are you doing") ||
    q.includes("what's up") ||
    q.includes("whats up") ||
    q.includes("how do you feel") ||
    q.includes("how's your day") ||
    q.includes("how is your day")
  ) {
    return {
      message:
        `I'm doing great, thank you for asking! All diagnostic routines, telemetry channels, and parts databases are running at 100%.\n\n` +
        `More importantly, how are things going on your end of the facility today? Keeping up with the work orders, or is anything acting up on the line?`,
      suggestions: [
        "Can you talk normally?",
        "Why is my motor overheating?",
        "Show wiring diagram",
      ],
    };
  }

  // D. IDENTITY / CAPABILITIES ("WHO ARE YOU", "WHAT CAN YOU DO")
  if (
    q.includes("who are you") ||
    q.includes("what are you") ||
    q.includes("what is your name") ||
    q.includes("whats your name") ||
    q.includes("introduce yourself") ||
    q.includes("tell me about yourself") ||
    q.includes("what can you do") ||
    q.includes("what do you do") ||
    q.includes("what are your capabilities")
  ) {
    return {
      message:
        `I'm **FixBot**, your dedicated AI maintenance assistant and plant reliability copilot!\n\n` +
        `Think of me as an experienced senior maintenance tech who's always on shift with you. Here is what I can do:\n\n` +
        `- **Chat Normally:** You can talk with me like a regular human colleague—casual conversation, daily shift check-ins, or bouncing maintenance ideas back and forth.\n` +
        `- **Machine Diagnostics:** Describe any issue—such as overheating motors, squealing belts, leaking hydraulics, or tripped breakers—and I'll diagnose probable root causes.\n` +
        `- **Exact Engineering Specs:** I know ISO metric bolt torque values (Nm), 3-phase electrical wiring standards, belt tensioning deflection specs, and ISO vibration limits.\n` +
        `- **Step-by-Step Action Plans:** Clear, numbered procedures with safety Lockout/Tagout (LOTO) protocols.\n` +
        `- **Parts Catalog & Inventory:** I can help you locate OEM replacement components from our 36-part warehouse catalog.\n\n` +
        `Feel free to ask me anything—casual conversation or complex machine questions!`,
      suggestions: [
        "Can you talk normally?",
        "Why is my motor overheating?",
        "What's the torque spec?",
      ],
    };
  }

  // E. GRATITUDE / COMPLIMENTS / PRAISE
  if (
    q === "thanks" ||
    q === "thank you" ||
    q === "thx" ||
    q.startsWith("thanks") ||
    q.startsWith("thank you") ||
    q.includes("appreciate it") ||
    q.includes("great job") ||
    q.includes("good job") ||
    q.includes("awesome") ||
    q.includes("nice work") ||
    q.includes("well done") ||
    q.includes("you are great") ||
    q.includes("you rock") ||
    q.includes("perfect")
  ) {
    return {
      message:
        `You're very welcome! Always happy to help out. Keeping the plant running safely and efficiently is always a team effort.\n\n` +
        `Let me know if you need anything else, or if another machine starts giving you trouble!`,
      suggestions: [
        "What's the torque spec?",
        "How do I replace the belt?",
        "Show safety warnings",
      ],
    };
  }

  // F. FAREWELLS / SIGN-OFF
  if (
    q === "bye" ||
    q === "goodbye" ||
    q === "cya" ||
    q === "see you" ||
    q === "see ya" ||
    q.includes("have a good day") ||
    q.includes("have a nice day") ||
    q.includes("good night") ||
    q.includes("take care") ||
    q.includes("catch you later") ||
    q.includes("signing off")
  ) {
    return {
      message:
        `Take care and have a safe, productive rest of your shift! Remember to tag out your equipment, stow your tools, and stay safe on the floor.\n\n` +
        `Whenever you need a hand, just open FixBot—I'll be right here!`,
      suggestions: [
        "Hi FixBot",
        "What can you do?",
      ],
    };
  }

  // G. HUMOR & JOKES
  if (
    q.includes("joke") ||
    q.includes("make me laugh") ||
    q.includes("funny")
  ) {
    return {
      message:
        `Here's an industrial engineering classic for you:\n\n` +
        `*Why did the maintenance technician marry the calibrated torque wrench?*\n` +
        `*Because the moment things were just right, it clicked!* 🔧\n\n` +
        `Got any machines acting up on the shop floor today, or should we keep the good vibes going?`,
      suggestions: [
        "Tell me another joke",
        "Why is my motor overheating?",
        "What's the torque spec?",
      ],
    };
  }

  // H. FATIGUE / BREAK TIME / COFFEE
  if (
    q.includes("tired") ||
    q.includes("exhausted") ||
    q.includes("coffee") ||
    q.includes("break time") ||
    q.includes("lunch") ||
    q.includes("long day") ||
    q.includes("rough day") ||
    q.includes("hard day")
  ) {
    return {
      message:
        `I hear you! Plant shifts can be tough, especially when equipment throws unexpected curveballs.\n\n` +
        `Take your well-deserved break, grab some coffee or water, and recharge. Safety always comes first—fatigue is when workshop slip-ups happen, so don't rush through any high-voltage or heavy mechanical tasks.\n\n` +
        `Take it easy, and I'll be right here whenever you're ready to jump back in!`,
      suggestions: [
        "Tell me a joke",
        "Can you talk normally?",
        "Show safety warnings",
      ],
    };
  }

  // I. ABOUT MAINTAI PLATFORM
  if (
    q.includes("what is maintai") ||
    q.includes("about maintai") ||
    q.includes("what is this platform") ||
    q.includes("what is this website") ||
    q.includes("what is this app") ||
    q.includes("tell me about maintai") ||
    q.includes("what can this app do")
  ) {
    return {
      message:
        `**MaintAI** is an intelligent next-generation maintenance and reliability operations platform designed for modern manufacturing facilities!\n\n` +
        `Here are the core features at your fingertips:\n` +
        `- **FixBot Copilot:** Expert diagnostic assistant (that's me!) for real-time troubleshooting, torque specs, wiring schematics, and LOTO safety.\n` +
        `- **Computer Vision & AR Inspection:** AI photo analysis of worn components, oil leaks, and thermal anomalies directly from your camera.\n` +
        `- **Smart Parts & Inventory:** 36 verified OEM replacement components with real photographs, real-time stock levels, and instant Code128 barcode generation.\n` +
        `- **Machine Health & Telemetry:** Live machine operational status, health scores, vibration monitoring, and work order assignment.\n\n` +
        `Which section would you like to explore?`,
      suggestions: [
        "Show parts inventory",
        "Why is my motor overheating?",
        "What's the torque spec?",
      ],
    };
  }

  // J. GENERAL HELP / GUIDANCE
  if (
    q === "help" ||
    q === "can you help me" ||
    q === "i need help" ||
    q.includes("what should i do") ||
    q.includes("how do i use this")
  ) {
    return {
      message:
        `I'm ready to help! What are you working on right now?\n\n` +
        `You can:\n` +
        `1. **Talk normally:** Ask me casual questions or bounce an idea around.\n` +
        `2. **Describe a machine symptom:** For example, *"motor is overheating"*, *"pump has gravel noise"*, or *"cylinder is leaking"*.\n` +
        `3. **Ask for engineering data:** Like *"what is the torque spec for M12 bolts?"* or *"show 3-phase wire colors"*.\n` +
        `4. **Check parts:** Ask about replacement parts like bearings, belts, filters, or contactors in our inventory.\n\n` +
        `Just type whatever you need!`,
      suggestions: [
        "Why is my motor overheating?",
        "What's the torque spec?",
        "Show wiring diagram",
      ],
    };
  }

  // 1. MOTOR OVERHEATING / TEMPERATURE
  if (
    q.includes("overheat") ||
    q.includes("motor overheat") ||
    q.includes("temperature") ||
    q.includes("thermal") ||
    q.includes("too hot") ||
    q.includes("burning smell")
  ) {
    return {
      message:
        `${machinePrefix}**Thermal Diagnostic: Abnormal Motor Overheating**\n\n` +
        `Motor surface temperatures above 80°C or thermal overload tripping are commonly driven by restricted airflow, continuous over-amperage, or mechanical resistance in the driveline.\n\n` +
        `1. **Isolate and Lockout:** Engage Lockout/Tagout (LOTO) on the main breaker and verify zero electrical energy with a multimeter before touching the housing.\n` +
        `2. **Inspect Ventilation & Fan Shroud:** Remove fan cowl. Clean packed debris, swarf, or oil sludge from cooling fins and fan impeller blades.\n` +
        `3. **Test Phase Resistance & Amperage:** Measure phase-to-phase winding resistance with a calibrated multimeter (variance must be <2%). Verify running current against nameplate Full Load Amps (FLA).\n` +
        `4. **Check Bearing Condition:** Rotate the shaft by hand. Listen for metallic clicking or grinding. Check for radial play; worn bearings generate severe frictional heat.\n` +
        `5. **Verify Ambient & Duty Cycle:** Ensure operating ambient is <40°C and ventilation is unblocked.\n\n` +
        `**Specifications & Tolerances:**\n` +
        `- **Max Temperature Rise:** Class F insulation allows 105°C rise above ambient (max total 145°C)\n` +
        `- **Winding Insulation Resistance:** >1.0 MΩ at 500V DC test (IEEE 43 standard)\n` +
        `- **Phase Current Balance:** Winding current imbalance must not exceed 5%\n` +
        `- **Motor Foot Bolt Torque (M8):** 25 - 30 Nm\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** Calibrated Digital Multimeter, Infrared Thermal Camera / Laser Pyrometer, Torque Wrench, Fan Shroud Screwdriver\n` +
        `- **Parts:** Ball Bearing 6205 (PN-01002), Cooling Fan CF-120 (PN-01027), Motor Coupling MC-12 (PN-01004)\n\n` +
        `**Safety Warning:** Thermal burn hazard! Motor housing can exceed 90°C. Allow minimum 30 minutes cooldown before physical contact. Never defeat thermal overload relays.`,
      suggestions: [
        "What's the torque spec?",
        "How do I test with a multimeter?",
        "Show bearing replacement procedure",
      ],
    };
  }

  // 2. TORQUE SPECIFICATIONS
  if (
    q.includes("torque") ||
    q.includes("tighten") ||
    q.includes("bolt spec") ||
    q.includes("fastener") ||
    q.includes("ft-lb") ||
    q.includes("nm")
  ) {
    return {
      message:
        `${machinePrefix}**Fastener Engineering: Standard Industrial Torque Specifications**\n\n` +
        `Standard metric ISO 898-1 bolt torque values (Grade 8.8 medium-carbon steel, zinc-plated or lightly lubricated threads):\n\n` +
        `1. **M6 Bolts:** 10 - 12 Nm (7.4 - 8.8 ft-lbs)  -  Sheet metal guards, small sensor brackets, terminal covers\n` +
        `2. **M8 Bolts:** 25 - 30 Nm (18.5 - 22.1 ft-lbs)  -  Motor faceplates, pump end-shields, small pillow blocks\n` +
        `3. **M10 Bolts:** 45 - 50 Nm (33.2 - 36.9 ft-lbs)  -  Machine base mounting, gearbox brackets, heavy pipe flanges\n` +
        `4. **M12 Bolts:** 75 - 85 Nm (55.3 - 62.7 ft-lbs)  -  Structural motor feet, heavy press bolsters, main frame connections\n` +
        `5. **M16 Bolts:** 180 - 200 Nm (133 - 148 ft-lbs)  -  Foundation anchor studs, crane rails, heavy hydraulic cylinders\n` +
        `6. **Electrical Terminal Screws:** 0.5 - 0.8 Nm (M3/M3.5 control blocks), 2.5 - 3.0 Nm (M5/M6 contactor power lugs)\n\n` +
        `**Tightening Best Practices:**\n` +
        `- **3-Stage Torquing:** Tighten in star/cross pattern at 30% → 70% → 100% of target torque to eliminate flange distortion\n` +
        `- **Thread Condition:** Clean threads with wire brush; apply medium-strength threadlocker (Loctite 242/243) where vibration occurs\n` +
        `- **Belt Tension:** 15 - 20 lbs deflection force at span center (~1% deflection distance)\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** 1/2" and 3/8" Drive Calibrated Click Torque Wrenches, Hex Bit Sockets, Calibrated Dial Indicator\n` +
        `- **Parts:** Terminal Block TB-12 (PN-01019), Motor Coupling MC-12 (PN-01004)\n\n` +
        `**Safety Warning:** Never use impact guns for final torquing. Over-torqued fasteners yield and shear under dynamic cyclic loads.`,
      suggestions: [
        "How do I replace the belt?",
        "Show motor overheating causes",
        "What tools do I need?",
      ],
    };
  }

  // 3. WIRING DIAGRAM & ELECTRICAL INSPECTION
  if (
    q.includes("wiring") ||
    q.includes("wire") ||
    q.includes("diagram") ||
    q.includes("schematic") ||
    q.includes("electrical") ||
    q.includes("phase") ||
    q.includes("short circuit")
  ) {
    return {
      message:
        `${machinePrefix}**Electrical Schematic & Wiring Architecture Standards**\n\n` +
        `Industrial 3-Phase 415V/480V and 24V DC Control Wiring Standard (IEC 60204-1 / NFPA 79):\n\n` +
        `1. **Main 3-Phase Power Rails:**\n` +
        `   - **Line 1 (L1 / U):** Brown (IEC) or Black (NEC)\n` +
        `   - **Line 2 (L2 / V):** Black (IEC) or Red (NEC)\n` +
        `   - **Line 3 (L3 / W):** Grey (IEC) or Blue (NEC)\n` +
        `   - **Neutral (N):** Light Blue (IEC) or White (NEC)\n` +
        `   - **Protective Earth (PE / Ground):** Green-Yellow dual stripe  -  continuous bonding <0.1 Ω\n` +
        `2. **24V DC Control Circuits:**\n` +
        `   - **+24V DC Positive:** Dark Blue or Red\n` +
        `   - **0V DC Common:** Dark Blue with White stripe or Black\n` +
        `   - **Interlock / Safety Chain:** Yellow (indicates external source remain-live hazard)\n` +
        `3. **Step-by-Step Electrical Verification:**\n` +
        `   - Open main disconnect and attach personal padlock\n` +
        `   - Test voltage: L1-L2, L2-L3, L3-L1 (<3V residual before servicing)\n` +
        `   - Verify terminal torque (0.5 - 0.8 Nm for control, 2.5 - 3.0 Nm for power)\n` +
        `   - Check contactor coil suppressor diode / varistor to prevent inductive back-EMF spikes\n\n` +
        `**Specifications & Tolerances:**\n` +
        `- **Insulation Resistance:** >1.0 MΩ at 500V DC test (megohmmeter)\n` +
        `- **Control Voltage Tolerance:** 24V DC +/-10% (21.6V - 26.4V range)\n` +
        `- **Phase-to-Phase Voltage Balance:** <2% voltage unbalance between phases\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** CAT-III/IV 1000V True-RMS Digital Multimeter, Insulated 1000V Screwdrivers, Wire Ferrule Crimper\n` +
        `- **Parts:** Contactor LC1D25 (PN-01009), Relay 24V DC (PN-01010), Fuse 32A (PN-01008), Terminal Block TB-12 (PN-01019)\n\n` +
        `**Safety Warning:** Arc Flash & Lethal Voltage hazard! Only certified personnel in NFPA 70E PPE should open live electrical cabinets. Always prove test equipment on a known live source before and after zero-energy testing.`,
      suggestions: [
        "Why is my motor overheating?",
        "What's the torque spec?",
        "How do I test a 24V relay?",
      ],
    };
  }

  // 4. BELTS, DRIVES & PULLEYS
  if (
    q.includes("belt") ||
    q.includes("v-belt") ||
    q.includes("timing belt") ||
    q.includes("pulley") ||
    q.includes("sheave") ||
    q.includes("slipping") ||
    q.includes("squeal")
  ) {
    return {
      message:
        `${machinePrefix}**Mechanical Drive Transmission: Belt Replacement & Tensioning**\n\n` +
        `Drive belt slipping, chirping, or glazed rubber indicates loss of tension, pulley misalignment, or oil contamination on friction surfaces.\n\n` +
        `1. **Lockout Machine:** De-energize and lock main electrical disconnect. Verify zero energy.\n` +
        `2. **Relieve Tension:** Loosen motor mounting base fasteners and turn belt tensioning jackscrew counter-clockwise.\n` +
        `3. **Remove & Inspect:** Slip old belt off pulleys. Inspect pulley V-grooves for dishing or scoring. Replace if sidewall wear exceeds 0.8 mm.\n` +
        `4. **Install New Belt:** Place replacement belt (e.g., V-Belt A68 or Drive Belt DB-900) into grooves by hand. NEVER pry with a screwdriver as prying fractures internal tensile cords.\n` +
        `5. **Align Sheaves:** Check parallel and angular alignment using a precision straightedge or laser tool (<0.5° tolerance).\n` +
        `6. **Tension to Specification:** Adjust jackscrew until midpoint deflection equals 1/64" per inch of span under 15-20 lbs pressure.\n` +
        `7. **Test Run:** Replace guards, run for 15 minutes, shut down, and re-check tension.\n\n` +
        `**Specifications & Tolerances:**\n` +
        `- **Target Deflection Force:** 15 - 20 lbs (68 - 90 N) at belt span midpoint\n` +
        `- **Pulley Angular Alignment:** <0.5 degrees maximum angular error\n` +
        `- **Pulley Parallel Offset:** <1.5 mm (1/16") maximum parallel offset\n` +
        `- **Motor Mounting Bolt Torque (M10):** 45 - 50 Nm\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** Belt Tension Gauge, Precision Aluminum Straightedge, Socket Set, Open-End Wrenches\n` +
        `- **Parts:** V-Belt A68 (PN-01000), Drive Belt DB-900 (PN-01005), Pulley PL-6 (PN-01016)\n\n` +
        `**Safety Warning:** Rotating pinch point hazard! Never operate equipment with belt guards removed. Never reach toward belts while the shaft is coasting.`,
      suggestions: [
        "What's the torque spec?",
        "Why is there excessive vibration?",
        "Show safety warnings",
      ],
    };
  }

  // 5. VIBRATION, UNBALANCE & ALIGNMENT
  if (
    q.includes("vibrat") ||
    q.includes("shak") ||
    q.includes("wobbl") ||
    q.includes("unbalance") ||
    q.includes("imbalance") ||
    q.includes("rattle") ||
    q.includes("chatter")
  ) {
    return {
      message:
        `${machinePrefix}**Dynamic Diagnostics: Machinery Vibration & Unbalance Analysis**\n\n` +
        `Excessive vibration accelerates bearing fatigue, destroys shaft seals, and causes structural fastener loosening. Vibration frequencies reveal the root cause:\n\n` +
        `1. **1X RPM Frequency (Unbalance):** Caused by dirt buildup on fan/impeller, lost balance weights, or bent shaft.\n` +
        `2. **2X RPM Frequency (Misalignment / Soft Foot):** Caused by angular or offset misalignment across the flexible coupling.\n` +
        `3. **High Frequency (>10X RPM):** Indicates bearing raceway micro-spalling or gear mesh tooth pitting.\n\n` +
        `**Step-by-Step Rectification:**\n` +
        `1. **Check Base Mounting (Soft Foot):** Loosen one hold-down bolt at a time with a dial indicator mounted on the foot. Any foot lifting >0.05 mm must be shimmed with precision stainless shims.\n` +
        `2. **Inspect Coupling Spider:** Remove coupling guard. Inspect Motor Coupling MC-12 red polyurethane spider for chunking, backlash, or extrusion.\n` +
        `3. **Perform Laser Alignment:** Align motor and pump/driven shaft to <0.05 mm radial and axial offset.\n` +
        `4. **Clean Rotating Elements:** Scrape encrusted coolant scale, resin, or debris from impellers and fan hubs.\n\n` +
        `**Specifications & Tolerances (ISO 10816-3):**\n` +
        `- **Zone A (Good):** <1.4 mm/s RMS vibration velocity\n` +
        `- **Zone B (Acceptable):** 1.4 - 2.8 mm/s RMS\n` +
        `- **Zone C (Alert / Action Required):** 2.8 - 4.5 mm/s RMS\n` +
        `- **Zone D (Danger / Immediate Shutdown):** >7.1 mm/s RMS\n` +
        `- **Total Shaft Radial Runout (TIR):** <0.025 mm\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** Digital Vibration Pen / Triaxial Accelerometer, Dial Test Indicator with Magnetic Base, Stainless Shim Kit (0.05-1.0 mm)\n` +
        `- **Parts:** Motor Coupling MC-12 (PN-01004), Ball Bearing 6205 (PN-01002), V-Belt A68 (PN-01000)\n\n` +
        `**Safety Warning:** Running equipment above 7.1 mm/s vibration risks catastrophic fatigue fracture of shafts and thrown components. Shut down immediately if severe shaking begins.`,
      suggestions: [
        "What's the torque spec?",
        "Show bearing replacement procedure",
        "How do I check coupling alignment?",
      ],
    };
  }

  // 6. BEARINGS & NOISE
  if (
    q.includes("bearing") ||
    q.includes("6205") ||
    q.includes("grinding noise") ||
    q.includes("humming") ||
    q.includes("shaft play")
  ) {
    return {
      message:
        `${machinePrefix}**Rotating Equipment: Bearing Inspection & Replacement Protocol**\n\n` +
        `High-pitched squealing, growling, or radial play in standard deep groove ball bearings (e.g. SKF 6205-2RS) indicates fatigue spalling, contaminated grease, or lack of lubricant.\n\n` +
        `1. **Lockout & Disassemble:** De-energize machine (LOTO). Remove drive belts, motor coupling hub, and bearing housing end-cover.\n` +
        `2. **Remove Retaining Rings:** Use snap-ring pliers to unseat external shaft circlips without gouging the shaft seat.\n` +
        `3. **Extract Bearing with Puller:** Anchor 3-jaw mechanical puller onto inner ring. Apply uniform pressure. NEVER apply puller force across balls/outer ring.\n` +
        `4. **Clean & Inspect Journal:** Clean shaft journal with solvent. Measure diameter with micrometer (25.000 mm +0.015/+0.002 mm for m5/k5 fit).\n` +
        `5. **Mount Replacement Bearing:** Heat new Ball Bearing 6205 on an induction bearing heater to 110°C (230°F) and slide onto journal until seated squarely against shoulder.\n` +
        `6. **Lubricate:** If open bearing, pack 30-40% free volume with NLGI 2 lithium complex grease (Lubrication Grease LG-500). If sealed (-2RS), pre-lubricated for life.\n\n` +
        `**Specifications & Tolerances (6205-2RS):**\n` +
        `- **Dimensions:** 25 mm Bore (ID) × 52 mm Outer Diameter (OD) × 15 mm Width\n` +
        `- **Dynamic Load Rating (C):** 14.8 kN\n` +
        `- **Radial Internal Clearance (CN/C3):** 5 - 20 um (C3: 13 - 28 um for thermal expansion)\n` +
        `- **Max Operating Temperature:** 120°C with standard nitrile rubber contact seals\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** 3-Jaw Bearing Puller, Induction Bearing Heater or Arbor Press, Internal/External Snap Ring Pliers, Outside Micrometer\n` +
        `- **Parts:** Ball Bearing 6205-2RS (PN-01002), Shaft Seal SS-30 (PN-01017), Lubrication Grease LG-500 (PN-01013)\n\n` +
        `**Safety Warning:** Snap rings can spring out at high velocity. Always wear ANSI approved safety goggles during removal and installation. Never strike a bearing with a steel hammer.`,
      suggestions: [
        "What's the torque spec?",
        "What type of grease should I use?",
        "Why is my motor overheating?",
      ],
    };
  }

  // 7. OIL, LUBRICATION & GREASING
  if (
    q.includes("oil") ||
    q.includes("lubricat") ||
    q.includes("grease") ||
    q.includes("lube") ||
    q.includes("oil change") ||
    q.includes("viscosity")
  ) {
    return {
      message:
        `${machinePrefix}**Tribology & Lubrication Management Protocol**\n\n` +
        `Proper lubrication maintains hydrodynamic film thickness, prevents metal-to-metal boundary contact, and carries away heat and microscopic wear particulates.\n\n` +
        `1. **Hydraulic Systems:** Use ISO VG 46 or ISO VG 68 anti-wear hydraulic oil (Hydraulic Fluid 20L). Change fluid every 2,000-4,000 operating hours or when acid number (TAN) rises >0.5 mg KOH/g.\n` +
        `2. **Grease Bearings:** Use NLGI Grade 2 extreme-pressure synthetic lithium complex grease (Lubrication Grease LG-500). Pump slowly until slight resistance is felt (do not overgrease as churning causes overheating).\n` +
        `3. **Oil Filter Replacement:** Replace spin-on Oil Filter OF-200 at every oil drain or when differential pressure indicator enters red (>1.5 bar drop).\n` +
        `4. **Inspection Points:** Check oil sight glass level (maintain halfway up glass). Milky oil indicates water contamination (>500 ppm); dark pungent oil indicates thermal breakdown.\n\n` +
        `**Specifications & Tolerances:**\n` +
        `- **Hydraulic Oil Viscosity:** ISO VG 46: 41.4 - 50.6 cSt at 40°C; ISO VG 68: 61.2 - 74.8 cSt\n` +
        `- **Target ISO Cleanliness Code:** 16/14/11 for servo valves; 18/16/13 for standard gear pumps\n` +
        `- **Regreasing Volume Formula:** G (grams) = 0.005 × D (OD mm) × B (width mm)\n` +
        `- **Oil Drain Plug Torque:** 25 - 30 Nm with fresh copper crush washer\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** Oil Filter Strap Wrench, Manual Lever Grease Gun, Oil Catch Pan, Fluid Sampling Bottle\n` +
        `- **Parts:** Oil Filter OF-200 (PN-01001), Lubrication Grease LG-500 (PN-01013), Hydraulic Fluid 20L (PN-01034), O-Ring Kit OR-50 (PN-01018)\n\n` +
        `**Safety Warning:** Hot oil creates severe burn risks. Do not open drain plugs when machine is above 50°C. Dispose of used oil and spent filters in certified environmental HazMat barrels.`,
      suggestions: [
        "How do I replace the oil filter?",
        "What's the torque spec?",
        "Why is my motor overheating?",
      ],
    };
  }

  // 8. LEAKS, GASKETS & HYDRAULIC SEALS
  if (
    q.includes("leak") ||
    q.includes("seal") ||
    q.includes("gasket") ||
    q.includes("drip") ||
    q.includes("o-ring") ||
    q.includes("weep")
  ) {
    return {
      message:
        `${machinePrefix}**Fluid Sealing & Leak Containment Protocol**\n\n` +
        `External oil leaks degrade machine cleanliness, create slip hazards, and cause pump cavitation due to air ingress.\n\n` +
        `1. **Depressurize System:** Disengage pump power. Cycle manual valves or open accumulator bleed port to confirm 0 bar on all system gauges.\n` +
        `2. **Pinpoint Source:** Wipe down housing with degreaser. Dust with talc powder or inspect under UV dye light to trace exact origin (fitting, flange gasket, or shaft lip seal).\n` +
        `3. **Flange Gasket Replacement:** Separate flange faces. Scrape old gasket material clean using a brass scraper. Install new Gasket Set GS-100 without sealant.\n` +
        `4. **Hydraulic Cylinder Rod Seal:** Pull gland retainer. Replace worn polyurethane U-cup with Hydraulic Seal HS-45. Lightly coat lips with hydraulic oil.\n` +
        `5. **Rotary Shaft Seal:** Install Shaft Seal SS-30 with spring garter facing inward toward fluid side. Use a seal driver to press squarely.\n\n` +
        `**Specifications & Tolerances:**\n` +
        `- **Hydraulic Rod Seal Tolerance:** HS-45: 45 mm Rod ID × 55 mm Housing Bore × 10 mm Height\n` +
        `- **O-Ring Material:** Nitrile NBR 70 Shore A (temperature -30°C to +120°C)\n` +
        `- **Flange Bolt Torque Pattern:** Star pattern torqued in 3 passes: 30% → 70% → 100%\n` +
        `- **Max Allowable Shaft Seal Lip Eccentricity:** <0.05 mm total runout\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** Brass Scraper, O-Ring Pick Set, Seal Driver Kit, Calibrated Torque Wrench\n` +
        `- **Parts:** Gasket Set GS-100 (PN-01004), Hydraulic Seal Kit HS-45 (PN-01003), O-Ring Kit OR-50 (PN-01018), Shaft Seal SS-30 (PN-01017)\n\n` +
        `**Safety Warning:** High pressure fluid injection hazard! A pinhole hydraulic leak at 150 bar can penetrate safety gloves and flesh. Never inspect pressurized hydraulic lines with your hands. Use cardboard or wood.`,
      suggestions: [
        "What's the torque spec?",
        "What type of hydraulic oil is needed?",
        "Show safety warnings",
      ],
    };
  }

  // 9. PUMPS & CAVITATION
  if (
    q.includes("pump") ||
    q.includes("water pump") ||
    q.includes("coolant pump") ||
    q.includes("cavitat") ||
    q.includes("no prime") ||
    q.includes("low pressure")
  ) {
    return {
      message:
        `${machinePrefix}**Hydraulic & Centrifugal Pump Diagnostics**\n\n` +
        `Pumps producing marbles-in-a-can popping sounds, erratic pressure gauges, or low output flow are suffering from cavitation, air ingress, or impeller clogging.\n\n` +
        `1. **Check Suction Restriction:** Inspect suction strainer basket and intake lines for swarf, lint, or sludge buildup. Restricted suction causes fluid vaporization (cavitation).\n` +
        `2. **Inspect Suction Head (NPSH):** Ensure fluid level in reservoir or sump is above minimum submergence mark (preventing suction vortexing).\n` +
        `3. **Verify Motor Rotation:** Momentarily jog motor switch. Verify impeller rotates in direction of cast casing arrow (reversed rotation yields only ~50% pressure).\n` +
        `4. **Bleed Trapped Air:** Crack casing air-bleed cock until a steady bubble-free stream of fluid emerges.\n` +
        `5. **Examine Mechanical Seal:** Check seal weep hole for continuous dripping (>5 drops/min indicates failed stationary/rotary ceramic seal faces).\n\n` +
        `**Specifications & Tolerances (Coolant Pump CP-55):**\n` +
        `- **Rated Flow Capacity:** 55 L/min at 2.8 bar head\n` +
        `- **Motor Rating:** 1.5 kW, 3-Phase 415V, 2850 RPM\n` +
        `- **Suction Vacuum Limit:** Not to exceed -0.3 bar (-4.3 PSI) gauge\n` +
        `- **Flange Bolting Torque (M10):** 45 - 50 Nm\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** Compound Pressure/Vacuum Gauge, Tachometer, Laser Alignment Kit, Flange Wrenches\n` +
        `- **Parts:** Coolant Pump CP-55 (PN-01007), Shaft Seal SS-30 (PN-01017), Gasket Set GS-100 (PN-01004)\n\n` +
        `**Safety Warning:** Ensure pump is electrically isolated and line pressure discharged before breaking flange bolts. Hot coolant contains biocides; wear nitrile gloves and chemical splash goggles.`,
      suggestions: [
        "Why is there excessive vibration?",
        "What's the torque spec?",
        "Show safety warnings",
      ],
    };
  }

  // 10. AIR COMPRESSOR & PNEUMATICS
  if (
    q.includes("compressor") ||
    q.includes("air filter") ||
    q.includes("pneumatic") ||
    q.includes("pressure switch") ||
    q.includes("unloader") ||
    q.includes("air leak")
  ) {
    return {
      message:
        `${machinePrefix}**Pneumatic Power & Air Compressor Maintenance**\n\n` +
        `Compressors running continuously without building pressure or cycling rapidly indicate unloader valve failure, clogged intake filter, or heavy downstream line leakage.\n\n` +
        `1. **Inspect Intake Particulate Filter:** Check Air Filter AF-300 element. Sintered bronze/paper element coated in dust starves compressor cylinders.\n` +
        `2. **Check Unloader Valve:** When compressor motor cuts out, listen for brief, sharp hiss at unloader valve. If hissing is continuous, tank check valve is leaking back.\n` +
        `3. **Purge Condensate Tank:** Open bottom receiver drain cock to drain accumulated water. Water reduces effective air volume and rusts internal tank walls.\n` +
        `4. **Calibrate Pressure Switch PS-100:** Adjust range screw for cut-in pressure (6.0 bar) and differential screw for cut-out pressure (8.0 bar).\n` +
        `5. **Ultrasonic Leak Survey:** Inspect quick-connect couplings, FRL regulators, and solenoid valve exhausts for audible air hiss.\n\n` +
        `**Specifications & Tolerances:**\n` +
        `- **System Operating Band:** 6.0 bar (87 PSI) Cut-In / 8.0 bar (116 PSI) Cut-Out\n` +
        `- **Air Filter Pressure Drop:** Replace filter if ΔP exceeds 0.35 bar (5 PSI)\n` +
        `- **Safety Relief Valve Pop Pressure:** 10.0 bar (145 PSI) ASME stamped\n` +
        `- **Belt Tension Deflection:** 15 - 20 lbs deflection force at span center\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** Ultrasonic Air Leak Detector, Test Pressure Gauge (0-16 bar), Soapy Water Bubble Solution\n` +
        `- **Parts:** Air Filter AF-300 (PN-01006), Pressure Switch PS-100 (PN-01011), V-Belt A68 (PN-01000)\n\n` +
        `**Safety Warning:** Compressed air is stored energy. Never unscrew pneumatic fittings or filter bowls while line pressure is above 0 bar. Never point compressed air nozzles at skin or clothing.`,
      suggestions: [
        "How do I set the pressure switch?",
        "What's the torque spec?",
        "Show belt replacement procedure",
      ],
    };
  }

  // 11. SENSORS, PROXIMITY & ENCODERS
  if (
    q.includes("sensor") ||
    q.includes("proximity") ||
    q.includes("encoder") ||
    q.includes("limit switch") ||
    q.includes("pr-18") ||
    q.includes("pt100")
  ) {
    return {
      message:
        `${machinePrefix}**Instrumentation, Sensors & Position Feedback Diagnostics**\n\n` +
        `Automation faults, missed machine cycles, or axis overtravel are frequently traced to loose sensor brackets, metal dust accretion, or mechanical misalignment.\n\n` +
        `1. **Proximity Sensor PR-18 (Inductive M18):** Verify sensing face is clean of metal filings. Gap must be set to 60-80% of rated 8 mm sensing range (~5.0 mm from metal dog). Ensure LED illuminates.\n` +
        `2. **Rotary Encoder EN-1024:** Verify flexible shaft coupling is not broken or slipping. Check shielded cable (Servo Cable SC-5M) grounding to eliminate electrical noise spikes.\n` +
        `3. **Limit Switch LS-10:** Check roller arm free travel. Roller must strike cam tangentially at 15°-20° angle, avoiding direct head-on impacts.\n` +
        `4. **Temperature Sensor TS-200 (PT100):** Measure resistance with digital multimeter. At 0°C = 100.0 Ω, at 25°C = 109.7 Ω, at 100°C = 138.5 Ω. Infinity indicates open probe wire.\n\n` +
        `**Specifications & Tolerances:**\n` +
        `- **Proximity Sensor PR-18:** M18 × 1.0 thread, 24V DC PNP NO, 8 mm nominal sensing distance, locknut torque 20 Nm\n` +
        `- **Encoder EN-1024:** 1024 Pulses Per Revolution (PPR), HTL 10-30V DC output, max speed 6,000 RPM\n` +
        `- **Limit Switch LS-10:** IP67 die-cast zinc, 10A 250V AC rating, mechanical life 10 million cycles\n` +
        `- **Cable Shield Grounding:** 360-degree clamp to chassis ground within 50 mm of entry\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** Digital Multimeter, Feeler Gauges, Non-magnetic Alignment Screwdrivers, Oscilloscope\n` +
        `- **Parts:** Proximity Sensor PR-18 (PN-01022), Encoder EN-1024 (PN-01023), Limit Switch LS-10 (PN-01021), Servo Cable SC-5M (PN-01024)\n\n` +
        `**Safety Warning:** Always test limit switches and emergency interlocks in manual jog mode before enabling full-speed automated production.`,
      suggestions: [
        "Show wiring diagram",
        "How do I calibrate the temperature sensor?",
        "What's the torque spec?",
      ],
    };
  }

  // 12. CNC MACHINING & TOOLING
  if (
    q.includes("cnc") ||
    q.includes("milling") ||
    q.includes("lathe") ||
    q.includes("spindle") ||
    q.includes("end mill") ||
    q.includes("insert") ||
    q.includes("tool wear")
  ) {
    return {
      message:
        `${machinePrefix}**Precision Machining & CNC Spindle Tooling Protocol**\n\n` +
        `Chatter marks, poor surface roughness (Ra), dimensional taper, or premature cutting edge chipping stem from spindle runout, tool wear, or excessive tool overhang.\n\n` +
        `1. **Spindle Runout Check:** Mount 0.001 mm dial test indicator against spindle test arbor. Hand-rotate spindle. Runout must not exceed 0.003 mm.\n` +
        `2. **Inspect Cutting Tool Insert:** Check carbide insert cutting tip under magnifier. Replace or index insert if flank wear land (Vb) exceeds 0.25 mm.\n` +
        `3. **Solid Carbide End Mill 10mm:** Inspect flute helix for micro-chipping. Ensure tool projection length is minimum required (<3× cutter diameter) to prevent deflection.\n` +
        `4. **Coolant Concentration:** Measure water-soluble cutting fluid with optical refractometer (maintain 7% - 9% Brix for steel alloys).\n` +
        `5. **Clean Collet & Toolholder:** Wipe taper with clean felt wiper. Debris between BT40/CAT40 taper and spindle multiplies runout error tenfold.\n\n` +
        `**Specifications & Tolerances:**\n` +
        `- **End Mill 10mm (PN-01032):** 4-Flute solid carbide TiAlN, recommended cutting speed Vc = 120-180 m/min\n` +
        `- **Cutting Insert Clamp Screw Torque:** 1.5 - 2.0 Nm (Torx T8/T15 wrench)\n` +
        `- **Collet Nut Clamping Torque (ER32):** 135 - 140 Nm\n` +
        `- **Spindle Bearing Preload Deflection:** <0.002 mm axial play\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** 0.001 mm Dial Test Indicator, Optical Brix Refractometer, ER Collet Torque Wrench, Taper Wiper\n` +
        `- **Parts:** End Mill 10mm (PN-01032), Cutting Tool Insert (PN-01031), Coolant Pump CP-55 (PN-01007)\n\n` +
        `**Safety Warning:** High-speed spindle rotating at 10,000+ RPM. Never bypass safety door interlocks. Ejected carbide shards can penetrate standard safety gear.`,
      suggestions: [
        "What's the torque spec?",
        "Show coolant pump procedure",
        "Why is my motor overheating?",
      ],
    };
  }

  // 13. SAFETY, LOTO & EMERGENCY PROCEDURES
  if (
    q.includes("safety") ||
    q.includes("loto") ||
    q.includes("lockout") ||
    q.includes("tagout") ||
    q.includes("ppe") ||
    q.includes("emergency stop") ||
    q.includes("e-stop")
  ) {
    return {
      message:
        `${machinePrefix}**Industrial Safety & OSHA 1910.147 Lockout/Tagout (LOTO) Protocol**\n\n` +
        `Zero Energy State verification must precede any inspection, maintenance, or mechanical disassembly.\n\n` +
        `1. **Preparation & Notification:** Notify machine operators and floor supervisors that maintenance is initiating.\n` +
        `2. **Machine Shutdown:** Depress Emergency Stop and cycle machine through normal shutdown sequence.\n` +
        `3. **Isolation of All Energy Sources:**\n` +
        `   - **Electrical:** Disengage main rotary disconnect switch and install personal red padlock and danger tag.\n` +
        `   - **Pneumatics:** Close main supply ball valve; lock handle with lockout hasp; vent residual pressure.\n` +
        `   - **Hydraulics:** Lock hydraulic pump switch; open accumulator manual bleed valve until gauge reads 0 bar.\n` +
        `   - **Mechanical / Gravity:** Insert physical mechanical safety drop-pins / locking wedges under elevated rams.\n` +
        `4. **Zero Energy Verification (Try-Step):** Press local start buttons to confirm equipment will not start. Verify 0V across all phases using a CAT-III multimeter.\n\n` +
        `**Personal Protective Equipment (PPE) Matrix:**\n` +
        `- **General Maintenance:** ANSI Z87.1 Safety Glasses, Steel-Toed Boots (ASTM F2413), Cut-Resistant Gloves (ANSI Level A4)\n` +
        `- **Electrical Work:** NFPA 70E Arc Flash Face Shield (8 cal/cm²), 1000V Insulated Rubber Gloves\n` +
        `- **Hot Mechanical Work:** Heavy-duty heat-resistant cowhide leather gloves\n\n` +
        `**Recommended Tools & Parts:**\n` +
        `- **Tools:** Safety Lockout Padlocks, Danger LOTO Tags, Steel Lockout Hasps, CAT-III/IV 1000V Multimeter\n` +
        `- **Parts:** Fuse 32A (PN-01008), Limit Switch LS-10 (PN-01021)\n\n` +
        `**Safety Warning:** One lock, one key, one worker. Never allow another employee to remove your safety lock. Never assume a line is de-energized without physical instrument verification.`,
      suggestions: [
        "What's the torque spec?",
        "Show electrical wiring diagram",
        "What tools do I need?",
      ],
    };
  }

  // 14. PARTS INVENTORY, STOCK & RESTOCKING
  if (
    q.includes("part") ||
    q.includes("stock") ||
    q.includes("inventory") ||
    q.includes("order") ||
    q.includes("sku") ||
    q.includes("supplier")
  ) {
    return {
      message:
        `${machinePrefix}**MaintAI Warehouse Inventory & Parts Restock Protocol**\n\n` +
        `The MaintAI parts catalog contains 36 verified industrial replacement components with real photographs, OEM part numbers, and real-time inventory tracking.\n\n` +
        `1. **Check Real-Time Stock:** Open the **Parts** section from the navigation menu. Parts with stock below safety threshold are highlighted with yellow warning badges.\n` +
        `2. **Filter by Urgency:** Click the **Low Stock** status pill at the top of the Parts page to see all items requiring immediate procurement.\n` +
        `3. **1-Click Restock Request:** Click **Create Purchase Request** to open the order modal. Adjust quantity and submit requisition directly to purchasing.\n` +
        `4. **Print Barcode Bin Labels:** Tap the **Barcode** icon on any part card to generate and print Code128 bin labels for physical warehouse shelving.\n` +
        `5. **Machine Compatibility:** View technical details to verify which production machines (e.g. CNC Machine, Water Pump, Lathe) are compatible with the selected component.\n\n` +
        `**Key Fast-Moving Industrial Parts:**\n` +
        `- **PN-01000:** V-Belt A68 (Mechanical, Gates Industrial)  -  $45.00\n` +
        `- **PN-01001:** Oil Filter OF-200 (Consumable, Donaldson)  -  $28.50\n` +
        `- **PN-01002:** Ball Bearing 6205-2RS (Mechanical, SKF)  -  $35.00\n` +
        `- **PN-01009:** Contactor LC1D25 (Electrical, Schneider)  -  $65.00\n` +
        `- **PN-01018:** O-Ring Kit OR-50 (Consumable, Parker)  -  $45.00\n\n` +
        `**Recommended Tools:**\n` +
        `- **Tools:** Barcode Scanner, Warehouse Thermal Label Printer, MaintAI Mobile PWA\n\n` +
        `**Safety Warning:** Verify part numbers and specifications before installing. Never substitute standard bolts or non-pressure-rated hoses in high-pressure hydraulic circuits.`,
      suggestions: [
        "What's the torque spec?",
        "Why is my motor overheating?",
        "How do I replace the belt?",
      ],
    };
  }

  // 15. DYNAMIC GENERAL INDUSTRIAL FALLBACK (Answers ANY extra question in the requested manner)
  const technicalKeywords = [
    "motor", "pump", "bearing", "belt", "torque", "wire", "wiring", "electrical", "voltage", "amp",
    "vibrat", "leak", "oil", "grease", "lube", "heat", "hot", "overheat", "pressure", "compressor",
    "cylinder", "hydraulic", "pneumatic", "gear", "spindle", "cnc", "lathe", "sensor", "valve",
    "fuse", "relay", "contactor", "breaker", "noise", "sound", "grind", "smoke", "smell", "trip",
    "fault", "error", "fail", "broken", "fix", "repair", "replace", "inspect", "maintenance",
    "machine", "equipment", "spec", "part", "inventory", "tool", "loto", "lockout", "safety", "bolt",
    "speed", "rpm", "alignment", "shaft", "coupling", "seal", "gasket", "chatter", "feed"
  ];

  const hasTechnicalContext = Boolean(machine) || technicalKeywords.some((k) => q.includes(k));

  if (!hasTechnicalContext) {
    return {
      message:
        `I hear you! As your plant copilot, I can chat about normal everyday topics or dive into deep industrial engineering whenever you need it.\n\n` +
        `If you have questions about equipment or need assistance on the floor, feel free to describe what you're seeing—like **"motor is overheating"**, **"unusual vibration in pump"**, or **"what's the torque spec for M10 bolts"**.\n\n` +
        `Or if you just want to talk through ideas or have a casual question, feel free to share more!`,
      suggestions: [
        "Can you talk normally?",
        "Why is my motor overheating?",
        "What's the torque spec?",
      ],
    };
  }

  return {
    message:
      `${machinePrefix}**Technical Diagnosis & Maintenance Engineering Plan**\n\n` +
      `Regarding your question: *"**${query}**"*\n\n` +
      `For industrial production machinery, this issue requires a systematic mechanical, electrical, and operational inspection:\n\n` +
      `1. **Verify Operating Conditions:** Compare current operating temperature, vibration levels, and electrical load against OEM machine baseline specifications.\n` +
      `2. **Mechanical Inspection:** Inspect driveline components for physical wear, fastener loosening, belt tension loss, or coupling backlash.\n` +
      `3. **Fluid & Lubrication Check:** Verify fluid levels, oil clarity, filter differential pressure, and seal integrity throughout the lubrication circuit.\n` +
      `4. **Electrical Continuity & Controls:** Measure supply voltage balance across terminals (<2% variance) and inspect sensor LEDs and interlock switches.\n` +
      `5. **Document & Log:** Record findings, measured values, and replaced components in the MaintAI maintenance log for historical tracking.\n\n` +
      `**Standard Engineering Specifications:**\n` +
      `- **General Fastener Torque (M8/M10):** M8: 25 - 30 Nm | M10: 45 - 50 Nm\n` +
      `- **Insulation Resistance:** >1.0 MΩ at 500V DC test\n` +
      `- **Vibration Velocity Limit (ISO 10816-3):** <2.8 mm/s RMS (acceptable), <4.5 mm/s (alert threshold)\n` +
      `- **Operating Temperature Limit:** Housing surface must remain below 75°C under continuous load\n\n` +
      `**Recommended Tools & Consumables:**\n` +
      `- **Tools:** Calibrated Click Torque Wrench, True-RMS Multimeter, Non-contact Infrared Thermometer, Feeler Gauge Set\n` +
      `- **Inventory Parts:** Check MaintAI Parts section for compatible replacement bearings, seals, filters, and drive belts\n\n` +
      `**Safety Warning:** Always engage Lockout/Tagout (LOTO) protocols and verify zero energy state before placing hands near moving mechanisms or exposed electrical connections.`,
    suggestions: [
      "What tools do I need?",
      "Show safety warnings",
      "What's the torque spec?",
    ],
  };
}

export async function POST(req: Request) {
  try {
    const { messages, machineContext } = await req.json();
    const lastMessage = messages[messages.length - 1]?.content ?? "";

    // If online AI provider is configured, attempt it with a strict timeout
    if (isAIConfigured()) {
      try {
        const systemPrompt =
          `You are FixBot, an expert industrial maintenance AI assistant and plant copilot for MaintAI. ` +
          `${machineContext ? `The technician is currently working on: ${machineContext}.` : ""} ` +
          `Communication Guidelines:\n` +
          `- Casual & Conversational: When the user engages in normal conversation, chit-chat, greetings (e.g. "hi", "how are you", "who are you", "can you talk normally"), gratitude ("thanks"), humor, or casual questions, respond naturally, warmly, and conversationally like an experienced, friendly engineering colleague. Do NOT force a rigid 5-step repair template for casual chat.\n` +
          `- Technical & Maintenance: When the user asks technical, mechanical, electrical, maintenance, troubleshooting, or repair questions, provide an authoritative, structured industrial engineering response with:\n` +
          `  1. **Diagnostic Finding / Root Cause**\n` +
          `  2. **Numbered Step-by-Step Action Plan** with bold step titles\n` +
          `  3. **Specifications & Tolerances** (exact bolt torques in Nm, pressures in bar, voltages, clearances)\n` +
          `  4. **Recommended Tools & Parts**\n` +
          `  5. **Safety Warning / LOTO Protocol**\n` +
          `Be practical, friendly, adaptive to tone, and prioritize worker safety.`;

        // Timeout promise after 2000ms so it never hangs
        const timeoutPromise = new Promise<string>((_, reject) =>
          setTimeout(() => reject(new Error("AI generation timeout")), 2000)
        );

        const aiPromise = generateTextResponse(
          [{ role: "system", content: systemPrompt }, ...messages],
          800
        );

        const message = await Promise.race([aiPromise, timeoutPromise]);

        const suggestions = [
          "What tools do I need?",
          "Show safety warnings",
          "What's the torque spec?",
        ];

        return NextResponse.json({ message, suggestions });
      } catch (aiError) {
        console.warn("FixBot AI call fell back to local industrial knowledge engine:", (aiError as Error).message);
      }
    }

    // Comprehensive industrial knowledge engine fallback
    const result = getStructuredIndustrialResponse(lastMessage, machineContext);
    return NextResponse.json(result);
  } catch (error) {
    console.error("FixBot chat error:", error);
    return NextResponse.json({
      message:
        "**FixBot System Notice**\n\n" +
        "Unable to process request at this moment. Please verify your connection or retry your question.",
      suggestions: [
        "Why is my motor overheating?",
        "What's the torque spec?",
        "Show safety warnings",
      ],
    });
  }
}

