import urllib.request
import urllib.parse
import json
import os
import sys
from PIL import Image
import io

PARTS = [
    {
        "slug": "v-belt-a68",
        "name": "V-Belt A68",
        "category": "Mechanical",
        "supplier": "Gates Industrial",
        "lead_time_days": 2,
        "price": 45.00,
        "queries": ["Keilriemen", "V-belt rubber", "V-belt"],
        "description": "Heavy-duty wrapped classical V-belt for industrial drive transmissions.",
    },
    {
        "slug": "oil-filter-of-200",
        "name": "Oil Filter OF-200",
        "category": "Consumable",
        "supplier": "Donaldson Filtration",
        "lead_time_days": 1,
        "price": 28.50,
        "queries": ["Oil filter spin-on", "Automotive oil filter", "Oil filter"],
        "description": "High-efficiency spin-on hydraulic and lubricant oil filter element.",
    },
    {
        "slug": "ball-bearing-6205",
        "name": "Ball Bearing 6205",
        "category": "Mechanical",
        "supplier": "SKF Bearings",
        "lead_time_days": 3,
        "price": 35.00,
        "queries": ["Deep groove ball bearing", "Kugellager", "Ball bearing"],
        "description": "Deep groove single-row chrome steel ball bearing (25x52x15mm).",
    },
    {
        "slug": "gasket-set-gs-100",
        "name": "Gasket Set GS-100",
        "category": "Consumable",
        "supplier": "Flexitallic Gaskets",
        "lead_time_days": 2,
        "price": 42.00,
        "queries": ["Flange gasket", "Gasket sealing", "Flachdichtung"],
        "description": "Universal graphite & PTFE flange gasket replacement kit.",
    },
    {
        "slug": "hydraulic-seal-hs-45",
        "name": "Hydraulic Seal HS-45",
        "category": "Hydraulic",
        "supplier": "Parker Hannifin",
        "lead_time_days": 4,
        "price": 125.00,
        "queries": ["Hydraulic cylinder seal", "Nutring", "Hydraulic seal piston"],
        "description": "High-pressure polyurethane rod/piston U-cup seal (45mm ID).",
    },
    {
        "slug": "motor-coupling-mc-12",
        "name": "Motor Coupling MC-12",
        "category": "Mechanical",
        "supplier": "Lovejoy Couplings",
        "lead_time_days": 3,
        "price": 89.00,
        "queries": ["Jaw coupling", "Flexible coupling shaft", "Klauenkupplung"],
        "description": "Jaw-type flexible shaft elastomer coupling hub.",
    },
    {
        "slug": "drive-belt-db-900",
        "name": "Drive Belt DB-900",
        "category": "Mechanical",
        "supplier": "Continental ContiTech",
        "lead_time_days": 2,
        "price": 52.00,
        "queries": ["Timing belt toothed", "Zahnriemen", "Timing belt"],
        "description": "Synchronous timing belt with high tensile fiberglass cords.",
    },
    {
        "slug": "air-filter-af-300",
        "name": "Air Filter AF-300",
        "category": "Pneumatic",
        "supplier": "Festo Pneumatics",
        "lead_time_days": 1,
        "price": 42.00,
        "queries": ["Pneumatic filter regulator", "Compressed air filter", "Druckluftfilter"],
        "description": "Sintered bronze 5-micron compressed air particulate filter.",
    },
    {
        "slug": "coolant-pump-cp-55",
        "name": "Coolant Pump CP-55",
        "category": "Hydraulic",
        "supplier": "Grundfos Direct",
        "lead_time_days": 5,
        "price": 245.00,
        "queries": ["Coolant pump machine", "Kühlmittelpumpe", "Centrifugal coolant pump"],
        "description": "Submerged coolant & cutting fluid circulation pump (55 L/min).",
    },
    {
        "slug": "fuse-32a",
        "name": "Fuse 32A",
        "category": "Electrical",
        "supplier": "Bussmann / Eaton",
        "lead_time_days": 1,
        "price": 18.00,
        "queries": ["Cartridge fuse industrial", "Schmelzsicherung", "HRC fuse"],
        "description": "Industrial ceramic high-breaking capacity cartridge fuse (32A 500V).",
    },
    {
        "slug": "contactor-lc1d25",
        "name": "Contactor LC1D25",
        "category": "Electrical",
        "supplier": "Schneider Electric",
        "lead_time_days": 2,
        "price": 65.00,
        "queries": ["Contactor electrical", "Schütz", "Telemecanique contactor"],
        "description": "3-Pole 25A motor control magnetic AC contactor 24V coil.",
    },
    {
        "slug": "relay-24v-dc",
        "name": "Relay 24V DC",
        "category": "Electrical",
        "supplier": "Omron Automation",
        "lead_time_days": 2,
        "price": 22.00,
        "queries": ["Electromechanical relay", "Relay industrial", "Finder relay"],
        "description": "Miniature plug-in electromagnetic control relay with LED indicator.",
    },
    {
        "slug": "pressure-switch-ps-100",
        "name": "Pressure Switch PS-100",
        "category": "Pneumatic",
        "supplier": "Danfoss Controls",
        "lead_time_days": 3,
        "price": 78.00,
        "queries": ["Pressure switch Danfoss", "Druckschalter", "Differential pressure switch"],
        "description": "Adjustable range differential pressure switch 0-10 bar.",
    },
    {
        "slug": "temperature-sensor-ts-200",
        "name": "Temperature Sensor TS-200",
        "category": "Electrical",
        "supplier": "Endress+Hauser",
        "lead_time_days": 3,
        "price": 95.00,
        "queries": ["Resistance thermometer probe", "Pt100 sensor", "RTD probe"],
        "description": "PT100 RTD mineral-insulated probe sensor with terminal head.",
    },
    {
        "slug": "lubrication-grease-lg-500",
        "name": "Lubrication Grease LG-500",
        "category": "Consumable",
        "supplier": "Mobil Industrial",
        "lead_time_days": 1,
        "price": 35.00,
        "queries": ["Grease gun cartridge", "Schmierfett", "Lubricating grease tube"],
        "description": "NLGI 2 extreme-pressure synthetic lithium complex grease (500g cartridge).",
    },
    {
        "slug": "chain-link-cl-38",
        "name": "Chain Link CL-38",
        "category": "Mechanical",
        "supplier": "Tsubaki Chain",
        "lead_time_days": 2,
        "price": 28.00,
        "queries": ["Roller chain connecting link", "Master link chain", "Kettenglied"],
        "description": "ANSI #40 master connecting chain link with spring clip.",
    },
    {
        "slug": "sprocket-sp-24",
        "name": "Sprocket SP-24",
        "category": "Mechanical",
        "supplier": "Martin Sprocket",
        "lead_time_days": 3,
        "price": 55.00,
        "queries": ["Chain sprocket", "Kettenrad", "Roller chain sprocket"],
        "description": "24-Tooth hardened carbon steel roller chain sprocket (B-hub).",
    },
    {
        "slug": "pulley-pl-6",
        "name": "Pulley PL-6",
        "category": "Mechanical",
        "supplier": "TB Wood's",
        "lead_time_days": 3,
        "price": 42.00,
        "queries": ["V-belt pulley", "Belt pulley sheave", "Riemenscheibe"],
        "description": "6-inch cast iron single-groove A-section V-belt sheave pulley.",
    },
    {
        "slug": "shaft-seal-ss-30",
        "name": "Shaft Seal SS-30",
        "category": "Mechanical",
        "supplier": "Timken Seals",
        "lead_time_days": 2,
        "price": 38.00,
        "queries": ["Radial shaft seal", "Wellendichtring", "Rotary shaft lip seal"],
        "description": "Rotary double-lip oil shaft seal with garter spring (30mm).",
    },
    {
        "slug": "o-ring-kit-or-50",
        "name": "O-Ring Kit OR-50",
        "category": "Consumable",
        "supplier": "Parker O-Rings",
        "lead_time_days": 1,
        "price": 45.00,
        "queries": ["O-ring assortment kit", "O-ring box", "O-Ringe Sortiment"],
        "description": "386-Piece NBR 70 Shore A metric O-ring assortment case.",
    },
    {
        "slug": "terminal-block-tb-12",
        "name": "Terminal Block TB-12",
        "category": "Electrical",
        "supplier": "Phoenix Contact",
        "lead_time_days": 2,
        "price": 12.00,
        "queries": ["DIN rail terminal blocks", "Reihenklemme", "Terminal block modular"],
        "description": "DIN-rail feed-through spring cage terminal blocks (pack of 10).",
    },
    {
        "slug": "cable-gland-cg-25",
        "name": "Cable Gland CG-25",
        "category": "Electrical",
        "supplier": "LAPP Group",
        "lead_time_days": 2,
        "price": 8.50,
        "queries": ["Cable gland brass", "Kabelverschraubung", "Cable gland"],
        "description": "Nickel-plated brass IP68 waterproof strain relief cable gland (M25).",
    },
    {
        "slug": "limit-switch-ls-10",
        "name": "Limit Switch LS-10",
        "category": "Electrical",
        "supplier": "Honeywell Sensing",
        "lead_time_days": 3,
        "price": 32.00,
        "queries": ["Limit switch roller", "Endschalter Rolle", "Position limit switch"],
        "description": "Heavy-duty roller lever enclosed position limit switch (1NO/1NC).",
    },
    {
        "slug": "proximity-sensor-pr-18",
        "name": "Proximity Sensor PR-18",
        "category": "Electrical",
        "supplier": "IFM Efector",
        "lead_time_days": 3,
        "price": 85.00,
        "queries": ["Inductive proximity sensor", "Induktiver Näherungsschalter", "Proximity switch M18"],
        "description": "M18 Inductive proximity switch PNP normally open (8mm sensing).",
    },
    {
        "slug": "encoder-en-1024",
        "name": "Encoder EN-1024",
        "category": "Electrical",
        "supplier": "Sick Sensor Intelligence",
        "lead_time_days": 4,
        "price": 185.00,
        "queries": ["Rotary encoder optical", "Drehgeber", "Incremental rotary encoder"],
        "description": "1024 PPR incremental optical rotary encoder with HTL output.",
    },
    {
        "slug": "servo-cable-sc-5m",
        "name": "Servo Cable SC-5M",
        "category": "Electrical",
        "supplier": "Igus Motion Plastics",
        "lead_time_days": 2,
        "price": 120.00,
        "queries": ["Shielded multi-core cable", "Schleppkettengerechte Leitung", "Industrial power cable"],
        "description": "5-Meter high-flex shielded power & feedback servo drive cable.",
    },
    {
        "slug": "plc-module-im-16",
        "name": "PLC Module IM-16",
        "category": "Electrical",
        "supplier": "Siemens Automation",
        "lead_time_days": 4,
        "price": 450.00,
        "queries": ["PLC module digital input", "Simatic S7 module", "SPS Baugruppe"],
        "description": "16-Channel 24V DC digital input slice module for S7 system.",
    },
    {
        "slug": "transformer-fuse-tf-63",
        "name": "Transformer Fuse TF-63",
        "category": "Electrical",
        "supplier": "ABB Electrification",
        "lead_time_days": 3,
        "price": 25.00,
        "queries": ["High voltage fuse link", "HH-Sicherung", "Current limiting fuse"],
        "description": "63A 12kV medium voltage current-limiting back-up fuse link.",
    },
    {
        "slug": "cooling-fan-cf-120",
        "name": "Cooling Fan CF-120",
        "category": "Mechanical",
        "supplier": "ebm-papst",
        "lead_time_days": 2,
        "price": 68.00,
        "queries": ["Axial fan 120mm", "Computer cooling fan", "Axiallüfter"],
        "description": "120mm ball-bearing 230V AC cabinet ventilation exhaust fan.",
    },
    {
        "slug": "heating-element-he-3kw",
        "name": "Heating Element HE-3kW",
        "category": "Electrical",
        "supplier": "Watlow Thermal",
        "lead_time_days": 4,
        "price": 95.00,
        "queries": ["Immersion heater tubular", "Heizstab", "Heating element industrial"],
        "description": "3kW 415V Incoloy screw-plug industrial immersion heating element.",
    },
    {
        "slug": "welding-wire-08mm",
        "name": "Welding Wire 0.8mm",
        "category": "Consumable",
        "supplier": "ESAB Welding",
        "lead_time_days": 2,
        "price": 28.00,
        "queries": ["MIG welding wire spool", "Schweißdraht Spule", "Welding wire spool"],
        "description": "0.8mm ER70S-6 copper-coated solid MIG welding wire (15kg spool).",
    },
    {
        "slug": "welding-gas-cylinder",
        "name": "Welding Gas Cylinder",
        "category": "Consumable",
        "supplier": "Linde Gas",
        "lead_time_days": 3,
        "price": 180.00,
        "queries": ["Gas cylinder argon", "Gasflasche Druckgas", "Shielding gas cylinder"],
        "description": "50L high-pressure Argon/CO2 shielding gas cylinder (200 bar).",
    },
    {
        "slug": "cutting-tool-insert",
        "name": "Cutting Tool Insert",
        "category": "Consumable",
        "supplier": "Sandvik Coromant",
        "lead_time_days": 2,
        "price": 15.00,
        "queries": ["Indexable carbide insert", "Wendeplatte", "Tungsten carbide milling insert"],
        "description": "TiAlN coated carbide indexable milling insert for steel & alloys.",
    },
    {
        "slug": "end-mill-10mm",
        "name": "End Mill 10mm",
        "category": "Consumable",
        "supplier": "Kennametal",
        "lead_time_days": 2,
        "price": 35.00,
        "queries": ["Carbide end mill cutter", "Schaftfräser VHM", "End mill 4 flute"],
        "description": "10mm 4-flute solid carbide high-performance CNC end mill.",
    },
    {
        "slug": "forklift-tire-23x9-10",
        "name": "Forklift Tire 23x9-10",
        "category": "Mechanical",
        "supplier": "Continental Industrial",
        "lead_time_days": 4,
        "price": 285.00,
        "queries": ["Forklift solid tire", "Gabelstapler Reifen", "Industrial solid tire"],
        "description": "23x9-10 resilient solid rubber non-marking forklift drive tire.",
    },
    {
        "slug": "hydraulic-fluid-20l",
        "name": "Hydraulic Fluid 20L",
        "category": "Consumable",
        "supplier": "Shell Industrial",
        "lead_time_days": 1,
        "price": 145.00,
        "queries": ["Hydraulic oil container", "Hydrauliköl Kanister", "Industrial oil drum"],
        "description": "ISO VG 46 premium anti-wear hydraulic oil (20 Liter pail).",
    },
]

out_dir = r"c:\dev\pro\public\parts"
os.makedirs(out_dir, exist_ok=True)

def search_image(query):
    try:
        url = (
            f"https://commons.wikimedia.org/w/api.php?action=query"
            f"&generator=search&gsrsearch={urllib.parse.quote(query)}"
            f"&gsrnamespace=6&gsrlimit=8&prop=imageinfo&iiprop=url|mime|size&format=json"
        )
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "MaintAI-ImageHarvester/1.0 (hetjo@maint-ai.demo; contact@maint-ai.io)"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pages = data.get("query", {}).get("pages", {})
            for pid, p in pages.items():
                title = p.get("title", "").lower()
                ii = p.get("imageinfo", [{}])[0]
                img_url = ii.get("url", "")
                mime = ii.get("mime", "").lower()
                # Exclude SVG, audio, video, pdf, diagrams, or icon flags
                if not ("image/jpeg" in mime or "image/png" in mime or "image/webp" in mime):
                    continue
                if any(x in title for x in [".svg", ".ogg", ".webm", ".pdf", "flag_", "icon", "logo", "diagram", "drawing", "map"]):
                    continue
                return img_url, title
    except Exception as e:
        print(f"Error searching {query}: {e}")
    return None, None

def download_and_process(img_url, target_path):
    try:
        req = urllib.request.Request(
            img_url,
            headers={"User-Agent": "MaintAI-ImageHarvester/1.0 (hetjo@maint-ai.demo)"}
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw_bytes = resp.read()
        
        img = Image.open(io.BytesIO(raw_bytes))
        img = img.convert("RGB")
        
        # Max dimensions 800x800
        img.thumbnail((800, 800), Image.Resampling.LANCZOS)
        img.save(target_path, "JPEG", quality=85, optimize=True)
        return True
    except Exception as e:
        print(f"Failed to process {img_url}: {e}")
        return False

print(f"Starting image fetch for {len(PARTS)} parts...")

results = {}
for p in PARTS:
    slug = p["slug"]
    target_file = os.path.join(out_dir, f"{slug}.jpg")
    found = False
    
    for q in p["queries"]:
        img_url, title = search_image(q)
        if img_url:
            safe_title = title.encode('ascii', 'replace').decode('ascii')
            print(f"Found for '{p['name']}' using '{q}': {safe_title}")
            ok = download_and_process(img_url, target_file)
            if ok:
                results[slug] = f"/parts/{slug}.jpg"
                found = True
                break
    
    if not found:
        print(f"[-] Could not find photographic image for {p['name']}")

print(f"\nDone! Downloaded {len(results)} / {len(PARTS)} parts images.")

