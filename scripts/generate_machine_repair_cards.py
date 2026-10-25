import os
import base64
import subprocess
import pymupdf
import shutil

BASE = r"c:\dev\pro"
PDF_DIR = os.path.join(BASE, "pdf_images")

def to_b64(filepath):
    ext = os.path.splitext(filepath)[1].lower().replace('.', '')
    if ext == 'jpg': ext = 'jpeg'
    mime = f"image/{ext}" if ext in ['png', 'jpeg', 'svg'] else 'image/jpeg'
    with open(filepath, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode("utf-8")

# Assets for the 3 new machines + 3 primary machines
b64_img_pump = to_b64(os.path.join(PDF_DIR, "mach_grundfos_pump.jpg"))
b64_qr_pump = to_b64(os.path.join(PDF_DIR, "qr_grundfos_pump.png"))
b64_bc_pump = to_b64(os.path.join(PDF_DIR, "bc_grundfos.png"))

b64_img_gen = to_b64(os.path.join(PDF_DIR, "mach_cummins_gen.jpg"))
b64_qr_gen = to_b64(os.path.join(PDF_DIR, "qr_cummins_gen.png"))
b64_bc_gen = to_b64(os.path.join(PDF_DIR, "bc_cummins.png"))

b64_img_press = to_b64(os.path.join(PDF_DIR, "mach_schuler_press.jpg"))
b64_qr_press = to_b64(os.path.join(PDF_DIR, "qr_schuler_press.png"))
b64_bc_press = to_b64(os.path.join(PDF_DIR, "bc_schuler.png"))

# Also load Haas, Siemens, Atlas for a complete 6-card set
b64_img_cnc = to_b64(os.path.join(BASE, "public", "machines", "cnc-machine.jpg"))
b64_qr_cnc = to_b64(os.path.join(PDF_DIR, "qr_haas_cnc.png"))

b64_img_motor = to_b64(os.path.join(BASE, "public", "machines", "electric-motor.jpg"))
b64_qr_motor = to_b64(os.path.join(PDF_DIR, "qr_siemens_motor.png"))

b64_img_comp = to_b64(os.path.join(BASE, "public", "machines", "air-compressor.jpeg"))
b64_qr_comp = to_b64(os.path.join(PDF_DIR, "qr_atlas_compressor.png"))

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MaintAI - Machine Repair Barcode Badges (Modular Chart Cut-outs)</title>
  <style>
    @page {{
      size: 420mm 297mm; /* A3 Landscape */
      margin: 0;
    }}
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      width: 420mm;
      height: 297mm;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: #0b1120;
      color: #f1f5f9;
      display: flex;
      flex-direction: column;
      padding: 8mm 10mm;
      overflow: hidden;
    }}

    /* Header Bar */
    header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 2px solid #334155;
      padding-bottom: 6px;
      margin-bottom: 8px;
    }}
    .header-left {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .header-title {{
      font-size: 16pt;
      font-weight: 900;
      color: #38bdf8;
      letter-spacing: -0.3px;
    }}
    .badge-strip {{
      font-size: 8pt;
      font-weight: 700;
      background: #f59e0b;
      color: #000;
      padding: 2px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .header-hint {{
      font-size: 8pt;
      color: #94a3b8;
    }}

    /* Grid of 6 Machine Repair Cards (3 columns x 2 rows) */
    .cards-grid {{
      flex: 1;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: 8mm;
    }}

    /* Individual Machine Card */
    .machine-badge-card {{
      background: linear-gradient(145deg, #111827 0%, #0f172a 100%);
      border: 2px dashed #0284c7;
      border-radius: 12px;
      padding: 8px 10px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 4px 14px rgba(0,0,0,0.4);
      position: relative;
    }}
    .machine-badge-card.amber-theme {{ border-color: #f59e0b; }}
    .machine-badge-card.emerald-theme {{ border-color: #10b981; }}
    .machine-badge-card.cyan-theme {{ border-color: #06b6d4; }}
    .machine-badge-card.violet-theme {{ border-color: #8b5cf6; }}
    .machine-badge-card.rose-theme {{ border-color: #f43f5e; }}

    /* Scissor Cutout Marker */
    .cut-marker {{
      position: absolute;
      top: -9px;
      right: 12px;
      background: #0b1120;
      color: #64748b;
      font-size: 7.5pt;
      padding: 0 5px;
      font-family: monospace;
    }}

    /* Card Top: Asset ID & Status */
    .card-top-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
    }}
    .asset-id-tag {{
      font-size: 8pt;
      font-weight: 800;
      font-family: monospace;
      color: #fbbf24;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 2px 6px;
      border-radius: 4px;
    }}
    .location-tag {{
      font-size: 7.5pt;
      font-weight: 600;
      color: #94a3b8;
    }}

    /* Middle Row: Photo + Identity */
    .card-middle {{
      display: flex;
      gap: 10px;
      margin-bottom: 6px;
    }}
    .machine-thumb {{
      width: 48mm;
      height: 38mm;
      border-radius: 6px;
      overflow: hidden;
      border: 1.5px solid #334155;
      background: #000;
      flex-shrink: 0;
    }}
    .machine-thumb img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .machine-meta {{
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 3px;
      flex: 1;
    }}
    .machine-title {{
      font-size: 11pt;
      font-weight: 800;
      color: #f8fafc;
      line-height: 1.2;
    }}
    .machine-subtitle {{
      font-size: 8pt;
      color: #38bdf8;
      font-weight: 600;
    }}
    .specs-pill {{
      display: inline-block;
      font-size: 7.5pt;
      color: #cbd5e1;
      background: #1e293b;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: monospace;
      margin-top: 2px;
      width: fit-content;
    }}

    /* Card Bottom: Prominent Scan Area */
    .scan-repair-panel {{
      background: #020617;
      border: 1.5px solid #1e293b;
      border-radius: 8px;
      padding: 6px 8px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .qr-box {{
      width: 58px;
      height: 58px;
      background: #ffffff;
      border-radius: 6px;
      padding: 3px;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.25);
    }}
    .qr-box img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
    }}
    .scan-details {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .scan-action-title {{
      font-size: 9pt;
      font-weight: 800;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .scan-action-title::before {{
      content: "⚡";
      font-size: 9.5pt;
    }}
    .qr-string {{
      font-size: 7.5pt;
      font-family: monospace;
      font-weight: 700;
      color: #fbbf24;
    }}
    .barcode-strip {{
      margin-top: 2px;
      background: #ffffff;
      padding: 2px 4px;
      border-radius: 3px;
      display: flex;
      align-items: center;
      justify-content: center;
      max-width: 160px;
    }}
    .barcode-strip img {{
      height: 18px;
      max-width: 100%;
      object-fit: contain;
    }}
    .scan-hint {{
      font-size: 6.8pt;
      color: #94a3b8;
    }}
  </style>
</head>
<body>

  <!-- HEADER -->
  <header>
    <div class="header-left">
      <div class="header-title">MAINTAI™ EQUIPMENT REPAIR BARCODE & ASSET TAG MATRIX</div>
      <span class="badge-strip">MODULAR SHOP-FLOOR CARDS</span>
    </div>
    <div class="header-hint">
      ✂️ Cut along dashed lines to paste onto physical chart paper model, or scan directly from sheet during live interview demo.
    </div>
  </header>

  <!-- CARDS GRID -->
  <div class="cards-grid">

    <!-- CARD 1: GRUNDFOS WATER PUMP (NEW) -->
    <div class="machine-badge-card cyan-theme">
      <div class="cut-marker">✂ CUT / ATTACH</div>
      <div class="card-top-bar">
        <span class="asset-id-tag">CR15-5-2022-1234</span>
        <span class="location-tag">Bay A - Floor 1</span>
      </div>
      <div class="card-middle">
        <div class="machine-thumb">
          <img src="{b64_img_pump}" alt="Grundfos Water Pump">
        </div>
        <div class="machine-meta">
          <div class="machine-title">Grundfos CR15-5 Water Pump</div>
          <div class="machine-subtitle">Vertical Multistage Centrifugal Pump</div>
          <div class="specs-pill">5.5 kW | 380V | 15 m³/h | Head: 45m</div>
        </div>
      </div>
      <div class="scan-repair-panel">
        <div class="qr-box">
          <img src="{b64_qr_pump}" alt="Pump QR">
        </div>
        <div class="scan-details">
          <div class="scan-action-title">SCAN TO START PUMP REPAIR</div>
          <div class="qr-string">MACHINE:grundfos-cr-15-001</div>
          <div class="barcode-strip">
            <img src="{b64_bc_pump}" alt="Barcode">
          </div>
          <div class="scan-hint">Triggers Impeller & Mechanical Seal Replacement</div>
        </div>
      </div>
    </div>

    <!-- CARD 2: CUMMINS DIESEL GENERATOR (NEW) -->
    <div class="machine-badge-card emerald-theme">
      <div class="cut-marker">✂ CUT / ATTACH</div>
      <div class="card-top-bar">
        <span class="asset-id-tag">CUMM-C110-2019-0345</span>
        <span class="location-tag">Bay A - Floor 1</span>
      </div>
      <div class="card-middle">
        <div class="machine-thumb">
          <img src="{b64_img_gen}" alt="Cummins Diesel Generator">
        </div>
        <div class="machine-meta">
          <div class="machine-title">Cummins C110D5 Generator</div>
          <div class="machine-subtitle">Soundproof Enclosed Diesel Genset</div>
          <div class="specs-pill">110 kVA | 415V 3Φ | 300L Fuel Tank</div>
        </div>
      </div>
      <div class="scan-repair-panel">
        <div class="qr-box">
          <img src="{b64_qr_gen}" alt="Cummins QR">
        </div>
        <div class="scan-details">
          <div class="scan-action-title">SCAN FOR GENERATOR SERVICE</div>
          <div class="qr-string">MACHINE:cummins-c110d5-001</div>
          <div class="barcode-strip">
            <img src="{b64_bc_gen}" alt="Barcode">
          </div>
          <div class="scan-hint">Triggers Fuel Filter & Governor Calibration</div>
        </div>
      </div>
    </div>

    <!-- CARD 3: SCHULER HYDRAULIC PRESS (NEW) -->
    <div class="machine-badge-card amber-theme">
      <div class="cut-marker">✂ CUT / ATTACH</div>
      <div class="card-top-bar">
        <span class="asset-id-tag">SCH-PH400-2020-0456</span>
        <span class="location-tag">Bay B - Floor 1</span>
      </div>
      <div class="card-middle">
        <div class="machine-thumb">
          <img src="{b64_img_press}" alt="Schuler Hydraulic Press">
        </div>
        <div class="machine-meta">
          <div class="machine-title">Schuler PH-400 Press</div>
          <div class="machine-subtitle">High-Tonnage Hydraulic Stamping Press</div>
          <div class="specs-pill">4000 kN Force | 500mm Stroke | 75 kW</div>
        </div>
      </div>
      <div class="scan-repair-panel">
        <div class="qr-box">
          <img src="{b64_qr_press}" alt="Press QR">
        </div>
        <div class="scan-details">
          <div class="scan-action-title">SCAN FOR PRESS OVERHAUL</div>
          <div class="qr-string">MACHINE:schuler-ph-400-001</div>
          <div class="barcode-strip">
            <img src="{b64_bc_press}" alt="Barcode">
          </div>
          <div class="scan-hint">Triggers Ram Seal & Hydraulic Valve Inspection</div>
        </div>
      </div>
    </div>

    <!-- CARD 4: HAAS VF-2SS CNC -->
    <div class="machine-badge-card cyan-theme">
      <div class="cut-marker">✂ CUT / ATTACH</div>
      <div class="card-top-bar">
        <span class="asset-id-tag">HAAS-VF2-2021-0847</span>
        <span class="location-tag">Bay A - Floor 1</span>
      </div>
      <div class="card-middle">
        <div class="machine-thumb">
          <img src="{b64_img_cnc}" alt="Haas CNC">
        </div>
        <div class="machine-meta">
          <div class="machine-title">Haas VF-2SS CNC Center</div>
          <div class="machine-subtitle">Vertical Machining Center</div>
          <div class="specs-pill">22 kW | 480V 3Φ | 12,000 RPM Spindle</div>
        </div>
      </div>
      <div class="scan-repair-panel">
        <div class="qr-box">
          <img src="{b64_qr_cnc}" alt="Haas QR">
        </div>
        <div class="scan-details">
          <div class="scan-action-title">SCAN TO REPAIR HAAS CNC</div>
          <div class="qr-string">MACHINE:haas-vf-2-001</div>
          <div class="scan-hint">Triggers 9-step Spindle Lubrication Procedure</div>
        </div>
      </div>
    </div>

    <!-- CARD 5: SIEMENS INDUCTION MOTOR -->
    <div class="machine-badge-card violet-theme">
      <div class="cut-marker">✂ CUT / ATTACH</div>
      <div class="card-top-bar">
        <span class="asset-id-tag">SIEM-1LE-2021-0891</span>
        <span class="location-tag">Bay A - Floor 1</span>
      </div>
      <div class="card-middle">
        <div class="machine-thumb">
          <img src="{b64_img_motor}" alt="Siemens Motor">
        </div>
        <div class="machine-meta">
          <div class="machine-title">Siemens 1LE0102 Motor</div>
          <div class="machine-subtitle">Three-Phase Induction Motor</div>
          <div class="specs-pill">15 kW | 400V 50Hz | 1450 RPM (IE3)</div>
        </div>
      </div>
      <div class="scan-repair-panel">
        <div class="qr-box">
          <img src="{b64_qr_motor}" alt="Siemens QR">
        </div>
        <div class="scan-details">
          <div class="scan-action-title">SCAN FOR MOTOR INSPECTION</div>
          <div class="qr-string">MACHINE:siemens-1le0102-001</div>
          <div class="scan-hint">Triggers Winding Megger & Bearing Check</div>
        </div>
      </div>
    </div>

    <!-- CARD 6: ATLAS COPCO ROTARY COMPRESSOR -->
    <div class="machine-badge-card rose-theme">
      <div class="cut-marker">✂ CUT / ATTACH</div>
      <div class="card-top-bar">
        <span class="asset-id-tag">AC-GA37-2020-0567</span>
        <span class="location-tag">Bay A - Floor 1</span>
      </div>
      <div class="card-middle">
        <div class="machine-thumb">
          <img src="{b64_img_comp}" alt="Atlas Copco">
        </div>
        <div class="machine-meta">
          <div class="machine-title">Atlas Copco GA 37+</div>
          <div class="machine-subtitle">Rotary Screw Air Compressor</div>
          <div class="specs-pill">37 kW | 400V | 8.0 bar | 5.8 m³/min</div>
        </div>
      </div>
      <div class="scan-repair-panel">
        <div class="qr-box">
          <img src="{b64_qr_comp}" alt="Atlas QR">
        </div>
        <div class="scan-details">
          <div class="scan-action-title">SCAN TO OVERHAUL COMPRESSOR</div>
          <div class="qr-string">MACHINE:atlas-ga-37-001</div>
          <div class="scan-hint">Triggers Oil Separator & Minimum Pressure Valve</div>
        </div>
      </div>
    </div>

  </div>

</body>
</html>
"""

out_html = os.path.join(BASE, "MaintAI_Machine_Repair_Cards.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[OK] Generated {out_html}")

# Compile to PDF
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_pdf = os.path.join(BASE, "MaintAI_Machine_Repair_Cards.pdf")
url = "file:///" + os.path.abspath(out_html).replace("\\", "/")
cmd = [
    chrome,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={out_pdf}",
    url
]
subprocess.run(cmd, check=True)
print(f"[COMPILED] {out_pdf}")

# Render preview
doc = pymupdf.open(out_pdf)
print(f"PDF Pages: {len(doc)}")
pix = doc[0].get_pixmap(dpi=140)
out_png = os.path.join(PDF_DIR, "preview_machine_repair_cards.png")
pix.save(out_png)
print(f"[RENDERED] Preview: {out_png} ({pix.width}x{pix.height})")

# Copy to downloads
downloads = r"C:\Users\hetjo\Downloads"
shutil.copy2(out_pdf, os.path.join(downloads, "MaintAI_Machine_Repair_Cards.pdf"))
print("[MIRRORED] Copied to Downloads folder.")
