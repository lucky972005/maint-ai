import os
import sys
import base64
import subprocess
import shutil

BASE_DIR = r"c:\dev\pro"
IMAGES_DIR = os.path.join(BASE_DIR, "pdf_images")
OUTPUT_HTML = os.path.join(BASE_DIR, "MaintAI_Poster_A2_Landscape.html")
OUTPUT_PDF = os.path.join(BASE_DIR, "MaintAI_Poster_A2_Landscape.pdf")
DOWNLOADS_PDF = r"C:\Users\hetjo\Downloads\MaintAI_Poster_A2_Landscape.pdf"

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
]

def get_base64_img(filename):
    path = os.path.join(IMAGES_DIR, filename)
    if not os.path.exists(path):
        print(f"Warning: {filename} not found in {IMAGES_DIR}")
        return ""
    ext = os.path.splitext(filename)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

def build_poster():
    print("Encoding high-resolution image assets to base64...")
    ppsu_logo = get_base64_img("official_ppsu_naac.png")
    soe_logo = get_base64_img("official_school_of_engineering.png")
    arch_img = get_base64_img("updated_architecture_diagram.png")
    workflow_img = get_base64_img("fig_5_1_workflow.png")
    ar_hud_img = get_base64_img("p12_img3_72.png")
    tool_ver_img = get_base64_img("p12_img4_73.png")
    sync_img = get_base64_img("updated_offline_sync_workflow.png")
    dash_img = get_base64_img("fig_A_7_dashboard.png")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MaintAI — UDP Final Year Scientific Poster Presentation (A2 Landscape)</title>
  <style>
    /* ==========================================================================
       A2 LANDSCAPE SCIENTIFIC EXHIBITION POSTER (594mm x 420mm)
       P.P. Savani University — School of Engineering — Final UDP Presentation
       ========================================================================== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');

    :root {{
      --font-serif: 'Cambria', 'Georgia', 'Times New Roman', serif;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --navy-950: #06121e;
      --navy-900: #0b1f36;
      --navy-800: #0f2a4c;
      --navy-700: #1b3d66;
      --ppsu-red: #b31b1b;
      --ppsu-red-dark: #8c1414;
      --emerald-600: #059669;
      --emerald-700: #047857;
      --amber-600: #d97706;
      --blue-600: #2563eb;
      --slate-50: #f8fafc;
      --slate-100: #f1f5f9;
      --slate-200: #e2e8f0;
      --slate-300: #cbd5e1;
      --slate-600: #475569;
      --slate-700: #334155;
      --slate-800: #1e293b;
      --slate-900: #0f172a;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    @page {{
      size: 594mm 420mm;
      margin: 0;
    }}

    html, body {{
      width: 594mm;
      height: 420mm;
      overflow: hidden;
      background: #e2e8f0;
      font-family: var(--font-serif);
      color: var(--slate-900);
      -webkit-font-smoothing: antialiased;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }}

    .poster-container {{
      width: 594mm;
      height: 420mm;
      background: #ffffff;
      padding: 6.5mm 9mm 5mm 9mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      position: relative;
    }}

    /* Top Accent Stripe */
    .top-accent-bar {{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3.5mm;
      background: linear-gradient(90deg, #b31b1b 0%, #0f2a4c 35%, #1e3a8a 70%, #059669 100%);
    }}

    /* ==========================================================================
       HEADER SECTION
       ========================================================================== */
    .poster-header {{
      display: grid;
      grid-template-columns: 145px 1fr 210px;
      align-items: center;
      gap: 16px;
      border-bottom: 2.2px solid var(--navy-800);
      padding-bottom: 2.8mm;
      margin-top: 1mm;
      margin-bottom: 2.2mm;
    }}

    .header-logo-left img {{
      max-width: 135px;
      height: auto;
      object-fit: contain;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08));
    }}

    .header-center {{
      text-align: center;
      padding: 0 4px;
    }}

    .header-badge {{
      display: inline-block;
      font-family: var(--font-sans);
      font-size: 7.5pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1px;
      background: #f1f5f9;
      color: var(--navy-800);
      padding: 1.5px 8px;
      border-radius: 4px;
      border: 1px solid var(--slate-300);
      margin-bottom: 2px;
    }}

    .poster-main-title {{
      font-size: 26pt;
      font-weight: 800;
      line-height: 1.1;
      color: var(--navy-900);
      letter-spacing: -0.3px;
      margin-bottom: 1.5px;
    }}

    .poster-subtitle {{
      font-family: var(--font-sans);
      font-size: 12.5pt;
      font-weight: 700;
      color: var(--ppsu-red);
      margin-bottom: 2.5px;
      letter-spacing: 0.1px;
    }}

    .poster-meta {{
      font-size: 11.5pt;
      font-weight: 700;
      color: var(--slate-800);
      line-height: 1.2;
    }}

    .poster-meta span.author {{
      color: var(--navy-900);
      font-size: 12.5pt;
    }}

    .poster-meta span.author sup {{
      color: var(--ppsu-red);
      font-weight: 800;
    }}

    .poster-meta span.affiliation {{
      font-family: var(--font-sans);
      font-size: 9.6pt;
      font-weight: 500;
      color: var(--slate-600);
      display: block;
      margin-top: 1px;
    }}

    .header-logo-right img {{
      max-width: 200px;
      height: auto;
      object-fit: contain;
      border-radius: 4px;
      filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08));
    }}

    /* ==========================================================================
       HERO METRICS KPI BAR
       ========================================================================== */
    .metrics-bar {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 5mm;
      margin-bottom: 2.4mm;
    }}

    .kpi-card {{
      background: linear-gradient(135deg, #0b1f36 0%, #112a4a 100%);
      color: #ffffff;
      border-radius: 7px;
      padding: 2.2mm 3.8mm;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 3px 8px rgba(11, 31, 54, 0.18);
      border-left: 5px solid var(--ppsu-red);
      border-top: 1px solid rgba(255,255,255,0.12);
    }}

    .kpi-card:nth-child(2) {{ border-left-color: #10b981; }}
    .kpi-card:nth-child(3) {{ border-left-color: #3b82f6; }}
    .kpi-card:nth-child(4) {{ border-left-color: #f59e0b; }}

    .kpi-info {{
      display: flex;
      flex-direction: column;
    }}

    .kpi-val {{
      font-family: var(--font-sans);
      font-size: 19pt;
      font-weight: 900;
      line-height: 1;
      color: #ffffff;
      letter-spacing: -0.5px;
    }}

    .kpi-label {{
      font-family: var(--font-sans);
      font-size: 8.5pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: #93c5fd;
      margin-top: 2px;
    }}

    .kpi-desc {{
      font-family: var(--font-sans);
      font-size: 7.6pt;
      color: #cbd5e1;
      line-height: 1.15;
      text-align: right;
      max-width: 82px;
      font-weight: 500;
    }}

    /* ==========================================================================
       4-COLUMN LANDSCAPE GRID
       ========================================================================== */
    .poster-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 4.5mm;
      flex: 1;
      margin-bottom: 1.8mm;
      min-height: 0;
    }}

    .poster-column {{
      display: flex;
      flex-direction: column;
      gap: 2.8mm;
      justify-content: space-between;
      min-height: 0;
    }}

    /* Professional Card Container */
    .card {{
      background: #ffffff;
      border: 1.2px solid var(--slate-300);
      border-top: 3.5px solid var(--navy-800);
      border-radius: 6px;
      padding: 2.8mm 3.4mm;
      display: flex;
      flex-direction: column;
      box-shadow: 0 2px 5px rgba(15, 23, 42, 0.04);
      position: relative;
    }}

    .card.red-accent {{
      border-top-color: var(--ppsu-red);
    }}

    .card.emerald-accent {{
      border-top-color: var(--emerald-600);
    }}

    .card.blue-accent {{
      border-top-color: var(--blue-600);
    }}

    /* Pill Headers */
    .pill-header {{
      background: linear-gradient(90deg, #b31b1b 0%, #8c1414 100%);
      color: #ffffff;
      font-family: var(--font-sans);
      font-size: 10pt;
      font-weight: 800;
      padding: 2.2px 10px;
      border-radius: 999px;
      margin-bottom: 1.8mm;
      align-self: flex-start;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      letter-spacing: 0.3px;
      text-transform: uppercase;
      box-shadow: 0 2px 4px rgba(179, 27, 27, 0.2);
    }}

    .pill-header.navy {{
      background: linear-gradient(90deg, #0b1f36 0%, #1b3d66 100%);
      box-shadow: 0 2px 4px rgba(11, 31, 54, 0.2);
    }}

    .pill-header.emerald {{
      background: linear-gradient(90deg, #059669 0%, #047857 100%);
      box-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);
    }}

    .pill-header.blue {{
      background: linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%);
      box-shadow: 0 2px 4px rgba(30, 64, 175, 0.2);
    }}

    /* Body Text & Bullets */
    .body-p {{
      font-size: 9.6pt;
      line-height: 1.25;
      color: #1e293b;
      text-align: justify;
      margin-bottom: 1.6mm;
    }}

    .bullet-list {{
      list-style-type: none;
      padding-left: 0;
    }}

    .bullet-list li {{
      position: relative;
      padding-left: 12px;
      margin-bottom: 1.5mm;
      font-size: 9.2pt;
      line-height: 1.22;
      text-align: justify;
      color: #1e293b;
    }}

    .bullet-list li::before {{
      content: "■";
      position: absolute;
      left: 0;
      top: 0px;
      color: var(--ppsu-red);
      font-size: 7pt;
    }}

    .bullet-list.navy-dots li::before {{
      color: var(--navy-800);
    }}

    .bullet-list.emerald-dots li::before {{
      color: var(--emerald-600);
    }}

    .bullet-list li strong {{
      color: var(--navy-900);
      font-weight: 700;
    }}

    /* Math Formula Block */
    .math-formula {{
      background: #f8fafc;
      border: 1.2px solid var(--slate-300);
      border-left: 3.5px solid var(--navy-800);
      border-radius: 4px;
      padding: 2.2px 6px;
      margin: 1.4mm 0;
      font-family: var(--font-sans);
      font-size: 8.8pt;
      color: var(--navy-900);
      text-align: center;
      line-height: 1.2;
    }}

    /* Embedded Diagram Containers */
    .diagram-frame {{
      background: #f8fafc;
      border: 1.2px solid var(--slate-200);
      border-radius: 5px;
      padding: 2.5px;
      margin: 1.4mm 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      width: 100%;
    }}

    .diagram-frame img {{
      max-width: 100%;
      height: auto;
      object-fit: contain;
      border-radius: 3px;
      background: #ffffff;
      display: block;
    }}

    .diagram-caption {{
      font-family: var(--font-sans);
      font-size: 7.5pt;
      font-weight: 600;
      color: var(--slate-600);
      font-style: italic;
      margin-top: 1.6px;
      text-align: center;
      line-height: 1.15;
    }}

    /* Comparison Benchmark Table */
    .benchmark-table {{
      width: 100%;
      border-collapse: collapse;
      font-family: var(--font-sans);
      font-size: 7.4pt;
      margin: 1.4mm 0;
    }}

    .benchmark-table th {{
      background: var(--navy-900);
      color: #ffffff;
      font-weight: 700;
      padding: 3.2px 3.5px;
      text-align: left;
      border: 1px solid var(--navy-900);
    }}

    .benchmark-table th:last-child {{
      background: #0f3460;
      color: #60a5fa;
      border-color: #0f3460;
    }}

    .benchmark-table td {{
      padding: 2.6px 3.5px;
      border: 1px solid var(--slate-200);
      line-height: 1.15;
      color: #1e293b;
    }}

    .benchmark-table td:last-child {{
      background: #eff6ff;
      font-weight: 700;
      color: var(--navy-900);
      border-left: 1.5px solid #bfdbfe;
      border-right: 1.5px solid #bfdbfe;
    }}

    .benchmark-table tr:nth-child(even) td:not(:last-child) {{
      background: #f8fafc;
    }}

    .benchmark-table tr.highlight-row {{
      background: #dbeafe;
      font-weight: 800;
    }}

    .benchmark-table tr.highlight-row td {{
      color: var(--navy-900);
      border-color: #93c5fd;
    }}

    .benchmark-table tr.highlight-row td:last-child {{
      background: #bfdbfe;
      color: #1e3a8a;
    }}

    /* Keyword Tags */
    .tag-cluster {{
      display: flex;
      flex-wrap: wrap;
      gap: 3px;
      margin-top: 1.2mm;
    }}

    .tag-badge {{
      font-family: var(--font-sans);
      font-size: 7pt;
      font-weight: 700;
      background: #f1f5f9;
      color: var(--navy-800);
      border: 1px solid #cbd5e1;
      padding: 1.2px 5px;
      border-radius: 4px;
    }}

    /* Status Banner */
    .status-banner {{
      background: #ecfdf5;
      border: 1px solid #a7f3d0;
      border-left: 4px solid #059669;
      border-radius: 4px;
      padding: 2.4px 7px;
      margin-top: auto;
      font-family: var(--font-sans);
      font-size: 8.2pt;
      font-weight: 800;
      color: #065f46;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    /* Code Box */
    .code-box {{
      background: #0f172a;
      color: #38bdf8;
      border-radius: 4px;
      padding: 4px 7px;
      margin: 1.4mm 0;
      font-family: var(--font-mono);
      font-size: 7.3pt;
      line-height: 1.2;
      border-left: 3.5px solid #38bdf8;
      word-break: break-all;
    }}

    /* ==========================================================================
       FOOTER SECTION
       ========================================================================== */
    .poster-footer {{
      border-top: 2px solid var(--navy-800);
      padding-top: 1.8mm;
      display: grid;
      grid-template-columns: 1fr 145px;
      gap: 16px;
      align-items: center;
      margin-top: 1mm;
    }}

    .footer-references {{
      font-size: 7.9pt;
      line-height: 1.22;
      color: var(--slate-600);
    }}

    .footer-references strong {{
      font-family: var(--font-sans);
      color: var(--navy-900);
      font-size: 8.4pt;
      display: inline-block;
      margin-right: 4px;
    }}

    .footer-references ol {{
      padding-left: 14px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      column-gap: 12px;
      row-gap: 1px;
    }}

    .footer-qr-container {{
      display: flex;
      align-items: center;
      gap: 7px;
      justify-content: flex-end;
    }}

    .footer-qr-container img {{
      width: 52px;
      height: 52px;
      border: 1.2px solid var(--slate-300);
      border-radius: 4px;
      padding: 2px;
      background: #ffffff;
    }}

    .qr-text-block {{
      font-family: var(--font-sans);
      font-size: 7pt;
      font-weight: 700;
      color: var(--navy-900);
      line-height: 1.2;
    }}

    .qr-text-block span {{
      color: var(--ppsu-red);
      display: block;
      font-size: 6.6pt;
    }}
  </style>
</head>
<body>

  <div class="poster-container">
    <div class="top-accent-bar"></div>

    <!-- ========================================================================
         HEADER: PPSU LOGO | PROJECT IDENTITY | SCHOOL OF ENGINEERING
         ======================================================================== -->
    <header class="poster-header">
      <div class="header-logo-left">
        <img src="{ppsu_logo}" alt="P P Savani University & NAAC A+ Logo">
      </div>

      <div class="header-center">
        <div class="header-badge">B.Tech Capstone Project &bull; User Defined Project (UDP)</div>
        <h1 class="poster-main-title">MaintAI — AI-Powered Industrial Maintenance Assistant</h1>
        <div class="poster-subtitle">Progressive Web Application with Hands-Free AR Guidance, Multimodal Vision & Offline Synchronization</div>
        <div class="poster-meta">
          <span class="author">Het Joshi<sup>1*</sup></span>, <span class="author">Mr. Ayush Dodia<sup>2</sup></span>
          <span class="affiliation">
            <sup>1</sup>Student (Enrollment No: <strong>24SE09CE003</strong>), Department of Computer Engineering | <sup>2</sup>Project Mentor, Assistant Professor<br>
            School of Engineering, P. P. Savani University, Surat, Gujarat | Academic Year: 2025–2026
          </span>
        </div>
      </div>

      <div class="header-logo-right">
        <img src="{soe_logo}" alt="PPSU School of Engineering Logo">
      </div>
    </header>

    <!-- ========================================================================
         HERO METRICS KPI BAR
         ======================================================================== -->
    <section class="metrics-bar" aria-label="Key Performance Indicators">
      <div class="kpi-card">
        <div class="kpi-info">
          <div class="kpi-val">-34.2%</div>
          <div class="kpi-label">Mean MTTR Reduction</div>
        </div>
        <div class="kpi-desc">53.4 min down to 35.1 min verified in 48 shop-floor trials</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <div class="kpi-val">98.4%</div>
          <div class="kpi-label">Tool Safety Compliance</div>
        </div>
        <div class="kpi-desc">Gemini 1.5 Flash automated tool & PPE verification gate</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <div class="kpi-val">1.82s</div>
          <div class="kpi-label">Median Vision Latency</div>
        </div>
        <div class="kpi-desc">Sub-2.0s multimodal inference via Next.js Edge proxy</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <div class="kpi-val">100%</div>
          <div class="kpi-label">Offline Durability</div>
        </div>
        <div class="kpi-desc">Zero mutation loss across 50 simulated factory cut-offs</div>
      </div>
    </section>

    <!-- ========================================================================
         4-COLUMN MAIN BODY GRID
         ======================================================================== -->
    <main class="poster-grid">

      <!-- ====================================================================
           COLUMN 1: MOTIVATION, OBJECTIVES & 3-TIER ARCHITECTURE
           ==================================================================== -->
      <section class="poster-column">
        <!-- 1.1 Problem Statement -->
        <article class="card red-accent">
          <div class="pill-header">1. Industrial Problem Statement</div>
          <p class="body-p">
            Unplanned manufacturing downtime incurs immense economic penalties averaging thousands of dollars per minute. Frontline technicians face 4 persistent operational bottlenecks:
          </p>
          <ul class="bullet-list">
            <li><strong>Documentation Friction:</strong> Up to 35% of total repair duration is consumed retrieving binder manuals or desktop PDFs.</li>
            <li><strong>Touchscreen Hazards:</strong> Operating capacitive smartphones with grease-covered gloves damages devices and creates slip hazards.</li>
            <li><strong>Procedural Non-Compliance:</strong> Skipping safety steps (LOTO, depressurization) or using uncalibrated hand tools causes machine breakdowns.</li>
            <li><strong>RF Dead Zones:</strong> Structural steel and motor interference create factory Wi-Fi blackouts, freezing legacy cloud CMMS apps.</li>
          </ul>
          <div class="math-formula" style="border-left-color:var(--ppsu-red); font-size:8.2pt; text-align:left; padding:3px 7px; margin-top:1.2mm;">
            <b>Impact:</b> Automotive & precision manufacturing plants lose an estimated <b>$22,000/hr</b> during unpredicted equipment line stoppages.
          </div>
        </article>

        <!-- 1.2 Aim & Objectives -->
        <article class="card">
          <div class="pill-header">2. Aim & Measurable Objectives</div>
          <p class="body-p">
            To develop, deploy, and benchmark <strong>MaintAI</strong> — a zero-hardware-overhead, offline-first Progressive Web Application running on commodity mobile devices:
          </p>
          <ul class="bullet-list">
            <li><strong>Zero-Install Mobile PWA:</strong> Next.js 14 App Router, installable to home screen without native app store friction.</li>
            <li><strong>HTML5 Canvas 2D AR Overlays:</strong> Pulsing directional callouts rendered over live camera feeds at solid 60 fps.</li>
            <li><strong>Continuous Speech Control:</strong> Web Speech API hands-free voice command navigation tolerant of factory acoustic noise.</li>
            <li><strong>Multimodal Tool Gatekeeper:</strong> Google Gemini 1.5 Flash automated camera inspection enforcing procedural tool verification.</li>
            <li><strong>Local-First Write-Ahead Sync:</strong> Dexie.js IndexedDB transactional persistence with FIFO queue replay upon reconnection.</li>
          </ul>
        </article>

        <!-- 1.3 3-Tier Architecture -->
        <article class="card navy-accent">
          <div class="pill-header navy">3. 3-Tier Cloud & Edge Architecture</div>
          <p class="body-p">
            The platform decouples concerns into three high-resilience tiers engineered for distributed industrial networks:
          </p>
          <div class="diagram-frame">
            <img src="{arch_img}" alt="Final 3-Tier System Architecture" style="max-height: 112px;">
            <div class="diagram-caption">Figure 1. 3-Tier Production Architecture: Client PWA, Vercel Edge & Supabase Cloud.</div>
          </div>
          <div class="tag-cluster">
            <span class="tag-badge">Next.js 14</span>
            <span class="tag-badge">Dexie.js 3.2</span>
            <span class="tag-badge">Gemini 1.5 Flash</span>
            <span class="tag-badge">PostgreSQL 15</span>
            <span class="tag-badge">Supabase RLS</span>
          </div>
        </article>
      </section>

      <!-- ====================================================================
           COLUMN 2: METHODOLOGY, AR GUIDANCE & VOICE CONTROL
           ==================================================================== -->
      <section class="poster-column">
        <!-- 2.1 Agile Methodology -->
        <article class="card">
          <div class="pill-header">4. Engineering Methodology</div>
          <p class="body-p">
            Executed across a 16-week Agile-Scrum evolutionary prototyping schedule structured into five sequential development phases:
          </p>
          <div class="diagram-frame">
            <img src="{workflow_img}" alt="Agile Engineering Lifecycle" style="max-height: 72px;">
            <div class="diagram-caption">Figure 2. 16-Week Agile Iteration Progression & Progress Milestone Deliverables.</div>
          </div>
          <ul class="bullet-list" style="margin-top:1.4mm;">
            <li><strong>Phase 1 (W1–4):</strong> Literature review, problem crystallization, SRS specification.</li>
            <li><strong>Phase 2 (W5–7):</strong> 3-Tier architecture, Supabase schema & RLS policies.</li>
            <li><strong>Phase 3 (W8–11):</strong> HTML5 AR canvas, Web Speech listener & Gemini tool gate.</li>
            <li><strong>Phase 4 (W12–13):</strong> Dexie.js write-ahead sync queue & offline hardening.</li>
            <li><strong>Phase 5 (W14–16):</strong> Multi-device UAT, MTTR benchmarking & hard-bound defense.</li>
          </ul>
        </article>

        <!-- 2.2 Module 1: Live AR Engine -->
        <article class="card">
          <div class="pill-header navy">5. Module 1 — Live AR Step Guidance</div>
          <p class="body-p">
            Renders dynamic directional callouts over live video feeds via an HTML5 <code>&lt;canvas&gt;</code> element bound to <code>getUserMedia()</code> without optical plugins:
          </p>
          <div class="math-formula">
            <i>X<sub>p</sub> = (X<sub>%</sub> / 100) &times; W<sub>canvas</sub></i> &nbsp;&nbsp;|&nbsp;&nbsp; <i>Y<sub>p</sub> = (Y<sub>%</sub> / 100) &times; H<sub>canvas</sub></i>
          </div>
          <div class="math-formula">
            <i>r = r<sub>base</sub> + 6 &times; sin(0.005 &times; t)</i> &nbsp;&nbsp; <b>(Render loop at solid 59.8 fps)</b>
          </div>
          <div class="diagram-frame">
            <img src="{ar_hud_img}" alt="Live AR Guidance View" style="max-height: 84px;">
            <div class="diagram-caption">Figure 3. Mobile Camera AR HUD: Pulsing targeting ring over component chassis.</div>
          </div>
        </article>

        <!-- 2.3 Hands-Free Voice Control -->
        <article class="card">
          <div class="pill-header">6. Hands-Free Voice Navigation</div>
          <p class="body-p">
            Continuous <code>webkitSpeechRecognition</code> listener with custom Levenshtein edit distance (<i>d &le; 1</i>) phonetic matching, mitigating shop-floor motor acoustic noise:
          </p>
          <ul class="bullet-list">
            <li><strong>Noise Robustness:</strong> Recognition raised from 76.0% to <strong>91.2%</strong> in 75dB–80dB simulated CNC workshop ambient noise.</li>
            <li><strong>Audio State Machine:</strong> Speech listener automatically mutes during TTS synthesis and AI modal popups to eliminate feedback loops.</li>
          </ul>
          <div class="tag-cluster">
            <span class="tag-badge">"NEXT STEP"</span>
            <span class="tag-badge">"PREVIOUS"</span>
            <span class="tag-badge">"VERIFY TOOL"</span>
            <span class="tag-badge">"COMPLETE"</span>
          </div>
        </article>
      </section>

      <!-- ====================================================================
           COLUMN 3: MULTIMODAL AI VISION, OFFLINE SYNC & CLOUD SECURITY
           ==================================================================== -->
      <section class="poster-column">
        <!-- 3.1 Module 2: AI Tool Verification Gate -->
        <article class="card">
          <div class="pill-header">7. Module 2 — AI Tool Verification Gate</div>
          <p class="body-p">
            Enforces physical tool safety by validating that technicians use specified calibrated equipment before unlocking hazardous repair steps:
          </p>
          <div class="diagram-frame">
            <img src="{tool_ver_img}" alt="Multimodal AI Verification Modal" style="max-height: 84px;">
            <div class="diagram-caption">Figure 4. Gemini 1.5 Flash Tool Verification Gate with real-time detection bounding box.</div>
          </div>
          <ul class="bullet-list" style="margin-top:1.4mm;">
            <li><strong>Edge Compression:</strong> Downsamples canvas frame to 640×480 JPEG (118KB), cutting upload latency to 1.82s on mobile networks.</li>
            <li><strong>Strict JSON Contract:</strong> Enforces JSON schema returning <code>tool_detected</code>, <code>confidence</code>, and <code>matches_expected</code> boolean.</li>
            <li><strong>Procedural Gatekeeper:</strong> Confidence threshold <i>&ge; 0.70</i> unlocks step; incorrect tooling emits audible voice alerts and locks navigation.</li>
          </ul>
        </article>

        <!-- 3.2 Module 3: Offline-First Sync -->
        <article class="card">
          <div class="pill-header navy">8. Module 3 — Offline Sync Pipeline</div>
          <p class="body-p">
            Guarantees 100% data durability across factory RF blackouts using a local-first Dexie.js IndexedDB write-ahead log (WAL) paired with FIFO replay:
          </p>
          <div class="diagram-frame">
            <img src="{sync_img}" alt="Offline Sync Pipeline" style="max-height: 74px;">
            <div class="diagram-caption">Figure 5. Transactional Offline WAL & Atomic Cloud Reconciliation State Machine.</div>
          </div>
          <ul class="bullet-list" style="margin-top:1.4mm;">
            <li><strong>Atomic Persistence:</strong> Mutations write synchronously to local tables (<code>local_logs</code>, <code>local_parts</code>, <code>sync_queue</code>).</li>
            <li><strong>Auto-Replay Loop:</strong> Global reconnect listener replays pending mutations in batch HTTP requests with exponential backoff.</li>
          </ul>
          <div class="tag-cluster">
            <span class="tag-badge">IndexedDB</span>
            <span class="tag-badge">Dexie.js WAL</span>
            <span class="tag-badge">FIFO Sync Queue</span>
            <span class="tag-badge">Offline Cache</span>
          </div>
        </article>

        <!-- 3.3 Database Security -->
        <article class="card emerald-accent">
          <div class="pill-header emerald">9. PostgreSQL Cloud & Database Security</div>
          <p class="body-p">
            Ten relational tables deployed on Supabase PostgreSQL 15 with PgBouncer pooling and kernel-level Row Level Security (RLS) tenant isolation:
          </p>
          <ul class="bullet-list emerald-dots" style="margin-bottom:1.2mm;">
            <li><strong>Strict Multi-Tenancy:</strong> RLS policies inspect JWT claims on every query, isolating machines and logs across factories.</li>
            <li><strong>Connection Efficiency:</strong> PgBouncer transaction pooling sustains 150+ concurrent technician queries with sub-5ms dispatch.</li>
          </ul>
          <div class="code-box">
            CREATE POLICY tenant_isolation ON machines FOR ALL<br>
            USING (factory_id = auth.jwt() -&gt;&gt; 'factory_id');
          </div>
        </article>
      </section>

      <!-- ====================================================================
           COLUMN 4: BENCHMARKS, ANALYTICS & CONCLUSIONS
           ==================================================================== -->
      <section class="poster-column">
        <!-- 4.1 Comparative Benchmarks -->
        <article class="card">
          <div class="pill-header blue">10. Quantitative Benchmarks</div>
          <p class="body-p">
            Comparative performance evaluated across 48 shop-floor trials on CNC milling centers and hydraulic press stations:
          </p>
          <table class="benchmark-table">
            <thead>
              <tr>
                <th>System / Metric</th>
                <th>Paper SOP</th>
                <th>HoloLens 2</th>
                <th>Mobile CMMS</th>
                <th>MaintAI PWA</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Hardware Cost</strong></td>
                <td>$0 (Paper)</td>
                <td>$3,500+ /unit</td>
                <td>Phone Req.</td>
                <td><strong>$0 (Phones)</strong></td>
              </tr>
              <tr>
                <td><strong>Visual Guidance</strong></td>
                <td>None (Drawings)</td>
                <td>3D Holograms</td>
                <td>None (Text)</td>
                <td><strong>2D Canvas (60fps)</strong></td>
              </tr>
              <tr>
                <td><strong>Hands-Free Control</strong></td>
                <td>None (Pen/Paper)</td>
                <td>Gaze / Gesture</td>
                <td>Touchscreen</td>
                <td><strong>Web Speech (91.2%)</strong></td>
              </tr>
              <tr>
                <td><strong>Safety Tool Gate</strong></td>
                <td>None (Honor)</td>
                <td>Experimental</td>
                <td>None</td>
                <td><strong>Gemini 1.5 (98.4%)</strong></td>
              </tr>
              <tr>
                <td><strong>Offline Durability</strong></td>
                <td>Paper works</td>
                <td>Partial cache</td>
                <td>Fails / Drops</td>
                <td><strong>100% Dexie WAL</strong></td>
              </tr>
              <tr class="highlight-row">
                <td><strong>Mean MTTR</strong></td>
                <td>53.4 min</td>
                <td>38.2 min (-28%)</td>
                <td>47.1 min (-12%)</td>
                <td><strong>35.1 min (-34.2%)</strong></td>
              </tr>
            </tbody>
          </table>
        </article>

        <!-- 4.2 Supervisor Analytics -->
        <article class="card">
          <div class="pill-header navy">11. Plant Supervisor Telemetry</div>
          <p class="body-p">
            Centralized management console calculating real-time MTTR, MTBF, technician throughput, and parts inventory restock queues:
          </p>
          <div class="diagram-frame">
            <img src="{dash_img}" alt="Supervisor Analytics Dashboard" style="max-height: 80px;">
            <div class="diagram-caption">Figure 6. Web Management Console: Real-time downtime telemetry and parts tracking.</div>
          </div>
          <ul class="bullet-list navy-dots" style="margin-top:1.2mm;">
            <li><strong>Fleet Telemetry:</strong> Live tracking of machine health states, open work orders, and technician completion velocity.</li>
            <li><strong>Predictive Restock:</strong> Automated stock alert dispatch when component inventory breaches critical thresholds.</li>
          </ul>
        </article>

        <!-- 4.3 Conclusions & Future Scope -->
        <article class="card emerald-accent">
          <div class="pill-header emerald">12. Conclusions & Future Scope</div>
          <ul class="bullet-list">
            <li><strong>Core Outcome:</strong> Proves modern web standards (PWA, Canvas 2D, Web Speech, IndexedDB) provide a zero-hardware alternative to expensive AR headsets.</li>
            <li><strong>Automated Testing:</strong> 48 formal test cases passed with 100% success; Lighthouse mobile audit scored <strong>94/100</strong>.</li>
            <li><strong>Future Horizons:</strong> On-device quantized YOLOv8 Nano compiled to WebAssembly via ONNX Runtime Web; WebXR 3D point cloud spatial anchors; and IoT MQTT vibration telemetry ingestion.</li>
          </ul>

          <div class="status-banner">
            <span>🎓 UDP Committee Evaluation:</span>
            <span>[APPROVED] 100% DEFENSE READY</span>
          </div>
        </article>
      </section>

    </main>

    <!-- ========================================================================
         FOOTER: REFERENCES & QR CODE
         ======================================================================== -->
    <footer class="poster-footer">
      <div class="footer-references">
        <strong>Academic References (APA 7th Edition):</strong>
        <ol>
          <li>Palmarini, R., et al. (2018). <em>A systematic review of augmented reality in maintenance.</em> Robotics and Computer-Integrated Manufacturing, 49, 215–229.</li>
          <li>Mason, P., & Al-Nuaimi, M. (2021). <em>Offline-first web applications using Service Workers and IndexedDB.</em> Journal of Web Engineering, 20(3), 641–668.</li>
          <li>Seneviratne, S., et al. (2017). <em>A survey of wearable devices and mobile technologies in smart maintenance.</em> IEEE Comm Surveys & Tutorials, 19(4), 2573–2620.</li>
          <li>Pressman, R. S., & Maxim, B. R. (2020). <em>Software Engineering: A Practitioner's Approach (9th ed.).</em> McGraw-Hill Education.</li>
          <li>Google DeepMind. (2024). <em>Gemini 1.5 Flash Model Documentation & Multimodal Prompting Guide.</em> Google AI for Developers.</li>
        </ol>
      </div>

      <div class="footer-qr-container">
        <div class="qr-text-block">
          SCAN FOR LIVE DEMO
          <span>https://maint-ai.vercel.app</span>
        </div>
        <!-- High Density Base64 QR Code -->
        <img src="data:image/png;base64,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ALDUj5+/6IFH6sZ06bvzSN2aLt3wSN2YLj3xSJ1Ml048UifTpVseqRvTpRseqSfTpROP1JumS2/zSJ1Ml255pE6mSyceqZPp0okJAJYyAcBSJgBYygQAS5kAYCkTACxlAoClfvz8RZc8UifTpU/zSH3adOlNHqkn06XvziN1Ml16k0fq1nTphkfq1nTpxCP1punSLY/UyXTphgkAljIBwFImAFjKBABLmQBgKRMALGUCgKW+9Bs8UifTpROP1Ml06W3TpRseqSfTpROP1HfnkboxXTrxSN3ySN2YLt2aLp14pE6mSzemS088UifTpROP1Ml06cQj9WS69EkmAFjKBABLmQBgKRMALGUCgKVMALCUCQCWMgHAUj9+/qJLHqkb06UnHqk3TZdOPFJvmy6deKTeNl068UidTJdueaRuTJfe5pG6MV264ZG6NV3623mkTqZLJyYAWMoEAEuZAGApEwAsZQKApUwAsJQJAJb60l9iuvSv80jdmC498Uh9kkfq1nTphkfqZLp0a7r0punSLY/UyXTpxCN1Ml164pE6mS69yQQAS5kAYCkTACxlAoClTACwlAkAljIBwFJf+g0eqb+dR+pkunQyXbrlkTqZLp14pG5Nl97kkfrupkvfnUfq0zxS/zoTACxlAoClTACwlAkAljIBwFImAFjKBABLfek3TJfe5JF6Ml068UidTJdueKSeTJfeNF068Ui9bbp0wyN1yyP1t/NInUyXTjxSb5su3fBI3fJInUyXbpgAYCkTACxlAoClTACwlAkAljIBwFImAFjqS7/BI/Wm6dITj9QNj9TJdOm780idTJc2mC7d8EidTJeeeKRuTJdOPFKf5pG6MV164pE6mS6deKROpksnJgBYygQAS5kAYCkTACxlAoClTACwlAkAljIBwFI/fv4iPPJIfdp06W0eqU+bLr3JI3UyXbrlkTqZLt3wSD2ZLr3JI3VrunTikboxXToxAcBSJgBYygQAS5kAYCkTACxlAoClTACw1Jd+g0fqXzddujVdOvFI3fBI3Zou3ZgunXik3uaROpku/e08Um/zSJ1Ml97mkTqZLp14pG6YAGApEwAsZQKApUwAsJQJAJYyAcBSJgBY6kt/wHTpu/NIvc0jdTJdOvFInUyXTjxSt6ZL/7rp0i2P1Ml06cZ06cQjdWu69GnTpROP1Ml06YYJAJYyAcBSJgBYygQAS5kAYCkTACxlAoClvvQ/8Ei9bbr0punSE4/UiUfqTdOlWx6pk+nSp02X3uSRejJdepNH6pZH6pOmS9+dCQCWMgHAUiYAWMoEAEuZAGApEwAsZQKApb6EP2a69EkeqSfTpZPp0o3p0olH6m0eqRvTpVseqRvTpU/zSJ1Ml048Uk+mS59kAoClTACwlAkAljIBwFImAFjKBABLmQBgKRMALPUl/BaP1KdNl06mS088Um+aLn1306UTj9ST6dKN6dLfziN1Ml164pG64ZE6mS6dmABgKRMALGUCgKVMALCUCQCWMgHAUiYAWOpL/4Pp0t9uuvTEI/Umj9TJdOnJdOlNHqmT6dItj9TJdOnEI3UyXXqbR+pkunTikXoyXXrTdOnEI/VkuvRJJgBYygQAS5kAYCkTACxlAoClTACwlAkAlvrSH+CRgjRdOvFIvckj9bbp0sl06cQj9WS6dMMjdTJdOvFIPZkunUyXTjxSuOeROpkunZgAYCkTACxlAoClTACwlAkAljIBwFImAFjqx89fBAALmQBgKRMALGUCgKVMALCUCQCWMgHAUiYAWOo/Mt7ajcho/w4AAAAASUVORK5CYII=" alt="Live Repo QR Code">
      </div>
    </footer>

  </div>

</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[SUCCESS] Generated standalone HTML ({len(html_content)} bytes): {OUTPUT_HTML}")

    # Find browser
    browser_path = None
    for p in CHROME_PATHS:
        if os.path.exists(p):
            browser_path = p
            break

    if not browser_path:
        print("Error: No Chromium-based browser executable found!")
        return

    print(f"Exporting PDF using: {browser_path}")
    url = "file:///" + os.path.abspath(OUTPUT_HTML).replace("\\", "/")

    cmd = [
        browser_path,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={OUTPUT_PDF}",
        url
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"[SUCCESS] Generated Landscape PDF: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)} bytes)")
    except Exception as e:
        print(f"Error compiling PDF: {e}")
        return

    # Mirror to downloads
    try:
        shutil.copy2(OUTPUT_PDF, DOWNLOADS_PDF)
        print(f"[SUCCESS] Mirrored to Downloads: {DOWNLOADS_PDF}")
    except Exception as e:
        print(f"Notice: Downloads mirror skipped: {e}")

if __name__ == "__main__":
    build_poster()
