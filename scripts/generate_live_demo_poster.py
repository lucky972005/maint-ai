import os
import base64
import subprocess
import pymupdf
import shutil

BASE = r"c:\dev\pro"
PDF_DIR = os.path.join(BASE, "pdf_images")
PUB_DIR = os.path.join(BASE, "public")

def to_b64(filepath):
    ext = os.path.splitext(filepath)[1].lower().replace('.', '')
    if ext == 'jpg': ext = 'jpeg'
    mime = f"image/{ext}" if ext in ['png', 'jpeg', 'svg'] else 'image/jpeg'
    with open(filepath, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode("utf-8")

# Assets
b64_qr_haas = to_b64(os.path.join(PDF_DIR, "qr_haas_cnc.png"))
b64_qr_siemens = to_b64(os.path.join(PDF_DIR, "qr_siemens_motor.png"))
b64_qr_atlas = to_b64(os.path.join(PDF_DIR, "qr_atlas_compressor.png"))
b64_qr_flexco = to_b64(os.path.join(PDF_DIR, "qr_flexco_conveyor.png"))
b64_qr_launcher = to_b64(os.path.join(PDF_DIR, "qr_app_scan_launcher.png"))

b64_bc_01001 = to_b64(os.path.join(PDF_DIR, "barcode_pn_01001.png"))
b64_bc_01002 = to_b64(os.path.join(PDF_DIR, "barcode_pn_01002.png"))
b64_bc_01004 = to_b64(os.path.join(PDF_DIR, "barcode_pn_01004.png"))
b64_bc_01006 = to_b64(os.path.join(PDF_DIR, "barcode_pn_01006.png"))

b64_tool_multi = to_b64(os.path.join(PDF_DIR, "tool_multimeter.jpg"))
b64_tool_wrench = to_b64(os.path.join(PDF_DIR, "tool_wrench.jpg"))
b64_tool_pliers = to_b64(os.path.join(PDF_DIR, "tool_pliers.jpg"))
b64_tool_allen = to_b64(os.path.join(PDF_DIR, "tool_allen_key.jpg"))

b64_mach_cnc = to_b64(os.path.join(PUB_DIR, "machines", "cnc-machine.jpg"))
b64_mach_motor = to_b64(os.path.join(PUB_DIR, "machines", "electric-motor.jpg"))
b64_mach_comp = to_b64(os.path.join(PUB_DIR, "machines", "air-compressor.jpeg"))
b64_mach_conv = to_b64(os.path.join(PUB_DIR, "machines", "conveyor-belt.jpg"))

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MaintAI - Live Demo Interactive Shop-Floor Simulation & Calibration Rig</title>
  <style>
    @page {{
      size: 594mm 420mm; /* A2 Landscape */
      margin: 0;
    }}
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      width: 594mm;
      height: 420mm;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: #0b1120;
      color: #f1f5f9;
      display: flex;
      flex-direction: column;
      padding: 10mm 12mm 8mm 12mm;
      overflow: hidden;
      position: relative;
    }}

    /* Hazard Border Accent */
    .hazard-stripe {{
      height: 5px;
      width: 100%;
      background: repeating-linear-gradient(
        -45deg,
        #f59e0b,
        #f59e0b 12px,
        #0b1120 12px,
        #0b1120 24px
      );
      margin-bottom: 8px;
    }}

    /* Header */
    header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      border: 1.5px solid #334155;
      border-radius: 8px;
      padding: 10px 18px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.4);
      margin-bottom: 10px;
    }}
    .header-left {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .brand-title {{
      font-size: 24pt;
      font-weight: 900;
      letter-spacing: -0.5px;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-badge {{
      background: #f59e0b;
      color: #000;
      font-size: 10pt;
      font-weight: 800;
      padding: 3px 9px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
    }}
    .subtitle {{
      font-size: 11pt;
      color: #94a3b8;
      font-weight: 500;
    }}
    .tech-pill-row {{
      display: flex;
      gap: 8px;
      margin-top: 4px;
    }}
    .tech-pill {{
      font-size: 8.5pt;
      font-weight: 600;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.35);
      color: #7dd3fc;
      padding: 2px 8px;
      border-radius: 4px;
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: rgba(15, 23, 42, 0.85);
      padding: 6px 14px;
      border-radius: 8px;
      border: 1.5px solid #0284c7;
    }}
    .launcher-qr {{
      width: 65px;
      height: 65px;
      background: #fff;
      padding: 3px;
      border-radius: 6px;
    }}
    .launcher-text {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .launcher-title {{
      font-size: 11pt;
      font-weight: 800;
      color: #38bdf8;
    }}
    .launcher-url {{
      font-size: 9.5pt;
      font-weight: 700;
      color: #f8fafc;
      font-family: monospace;
    }}
    .launcher-cred {{
      font-size: 8pt;
      color: #fbbf24;
      font-weight: 600;
    }}

    /* Main Grid Layout */
    .main-grid {{
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    /* Workstations Section */
    .section-title-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-left: 4px solid #38bdf8;
      padding-left: 8px;
      margin-bottom: 6px;
    }}
    .section-title {{
      font-size: 12pt;
      font-weight: 800;
      color: #f8fafc;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .section-desc {{
      font-size: 9pt;
      color: #94a3b8;
    }}

    .machines-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      height: 148mm;
    }}

    .machine-card {{
      background: #111827;
      border: 1.5px solid #334155;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      padding: 8px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.5);
      position: relative;
    }}
    .machine-card:hover {{
      border-color: #38bdf8;
    }}
    .station-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 5px;
      border-bottom: 1px solid #1e293b;
      padding-bottom: 4px;
    }}
    .station-badge {{
      font-size: 8.5pt;
      font-weight: 800;
      background: #0284c7;
      color: #fff;
      padding: 2px 6px;
      border-radius: 3px;
    }}
    .station-loc {{
      font-size: 7.5pt;
      color: #94a3b8;
      font-weight: 600;
    }}
    .machine-name {{
      font-size: 11pt;
      font-weight: 800;
      color: #f1f5f9;
      margin-bottom: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .machine-model {{
      font-size: 8pt;
      color: #38bdf8;
      font-weight: 600;
      margin-bottom: 6px;
    }}

    /* Machine Photo with Target Crosshairs */
    .photo-container {{
      position: relative;
      width: 100%;
      height: 64mm;
      border-radius: 6px;
      overflow: hidden;
      border: 1px solid #334155;
      background: #000;
      margin-bottom: 6px;
    }}
    .photo-container img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    /* AR Target Overlays */
    .ar-target {{
      position: absolute;
      background: rgba(15, 23, 42, 0.85);
      border: 1.5px solid #f59e0b;
      color: #fbbf24;
      font-size: 6.8pt;
      font-weight: 800;
      padding: 2px 5px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      gap: 3px;
      box-shadow: 0 0 8px rgba(245, 158, 11, 0.5);
    }}
    .ar-target::before {{
      content: "🎯";
      font-size: 7.5pt;
    }}
    .target-1 {{ top: 12%; left: 8%; }}
    .target-2 {{ bottom: 12%; right: 8%; }}

    /* Specs bar */
    .specs-strip {{
      font-size: 7.2pt;
      color: #cbd5e1;
      background: #1e293b;
      padding: 4px 6px;
      border-radius: 4px;
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      font-family: monospace;
    }}

    /* Machine QR & Scan Prompt */
    .qr-action-box {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: #0f172a;
      border: 1.5px dashed #0ea5e9;
      border-radius: 6px;
      padding: 6px;
      margin-top: auto;
    }}
    .machine-qr-img {{
      width: 50px;
      height: 50px;
      background: #fff;
      padding: 2px;
      border-radius: 4px;
      flex-shrink: 0;
    }}
    .qr-info {{
      display: flex;
      flex-direction: column;
      gap: 1px;
    }}
    .qr-code-raw {{
      font-size: 7pt;
      font-family: monospace;
      color: #fbbf24;
      font-weight: 700;
    }}
    .qr-trigger-label {{
      font-size: 8pt;
      font-weight: 800;
      color: #38bdf8;
      line-height: 1.2;
    }}
    .qr-tap-hint {{
      font-size: 6.8pt;
      color: #94a3b8;
    }}

    /* Lower Section: 2 Columns (Tool Crib & Parts Barcodes) */
    .lower-row {{
      display: grid;
      grid-template-columns: 1.25fr 1fr;
      gap: 12px;
      height: 104mm;
    }}

    .module-card {{
      background: #111827;
      border: 1.5px solid #334155;
      border-radius: 8px;
      padding: 8px 12px;
      display: flex;
      flex-direction: column;
    }}

    /* Tool Crib Cards */
    .tools-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      flex: 1;
      margin-top: 4px;
    }}
    .tool-box {{
      background: #0f172a;
      border: 1.5px solid #1e293b;
      border-radius: 6px;
      padding: 6px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      position: relative;
    }}
    .tool-box:hover {{
      border-color: #10b981;
    }}
    .tool-img-wrap {{
      width: 100%;
      height: 48mm;
      background: #fff;
      border-radius: 4px;
      overflow: hidden;
      margin-bottom: 5px;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .tool-img-wrap img {{
      max-width: 96%;
      max-height: 96%;
      object-fit: contain;
    }}
    .tool-scan-reticle {{
      position: absolute;
      inset: 4px;
      border: 1.5px dashed rgba(16, 185, 129, 0.7);
      border-radius: 4px;
      pointer-events: none;
    }}
    .tool-name {{
      font-size: 8.5pt;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 1px;
    }}
    .tool-ai-tag {{
      font-size: 7.2pt;
      font-family: monospace;
      color: #10b981;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 1px 5px;
      border-radius: 3px;
      font-weight: 700;
      margin-bottom: 2px;
    }}
    .tool-role {{
      font-size: 6.8pt;
      color: #94a3b8;
      line-height: 1.1;
    }}

    /* Parts Barcode Cards */
    .parts-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      flex: 1;
      margin-top: 4px;
    }}
    .part-box {{
      background: #0f172a;
      border: 1.5px solid #1e293b;
      border-radius: 6px;
      padding: 6px 8px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .part-top {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 3px;
    }}
    .part-name {{
      font-size: 8.5pt;
      font-weight: 800;
      color: #f8fafc;
    }}
    .part-stock-badge {{
      font-size: 6.8pt;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 3px;
    }}
    .stock-low {{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }}
    .stock-ok {{ background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }}
    .part-detail {{
      font-size: 7pt;
      color: #94a3b8;
      margin-bottom: 4px;
    }}
    .barcode-img-wrap {{
      background: #ffffff;
      padding: 3px 6px;
      border-radius: 4px;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-top: auto;
    }}
    .barcode-img-wrap img {{
      max-width: 100%;
      height: 26mm;
      object-fit: contain;
    }}

    /* Interview Script Footer */
    footer {{
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      border: 1.5px solid #334155;
      border-radius: 8px;
      padding: 6px 14px;
      margin-top: 8px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }}
    .footer-title-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .footer-title {{
      font-size: 9.5pt;
      font-weight: 800;
      color: #fbbf24;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .footer-subtitle {{
      font-size: 8pt;
      color: #94a3b8;
    }}
    .script-steps-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
    }}
    .script-step {{
      background: rgba(15, 23, 42, 0.7);
      border-left: 3px solid #38bdf8;
      padding: 4px 8px;
      border-radius: 0 4px 4px 0;
    }}
    .script-step-num {{
      font-size: 7.5pt;
      font-weight: 800;
      color: #38bdf8;
      text-transform: uppercase;
    }}
    .script-step-text {{
      font-size: 7.2pt;
      color: #cbd5e1;
      line-height: 1.25;
    }}
    .highlight-bold {{
      color: #f8fafc;
      font-weight: 700;
    }}
  </style>
</head>
<body>

  <div class="hazard-stripe"></div>

  <!-- HEADER -->
  <header>
    <div class="header-left">
      <div class="brand-title">
        <span>MAINTAI™ INDUSTRIAL SHOP-FLOOR SIMULATION RIG</span>
        <span class="brand-badge">LIVE DEMO MATRIX</span>
      </div>
      <div class="subtitle">
        Apex Manufacturing Plant Simulation • Multimodal AR Guidance • On-Device AI Vision Verification • Offline WAL Sync
      </div>
      <div class="tech-pill-row">
        <span class="tech-pill">60 FPS HTML5 Canvas HUD</span>
        <span class="tech-pill">Gemini 1.5 Flash Vision Model</span>
        <span class="tech-pill">Dexie.js IndexedDB WAL</span>
        <span class="tech-pill">Hands-Free Web Speech Recognition</span>
        <span class="tech-pill">Supabase PostgreSQL 16</span>
      </div>
    </div>

    <div class="header-right">
      <img src="{b64_qr_launcher}" alt="App Scan Launcher" class="launcher-qr">
      <div class="launcher-text">
        <div class="launcher-title">LAUNCH MOBILE PWA</div>
        <div class="launcher-url">maint-ai.vercel.app/scan</div>
        <div class="launcher-cred">Demo Login: tech1@demo.com | demo123456</div>
      </div>
    </div>
  </header>

  <!-- MAIN BODY -->
  <div class="main-grid">

    <!-- ROW 1: 4 WORKSTATIONS -->
    <div>
      <div class="section-title-bar">
        <div class="section-title">PRIMARY INDUSTRIAL EQUIPMENT WORKSTATIONS (BAYS A & B)</div>
        <div class="section-desc">Scan equipment QR tag with phone camera to instantly trigger the corresponding guided maintenance workflow</div>
      </div>

      <div class="machines-row">

        <!-- WORKSTATION 1 -->
        <div class="machine-card">
          <div class="station-header">
            <span class="station-badge">WORKSTATION 01</span>
            <span class="station-loc">BAY A - FLOOR 1</span>
          </div>
          <div class="machine-name">Haas VF-2SS CNC Machining Center</div>
          <div class="machine-model">Haas Automation • High-Speed Milling Center</div>
          
          <div class="photo-container">
            <img src="{b64_mach_cnc}" alt="Haas CNC">
            <div class="ar-target target-1">TARGET 1: Spindle Drain (45 Nm)</div>
            <div class="ar-target target-2">TARGET 2: 480V LOTO Switch</div>
          </div>

          <div class="specs-strip">
            <span>22 kW | 480V 3Φ</span>
            <span>12,000 RPM</span>
            <span>HAAS-VF2-0847</span>
          </div>

          <div class="qr-action-box">
            <img src="{b64_qr_haas}" alt="Haas QR" class="machine-qr-img">
            <div class="qr-info">
              <span class="qr-code-raw">MACHINE:haas-vf-2-001</span>
              <span class="qr-trigger-label">SCAN TO REPAIR HAAS CNC</span>
              <span class="qr-tap-hint">Triggers 9-step Spindle Oil Procedure</span>
            </div>
          </div>
        </div>

        <!-- WORKSTATION 2 -->
        <div class="machine-card">
          <div class="station-header">
            <span class="station-badge">WORKSTATION 02</span>
            <span class="station-loc">BAY A - FLOOR 1</span>
          </div>
          <div class="machine-name">Siemens 1LE0102 Induction Motor</div>
          <div class="machine-model">Siemens • 3-Phase Squirrel Cage Motor</div>

          <div class="photo-container">
            <img src="{b64_mach_motor}" alt="Siemens Motor">
            <div class="ar-target target-1">TARGET 1: Terminal Box (Megger)</div>
            <div class="ar-target target-2">TARGET 2: Drive-End Bearing</div>
          </div>

          <div class="specs-strip">
            <span>15 kW | 400V 50Hz</span>
            <span>1450 RPM (IE3)</span>
            <span>SIEM-1LE-0891</span>
          </div>

          <div class="qr-action-box">
            <img src="{b64_qr_siemens}" alt="Siemens QR" class="machine-qr-img">
            <div class="qr-info">
              <span class="qr-code-raw">MACHINE:siemens-1le0102-001</span>
              <span class="qr-trigger-label">SCAN FOR MOTOR INSPECTION</span>
              <span class="qr-tap-hint">Triggers Insulation & Vibration Test</span>
            </div>
          </div>
        </div>

        <!-- WORKSTATION 3 -->
        <div class="machine-card">
          <div class="station-header">
            <span class="station-badge">WORKSTATION 03</span>
            <span class="station-loc">BAY A - FLOOR 1</span>
          </div>
          <div class="machine-name">Atlas Copco GA 37+ Rotary Compressor</div>
          <div class="machine-model">Atlas Copco • Oil-Injected Screw Compressor</div>

          <div class="photo-container">
            <img src="{b64_mach_comp}" alt="Atlas Copco">
            <div class="ar-target target-1">TARGET 1: Oil Separator Vessel</div>
            <div class="ar-target target-2">TARGET 2: Safety Relief Valve</div>
          </div>

          <div class="specs-strip">
            <span>37 kW | 400V</span>
            <span>8.0 bar | 5.8 m³/m</span>
            <span>AC-GA37-0567</span>
          </div>

          <div class="qr-action-box">
            <img src="{b64_qr_atlas}" alt="Atlas QR" class="machine-qr-img">
            <div class="qr-info">
              <span class="qr-code-raw">MACHINE:atlas-ga-37-001</span>
              <span class="qr-trigger-label">SCAN TO OVERHAUL COMPRESSOR</span>
              <span class="qr-tap-hint">Triggers Filter & Valve Inspection</span>
            </div>
          </div>
        </div>

        <!-- WORKSTATION 4 -->
        <div class="machine-card">
          <div class="station-header">
            <span class="station-badge">WORKSTATION 04</span>
            <span class="station-loc">BAY B - FLOOR 1</span>
          </div>
          <div class="machine-name">Flexco 1900 Heavy-Duty Conveyor</div>
          <div class="machine-model">Flexco • Bulk Materials Handling Line</div>

          <div class="photo-container">
            <img src="{b64_mach_conv}" alt="Flexco Conveyor">
            <div class="ar-target target-1">TARGET 1: Tensioner Jack Bolt</div>
            <div class="ar-target target-2">TARGET 2: E-Stop Pull-Wire</div>
          </div>

          <div class="specs-strip">
            <span>1200mm Width</span>
            <span>50m Span | 1.5 m/s</span>
            <span>FLX-1900-0789</span>
          </div>

          <div class="qr-action-box">
            <img src="{b64_qr_flexco}" alt="Flexco QR" class="machine-qr-img">
            <div class="qr-info">
              <span class="qr-code-raw">MACHINE:flexco-1900-001</span>
              <span class="qr-trigger-label">SCAN FOR BELT MAINTENANCE</span>
              <span class="qr-tap-hint">Triggers Alignment & Tracking Flow</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- ROW 2: TOOL CALIBRATION CRIB & PARTS BARCODES -->
    <div class="lower-row">

      <!-- TOOL CRIB -->
      <div class="module-card">
        <div class="section-title-bar">
          <div class="section-title">MULTIMODAL AI COMPUTER VISION TOOL CALIBRATION STATION</div>
          <div class="section-desc">Aim phone camera at these tool targets during steps requiring verification to trigger Gemini 1.5 Flash detection</div>
        </div>

        <div class="tools-grid">

          <!-- TOOL 1 -->
          <div class="tool-box">
            <div class="tool-img-wrap">
              <img src="{b64_tool_multi}" alt="Multimeter">
              <div class="tool-scan-reticle"></div>
            </div>
            <div class="tool-name">Digital Multimeter</div>
            <span class="tool-ai-tag">multimeter (98.4%)</span>
            <div class="tool-role">Required for: Siemens Motor Resistance & Wiring Verification</div>
          </div>

          <!-- TOOL 2 -->
          <div class="tool-box">
            <div class="tool-img-wrap">
              <img src="{b64_tool_wrench}" alt="Wrench">
              <div class="tool-scan-reticle"></div>
            </div>
            <div class="tool-name">14mm Combination Wrench</div>
            <span class="tool-ai-tag">wrench (97.1%)</span>
            <div class="tool-role">Required for: Haas CNC Oil Drain Plug & Flexco Belt Tensioner</div>
          </div>

          <!-- TOOL 3 -->
          <div class="tool-box">
            <div class="tool-img-wrap">
              <img src="{b64_tool_pliers}" alt="Pliers">
              <div class="tool-scan-reticle"></div>
            </div>
            <div class="tool-name">Insulated Lineman's Pliers</div>
            <span class="tool-ai-tag">pliers (96.5%)</span>
            <div class="tool-role">Required for: Terminal Cable Extraction & Fuse Pulling</div>
          </div>

          <!-- TOOL 4 -->
          <div class="tool-box">
            <div class="tool-img-wrap">
              <img src="{b64_tool_allen}" alt="Allen Key">
              <div class="tool-scan-reticle"></div>
            </div>
            <div class="tool-name">Metric L-Hex / Allen Keys</div>
            <span class="tool-ai-tag">allen_key (95.8%)</span>
            <div class="tool-role">Required for: Guard Shroud & Enclosure Disassembly</div>
          </div>

        </div>
      </div>

      <!-- PARTS BARCODE RACK -->
      <div class="module-card">
        <div class="section-title-bar">
          <div class="section-title">SPARE PARTS WAREHOUSE & CODE 128 BARCODES</div>
          <div class="section-desc">Open /parts in app and scan barcodes to demonstrate inventory lookup and reorder</div>
        </div>

        <div class="parts-grid">

          <!-- PART 1 -->
          <div class="part-box">
            <div class="part-top">
              <span class="part-name">Oil Filter OF-200</span>
              <span class="part-stock-badge stock-low">LOW STOCK: 4 LEFT</span>
            </div>
            <div class="part-detail">Donaldson Filtration • Haas & Compressor</div>
            <div class="barcode-img-wrap">
              <img src="{b64_bc_01001}" alt="PN-01001 Barcode">
            </div>
          </div>

          <!-- PART 2 -->
          <div class="part-box">
            <div class="part-top">
              <span class="part-name">Ball Bearing 6205</span>
              <span class="part-stock-badge stock-ok">IN STOCK: 25 UNITS</span>
            </div>
            <div class="part-detail">SKF Bearings • 25x52x15mm Chrome Steel</div>
            <div class="barcode-img-wrap">
              <img src="{b64_bc_01002}" alt="PN-01002 Barcode">
            </div>
          </div>

          <!-- PART 3 -->
          <div class="part-box">
            <div class="part-top">
              <span class="part-name">Hydraulic Seal HS-45</span>
              <span class="part-stock-badge stock-low">CRITICAL: 2 LEFT</span>
            </div>
            <div class="part-detail">Parker Hannifin • 45mm Polyurethane U-Cup</div>
            <div class="barcode-img-wrap">
              <img src="{b64_bc_01004}" alt="PN-01004 Barcode">
            </div>
          </div>

          <!-- PART 4 -->
          <div class="part-box">
            <div class="part-top">
              <span class="part-name">Drive Belt DB-900</span>
              <span class="part-stock-badge stock-ok">IN STOCK: 18 UNITS</span>
            </div>
            <div class="part-detail">Continental ContiTech • High Tensile Timing Belt</div>
            <div class="barcode-img-wrap">
              <img src="{b64_bc_01006}" alt="PN-01006 Barcode">
            </div>
          </div>

        </div>
      </div>

    </div>

  </div>

  <!-- INTERVIEW SCRIPT FOOTER -->
  <footer>
    <div class="footer-title-row">
      <div class="footer-title">60-SECOND LIVE DEMO SHOWSTOPPER SCRIPT FOR CANDIDATE</div>
      <div class="footer-subtitle">Follow this sequence in front of the interviewers for maximum impact</div>
    </div>

    <div class="script-steps-row">
      <div class="script-step">
        <div class="script-step-num">Step 1 • Optical QR Decode</div>
        <div class="script-step-text">
          Aim phone camera at <span class="highlight-bold">Haas CNC QR</span>. In 120ms, phone vibrates with audio chime and mounts the live 9-step procedure.
        </div>
      </div>

      <div class="script-step">
        <div class="script-step-num">Step 2 • Hands-Free Voice AR</div>
        <div class="script-step-text">
          Show 60 FPS Canvas reticle on Target 1. Speak: <span class="highlight-bold">"Antigravity Next"</span>. App advances without touching grease-covered hands to screen.
        </div>
      </div>

      <div class="script-step">
        <div class="script-step-num">Step 3 • Multimodal AI Vision Gate</div>
        <div class="script-step-text">
          Step requires tool check. Point camera at the <span class="highlight-bold">Multimeter</span> on this chart. Gemini 1.5 validates with 98% confidence and auto-advances.
        </div>
      </div>

      <div class="script-step">
        <div class="script-step-num">Step 4 • Airplane Mode WAL Sync</div>
        <div class="script-step-text">
          <span class="highlight-bold">Turn phone to Airplane Mode</span>. Complete the step. Show "1 mutation queued in Dexie WAL". Turn WiFi back on: instant background sync to PostgreSQL!
        </div>
      </div>
    </div>
  </footer>

</body>
</html>
"""

out_html = os.path.join(BASE, "MaintAI_Live_Demo_Testbed.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"[OK] Generated {out_html}")

# Compile to PDF
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_pdf = os.path.join(BASE, "MaintAI_Live_Demo_Testbed.pdf")
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

# Render preview image
doc = pymupdf.open(out_pdf)
print(f"PDF Pages: {len(doc)}")
pix = doc[0].get_pixmap(dpi=130)
out_png = os.path.join(PDF_DIR, "preview_live_demo_testbed.png")
pix.save(out_png)
print(f"[RENDERED] Preview image: {out_png} ({pix.width}x{pix.height})")

# Copy to downloads
downloads = r"C:\Users\hetjo\Downloads"
shutil.copy2(out_pdf, os.path.join(downloads, "MaintAI_Live_Demo_Testbed.pdf"))
shutil.copy2(out_pdf, os.path.join(downloads, "MaintAI_Chart_Paper_Model.pdf"))
print("[MIRRORED] Copied to Downloads for easy user access.")
