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

# Assets for all 6 machines
b64_img_pump = to_b64(os.path.join(PDF_DIR, "mach_grundfos_pump.jpg"))
b64_qr_pump = to_b64(os.path.join(PDF_DIR, "qr_grundfos_pump.png"))
b64_bc_pump = to_b64(os.path.join(PDF_DIR, "bc_grundfos.png"))

b64_img_gen = to_b64(os.path.join(PDF_DIR, "mach_cummins_gen.jpg"))
b64_qr_gen = to_b64(os.path.join(PDF_DIR, "qr_cummins_gen.png"))
b64_bc_gen = to_b64(os.path.join(PDF_DIR, "bc_cummins.png"))

b64_img_press = to_b64(os.path.join(PDF_DIR, "mach_schuler_press.jpg"))
b64_qr_press = to_b64(os.path.join(PDF_DIR, "qr_schuler_press.png"))
b64_bc_press = to_b64(os.path.join(PDF_DIR, "bc_schuler.png"))

b64_img_cnc = to_b64(os.path.join(BASE, "public", "machines", "cnc-machine.jpg"))
b64_qr_cnc = to_b64(os.path.join(PDF_DIR, "qr_haas_cnc.png"))
b64_bc_cnc = to_b64(os.path.join(PDF_DIR, "bc_haas.png"))

b64_img_motor = to_b64(os.path.join(BASE, "public", "machines", "electric-motor.jpg"))
b64_qr_motor = to_b64(os.path.join(PDF_DIR, "qr_siemens_motor.png"))
b64_bc_motor = to_b64(os.path.join(PDF_DIR, "bc_siemens.png"))

b64_img_comp = to_b64(os.path.join(BASE, "public", "machines", "air-compressor.jpeg"))
b64_qr_comp = to_b64(os.path.join(PDF_DIR, "qr_atlas_compressor.png"))
b64_bc_comp = to_b64(os.path.join(PDF_DIR, "bc_atlas.png"))

b64_qr_launcher = to_b64(os.path.join(PDF_DIR, "qr_app_scan_launcher.png"))

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MaintAI - Equipment Asset Matrix</title>
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
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
      background-color: #f8fafc;
      color: #0f172a;
      display: flex;
      flex-direction: column;
      padding: 10mm 13mm 8mm 13mm;
      overflow: hidden;
      letter-spacing: -0.01em;
    }}

    /* Minimalist Elegant Header */
    header {{
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      padding-bottom: 6mm;
      border-bottom: 1.5px solid #0f172a;
      margin-bottom: 7mm;
    }}
    .header-left {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .brand-eyebrow {{
      font-size: 8.5pt;
      font-weight: 700;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: #64748b;
    }}
    .brand-main-title {{
      font-size: 24pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.03em;
      line-height: 1.1;
    }}
    .brand-descriptor {{
      font-size: 10pt;
      color: #475569;
      font-weight: 400;
      margin-top: 2px;
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #ffffff;
      border: 1px solid #e2e8f0;
      padding: 6px 14px 6px 10px;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .header-launcher-qr {{
      width: 52px;
      height: 52px;
      background: #ffffff;
      display: block;
    }}
    .header-launcher-meta {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .launcher-tag {{
      font-size: 7.5pt;
      font-weight: 700;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: #0284c7;
    }}
    .launcher-url {{
      font-size: 9pt;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-weight: 600;
      color: #0f172a;
    }}
    .launcher-creds {{
      font-size: 7.5pt;
      color: #64748b;
    }}

    /* Grid Layout: 3 Columns x 2 Rows */
    .cards-grid {{
      flex: 1;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: 7mm;
    }}

    /* Classy Luxury Card */
    .machine-card {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04), 0 4px 14px rgba(15, 23, 42, 0.02);
      transition: all 0.2s ease;
    }}

    /* Card Top Bar */
    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      padding-bottom: 5px;
      border-bottom: 1px solid #f1f5f9;
      margin-bottom: 6px;
    }}
    .asset-id-text {{
      font-size: 7.8pt;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-weight: 600;
      color: #475569;
      letter-spacing: 0.04em;
    }}
    .location-text {{
      font-size: 7.8pt;
      font-weight: 500;
      color: #94a3b8;
    }}

    /* Card Middle: Image + Details */
    .card-body {{
      display: flex;
      gap: 12px;
      align-items: center;
      margin-bottom: 8px;
    }}
    .photo-frame {{
      width: 48mm;
      height: 37mm;
      border-radius: 6px;
      overflow: hidden;
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      flex-shrink: 0;
    }}
    .photo-frame img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    .details-frame {{
      display: flex;
      flex-direction: column;
      gap: 2px;
      flex: 1;
    }}
    .category-subtext {{
      font-size: 7.8pt;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #0284c7;
    }}
    .machine-title-text {{
      font-size: 11.5pt;
      font-weight: 700;
      color: #0f172a;
      line-height: 1.25;
      letter-spacing: -0.02em;
    }}
    .specs-container {{
      margin-top: 4px;
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
    }}
    .spec-item {{
      font-size: 7.2pt;
      font-weight: 500;
      color: #334155;
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }}

    /* Card Bottom: Elegant Clean Barcode Dock */
    .barcode-dock {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 7px 10px;
      display: flex;
      align-items: center;
      gap: 12px;
      margin-top: auto;
    }}
    .dock-qr-frame {{
      width: 54px;
      height: 54px;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 3px;
      flex-shrink: 0;
    }}
    .dock-qr-frame img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
    }}

    .dock-info-column {{
      display: flex;
      flex-direction: column;
      gap: 2px;
      flex: 1;
    }}
    .dock-callout {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .dock-action-label {{
      font-size: 8.5pt;
      font-weight: 700;
      color: #0f172a;
      letter-spacing: 0.03em;
    }}
    .dock-qr-raw {{
      font-size: 7.2pt;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-weight: 600;
      color: #0284c7;
    }}
    .dock-barcode-wrap {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 2px 6px;
      margin-top: 2px;
      display: flex;
      align-items: center;
      justify-content: center;
      max-width: 170px;
    }}
    .dock-barcode-wrap img {{
      height: 18px;
      max-width: 100%;
      object-fit: contain;
    }}
    .dock-subtitle {{
      font-size: 7pt;
      color: #64748b;
      margin-top: 1px;
    }}

    /* Footer Telemetry */
    footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 4mm;
      border-top: 1px solid #e2e8f0;
      font-size: 7.8pt;
      color: #64748b;
      margin-top: 4mm;
    }}
    .footer-left {{
      display: flex;
      gap: 16px;
    }}
    .footer-right {{
      font-weight: 500;
      color: #334155;
    }}
  </style>
</head>
<body>

  <!-- MINIMALIST ELEGANT HEADER -->
  <header>
    <div class="header-left">
      <div class="brand-eyebrow">Enterprise Field Maintenance Matrix</div>
      <div class="brand-main-title">MaintAI Industrial Asset Dispatch</div>
      <div class="brand-descriptor">Apex Manufacturing Plant • Real-Time Optical Barcode & Procedure Calibration Rig</div>
    </div>

    <div class="header-right">
      <img src="{b64_qr_launcher}" alt="Launch App" class="header-launcher-qr">
      <div class="header-launcher-meta">
        <span class="launcher-tag">Mobile PWA Console</span>
        <span class="launcher-url">maint-ai.vercel.app/scan</span>
        <span class="launcher-creds">Demo Login: tech1@demo.com</span>
      </div>
    </div>
  </header>

  <!-- CARDS GRID -->
  <div class="cards-grid">

    <!-- 1. GRUNDFOS WATER PUMP -->
    <div class="machine-card">
      <div class="card-header">
        <span class="asset-id-text">CR15-5-2022-1234</span>
        <span class="location-text">Bay A · Floor 1</span>
      </div>
      <div class="card-body">
        <div class="photo-frame">
          <img src="{b64_img_pump}" alt="Grundfos CR15-5">
        </div>
        <div class="details-frame">
          <span class="category-subtext">Centrifugal Pump</span>
          <div class="machine-title-text">Grundfos CR15-5 Water Pump</div>
          <div class="specs-container">
            <span class="spec-item">5.5 kW</span>
            <span class="spec-item">380V</span>
            <span class="spec-item">15 m³/h</span>
            <span class="spec-item">Head: 45m</span>
          </div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-frame">
          <img src="{b64_qr_pump}" alt="Pump QR">
        </div>
        <div class="dock-info-column">
          <div class="dock-callout">
            <span class="dock-action-label">Scan to Dispatch Repair</span>
            <span class="dock-qr-raw">MACHINE:grundfos-cr-15-001</span>
          </div>
          <div class="dock-barcode-wrap">
            <img src="{b64_bc_pump}" alt="Barcode">
          </div>
          <span class="dock-subtitle">Impeller & Mechanical Seal Replacement Procedure</span>
        </div>
      </div>
    </div>

    <!-- 2. CUMMINS GENERATOR -->
    <div class="machine-card">
      <div class="card-header">
        <span class="asset-id-text">CUMM-C110-2019-0345</span>
        <span class="location-text">Bay A · Floor 1</span>
      </div>
      <div class="card-body">
        <div class="photo-frame">
          <img src="{b64_img_gen}" alt="Cummins C110D5">
        </div>
        <div class="details-frame">
          <span class="category-subtext">Diesel Generator</span>
          <div class="machine-title-text">Cummins C110D5 Genset</div>
          <div class="specs-container">
            <span class="spec-item">110 kVA</span>
            <span class="spec-item">415V 3Φ</span>
            <span class="spec-item">300L Fuel</span>
            <span class="spec-item">Silent Canopy</span>
          </div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-frame">
          <img src="{b64_qr_gen}" alt="Cummins QR">
        </div>
        <div class="dock-info-column">
          <div class="dock-callout">
            <span class="dock-action-label">Scan to Dispatch Repair</span>
            <span class="dock-qr-raw">MACHINE:cummins-c110d5-001</span>
          </div>
          <div class="dock-barcode-wrap">
            <img src="{b64_bc_gen}" alt="Barcode">
          </div>
          <span class="dock-subtitle">Fuel System & Governor Calibration Procedure</span>
        </div>
      </div>
    </div>

    <!-- 3. SCHULER HYDRAULIC PRESS -->
    <div class="machine-card">
      <div class="card-header">
        <span class="asset-id-text">SCH-PH400-2020-0456</span>
        <span class="location-text">Bay B · Floor 1</span>
      </div>
      <div class="card-body">
        <div class="photo-frame">
          <img src="{b64_img_press}" alt="Schuler PH-400">
        </div>
        <div class="details-frame">
          <span class="category-subtext">Hydraulic Press</span>
          <div class="machine-title-text">Schuler PH-400 Stamping Press</div>
          <div class="specs-container">
            <span class="spec-item">4000 kN Force</span>
            <span class="spec-item">500mm Stroke</span>
            <span class="spec-item">75 kW</span>
          </div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-frame">
          <img src="{b64_qr_press}" alt="Schuler QR">
        </div>
        <div class="dock-info-column">
          <div class="dock-callout">
            <span class="dock-action-label">Scan to Dispatch Repair</span>
            <span class="dock-qr-raw">MACHINE:schuler-ph-400-001</span>
          </div>
          <div class="dock-barcode-wrap">
            <img src="{b64_bc_press}" alt="Barcode">
          </div>
          <span class="dock-subtitle">Ram Packing & Proportional Valve Overhaul</span>
        </div>
      </div>
    </div>

    <!-- 4. HAAS VF-2SS CNC -->
    <div class="machine-card">
      <div class="card-header">
        <span class="asset-id-text">HAAS-VF2-2021-0847</span>
        <span class="location-text">Bay A · Floor 1</span>
      </div>
      <div class="card-body">
        <div class="photo-frame">
          <img src="{b64_img_cnc}" alt="Haas VF-2SS">
        </div>
        <div class="details-frame">
          <span class="category-subtext">CNC Machining Center</span>
          <div class="machine-title-text">Haas VF-2SS Milling Center</div>
          <div class="specs-container">
            <span class="spec-item">22 kW</span>
            <span class="spec-item">480V 3Φ</span>
            <span class="spec-item">12,000 RPM</span>
            <span class="spec-item">30+1 ATC</span>
          </div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-frame">
          <img src="{b64_qr_cnc}" alt="Haas QR">
        </div>
        <div class="dock-info-column">
          <div class="dock-callout">
            <span class="dock-action-label">Scan to Dispatch Repair</span>
            <span class="dock-qr-raw">MACHINE:haas-vf-2-001</span>
          </div>
          <div class="dock-barcode-wrap">
            <img src="{b64_bc_cnc}" alt="Barcode">
          </div>
          <span class="dock-subtitle">Spindle Oil Change & LOTO Isolation Procedure</span>
        </div>
      </div>
    </div>

    <!-- 5. SIEMENS MOTOR -->
    <div class="machine-card">
      <div class="card-header">
        <span class="asset-id-text">SIEM-1LE-2021-0891</span>
        <span class="location-text">Bay A · Floor 1</span>
      </div>
      <div class="card-body">
        <div class="photo-frame">
          <img src="{b64_img_motor}" alt="Siemens 1LE0102">
        </div>
        <div class="details-frame">
          <span class="category-subtext">Induction Motor</span>
          <div class="machine-title-text">Siemens 1LE0102 Motor</div>
          <div class="specs-container">
            <span class="spec-item">15 kW</span>
            <span class="spec-item">400V 50Hz</span>
            <span class="spec-item">1450 RPM</span>
            <span class="spec-item">IE3 Premium</span>
          </div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-frame">
          <img src="{b64_qr_motor}" alt="Siemens QR">
        </div>
        <div class="dock-info-column">
          <div class="dock-callout">
            <span class="dock-action-label">Scan to Dispatch Repair</span>
            <span class="dock-qr-raw">MACHINE:siemens-1le0102-001</span>
          </div>
          <div class="dock-barcode-wrap">
            <img src="{b64_bc_motor}" alt="Barcode">
          </div>
          <span class="dock-subtitle">Stator Insulation Resistance & Bearing Inspection</span>
        </div>
      </div>
    </div>

    <!-- 6. ATLAS COPCO COMPRESSOR -->
    <div class="machine-card">
      <div class="card-header">
        <span class="asset-id-text">AC-GA37-2020-0567</span>
        <span class="location-text">Bay A · Floor 1</span>
      </div>
      <div class="card-body">
        <div class="photo-frame">
          <img src="{b64_img_comp}" alt="Atlas Copco GA 37+">
        </div>
        <div class="details-frame">
          <span class="category-subtext">Rotary Screw Compressor</span>
          <div class="machine-title-text">Atlas Copco GA 37+ Compressor</div>
          <div class="specs-container">
            <span class="spec-item">37 kW</span>
            <span class="spec-item">400V</span>
            <span class="spec-item">8.0 bar</span>
            <span class="spec-item">5.8 m³/min</span>
          </div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-frame">
          <img src="{b64_qr_comp}" alt="Atlas QR">
        </div>
        <div class="dock-info-column">
          <div class="dock-callout">
            <span class="dock-action-label">Scan to Dispatch Repair</span>
            <span class="dock-qr-raw">MACHINE:atlas-ga-37-001</span>
          </div>
          <div class="dock-barcode-wrap">
            <img src="{b64_bc_comp}" alt="Barcode">
          </div>
          <span class="dock-subtitle">Air/Oil Separator Element & Thermostatic Valve</span>
        </div>
      </div>
    </div>

  </div>

  <!-- MINIMAL FOOTER -->
  <footer>
    <div class="footer-left">
      <span>MaintAI™ Enterprise Field Maintenance System</span>
      <span>·</span>
      <span>Direct-Scan Equipment Matrix</span>
      <span>·</span>
      <span>Sub-150ms Camera QR Engine</span>
    </div>
    <div class="footer-right">
      Apex Manufacturing Plant · Pune, Maharashtra
    </div>
  </footer>

</body>
</html>
"""

# Output files
out_html = os.path.join(BASE, "MaintAI_Classy_Modern_Poster.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[OK] Generated {out_html}")

# Also update MaintAI_Machine_Repair_Cards.html so the user's open links get the luxury edition!
with open(os.path.join(BASE, "MaintAI_Machine_Repair_Cards.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

# Compile to PDF
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_pdf = os.path.join(BASE, "MaintAI_Classy_Modern_Poster.pdf")
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

# Overwrite MaintAI_Machine_Repair_Cards.pdf as well
shutil.copy2(out_pdf, os.path.join(BASE, "MaintAI_Machine_Repair_Cards.pdf"))

# Render preview
doc = pymupdf.open(out_pdf)
print(f"PDF Pages: {len(doc)}")
pix = doc[0].get_pixmap(dpi=140)
out_png = os.path.join(PDF_DIR, "preview_classy_modern_poster.png")
pix.save(out_png)
print(f"[RENDERED] Preview: {out_png} ({pix.width}x{pix.height})")

# Copy to downloads
downloads = r"C:\Users\hetjo\Downloads"
shutil.copy2(out_pdf, os.path.join(downloads, "MaintAI_Classy_Modern_Poster.pdf"))
shutil.copy2(out_pdf, os.path.join(downloads, "MaintAI_Machine_Repair_Cards.pdf"))
print("[MIRRORED] Copied to Downloads folder.")
