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
  <title>MaintAI - Industrial Equipment Repair & Calibration Matrix</title>
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
      background: radial-gradient(circle at 50% 10%, #0d1933 0%, #040814 65%, #02040a 100%);
      color: #f1f5f9;
      display: flex;
      flex-direction: column;
      padding: 8mm 11mm;
      overflow: hidden;
      position: relative;
    }}

    /* Subtle Technical Grid Overlay */
    body::before {{
      content: "";
      position: absolute;
      inset: 0;
      background-image: 
        linear-gradient(to right, rgba(56, 189, 248, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(56, 189, 248, 0.03) 1px, transparent 1px);
      background-size: 15mm 15mm;
      pointer-events: none;
    }}

    /* Outer Decorative Frame */
    .outer-frame-border {{
      position: absolute;
      inset: 5mm;
      border: 1px solid rgba(56, 189, 248, 0.2);
      border-radius: 10px;
      pointer-events: none;
    }}
    .corner-bracket {{
      position: absolute;
      width: 14px;
      height: 14px;
      border-color: #38bdf8;
      border-style: solid;
      pointer-events: none;
    }}
    .bracket-tl {{ top: 4mm; left: 4mm; border-width: 2.5px 0 0 2.5px; }}
    .bracket-tr {{ top: 4mm; right: 4mm; border-width: 2.5px 2.5px 0 0; }}
    .bracket-bl {{ bottom: 4mm; left: 4mm; border-width: 0 0 2.5px 2.5px; }}
    .bracket-br {{ bottom: 4mm; right: 4mm; border-width: 0 2.5px 2.5px 0; }}

    /* Header Bar */
    header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 100%);
      border: 1.5px solid #334155;
      border-radius: 10px;
      padding: 7px 18px;
      margin-bottom: 7mm;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
      position: relative;
      z-index: 10;
    }}
    .header-left {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .header-title-row {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-logo-text {{
      font-size: 18pt;
      font-weight: 900;
      color: #38bdf8;
      letter-spacing: -0.5px;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 8px;
      text-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
    }}
    .brand-chip {{
      font-size: 8.5pt;
      font-weight: 800;
      background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
      color: #000;
      padding: 3px 9px;
      border-radius: 4px;
      letter-spacing: 0.8px;
    }}
    .header-subtitle {{
      font-size: 9pt;
      color: #94a3b8;
      font-weight: 500;
    }}
    .telemetry-row {{
      display: flex;
      gap: 8px;
      margin-top: 2px;
    }}
    .telemetry-pill {{
      font-size: 7.5pt;
      font-weight: 600;
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.3);
      color: #7dd3fc;
      padding: 1px 7px;
      border-radius: 3px;
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(2, 6, 23, 0.9);
      padding: 5px 12px;
      border-radius: 8px;
      border: 1.5px solid #0284c7;
      box-shadow: 0 0 12px rgba(2, 132, 199, 0.3);
    }}
    .launcher-qr {{
      width: 52px;
      height: 52px;
      background: #ffffff;
      border-radius: 5px;
      padding: 2.5px;
    }}
    .launcher-desc {{
      display: flex;
      flex-direction: column;
      gap: 1px;
    }}
    .launcher-heading {{
      font-size: 9.5pt;
      font-weight: 800;
      color: #38bdf8;
    }}
    .launcher-link {{
      font-size: 8pt;
      font-family: monospace;
      font-weight: 700;
      color: #f8fafc;
    }}
    .launcher-auth {{
      font-size: 7pt;
      color: #fbbf24;
      font-weight: 600;
    }}

    /* Grid of 6 Machine Cards */
    .cards-grid {{
      flex: 1;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(2, 1fr);
      gap: 6.5mm;
      position: relative;
      z-index: 10;
    }}

    /* Card Aesthetic */
    .machine-card {{
      background: linear-gradient(160deg, #0e172a 0%, #070d1d 100%);
      border-radius: 12px;
      border: 1.5px solid #334155;
      padding: 9px 12px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      box-shadow: 0 8px 20px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.06);
    }}

    /* Color Theme Accents */
    .theme-cyan {{ border-color: #06b6d4; box-shadow: 0 4px 18px rgba(6, 182, 212, 0.15); }}
    .theme-emerald {{ border-color: #10b981; box-shadow: 0 4px 18px rgba(16, 185, 129, 0.15); }}
    .theme-amber {{ border-color: #f59e0b; box-shadow: 0 4px 18px rgba(245, 158, 11, 0.15); }}
    .theme-blue {{ border-color: #38bdf8; box-shadow: 0 4px 18px rgba(56, 189, 248, 0.15); }}
    .theme-violet {{ border-color: #a855f7; box-shadow: 0 4px 18px rgba(168, 85, 247, 0.15); }}
    .theme-rose {{ border-color: #f43f5e; box-shadow: 0 4px 18px rgba(244, 63, 94, 0.15); }}

    /* Card Header */
    .card-meta-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 5px;
      padding-bottom: 4px;
      border-bottom: 1px solid rgba(51, 65, 85, 0.6);
    }}
    .status-indicator {{
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 7.2pt;
      font-weight: 700;
      color: #34d399;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .status-led {{
      width: 7px;
      height: 7px;
      background: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
    }}
    .asset-tag-badge {{
      font-size: 7.5pt;
      font-family: monospace;
      font-weight: 800;
      color: #fbbf24;
      background: rgba(245, 158, 11, 0.12);
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 2px 7px;
      border-radius: 4px;
    }}
    .bay-badge {{
      font-size: 7.2pt;
      color: #94a3b8;
      font-weight: 600;
    }}

    /* Card Mid: Photo & Identity */
    .card-mid-section {{
      display: flex;
      gap: 11px;
      align-items: center;
      margin-bottom: 6px;
    }}
    .machine-photo-frame {{
      width: 50mm;
      height: 38mm;
      border-radius: 8px;
      overflow: hidden;
      border: 1.5px solid #334155;
      background: #000;
      flex-shrink: 0;
      position: relative;
      box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }}
    .machine-photo-frame img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .reticle-overlay-tag {{
      position: absolute;
      bottom: 3px;
      left: 3px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid #38bdf8;
      color: #7dd3fc;
      font-size: 6pt;
      font-weight: 700;
      padding: 1px 4px;
      border-radius: 3px;
    }}

    .machine-details {{
      display: flex;
      flex-direction: column;
      gap: 3px;
      flex: 1;
    }}
    .machine-headline {{
      font-size: 11.5pt;
      font-weight: 800;
      color: #f8fafc;
      letter-spacing: -0.2px;
      line-height: 1.2;
    }}
    .machine-category {{
      font-size: 8.2pt;
      color: #38bdf8;
      font-weight: 600;
    }}
    .specs-pill-box {{
      font-size: 7.2pt;
      color: #cbd5e1;
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid #334155;
      padding: 3px 7px;
      border-radius: 4px;
      font-family: monospace;
      margin-top: 3px;
      width: fit-content;
    }}

    /* Card Bottom: Barcode & QR Scan Dock */
    .barcode-dock {{
      background: rgba(2, 6, 23, 0.9);
      border: 1.5px solid #1e293b;
      border-radius: 8px;
      padding: 6px 9px;
      display: flex;
      align-items: center;
      gap: 10px;
      margin-top: auto;
    }}
    .dock-qr-wrap {{
      width: 58px;
      height: 58px;
      background: #ffffff;
      border-radius: 6px;
      padding: 3px;
      flex-shrink: 0;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }}
    .dock-qr-wrap img {{
      width: 100%;
      height: 100%;
      object-fit: contain;
    }}
    .dock-info {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .dock-action-title {{
      font-size: 8.8pt;
      font-weight: 800;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .dock-action-title::before {{
      content: "⚡";
      font-size: 9pt;
      color: #f59e0b;
    }}
    .dock-qr-text {{
      font-size: 7.2pt;
      font-family: monospace;
      font-weight: 700;
      color: #fbbf24;
    }}
    .dock-barcode-img {{
      margin-top: 2px;
      background: #ffffff;
      padding: 2px 5px;
      border-radius: 3px;
      display: flex;
      align-items: center;
      justify-content: center;
      max-width: 165px;
    }}
    .dock-barcode-img img {{
      height: 18px;
      max-width: 100%;
      object-fit: contain;
    }}
    .dock-desc {{
      font-size: 6.8pt;
      color: #94a3b8;
    }}

    /* Footer Telemetry Bar */
    footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid #334155;
      border-radius: 6px;
      padding: 4px 14px;
      margin-top: 5mm;
      font-size: 7.2pt;
      color: #64748b;
      position: relative;
      z-index: 10;
    }}
    .footer-left {{
      display: flex;
      gap: 12px;
    }}
    .footer-right {{
      color: #94a3b8;
      font-weight: 600;
    }}
  </style>
</head>
<body>

  <!-- CORNER BRACKETS -->
  <div class="outer-frame-border"></div>
  <div class="corner-bracket bracket-tl"></div>
  <div class="corner-bracket bracket-tr"></div>
  <div class="corner-bracket bracket-bl"></div>
  <div class="corner-bracket bracket-br"></div>

  <!-- HEADER -->
  <header>
    <div class="header-left">
      <div class="header-title-row">
        <div class="brand-logo-text">
          <span>MAINTAI™ INDUSTRIAL ASSET MATRIX</span>
        </div>
        <span class="brand-chip">ACTIVE SHOP-FLOOR DISPATCH</span>
      </div>
      <div class="header-subtitle">
        Apex Manufacturing Plant Simulation • High-Speed Optical QR & Barcode Dispatch Matrix for Mobile Field Technicians
      </div>
      <div class="telemetry-row">
        <span class="telemetry-pill">6 Heavy Assets Registered</span>
        <span class="telemetry-pill">Instant 120ms Optical Decode</span>
        <span class="telemetry-pill">Hands-Free AR Procedure Ready</span>
        <span class="telemetry-pill">Offline WAL Sync Protected</span>
      </div>
    </div>

    <div class="header-right">
      <img src="{b64_qr_launcher}" alt="Launch PWA" class="launcher-qr">
      <div class="launcher-desc">
        <div class="launcher-heading">LAUNCH MOBILE PWA</div>
        <div class="launcher-link">maint-ai.vercel.app/scan</div>
        <div class="launcher-auth">Demo Tech: tech1@demo.com | demo123456</div>
      </div>
    </div>
  </header>

  <!-- 6 CARDS GRID -->
  <div class="cards-grid">

    <!-- 1. GRUNDFOS WATER PUMP -->
    <div class="machine-card theme-cyan">
      <div class="card-meta-bar">
        <div class="status-indicator">
          <div class="status-led"></div>
          <span>Active Asset</span>
        </div>
        <span class="asset-tag-badge">CR15-5-2022-1234</span>
        <span class="bay-badge">Bay A - Floor 1</span>
      </div>
      <div class="card-mid-section">
        <div class="machine-photo-frame">
          <img src="{b64_img_pump}" alt="Grundfos Water Pump">
          <div class="reticle-overlay-tag">AR RETICLE READY</div>
        </div>
        <div class="machine-details">
          <div class="machine-headline">Grundfos CR15-5 Water Pump</div>
          <div class="machine-category">Vertical Multistage Centrifugal Pump</div>
          <div class="specs-pill-box">5.5 kW • 380V • 15 m³/h • Head: 45m</div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-wrap">
          <img src="{b64_qr_pump}" alt="Pump QR">
        </div>
        <div class="dock-info">
          <div class="dock-action-title">SCAN TO START PUMP REPAIR</div>
          <div class="dock-qr-text">MACHINE:grundfos-cr-15-001</div>
          <div class="dock-barcode-img">
            <img src="{b64_bc_pump}" alt="Barcode">
          </div>
          <div class="dock-desc">Triggers Impeller & Mechanical Seal Replacement</div>
        </div>
      </div>
    </div>

    <!-- 2. CUMMINS DIESEL GENERATOR -->
    <div class="machine-card theme-emerald">
      <div class="card-meta-bar">
        <div class="status-indicator">
          <div class="status-led"></div>
          <span>Active Asset</span>
        </div>
        <span class="asset-tag-badge">CUMM-C110-2019-0345</span>
        <span class="bay-badge">Bay A - Floor 1</span>
      </div>
      <div class="card-mid-section">
        <div class="machine-photo-frame">
          <img src="{b64_img_gen}" alt="Cummins Generator">
          <div class="reticle-overlay-tag">AR RETICLE READY</div>
        </div>
        <div class="machine-details">
          <div class="machine-headline">Cummins C110D5 Generator</div>
          <div class="machine-category">Soundproof Enclosed Diesel Genset</div>
          <div class="specs-pill-box">110 kVA • 415V 3Φ • 300L Fuel Tank</div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-wrap">
          <img src="{b64_qr_gen}" alt="Generator QR">
        </div>
        <div class="dock-info">
          <div class="dock-action-title">SCAN FOR GENERATOR SERVICE</div>
          <div class="dock-qr-text">MACHINE:cummins-c110d5-001</div>
          <div class="dock-barcode-img">
            <img src="{b64_bc_gen}" alt="Barcode">
          </div>
          <div class="dock-desc">Triggers Fuel Filter & Governor Calibration</div>
        </div>
      </div>
    </div>

    <!-- 3. SCHULER HYDRAULIC PRESS -->
    <div class="machine-card theme-amber">
      <div class="card-meta-bar">
        <div class="status-indicator">
          <div class="status-led"></div>
          <span>Active Asset</span>
        </div>
        <span class="asset-tag-badge">SCH-PH400-2020-0456</span>
        <span class="bay-badge">Bay B - Floor 1</span>
      </div>
      <div class="card-mid-section">
        <div class="machine-photo-frame">
          <img src="{b64_img_press}" alt="Schuler Press">
          <div class="reticle-overlay-tag">AR RETICLE READY</div>
        </div>
        <div class="machine-details">
          <div class="machine-headline">Schuler PH-400 Press</div>
          <div class="machine-category">High-Tonnage Hydraulic Stamping Press</div>
          <div class="specs-pill-box">4000 kN Force • 500mm Stroke • 75 kW</div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-wrap">
          <img src="{b64_qr_press}" alt="Press QR">
        </div>
        <div class="dock-info">
          <div class="dock-action-title">SCAN FOR PRESS OVERHAUL</div>
          <div class="dock-qr-text">MACHINE:schuler-ph-400-001</div>
          <div class="dock-barcode-img">
            <img src="{b64_bc_press}" alt="Barcode">
          </div>
          <div class="dock-desc">Triggers Ram Seal & Hydraulic Valve Inspection</div>
        </div>
      </div>
    </div>

    <!-- 4. HAAS VF-2SS CNC -->
    <div class="machine-card theme-blue">
      <div class="card-meta-bar">
        <div class="status-indicator">
          <div class="status-led"></div>
          <span>Active Asset</span>
        </div>
        <span class="asset-tag-badge">HAAS-VF2-2021-0847</span>
        <span class="bay-badge">Bay A - Floor 1</span>
      </div>
      <div class="card-mid-section">
        <div class="machine-photo-frame">
          <img src="{b64_img_cnc}" alt="Haas CNC">
          <div class="reticle-overlay-tag">AR RETICLE READY</div>
        </div>
        <div class="machine-details">
          <div class="machine-headline">Haas VF-2SS CNC Center</div>
          <div class="machine-category">Vertical Machining Center</div>
          <div class="specs-pill-box">22 kW • 480V 3Φ • 12,000 RPM Spindle</div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-wrap">
          <img src="{b64_qr_cnc}" alt="Haas QR">
        </div>
        <div class="dock-info">
          <div class="dock-action-title">SCAN TO REPAIR HAAS CNC</div>
          <div class="dock-qr-text">MACHINE:haas-vf-2-001</div>
          <div class="dock-barcode-img">
            <img src="{b64_bc_cnc}" alt="Barcode">
          </div>
          <div class="dock-desc">Triggers 9-step Spindle Lubrication Procedure</div>
        </div>
      </div>
    </div>

    <!-- 5. SIEMENS INDUCTION MOTOR -->
    <div class="machine-card theme-violet">
      <div class="card-meta-bar">
        <div class="status-indicator">
          <div class="status-led"></div>
          <span>Active Asset</span>
        </div>
        <span class="asset-tag-badge">SIEM-1LE-2021-0891</span>
        <span class="bay-badge">Bay A - Floor 1</span>
      </div>
      <div class="card-mid-section">
        <div class="machine-photo-frame">
          <img src="{b64_img_motor}" alt="Siemens Motor">
          <div class="reticle-overlay-tag">AR RETICLE READY</div>
        </div>
        <div class="machine-details">
          <div class="machine-headline">Siemens 1LE0102 Motor</div>
          <div class="machine-category">Three-Phase Induction Motor</div>
          <div class="specs-pill-box">15 kW • 400V 50Hz • 1450 RPM (IE3)</div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-wrap">
          <img src="{b64_qr_motor}" alt="Siemens QR">
        </div>
        <div class="dock-info">
          <div class="dock-action-title">SCAN FOR MOTOR INSPECTION</div>
          <div class="dock-qr-text">MACHINE:siemens-1le0102-001</div>
          <div class="dock-barcode-img">
            <img src="{b64_bc_motor}" alt="Barcode">
          </div>
          <div class="dock-desc">Triggers Winding Megger & Bearing Check</div>
        </div>
      </div>
    </div>

    <!-- 6. ATLAS COPCO COMPRESSOR -->
    <div class="machine-card theme-rose">
      <div class="card-meta-bar">
        <div class="status-indicator">
          <div class="status-led"></div>
          <span>Active Asset</span>
        </div>
        <span class="asset-tag-badge">AC-GA37-2020-0567</span>
        <span class="bay-badge">Bay A - Floor 1</span>
      </div>
      <div class="card-mid-section">
        <div class="machine-photo-frame">
          <img src="{b64_img_comp}" alt="Atlas Copco">
          <div class="reticle-overlay-tag">AR RETICLE READY</div>
        </div>
        <div class="machine-details">
          <div class="machine-headline">Atlas Copco GA 37+</div>
          <div class="machine-category">Rotary Screw Air Compressor</div>
          <div class="specs-pill-box">37 kW • 400V • 8.0 bar • 5.8 m³/min</div>
        </div>
      </div>
      <div class="barcode-dock">
        <div class="dock-qr-wrap">
          <img src="{b64_qr_comp}" alt="Atlas QR">
        </div>
        <div class="dock-info">
          <div class="dock-action-title">SCAN TO OVERHAUL COMPRESSOR</div>
          <div class="dock-qr-text">MACHINE:atlas-ga-37-001</div>
          <div class="dock-barcode-img">
            <img src="{b64_bc_comp}" alt="Barcode">
          </div>
          <div class="dock-desc">Triggers Oil Separator & Minimum Pressure Valve</div>
        </div>
      </div>
    </div>

  </div>

  <!-- FOOTER TELEMETRY -->
  <footer>
    <div class="footer-left">
      <span>MaintAI™ Enterprise Field System v2.4</span>
      <span>•</span>
      <span>ISO 55000 Physical Asset Management</span>
      <span>•</span>
      <span>PostgreSQL 16 & Dexie.js WAL Sync</span>
    </div>
    <div class="footer-right">
      Apex Manufacturing Plant Simulation Rig • Ready for Direct Print & Live Inspection
    </div>
  </footer>

</body>
</html>
"""

# Write to MaintAI_Decorative_Machine_Poster.html and MaintAI_Machine_Repair_Cards.html
for fname in ["MaintAI_Decorative_Machine_Poster.html", "MaintAI_Machine_Repair_Cards.html"]:
    p = os.path.join(BASE, fname)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Generated {p}")

# Compile to PDF
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_pdf = os.path.join(BASE, "MaintAI_Decorative_Machine_Poster.pdf")
url = "file:///" + os.path.abspath(os.path.join(BASE, "MaintAI_Decorative_Machine_Poster.html")).replace("\\", "/")
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
out_png = os.path.join(PDF_DIR, "preview_decorative_machine_poster.png")
pix.save(out_png)
print(f"[RENDERED] Preview: {out_png} ({pix.width}x{pix.height})")

# Copy to downloads
downloads = r"C:\Users\hetjo\Downloads"
shutil.copy2(out_pdf, os.path.join(downloads, "MaintAI_Decorative_Machine_Poster.pdf"))
shutil.copy2(out_pdf, os.path.join(downloads, "MaintAI_Machine_Repair_Cards.pdf"))
print("[MIRRORED] Copied to Downloads folder.")
