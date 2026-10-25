#!/usr/bin/env python3
"""
MaintAI - Authentic Human-Designed Academic Presentation Generator
Features:
- Real, diverse, attractive figures from the MaintAI system:
  * Live AR Step Guidance UI (p12_img4_73.png)
  * Live Fault Incident Report UI (screenshot7_fault_report.png)
  * Live Supervisor Analytics & MTTR Dashboard (p14_img4_81.png)
  * Live Spare Parts Inventory Dashboard (p13_img3_76.png)
  * Live Plant QR Code Batch Generator (p15_img3_84.png)
  * Rich AR HUD Reticle (rich_ar_hud.png)
  * Real Machine Photo (cnc-machine.jpg)
  * Real Calibrated Torque Wrench (tool_wrench.jpg)
  * Real Machine Asset QR Code (qr_grundfos_pump.png)
  * 3-Tier System Architecture & Offline Sync Diagrams
- Big, cozy, highly legible typography (Titles 26-34pt, Stats 48pt, Headings 15-18pt, Body 12.5-13.5pt)
- Exact MaintAI Website Color Palette: Signature Safety Orange (#F97316), Deep Slate (#0F172A),
  Cozy Slate Navy (#1A2639), AR Cyan (#38BDF8), and Verified Emerald (#10B981).

Candidate: Het Joshi (Enrollment No. 24SE09CE003)
Internal Guide: Mr. Ayush Dodia (Assistant Professor)
Institute: Department of Computer Engineering, School of Engineering, P P Savani University
"""

import os
import sys
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
PARTS_DIR = os.path.join(PUBLIC_DIR, "parts")
MACHINES_DIR = os.path.join(PUBLIC_DIR, "machines")
PDF_IMAGES_DIR = os.path.join(BASE_DIR, "pdf_images")

# Primary & Fallback Output Paths
OUTPUT_COZY = os.path.join(BASE_DIR, "MaintAI_Cozy_Presentation.pptx")
OUTPUT_PROJECT = os.path.join(BASE_DIR, "MaintAI_Project_Presentation.pptx")
OUTPUT_MENTOR = os.path.join(BASE_DIR, "MaintAI_Mentor_Presentation.pptx")

# Website Brand Colors
COLOR_BG = RGBColor(15, 23, 42)             # #0F172A Deep Industrial Dark
COLOR_CARD = RGBColor(26, 38, 57)           # #1A2639 Soft Industrial Slate
COLOR_CARD_WARM = RGBColor(38, 30, 26)      # #261E1A Warm Orange Tint Card
COLOR_CARD_DARK = RGBColor(19, 29, 45)      # #131D2D Dark Frame
COLOR_BORDER = RGBColor(47, 63, 86)         # #2F3F56 Soft Slate Border

# Accents
COLOR_ORANGE = RGBColor(249, 115, 22)       # #F97316 MaintAI Signature Industrial Safety Orange
COLOR_ORANGE_WARM = RGBColor(251, 146, 60)  # #FB923C Warm Light Orange
COLOR_AMBER = RGBColor(245, 158, 11)        # #F59E0B Warning Amber
COLOR_CYAN = RGBColor(56, 189, 248)         # #38BDF8 AR & Vision Telemetry Cyan
COLOR_GREEN = RGBColor(16, 185, 129)        # #10B981 Success / Verified Emerald
COLOR_RED = RGBColor(239, 68, 68)           # #EF4444 Alert Red

# Text Colors
COLOR_WHITE = RGBColor(255, 255, 255)       # Crisp Pure White
COLOR_BODY = RGBColor(226, 232, 240)        # #E2E8F0 Cozy Legible Body Text
COLOR_MUTED = RGBColor(148, 163, 184)       # #94A3B8 Secondary Muted Slate

FONT_FAMILY = "Segoe UI"


def create_base_slide(prs):
    """Creates a 16:9 widescreen slide with dark industrial background."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG
    return slide


def add_cozy_header(slide, kicker_text, title_text, subtitle_text=""):
    """Adds a human-designed header with large readable fonts and orange accent."""
    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(0.42), Inches(0.6), Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_ORANGE
    bar.line.color.rgb = COLOR_ORANGE

    tx_box = slide.shapes.add_textbox(Inches(0.85), Inches(0.55), Inches(11.63), Inches(1.15))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_kicker = tf.paragraphs[0]
    p_kicker.text = kicker_text.upper()
    p_kicker.font.name = FONT_FAMILY
    p_kicker.font.size = Pt(11)
    p_kicker.font.bold = True
    p_kicker.font.color.rgb = COLOR_ORANGE
    p_kicker.space_after = Pt(2)

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = FONT_FAMILY
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE

    if subtitle_text:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_FAMILY
        p_sub.font.size = Pt(12.5)
        p_sub.font.color.rgb = COLOR_MUTED
        p_sub.space_before = Pt(3)


def add_cozy_footer(slide, slide_num, total_slides=14):
    """Adds standard clean presentation footer."""
    tx_box = slide.shapes.add_textbox(Inches(0.85), Inches(7.05), Inches(11.63), Inches(0.32))
    tf = tx_box.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"MaintAI: Industrial Reliability Platform  |  School of Engineering, PPSU  |  Het Joshi (24SE09CE003)        Slide {slide_num} of {total_slides}"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(100, 116, 139)


def add_cozy_card(slide, left, top, width, height, title="", items=None, badge="", accent_color=COLOR_ORANGE, bg_color=COLOR_CARD, title_size=15, body_size=12.5):
    """Adds a soft rounded card with generous padding, big readable text, and warm accents."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = COLOR_BORDER
    card.line.width = Pt(1.2)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.26)
    tf.margin_right = Inches(0.26)
    tf.margin_top = Inches(0.22)
    tf.margin_bottom = Inches(0.22)

    p0 = tf.paragraphs[0]
    if badge:
        p0.text = badge.upper()
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(9)
        p0.font.bold = True
        p0.font.color.rgb = accent_color
        p0.space_after = Pt(3)
        p_title = tf.add_paragraph()
    else:
        p_title = p0

    if title:
        p_title.text = title
        p_title.font.name = FONT_FAMILY
        p_title.font.size = Pt(title_size)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE
        p_title.space_after = Pt(8)

    if items:
        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.name = FONT_FAMILY
            p.font.size = Pt(body_size)
            p.font.color.rgb = COLOR_BODY
            p.space_after = Pt(6)

    return card


def build_unique_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    total_slides = 14

    # =========================================================================
    # SLIDE 1: Title Slide (Warm, Cozy Hero with Big Typography)
    # =========================================================================
    s1 = create_base_slide(prs)

    # University Logos
    ppsu_logo = os.path.join(PUBLIC_DIR, "official_ppsu_naac.png")
    soe_logo = os.path.join(PUBLIC_DIR, "official_school_of_engineering.png")
    if os.path.exists(ppsu_logo):
        s1.shapes.add_picture(ppsu_logo, Inches(0.85), Inches(0.55), height=Inches(1.0))
    if os.path.exists(soe_logo):
        s1.shapes.add_picture(soe_logo, Inches(10.2), Inches(0.55), height=Inches(1.0))

    # Signature Orange Badge
    badge_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.4), Inches(1.85), Inches(6.5), Inches(0.48))
    badge_box.fill.solid()
    badge_box.fill.fore_color.rgb = COLOR_CARD_WARM
    badge_box.line.color.rgb = COLOR_ORANGE
    badge_box.line.width = Pt(1.5)
    tf_b = badge_box.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "UNDERGRADUATE DESIGN PROJECT (UDP) FINAL DEFENSE"
    p_b.font.name = FONT_FAMILY
    p_b.font.size = Pt(11.5)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_ORANGE
    p_b.alignment = PP_ALIGN.CENTER

    # Project Title
    tx_title = s1.shapes.add_textbox(Inches(0.85), Inches(2.55), Inches(11.63), Inches(1.9))
    tf1 = tx_title.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "MaintAI: Intelligent Industrial Maintenance\n& AR Guidance Platform"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(34)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.alignment = PP_ALIGN.CENTER
    p1.space_after = Pt(10)

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Multimodal AI Vision Diagnostics, Hands-Free Voice Controls & Offline-First Reliability"
    p1_sub.font.name = FONT_FAMILY
    p1_sub.font.size = Pt(15)
    p1_sub.font.color.rgb = COLOR_CYAN
    p1_sub.alignment = PP_ALIGN.CENTER

    # Candidate & Guide Cards
    card_cand = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(4.75), Inches(4.7), Inches(1.85))
    card_cand.fill.solid()
    card_cand.fill.fore_color.rgb = COLOR_CARD
    card_cand.line.color.rgb = COLOR_ORANGE
    card_cand.line.width = Pt(1.5)
    tf_c = card_cand.text_frame
    tf_c.word_wrap = True
    tf_c.margin_top = Inches(0.2)
    p_c0 = tf_c.paragraphs[0]
    p_c0.text = "CANDIDATE / RESEARCHER"
    p_c0.font.name = FONT_FAMILY
    p_c0.font.size = Pt(9.5)
    p_c0.font.bold = True
    p_c0.font.color.rgb = COLOR_ORANGE
    p_c0.space_after = Pt(3)
    p_c1 = tf_c.add_paragraph()
    p_c1.text = "HET JOSHI"
    p_c1.font.name = FONT_FAMILY
    p_c1.font.size = Pt(18)
    p_c1.font.bold = True
    p_c1.font.color.rgb = COLOR_WHITE
    p_c2 = tf_c.add_paragraph()
    p_c2.text = "Enrollment: 24SE09CE003  |  7th Sem B.Tech CE\nSchool of Engineering, P P Savani University"
    p_c2.font.name = FONT_FAMILY
    p_c2.font.size = Pt(11.5)
    p_c2.font.color.rgb = COLOR_MUTED

    card_guide = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.75), Inches(4.7), Inches(1.85))
    card_guide.fill.solid()
    card_guide.fill.fore_color.rgb = COLOR_CARD
    card_guide.line.color.rgb = COLOR_GREEN
    card_guide.line.width = Pt(1.5)
    tf_g = card_guide.text_frame
    tf_g.word_wrap = True
    tf_g.margin_top = Inches(0.2)
    p_g0 = tf_g.paragraphs[0]
    p_g0.text = "INTERNAL GUIDE & MENTOR"
    p_g0.font.name = FONT_FAMILY
    p_g0.font.size = Pt(9.5)
    p_g0.font.bold = True
    p_g0.font.color.rgb = COLOR_GREEN
    p_g0.space_after = Pt(3)
    p_g1 = tf_g.add_paragraph()
    p_g1.text = "MR. AYUSH DODIA"
    p_g1.font.name = FONT_FAMILY
    p_g1.font.size = Pt(18)
    p_g1.font.bold = True
    p_g1.font.color.rgb = COLOR_WHITE
    p_g2 = tf_g.add_paragraph()
    p_g2.text = "Assistant Professor, Dept. of Computer Engineering\nSchool of Engineering, P P Savani University"
    p_g2.font.name = FONT_FAMILY
    p_g2.font.size = Pt(11.5)
    p_g2.font.color.rgb = COLOR_MUTED

    add_cozy_footer(s1, 1, total_slides)

    # =========================================================================
    # SLIDE 2: Problem Context (Giant Stat + Real Machine Photo!)
    # =========================================================================
    s2 = create_base_slide(prs)
    add_cozy_header(s2, "01 | Problem Context", "The Shop-Floor Maintenance Dilemma", "Why modern manufacturing lines face crippling downtime costs and safety vulnerabilities")

    # Left: Giant $260k Stat Card (48pt font)
    stat_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(1.85), Inches(4.8), Inches(4.85))
    stat_box.fill.solid()
    stat_box.fill.fore_color.rgb = COLOR_CARD_WARM
    stat_box.line.color.rgb = COLOR_ORANGE
    stat_box.line.width = Pt(2)
    tf_s = stat_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = Inches(0.35)
    tf_s.margin_top = Inches(0.35)

    p_s0 = tf_s.paragraphs[0]
    p_s0.text = "THE DOWNTIME CRISIS"
    p_s0.font.name = FONT_FAMILY
    p_s0.font.size = Pt(11)
    p_s0.font.bold = True
    p_s0.font.color.rgb = COLOR_ORANGE
    p_s0.space_after = Pt(8)

    p_s1 = tf_s.add_paragraph()
    p_s1.text = "$260,000"
    p_s1.font.name = FONT_FAMILY
    p_s1.font.size = Pt(48)
    p_s1.font.bold = True
    p_s1.font.color.rgb = COLOR_WHITE

    p_s2 = tf_s.add_paragraph()
    p_s2.text = "Average Loss Per Hour of Plant Outage"
    p_s2.font.name = FONT_FAMILY
    p_s2.font.size = Pt(14)
    p_s2.font.bold = True
    p_s2.font.color.rgb = COLOR_ORANGE_WARM
    p_s2.space_after = Pt(16)

    p_s3 = tf_s.add_paragraph()
    p_s3.text = "• An unexpected mechanical breakdown on an interconnected line halts sequential production immediately.\n\n• Traditional manual incident dispatching incurs a 40 to 90 minute response lag.\n\n• Extended Mean Time to Repair (MTTR) causes compounding financial and throughput losses."
    p_s3.font.name = FONT_FAMILY
    p_s3.font.size = Pt(12.5)
    p_s3.font.color.rgb = COLOR_BODY

    # Right: Real Industrial Machine Figure + Key Plant Friction Points
    cnc_img = os.path.join(MACHINES_DIR, "cnc-machine.jpg")
    if os.path.exists(cnc_img):
        # Image frame
        s2.shapes.add_picture(cnc_img, Inches(5.85), Inches(1.85), width=Inches(6.6), height=Inches(2.5))

    add_cozy_card(s2, Inches(5.85), Inches(4.5), Inches(6.6), Inches(2.2),
                  "Key Shop-Floor Vulnerabilities",
                  [
                      "Paper Manual Fatigue: Technicians struggle through 300+ page binders with greasy hands.",
                      "Basement Signal Dead Zones: Heavy concrete shielding blocks Wi-Fi/4G; cloud apps crash.",
                      "Unverified Tool Usage: Skipping torque wrench calibration leads to bolt shearing and OSHA hazards."
                  ],
                  badge="SHOP-FLOOR REALITY", accent_color=COLOR_AMBER, title_size=15, body_size=12)

    add_cozy_footer(s2, 2, total_slides)

    # =========================================================================
    # SLIDE 3: Objectives & Solution (Clean 3-Pillar Visual Breakdown)
    # =========================================================================
    s3 = create_base_slide(prs)
    add_cozy_header(s3, "02 | Objectives & Architecture", "Engineering Deliverables vs Legacy Methods", "Delivering a hands-free, intelligent maintenance platform purpose-built for harsh plant floors")

    # 3 Distinct High-Impact Vertical Pillars
    col_w = Inches(3.72)
    col_h = Inches(4.85)

    add_cozy_card(s3, Inches(0.85), Inches(1.85), col_w, col_h,
                  "Multimodal AI Vision",
                  [
                      "Instant Defect Detection: Analyzes bearing spalling, gear wear, and hydraulic leaks in < 1.4s.",
                      "ISO 10816 Classification: Automatically maps mechanical severity to standard vibration zones.",
                      "Automated Incident Creation: Instantly alerts shift supervisor with pre-filled parts list.",
                      "Top-1 Accuracy: 94.2% verified accuracy across 120 empirical workshop test cases."
                  ],
                  badge="PILLAR 1: VISION AI", accent_color=COLOR_CYAN, title_size=16, body_size=12.5)

    add_cozy_card(s3, Inches(4.8), Inches(1.85), col_w, col_h,
                  "In-Situ Web AR HUD",
                  [
                      "Lightweight HTML5 Canvas: Runs directly in mobile browser with zero app installation.",
                      "Pulsing Spatial Crosshairs: Highlights exact fastener sequences and lubrication points at 60 FPS.",
                      "AI Tool Gatekeeper: Physically checks mandatory torque wrench before unlocking repair steps.",
                      "Hands-Free Voice Listener: Greasy-handed navigation via 'Next Step', 'Torch', and 'Repeat'."
                  ],
                  badge="PILLAR 2: AR & VOICE", accent_color=COLOR_ORANGE, title_size=16, body_size=12.5)

    add_cozy_card(s3, Inches(8.75), Inches(1.85), col_w, col_h,
                  "Offline-First Resilience",
                  [
                      "Dexie.js IndexedDB Store: Local write-ahead log ensures <5ms task save in deep basements.",
                      "Zero UI Freezing: Technicians continue checklists uninterrupted during complete signal loss.",
                      "FIFO Reconciliation: Queued mutations replay sequentially with idempotency upon reconnect.",
                      "38% MTTR Reduction: Proven reduction in Mean Time to Repair during shop-floor UAT."
                  ],
                  badge="PILLAR 3: OFFLINE SYNC", accent_color=COLOR_GREEN, title_size=16, body_size=12.5)

    add_cozy_footer(s3, 3, total_slides)

    # =========================================================================
    # SLIDE 4: Architecture Topology (System Architecture Diagram + Tier Breakdown)
    # =========================================================================
    s4 = create_base_slide(prs)
    add_cozy_header(s4, "03 | System Topology", "3-Tier Edge-Resilient Platform Architecture", "Decoupled cloud-native frontend, local offline edge cache, and serverless AI backend")

    arch_img = os.path.join(PUBLIC_DIR, "updated_architecture_diagram.png")
    if os.path.exists(arch_img):
        s4.shapes.add_picture(arch_img, Inches(0.85), Inches(1.85), width=Inches(6.6))

    t_left = Inches(7.7)
    t_w = Inches(4.78)

    add_cozy_card(s4, t_left, Inches(1.85), t_w, Inches(1.5),
                  "Tier 1: Presentation & Web AR",
                  ["Next.js 14 App Router, React 18, Tailwind CSS.",
                   "HTML5 Canvas 60 FPS spatial visual overlay engine.",
                   "PWA Service Worker caches shell for offline boot."],
                  badge="CLIENT PRESENTATION", accent_color=COLOR_ORANGE, title_size=15, body_size=12.5)

    add_cozy_card(s4, t_left, Inches(3.52), t_w, Inches(1.5),
                  "Tier 2: Local Edge Runtime",
                  ["Dexie.js IndexedDB write-ahead log (<5ms latency).",
                   "Web Speech STT voice engine with phonetic match.",
                   "FIFO Sync Queue replays queued updates on reconnect."],
                  badge="EDGE RUNTIME", accent_color=COLOR_CYAN, title_size=15, body_size=12.5)

    add_cozy_card(s4, t_left, Inches(5.2), t_w, Inches(1.5),
                  "Tier 3: Cloud & AI Backend",
                  ["Supabase PostgreSQL with Row Level Security (RLS).",
                   "Google Gemini 1.5 Flash Vision serverless API proxy.",
                   "Cryptographic JWT authentication & secure recovery."],
                  badge="CLOUD BACKEND", accent_color=COLOR_GREEN, title_size=15, body_size=12.5)

    add_cozy_footer(s4, 4, total_slides)

    # =========================================================================
    # SLIDE 5: Computer Vision Diagnostics (Attractive Real UI Screenshot!)
    # =========================================================================
    s5 = create_base_slide(prs)
    add_cozy_header(s5, "04 | Computer Vision", "Multimodal Defect Identification & Telemetry", "Computer vision pipeline transforming noisy camera frames into actionable engineering diagnostics")

    # Left: Actual Real App Screenshot (Fault Incident Report UI)
    report_ui_img = os.path.join(PDF_IMAGES_DIR, "screenshot7_fault_report.png")
    if os.path.exists(report_ui_img):
        s5.shapes.add_picture(report_ui_img, Inches(0.85), Inches(1.85), width=Inches(6.5))

    # Right: 4-Stage Pipeline + Standards Card
    r_w5 = Inches(4.88)
    add_cozy_card(s5, Inches(7.6), Inches(1.85), r_w5, Inches(2.35),
                  "4-Stage Vision Pipeline",
                  [
                      "1. Frame Acquisition: 1080p WebRTC capture with client-side canvas compression.",
                      "2. Vision Inference: Gemini 1.5 Flash detects bearing wear, pitting, and leaks.",
                      "3. Defect Taxonomy: Severity classification with 94.2% top-1 confidence score.",
                      "4. Auto Incident Creation: Pre-populates required parts and alerts supervisor."
                  ],
                  badge="COMPUTER VISION PIPELINE", accent_color=COLOR_ORANGE, title_size=15, body_size=12.5)

    add_cozy_card(s5, Inches(7.6), Inches(4.35), r_w5, Inches(2.35),
                  "Standards & Telemetry Norms",
                  [
                      "ISO 10816 Vibration Severity: Maps machine anomalies directly to Class A/B/C/D operational limits.",
                      "ISO 898-1 Fastener Ratings: Enforces specified bolt tension and star-pattern sequences.",
                      "Sub-1.4s Execution: Cloud edge serverless execution ensures instant shop-floor feedback."
                  ],
                  badge="ENGINEERING INTEGRITY", accent_color=COLOR_GREEN, title_size=15, body_size=12.5)

    add_cozy_footer(s5, 5, total_slides)

    # =========================================================================
    # SLIDE 6: AR HUD & AI Tool Gating (Live AR Screen + Tool Photo!)
    # =========================================================================
    s6 = create_base_slide(prs)
    add_cozy_header(s6, "05 | Augmented Reality", "In-Situ AR HUD & AI Tool Gatekeeper", "Interactive spatial step guidance with mandatory visual tool verification before step progression")

    # Left: Real Live AR Step Guidance UI (p12_img4_73.png)
    ar_step_ui = os.path.join(PUBLIC_DIR, "p12_img4_73.png")
    if os.path.exists(ar_step_ui):
        s6.shapes.add_picture(ar_step_ui, Inches(0.85), Inches(1.85), width=Inches(6.5))

    # Right: Tool Gatekeeper with Real Torque Wrench Photo
    r_w6 = Inches(4.88)
    add_cozy_card(s6, Inches(7.6), Inches(1.85), r_w6, Inches(2.1),
                  "HTML5 Canvas 60 FPS Web AR Engine",
                  [
                      "Zero Native App Downloads: Overlays visual reticles and safety zones directly on browser camera stream.",
                      "Percentage Coordinates (x%, y%): Dynamically scales across mobile phones, tablets, and smart glasses."
                  ],
                  badge="SPATIAL ENGINE", accent_color=COLOR_CYAN, title_size=15, body_size=12.5)

    # Tool Gatekeeper Card with Real Tool Photo
    tool_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.6), Inches(4.1), r_w6, Inches(2.6))
    tool_box.fill.solid()
    tool_box.fill.fore_color.rgb = COLOR_CARD_WARM
    tool_box.line.color.rgb = COLOR_ORANGE
    tool_box.line.width = Pt(1.5)

    # Insert Real Tool Photo
    tool_img = os.path.join(PDF_IMAGES_DIR, "tool_wrench.jpg")
    if os.path.exists(tool_img):
        s6.shapes.add_picture(tool_img, Inches(7.8), Inches(4.55), width=Inches(1.6), height=Inches(1.6))

    # Text next to Tool Photo
    tx_tool = s6.shapes.add_textbox(Inches(9.55), Inches(4.2), Inches(2.8), Inches(2.4))
    tf_t = tx_tool.text_frame
    tf_t.word_wrap = True
    tf_t.margin_top = Inches(0.1)
    p_tb = tf_t.paragraphs[0]
    p_tb.text = "TOOL GATE: 17MM TORQUE WRENCH"
    p_tb.font.name = FONT_FAMILY
    p_tb.font.size = Pt(8.5)
    p_tb.font.bold = True
    p_tb.font.color.rgb = COLOR_ORANGE
    p_tb.space_after = Pt(2)

    p_tt = tf_t.add_paragraph()
    p_tt.text = "Visual Tool Verification Protocol"
    p_tt.font.name = FONT_FAMILY
    p_tt.font.size = Pt(12)
    p_tt.font.bold = True
    p_tt.font.color.rgb = COLOR_WHITE
    p_tt.space_after = Pt(4)

    p_td = tf_t.add_paragraph()
    p_td.text = "Step progression locks until technician shows the calibrated wrench to camera. AI confirms tool presence with 97.8% confidence."
    p_td.font.name = FONT_FAMILY
    p_td.font.size = Pt(10.5)
    p_td.font.color.rgb = COLOR_BODY

    add_cozy_footer(s6, 6, total_slides)

    # =========================================================================
    # SLIDE 7: Hands-Free Voice Guidance (Voice Architecture + Command Table)
    # =========================================================================
    s7 = create_base_slide(prs)
    add_cozy_header(s7, "06 | Voice Interface", "Hands-Free Voice State Machine", "Enabling grease-handed technicians to operate complex workflows purely through spoken commands")

    add_cozy_card(s7, Inches(0.85), Inches(1.85), Inches(4.7), Inches(4.85),
                  "Acoustic Speech Architecture",
                  [
                      "Web Speech API Integration: Native browser speech recognition running in-browser with zero cloud delay.",
                      "Noise-Tolerant State Machine: Implements phonetic and Levenshtein distance matching to filter shop-floor hum.",
                      "Continuous Listening Daemon: Automatic restart loop maintains voice standby mode even through pauses.",
                      "Multi-Accent Tolerance: Robust tokenization handles diverse technical pronunciations effortlessly.",
                      "Auditory TTS Feedback: System speaks confirmations aloud, keeping technician's eyes locked on the machinery."
                  ],
                  badge="VOICE ARCHITECTURE", accent_color=COLOR_ORANGE, title_size=16, body_size=13)

    cmd_shape = s7.shapes.add_table(6, 2, Inches(5.8), Inches(1.85), Inches(6.68), Inches(4.85))
    cmd_tbl = cmd_shape.table
    cmd_tbl.columns[0].width = Inches(2.4)
    cmd_tbl.columns[1].width = Inches(4.28)

    cmd_headers = ["Spoken Voice Command", "System Action & Audio Feedback"]
    for c_idx, h_text in enumerate(cmd_headers):
        cell = cmd_tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_CARD_WARM if c_idx == 0 else COLOR_CARD
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_ORANGE if c_idx == 0 else COLOR_WHITE

    commands = [
        ('"Next Step" / "Continue"', "Advances AR guidance to the next sequential instruction"),
        ('"Repeat Step"', "Triggers text-to-speech audio readout of the current step"),
        ('"Previous Step" / "Back"', "Returns to previous step if verification is needed"),
        ('"Toggle Torch"', "Activates hardware camera LED for dark machinery cavities"),
        ('"Safety Checklist"', "Reads aloud mandatory PPE & Lockout/Tagout (LOTO) rules")
    ]

    for r_idx, (cmd_txt, action_txt) in enumerate(commands, 1):
        c0 = cmd_tbl.cell(r_idx, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = COLOR_CARD
        c0.vertical_anchor = MSO_ANCHOR.MIDDLE
        p0 = c0.text_frame.paragraphs[0]
        p0.text = cmd_txt
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_CYAN

        c1 = cmd_tbl.cell(r_idx, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = COLOR_CARD
        c1.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = c1.text_frame.paragraphs[0]
        p1.text = action_txt
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(11)
        p1.font.color.rgb = COLOR_BODY

    add_cozy_footer(s7, 7, total_slides)

    # =========================================================================
    # SLIDE 8: FixBot AI Copilot (Dual-Mode Comparison with Real Diagnostic Output)
    # =========================================================================
    s8 = create_base_slide(prs)
    add_cozy_header(s8, "07 | AI Copilot", "FixBot AI: Industrial Reliability Copilot", "Dual-mode assistant providing both friendly shop guidance and rigorous 5-part engineering diagnostics")

    fb_w = Inches(5.68)
    fb_h = Inches(4.85)

    add_cozy_card(s8, Inches(0.85), Inches(1.85), fb_w, fb_h,
                  "Mode 1: Shop Teammate",
                  [
                      "Natural Language Interface: Friendly conversational assistant for shift greetings, safety briefings, and casual maintenance inquiries.",
                      "Quick Shop Queries: 'Where is the 17mm torque wrench stored?', 'Who is the supervisor on duty?'",
                      "Pre-Shift Briefing: Quick plant status review and safety tips before beginning maintenance operations.",
                      "Context-Aware Memory: Maintains multi-turn dialog context across complex troubleshooting steps."
                  ],
                  badge="CONVERSATIONAL TEAMMATE", accent_color=COLOR_CYAN, title_size=16, body_size=13)

    add_cozy_card(s8, Inches(6.8), Inches(1.85), fb_w, fb_h,
                  "Mode 2: 5-Part Diagnostic Protocol",
                  [
                      "1. Safety & LOTO: Mandatory electrical 415V breaker isolation and hydraulic pressure bleeding to 0 bar.",
                      "2. Root Cause Hypothesis: Seal extrusion due to overpressure (92% probability).",
                      "3. Calibrated Torque & Clearance: Flange fasteners torqued to exact 45 Nm in star pattern; clearance 0.05mm.",
                      "4. OEM Replacement Parts: Part #HS-45-V (Hydraulic Seal 45mm); checks live store stock (14 in stock).",
                      "5. Step-by-Step SOP: Sequential disassembly, seal seating, and pressure testing with ISO compliance."
                  ],
                  badge="5-PART ENGINEERING PROTOCOL", accent_color=COLOR_ORANGE, title_size=16, body_size=13)

    add_cozy_footer(s8, 8, total_slides)

    # =========================================================================
    # SLIDE 9: Smart Spare Parts Inventory (Real Dashboard Screenshot + Part Photos!)
    # =========================================================================
    s9 = create_base_slide(prs)
    add_cozy_header(s9, "08 | Inventory Logistics", "Smart Spare Parts Catalog & Stock Tracking", "Real-time stock governance, OEM part mapping, and high-speed barcode scanning")

    # Left: Real Live Parts Inventory Dashboard UI (p13_img3_76.png)
    parts_ui_img = os.path.join(PUBLIC_DIR, "p13_img3_76.png")
    if os.path.exists(parts_ui_img):
        s9.shapes.add_picture(parts_ui_img, Inches(0.85), Inches(1.85), width=Inches(6.5))

    # Right: 4 Real Component Photos with Labels
    part_samples = [
        ("ball-bearing-6205.jpg", "Bearing 6205-2RS", "42 in stock"),
        ("contactor-lc1d25.jpg", "Contactor LC1D25", "8 in stock"),
        ("hydraulic-seal-hs-45.jpg", "Seal HS-45-V", "14 in stock"),
        ("oil-filter-of-200.jpg", "Filter OF-200", "22 in stock")
    ]

    r_x = Inches(7.6)
    r_w9 = Inches(4.88)

    add_cozy_card(s9, r_x, Inches(1.85), r_w9, Inches(1.6),
                  "36 Verified OEM Machine Components",
                  [
                      "Real-time stock tracking with automated reorder thresholds (Safe, Low, Out-of-Stock).",
                      "Machine Compatibility Matrix prevents wrong part installation by matching part numbers."
                  ],
                  badge="PARTS REPOSITORY", accent_color=COLOR_ORANGE, title_size=14, body_size=11.5)

    # 4 Real Photos in a 2x2 Grid
    for i, (p_file, p_name, p_stock) in enumerate(part_samples):
        px = r_x + Inches((i % 2) * 2.5)
        py = Inches(3.6 + (i // 2) * 1.55)
        
        c_shape = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, py, Inches(2.38), Inches(1.45))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = COLOR_CARD
        c_shape.line.color.rgb = COLOR_BORDER

        p_path = os.path.join(PARTS_DIR, p_file)
        if os.path.exists(p_path):
            s9.shapes.add_picture(p_path, px + Inches(0.12), py + Inches(0.18), width=Inches(1.05), height=Inches(1.05))

        tx = s9.shapes.add_textbox(px + Inches(1.22), py + Inches(0.2), Inches(1.1), Inches(1.0))
        tf_p = tx.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0
        p_n = tf_p.paragraphs[0]
        p_n.text = p_name
        p_n.font.name = FONT_FAMILY
        p_n.font.size = Pt(9.5)
        p_n.font.bold = True
        p_n.font.color.rgb = COLOR_WHITE

        p_st = tf_p.add_paragraph()
        p_st.text = p_stock
        p_st.font.name = FONT_FAMILY
        p_st.font.size = Pt(8.5)
        p_st.font.bold = True
        p_st.font.color.rgb = COLOR_GREEN

    add_cozy_footer(s9, 9, total_slides)

    # =========================================================================
    # SLIDE 10: Plant QR Asset Barcode Management (Real Print Matrix Figure!)
    # =========================================================================
    s10 = create_base_slide(prs)
    add_cozy_header(s10, "09 | Asset Tracking", "Plant QR Code Management & Asset Labeling", "Sub-200ms camera decode, batch barcode generation, and digital twin retrieval")

    # Left: Real Live QR Matrix UI (p15_img3_84.png)
    qr_ui_img = os.path.join(PUBLIC_DIR, "p15_img3_84.png")
    if os.path.exists(qr_ui_img):
        s10.shapes.add_picture(qr_ui_img, Inches(0.85), Inches(1.85), width=Inches(6.5))

    # Right: Real Asset QR Tag + Technical Features
    r_w10 = Inches(4.88)
    
    # Real Machine QR Card
    qr_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.6), Inches(1.85), r_w10, Inches(2.1))
    qr_card.fill.solid()
    qr_card.fill.fore_color.rgb = COLOR_CARD_WARM
    qr_card.line.color.rgb = COLOR_ORANGE
    qr_card.line.width = Pt(1.5)

    qr_img = os.path.join(PDF_IMAGES_DIR, "qr_grundfos_pump.png")
    if os.path.exists(qr_img):
        s10.shapes.add_picture(qr_img, Inches(7.8), Inches(2.1), width=Inches(1.6), height=Inches(1.6))

    tx_qr = s10.shapes.add_textbox(Inches(9.55), Inches(1.95), Inches(2.8), Inches(1.9))
    tf_q = tx_qr.text_frame
    tf_q.word_wrap = True
    p_qb = tf_q.paragraphs[0]
    p_qb.text = "ASSET TAG: PUMP-GRUNDFOS-01"
    p_qb.font.name = FONT_FAMILY
    p_qb.font.size = Pt(8.5)
    p_qb.font.bold = True
    p_qb.font.color.rgb = COLOR_ORANGE
    p_qb.space_after = Pt(2)

    p_qt = tf_q.add_paragraph()
    p_qt.text = "Instant Digital Twin Lookup"
    p_qt.font.name = FONT_FAMILY
    p_qt.font.size = Pt(12)
    p_qt.font.bold = True
    p_qt.font.color.rgb = COLOR_WHITE
    p_qt.space_after = Pt(4)

    p_qd = tf_q.add_paragraph()
    p_qd.text = "Scanning physical machine tag loads operational telemetry, maintenance log history, and open tickets in under 200ms."
    p_qd.font.name = FONT_FAMILY
    p_qd.font.size = Pt(10)
    p_qd.font.color.rgb = COLOR_BODY

    add_cozy_card(s10, Inches(7.6), Inches(4.15), r_w10, Inches(2.55),
                  "Batch Asset Generation Features",
                  [
                      "Built-In Code128 & QR Generator: Prints industrial tags directly from web interface.",
                      "Eliminates Dedicated Scanners: Operates using built-in smartphone or tablet camera stream.",
                      "Zero Offline Overhead: Machine metadata cached locally for offline lookups."
                  ],
                  badge="ASSET LIFECYCLE", accent_color=COLOR_CYAN, title_size=15, body_size=12.5)

    add_cozy_footer(s10, 10, total_slides)

    # =========================================================================
    # SLIDE 11: Supervisor Analytics & RBAC (Real Analytics Dashboard Figure!)
    # =========================================================================
    s11 = create_base_slide(prs)
    add_cozy_header(s11, "10 | Access Control", "Role-Based Security & Supervisor Analytics", "Real-time fleet reliability telemetry, MTTR tracking, and role-based permissions")

    # Left: Real Live Supervisor Analytics Dashboard (p14_img4_81.png)
    analytics_ui_img = os.path.join(PUBLIC_DIR, "p14_img4_81.png")
    if os.path.exists(analytics_ui_img):
        s11.shapes.add_picture(analytics_ui_img, Inches(0.85), Inches(1.85), width=Inches(6.5))

    # Right: 3 Clear Roles
    r_w11 = Inches(4.88)
    add_cozy_card(s11, Inches(7.6), Inches(1.85), r_w11, Inches(4.85),
                  "Role-Based Governance (RBAC)",
                  [
                      "Plant Administrator (Red): Global fleet telemetry, MTTR/MTBF analytics, inventory thresholds, user provisioning, and immutable cryptographic audit logs.",
                      "Shift Supervisor (Orange): Visual drag-and-drop fault triage, machine dispatch board, review of repair photos, and return-to-service authorization.",
                      "Field Technician (Green): Personal task inbox, hands-free AR camera guidance, voice checklists, tool verification, and digital certificate signing.",
                      "Supabase Row Level Security (RLS): Guarantees total data isolation and role boundaries at the PostgreSQL database level."
                  ],
                  badge="ACCESS CONTROL MATRIX", accent_color=COLOR_ORANGE, title_size=16, body_size=12.5)

    add_cozy_footer(s11, 11, total_slides)

    # =========================================================================
    # SLIDE 12: Offline-First Synchronization (Diagram + Technical Explanation)
    # =========================================================================
    s12 = create_base_slide(prs)
    add_cozy_header(s12, "11 | Data Resilience", "Offline-First Write-Ahead Synchronization", "Zero-data-loss architecture engineered specifically for metal-shielded industrial dead zones")

    sync_img = os.path.join(PUBLIC_DIR, "updated_offline_sync_workflow.png")
    if os.path.exists(sync_img):
        s12.shapes.add_picture(sync_img, Inches(0.85), Inches(1.85), width=Inches(6.6))

    sw_w12 = Inches(4.78)
    add_cozy_card(s12, Inches(7.7), Inches(1.85), sw_w12, Inches(2.35),
                  "Dexie.js IndexedDB Local Store",
                  [
                      "Local Write-Ahead Log: All maintenance updates, completed checklists, and photo evidence write locally in < 5ms.",
                      "IndexedDB Schema: Local relational tables for machines, parts, fault reports, and queued transactions.",
                      "Zero UI Lag: Technicians work completely uninterrupted when network connection drops."
                  ],
                  badge="LOCAL WRITE-AHEAD STORAGE", accent_color=COLOR_CYAN, title_size=15, body_size=12.5)

    add_cozy_card(s12, Inches(7.7), Inches(4.35), sw_w12, Inches(2.35),
                  "Background Reconciliation Worker",
                  [
                      "Network Sentinel: Real-time listener detects when Wi-Fi or cellular connectivity is restored.",
                      "FIFO Sync Queue: Queued mutations replay sequentially with idempotency keys to prevent duplicate records.",
                      "Zero Data Loss: Stress-tested over 50 offline cycles with 100% data integrity verified."
                  ],
                  badge="AUTOMATIC RECONCILIATION", accent_color=COLOR_ORANGE, title_size=15, body_size=12.5)

    add_cozy_footer(s12, 12, total_slides)

    # =========================================================================
    # SLIDE 13: Quantitative Benchmarks (4 Huge Cozy Stats + Clear Table)
    # =========================================================================
    s13 = create_base_slide(prs)
    add_cozy_header(s13, "12 | System Benchmarks", "Empirical Performance & Verification Results", "Empirical performance testing across computer vision, AR graphics, and offline synchronization")

    # 4 Giant Metric Callout Cards with 44pt Bold Fonts
    stat_w3 = Inches(2.76)
    stat_h3 = Inches(1.3)
    top_stat3 = Inches(1.85)

    stat_data3 = [
        ("94.2%", "AI Detection Accuracy", "120 fault images tested", COLOR_ORANGE),
        ("< 1.4s", "Vision API Latency", "Serverless edge inference", COLOR_GREEN),
        ("59.8 FPS", "Mobile AR HUD Speed", "HTML5 Canvas benchmark", COLOR_CYAN),
        ("38%", "MTTR Reduction", "Versus paper manuals in UAT", COLOR_ORANGE_WARM)
    ]

    for i, (val_s, title_s, desc_s, clr_s) in enumerate(stat_data3):
        sc = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85 + i * 2.96), top_stat3, stat_w3, stat_h3)
        sc.fill.solid()
        sc.fill.fore_color.rgb = COLOR_CARD
        sc.line.color.rgb = clr_s
        sc.line.width = Pt(1.5)
        tf_sc = sc.text_frame
        tf_sc.word_wrap = True
        tf_sc.margin_top = Inches(0.12)

        p_v = tf_sc.paragraphs[0]
        p_v.text = val_s
        p_v.font.name = FONT_FAMILY
        p_v.font.size = Pt(22)
        p_v.font.bold = True
        p_v.font.color.rgb = clr_s
        p_v.alignment = PP_ALIGN.CENTER

        p_t = tf_sc.add_paragraph()
        p_t.text = f"{title_s} ({desc_s})"
        p_t.font.name = FONT_FAMILY
        p_t.font.size = Pt(9)
        p_t.font.color.rgb = COLOR_WHITE
        p_t.alignment = PP_ALIGN.CENTER

    # Verification Table
    bm_shape = s13.shapes.add_table(5, 3, Inches(0.85), Inches(3.35), Inches(11.63), Inches(3.35))
    bm_t = bm_shape.table
    bm_t.columns[0].width = Inches(3.2)
    bm_t.columns[1].width = Inches(3.2)
    bm_t.columns[2].width = Inches(5.23)

    bm_headers = ["Benchmark Parameter", "Measured Performance", "Industry Benchmark / Standard"]
    for c_idx, h_text in enumerate(bm_headers):
        cell = bm_t.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_CARD_WARM if c_idx == 1 else COLOR_CARD
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_FAMILY
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_ORANGE if c_idx == 1 else COLOR_WHITE

    bm_rows = [
        ("Offline Write Latency", "4.2 ms (IndexedDB write-ahead)", "Target < 50 ms for seamless UX (10x faster)"),
        ("Barcode Decode Speed", "180 ms (Code128 / QR / DataMatrix)", "Target < 500 ms on standard 1080p camera feed"),
        ("Offline Stress Test", "50 cycles / 500+ mutations -> 0 loss", "Zero data collision with FIFO idempotency queue"),
        ("Lighthouse PWA Score", "Performance: 96 | PWA: 100 | Access: 98", "Google Web Vitals Gold Standard (Production Vercel)")
    ]

    for r_idx, (p_col, m_col, s_col) in enumerate(bm_rows, 1):
        c0 = bm_t.cell(r_idx, 0)
        c0.fill.solid()
        c0.fill.fore_color.rgb = COLOR_CARD
        c0.vertical_anchor = MSO_ANCHOR.MIDDLE
        p0 = c0.text_frame.paragraphs[0]
        p0.text = p_col
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_WHITE

        c1 = bm_t.cell(r_idx, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = COLOR_CARD
        c1.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = c1.text_frame.paragraphs[0]
        p1.text = m_col
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_GREEN

        c2 = bm_t.cell(r_idx, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = COLOR_CARD
        c2.vertical_anchor = MSO_ANCHOR.MIDDLE
        p2 = c2.text_frame.paragraphs[0]
        p2.text = s_col
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_BODY

    add_cozy_footer(s13, 13, total_slides)

    # =========================================================================
    # SLIDE 14: Conclusion & Future Scope (Warm Q&A Banner)
    # =========================================================================
    s14 = create_base_slide(prs)
    add_cozy_header(s14, "13 | Conclusion", "Summary of Achievements & Next Frontiers", "Bridging the gap between cutting-edge AI and rugged shop-floor operational realities")

    c_w2 = Inches(5.68)
    c_h2 = Inches(3.95)

    add_cozy_card(s14, Inches(0.85), Inches(1.85), c_w2, c_h2,
                  "Summary of Achievements",
                  [
                      "Successfully engineered MaintAI: a unified, lightweight, hands-free maintenance platform combining AI vision, Web AR, and offline resilience.",
                      "Overcame critical industrial pain points: eliminated paper manual delays, mitigated connection blackouts, and enforced tool safety compliance.",
                      "Demonstrates 100% individual design, coding, testing, and cloud deployment by candidate Het Joshi.",
                      "Fully deployed and live on Vercel with active Supabase cloud database synchronization."
                  ],
                  badge="PROJECT OUTCOMES", accent_color=COLOR_ORANGE, title_size=16, body_size=13)

    add_cozy_card(s14, Inches(6.8), Inches(1.85), c_w2, c_h2,
                  "Future Development Roadmap",
                  [
                      "Industrial IoT Integration: Ingesting live telemetry streams directly via MQTT / OPC-UA industrial automation protocols.",
                      "Thermal FLIR Camera Streaming: Incorporating infrared thermal imaging for heat dissipation and hotspot anomaly detection.",
                      "Spatial WebXR SLAM: Upgrading 2D canvas overlays to full 3D spatial anchoring on complex physical equipment assemblies.",
                      "Research Publication: Preparing findings on offline multimodal tool verification for IEEE/ACM conference submission."
                  ],
                  badge="FUTURE ROADMAP", accent_color=COLOR_GREEN, title_size=16, body_size=13)

    # Warm Academic Defense Q&A Banner
    qa_banner = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(5.95), Inches(11.63), Inches(0.88))
    qa_banner.fill.solid()
    qa_banner.fill.fore_color.rgb = COLOR_CARD_WARM
    qa_banner.line.color.rgb = COLOR_ORANGE
    qa_banner.line.width = Pt(1.5)

    tf_qa = qa_banner.text_frame
    tf_qa.word_wrap = True
    p_qa = tf_qa.paragraphs[0]
    p_qa.text = "Thank You! Questions & Discussion with Honorable Guide & External Examiner"
    p_qa.font.name = FONT_FAMILY
    p_qa.font.size = Pt(13)
    p_qa.font.bold = True
    p_qa.font.color.rgb = COLOR_WHITE
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.space_after = Pt(2)

    p_qa_sub = tf_qa.add_paragraph()
    p_qa_sub.text = "Candidate: Het Joshi (24SE09CE003)  |  Guide: Mr. Ayush Dodia  |  School of Engineering, PPSU"
    p_qa_sub.font.name = FONT_FAMILY
    p_qa_sub.font.size = Pt(10.5)
    p_qa_sub.font.bold = True
    p_qa_sub.font.color.rgb = COLOR_ORANGE
    p_qa_sub.alignment = PP_ALIGN.CENTER

    add_cozy_footer(s14, 14, total_slides)

    # Resilient saving across candidate filenames (in case PowerPoint has one locked)
    candidates = [
        os.path.join(BASE_DIR, "MaintAI_Defense_Presentation.pptx"),
        OUTPUT_PROJECT,
        OUTPUT_MENTOR,
        OUTPUT_COZY
    ]
    saved_files = []
    for c_path in candidates:
        try:
            prs.save(c_path)
            saved_files.append(c_path)
        except PermissionError:
            pass

    if saved_files:
        print(f"[SUCCESS] Unique presentation saved to: {saved_files[0]}")
        if len(saved_files) > 1:
            for extra in saved_files[1:]:
                print(f"[SUCCESS] Also updated: {extra}")
    else:
        # Ultimate fallback with timestamp
        import time
        fallback = os.path.join(BASE_DIR, f"MaintAI_Presentation_{int(time.time())}.pptx")
        prs.save(fallback)
        print(f"[SUCCESS] Saved presentation to: {fallback}")

    print(f"[STATS] Total slides generated: {len(prs.slides)}")


if __name__ == "__main__":
    build_unique_deck()
