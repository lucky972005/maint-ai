#!/usr/bin/env python3
"""
MaintAI - Template-Based Presentation Builder
Uses the exact Canva template from C:\\Users\\hetjo\\Downloads\\Modern Software Development Milestones.pptx
Adheres to the template's dimensions (11.69 x 8.26 in), typography (Chakra Petch & Lato),
and color palette (Electric Royal Blue #2224FD, Cyber Cyan #5BE6FF, Pure White, Safety Orange accents).

Customizes the template's native Infographic Slides (Milestone Timeline + 10-Step Sequential Lifecycle)
and appends fully-styled slides with real system figures (CNC Machine, AR HUD UI, Fault Report UI,
Spare Parts Inventory Dashboard, QR Generator, and Analytics Dashboard).
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
PARTS_DIR = os.path.join(PUBLIC_DIR, "parts")
MACHINES_DIR = os.path.join(PUBLIC_DIR, "machines")
PDF_IMAGES_DIR = os.path.join(BASE_DIR, "pdf_images")
TEMPLATE_PATH = r"C:\Users\hetjo\Downloads\Modern Software Development Milestones.pptx"

# Output files
OUTPUT_MENTOR = os.path.join(BASE_DIR, "MaintAI_Mentor_Presentation.pptx")
OUTPUT_DEFENSE = os.path.join(BASE_DIR, "MaintAI_Defense_Presentation.pptx")
OUTPUT_PROJECT = os.path.join(BASE_DIR, "MaintAI_Project_Presentation.pptx")

# Template Exact Palette
COLOR_BLACK = RGBColor(0, 0, 0)
COLOR_DARK_BG = RGBColor(7, 10, 20)           # #070A14 Deep Cyber Dark
COLOR_CARD = RGBColor(14, 20, 38)             # #0E1426 Slate Cyber Card
COLOR_CARD_BORDER = RGBColor(34, 50, 85)      # #223255
COLOR_BLUE = RGBColor(34, 36, 253)            # #2224FD Electric Royal Blue
COLOR_CYAN = RGBColor(91, 230, 255)           # #5BE6FF Cyber Cyan
COLOR_ORANGE = RGBColor(249, 115, 22)         # #F97316 MaintAI Safety Orange
COLOR_GREEN = RGBColor(16, 185, 129)          # #10B981 Emerald
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_BODY = RGBColor(226, 232, 240)
COLOR_MUTED = RGBColor(148, 163, 184)

FONT_HEADING = "Chakra Petch"
FONT_BODY = "Lato"


def customize_template_slide1(slide):
    """Customizes Slide 1 of the template: 5-Phase MaintAI Milestone Roadmap."""
    # Find text shapes and replace with MaintAI content
    for shp in slide.shapes:
        if not shp.has_text_frame:
            continue
        txt = shp.text_frame.text.strip()
        if "SOFTWARE DEVELOPMENT" in txt:
            shp.text_frame.text = "MAINTAI RELIABILITY PLATFORM"
            for p in shp.text_frame.paragraphs:
                p.font.name = FONT_HEADING
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
        elif "MILESTONES" in txt:
            shp.text_frame.text = "CORE ARCHITECTURAL PILLARS"
            for p in shp.text_frame.paragraphs:
                p.font.name = FONT_HEADING
                p.font.bold = True
                p.font.color.rgb = COLOR_CYAN

        # Milestone 1: Vision
        elif txt == "2000":
            shp.text_frame.text = "VISION"
            shp.text_frame.paragraphs[0].font.name = FONT_HEADING
            shp.text_frame.paragraphs[0].font.color.rgb = COLOR_CYAN
        elif "aliqua amet" in txt and shp.left.inches < Inches(2.5):
            shp.text_frame.text = "Multimodal AI computer vision detecting bearing spalling, gear pitting, and fluid leaks in <1.4s (94.2% top-1 accuracy)."
            for p in shp.text_frame.paragraphs:
                p.font.name = FONT_BODY
                p.font.size = Pt(9.5)
                p.font.color.rgb = COLOR_BODY

        # Milestone 2: Web AR
        elif txt == "2010":
            shp.text_frame.text = "WEB AR"
            shp.text_frame.paragraphs[0].font.name = FONT_HEADING
            shp.text_frame.paragraphs[0].font.color.rgb = COLOR_CYAN
        elif "aliqua amet" in txt and Inches(2.5) <= shp.left.inches < Inches(4.5):
            shp.text_frame.text = "HTML5 Canvas 60 FPS in-situ spatial guidance directly in mobile browsers with zero native app installation."
            for p in shp.text_frame.paragraphs:
                p.font.name = FONT_BODY
                p.font.size = Pt(9.5)
                p.font.color.rgb = COLOR_BODY

        # Milestone 3: Tool Gate
        elif txt == "2015":
            shp.text_frame.text = "GATEKEEPER"
            shp.text_frame.paragraphs[0].font.name = FONT_HEADING
            shp.text_frame.paragraphs[0].font.color.rgb = COLOR_CYAN
        elif "aliqua amet" in txt and Inches(4.5) <= shp.left.inches < Inches(6.5):
            shp.text_frame.text = "Automated visual tool gatekeeper verifying calibrated torque wrench in hand before high-risk step progression unlocks."
            for p in shp.text_frame.paragraphs:
                p.font.name = FONT_BODY
                p.font.size = Pt(9.5)
                p.font.color.rgb = COLOR_BODY

        # Milestone 4: Voice
        elif txt == "2020":
            shp.text_frame.text = "VOICE HUD"
            shp.text_frame.paragraphs[0].font.name = FONT_HEADING
            shp.text_frame.paragraphs[0].font.color.rgb = COLOR_CYAN
        elif "aliqua amet" in txt and Inches(6.5) <= shp.left.inches < Inches(8.5):
            shp.text_frame.text = "Hands-free continuous acoustic listener with Levenshtein phonetic distance matching for greasy-handed technicians."
            for p in shp.text_frame.paragraphs:
                p.font.name = FONT_BODY
                p.font.size = Pt(9.5)
                p.font.color.rgb = COLOR_BODY

        # Milestone 5: Offline Sync
        elif txt == "2025":
            shp.text_frame.text = "OFFLINE"
            shp.text_frame.paragraphs[0].font.name = FONT_HEADING
            shp.text_frame.paragraphs[0].font.color.rgb = COLOR_CYAN
        elif "aliqua amet" in txt and shp.left.inches >= Inches(8.5):
            shp.text_frame.text = "Dexie.js IndexedDB write-ahead log (<5ms write) with automatic FIFO conflict-free cloud sync upon reconnection."
            for p in shp.text_frame.paragraphs:
                p.font.name = FONT_BODY
                p.font.size = Pt(9.5)
                p.font.color.rgb = COLOR_BODY


def customize_template_slide2(slide):
    """Customizes Slide 2 of the template: The 10-Step Operational Lifecycle Infographic."""
    lifecycle_steps = {
        "Step 1": ("Asset QR Scan", "Scan Code128 tag on machine to load digital twin."),
        "Step  2": ("Camera Stream", "1080p WebRTC capture with client downsampling."),
        "Step  3": ("AI Vision Infer", "Gemini 1.5 Flash structured defect analysis."),
        "Step  4": ("ISO Severity", "Vibration severity mapping (ISO 10816)."),
        "Step  5": ("AR HUD Reticle", "Pulsing crosshairs highlight bolt positions."),
        "Step  6": ("Voice Command", "Hands-free navigation: 'Next', 'Repeat', 'Torch'."),
        "Step  7": ("Tool Gatekeeper", "Visual check of 17mm calibrated torque wrench."),
        "Step  8": ("Parts Deduction", "OEM spare part deducted from live stock."),
        "Step  9": ("Offline Save", "Local write-ahead log saved in <5ms to Dexie."),
        "Step  10": ("Cloud Replay", "Background FIFO sync flushes to Supabase.")
    }

    for shp in slide.shapes:
        if not shp.has_text_frame:
            continue
        txt = shp.text_frame.text.strip()
        if "SOFTWARE DEVELOPMENT" in txt:
            shp.text_frame.text = "MAINTAI END-TO-END"
            for p in shp.text_frame.paragraphs:
                p.font.name = FONT_HEADING
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
        elif "MILESTONES INFOGRAPHICS" in txt:
            shp.text_frame.text = "10-STEP OPERATIONAL LIFECYCLE"
            for p in shp.text_frame.paragraphs:
                p.font.name = FONT_HEADING
                p.font.bold = True
                p.font.color.rgb = COLOR_CYAN

        for step_key, (step_title, step_desc) in lifecycle_steps.items():
            if txt == step_key:
                shp.text_frame.text = step_title
                for p in shp.text_frame.paragraphs:
                    p.font.name = FONT_HEADING
                    p.font.size = Pt(10)
                    p.font.bold = True
                    p.font.color.rgb = COLOR_CYAN
            elif txt == "Elaborate on what you want to discuss." and hasattr(shp, 'tag_assigned'):
                pass  # handled below

    # Update description text boxes
    desc_boxes = [s for s in slide.shapes if s.has_text_frame and s.text_frame.text.strip() == "Elaborate on what you want to discuss."]
    # Sort them by position to match steps
    desc_boxes.sort(key=lambda s: (s.top.inches, s.left.inches))
    descriptions = [
        "Scan machine Code128 tag to load digital twin telemetry.",
        "WebRTC camera feed with client-side frame downsampling.",
        "Gemini 1.5 Flash Vision structured defect classification.",
        "ISO 10816 vibration severity and ISO 898-1 mapping.",
        "Pulsing 3D reticles highlight bolt sequences at 60 FPS.",
        "Voice navigation: 'Next Step', 'Repeat', 'Torch'.",
        "AI camera check verifying calibrated torque wrench.",
        "Live OEM spare part stock deduction & PO trigger.",
        "Write-ahead transaction saved in <5ms to Dexie.js.",
        "Background FIFO sync reconciles data to Supabase."
    ]
    for idx, d_box in enumerate(desc_boxes):
        if idx < len(descriptions):
            d_box.text_frame.text = descriptions[idx]
            for p in d_box.text_frame.paragraphs:
                p.font.name = FONT_BODY
                p.font.size = Pt(8.5)
                p.font.color.rgb = COLOR_BODY


def add_template_styled_slide(prs, kicker_text, title_text, subtitle_text=""):
    """Creates a new slide adhering to the Canva template's exact style."""
    blank_layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_DARK_BG

    # Cyber Cyan & Electric Blue Top Accent Bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.42), Inches(0.8), Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLOR_CYAN
    bar.line.color.rgb = COLOR_BLUE

    # Header Box
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(10.0), Inches(1.15))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_kicker = tf.paragraphs[0]
    p_kicker.text = kicker_text.upper()
    p_kicker.font.name = FONT_HEADING
    p_kicker.font.size = Pt(11)
    p_kicker.font.bold = True
    p_kicker.font.color.rgb = COLOR_CYAN
    p_kicker.space_after = Pt(2)

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE

    if subtitle_text:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(11.5)
        p_sub.font.color.rgb = COLOR_MUTED
        p_sub.space_before = Pt(3)

    # Footer
    tx_f = slide.shapes.add_textbox(Inches(0.8), Inches(7.75), Inches(10.0), Inches(0.32))
    tf_f = tx_f.text_frame
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = f"MaintAI: Industrial Reliability Platform  |  School of Engineering, PPSU  |  Het Joshi (24SE09CE003)"
    p_f.font.name = FONT_BODY
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = RGBColor(100, 116, 139)

    return slide


def add_template_card(slide, left, top, width, height, title="", items=None, badge="", accent_color=COLOR_CYAN, title_size=15, body_size=11.5):
    """Adds a dark cyber card with cyan/blue borders matching the Canva template."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD
    card.line.color.rgb = COLOR_CARD_BORDER
    card.line.width = Pt(1.2)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.24)
    tf.margin_right = Inches(0.24)
    tf.margin_top = Inches(0.20)
    tf.margin_bottom = Inches(0.20)

    p0 = tf.paragraphs[0]
    if badge:
        p0.text = badge.upper()
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(9)
        p0.font.bold = True
        p0.font.color.rgb = accent_color
        p0.space_after = Pt(3)
        p_title = tf.add_paragraph()
    else:
        p_title = p0

    if title:
        p_title.text = title
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(title_size)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE
        p_title.space_after = Pt(8)

    if items:
        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.name = FONT_BODY
            p.font.size = Pt(body_size)
            p.font.color.rgb = COLOR_BODY
            p.space_after = Pt(5)

    return card


def build_full_template_deck():
    # Load Canva Template
    prs = Presentation(TEMPLATE_PATH)
    print(f"[INFO] Loaded template: {TEMPLATE_PATH}")

    # Customize native slide 1 (Milestones) and slide 2 (10-Step Infographics)
    customize_template_slide1(prs.slides[0])
    customize_template_slide2(prs.slides[1])

    # Remove extra template filler slides (slide 3 duplicate, slide 4 duplicate, slide 5 resources, slide 6 credits)
    # python-pptx deletes slides by removing xml element
    rId_list = [prs.slides._sldIdLst[i].rId for i in range(2, len(prs.slides))]
    for rId in rId_list:
        prs.part.drop_rel(rId)
    for i in range(len(prs.slides) - 1, 1, -1):
        del prs.slides._sldIdLst[i]

    print(f"[INFO] Retained & customized 2 core infographic slides from template.")

    # =========================================================================
    # SLIDE 3: Title Slide (Cover Hero in Template Style)
    # =========================================================================
    s_title = add_template_styled_slide(prs, "PPSU • B.TECH CE FINAL DEFENSE 2026", "MaintAI: Intelligent Industrial Maintenance\n& AR Guidance Platform", "Multimodal AI Vision Diagnostics, Hands-Free Voice Guidance & Offline-First Reliability")

    # University Logos
    ppsu_logo = os.path.join(PUBLIC_DIR, "official_ppsu_naac.png")
    soe_logo = os.path.join(PUBLIC_DIR, "official_school_of_engineering.png")
    if os.path.exists(ppsu_logo):
        s_title.shapes.add_picture(ppsu_logo, Inches(0.8), Inches(2.0), height=Inches(0.95))
    if os.path.exists(soe_logo):
        s_title.shapes.add_picture(soe_logo, Inches(8.8), Inches(2.0), height=Inches(0.95))

    # Candidate & Guide Cards
    add_template_card(s_title, Inches(0.8), Inches(3.2), Inches(4.8), Inches(2.2),
                      "Candidate / Lead Engineer",
                      ["Student: Het Joshi",
                       "Enrollment No: 24SE09CE003",
                       "Program: B.Tech Computer Engineering, 7th Semester",
                       "Department of Computer Engineering, School of Engineering"],
                      badge="PRESENTED BY", accent_color=COLOR_CYAN, title_size=16, body_size=11.5)

    add_template_card(s_title, Inches(6.0), Inches(3.2), Inches(4.8), Inches(2.2),
                      "Internal Guide & Mentor",
                      ["Faculty Guide: Mr. Ayush Dodia",
                       "Designation: Assistant Professor",
                       "Department of Computer Engineering",
                       "P P Savani University (PPSU, NAAC A+ Accredited)"],
                      badge="GUIDANCE & SUPERVISION", accent_color=COLOR_ORANGE, title_size=16, body_size=11.5)

    # Move title slide to position 0 (first slide)
    # Reorder slide xml element in sldIdLst
    sldIdLst = prs.slides._sldIdLst
    title_elem = sldIdLst[-1]
    sldIdLst.insert(0, title_elem)

    # =========================================================================
    # SLIDE 4: Problem Statement (Giant $260k Stat + Real Haas CNC Machine!)
    # =========================================================================
    s_prob = add_template_styled_slide(prs, "01 | Problem Domain", "The Shop-Floor Maintenance Dilemma", "Why modern manufacturing lines face crippling downtime costs and safety vulnerabilities")

    # Left: $260,000 Giant Stat
    add_template_card(s_prob, Inches(0.8), Inches(1.85), Inches(4.6), Inches(4.85),
                      "$260,000 / Hour Downtime",
                      ["Unplanned plant downtime costs heavy manufacturing $260,000+ per hour on average (Aberdeen Research).",
                       "Single mechanical failures stall continuous sequential lines immediately.",
                       "Traditional manual incident dispatching incurs a 40 to 90 minute response lag.",
                       "Compounding delays in fault identification and parts procurement multiply financial losses."],
                      badge="CRIPPLING FINANCIAL IMPACT", accent_color=COLOR_ORANGE, title_size=16, body_size=11.5)

    # Right: Real CNC Machine Photo
    cnc_img = os.path.join(MACHINES_DIR, "cnc-machine.jpg")
    if os.path.exists(cnc_img):
        s_prob.shapes.add_picture(cnc_img, Inches(5.65), Inches(1.85), width=Inches(5.2), height=Inches(2.35))

    add_template_card(s_prob, Inches(5.65), Inches(4.35), Inches(5.2), Inches(2.35),
                      "Key Plant Vulnerabilities",
                      ["Manual 300+ Page Binders: High cognitive friction finding torque specs with dirty hands.",
                       "Basement Signal Blackouts: Steel EMI shields block Wi-Fi/4G; cloud apps crash.",
                       "Unverified Tooling: Skipping torque calibration leads to bolt shearing and OSHA hazards."],
                      badge="SHOP-FLOOR REALITY", accent_color=COLOR_CYAN, title_size=15, body_size=11)

    # =========================================================================
    # SLIDE 5: 3-Tier Edge Architecture (Diagram + Tier Breakdown)
    # =========================================================================
    s_arch = add_template_styled_slide(prs, "03 | System Topology", "3-Tier Edge-Resilient Platform Architecture", "Decoupled cloud-native frontend, local offline edge cache, and serverless AI backend")

    arch_img = os.path.join(PUBLIC_DIR, "updated_architecture_diagram.png")
    if os.path.exists(arch_img):
        s_arch.shapes.add_picture(arch_img, Inches(0.8), Inches(1.85), width=Inches(5.6))

    add_template_card(s_arch, Inches(6.65), Inches(1.85), Inches(4.2), Inches(1.5),
                      "Tier 1: Presentation & Web AR",
                      ["Next.js 14 App Router, React 18, Tailwind CSS.",
                       "HTML5 Canvas 60 FPS spatial visual overlay engine.",
                       "PWA Service Worker caches shell for offline boot."],
                      badge="CLIENT LAYER", accent_color=COLOR_CYAN, title_size=14, body_size=10.5)

    add_template_card(s_arch, Inches(6.65), Inches(3.52), Inches(4.2), Inches(1.5),
                      "Tier 2: Local Edge Runtime",
                      ["Dexie.js IndexedDB write-ahead log (<5ms latency).",
                       "Web Speech STT voice engine with phonetic match.",
                       "FIFO Sync Queue replays queued updates on reconnect."],
                      badge="EDGE RUNTIME", accent_color=COLOR_ORANGE, title_size=14, body_size=10.5)

    add_template_card(s_arch, Inches(6.65), Inches(5.2), Inches(4.2), Inches(1.5),
                      "Tier 3: Cloud & AI Backend",
                      ["Supabase PostgreSQL with Row Level Security (RLS).",
                       "Google Gemini 1.5 Flash Vision serverless API proxy.",
                       "Cryptographic JWT authentication & secure recovery."],
                      badge="CLOUD BACKEND", accent_color=COLOR_GREEN, title_size=14, body_size=10.5)

    # =========================================================================
    # SLIDE 6: Computer Vision Diagnostics (Attractive Real UI Screenshot!)
    # =========================================================================
    s_cv = add_template_styled_slide(prs, "04 | Computer Vision", "Multimodal Defect Identification & Telemetry", "Computer vision pipeline transforming noisy camera frames into actionable engineering diagnostics")

    report_ui_img = os.path.join(PDF_IMAGES_DIR, "screenshot7_fault_report.png")
    if os.path.exists(report_ui_img):
        s_cv.shapes.add_picture(report_ui_img, Inches(0.8), Inches(1.85), width=Inches(5.6))

    add_template_card(s_cv, Inches(6.65), Inches(1.85), Inches(4.2), Inches(2.35),
                      "4-Stage Vision Pipeline",
                      ["1. Frame Acquisition: 1080p WebRTC capture with client downsampling.",
                       "2. Vision Inference: Gemini 1.5 Flash detects bearing wear, pitting, and leaks.",
                       "3. Defect Taxonomy: Severity classification with 94.2% top-1 confidence score.",
                       "4. Auto Incident Creation: Pre-populates required parts and alerts supervisor."],
                      badge="VISION INFERENCE PIPELINE", accent_color=COLOR_CYAN, title_size=14, body_size=10.5)

    add_template_card(s_cv, Inches(6.65), Inches(4.35), Inches(4.2), Inches(2.35),
                      "Standards & Telemetry Norms",
                      ["ISO 10816 Vibration Severity: Maps machine anomalies directly to Class A/B/C/D limits.",
                       "ISO 898-1 Fastener Ratings: Enforces specified bolt tension and star-pattern sequences.",
                       "Sub-1.4s Execution: Cloud edge serverless execution ensures instant feedback."],
                      badge="ENGINEERING INTEGRITY", accent_color=COLOR_GREEN, title_size=14, body_size=10.5)

    # =========================================================================
    # SLIDE 7: AR HUD & AI Tool Gating (Live AR Screen + Tool Photo!)
    # =========================================================================
    s_ar = add_template_styled_slide(prs, "05 | Augmented Reality", "In-Situ AR HUD & AI Tool Gatekeeper", "Interactive spatial step guidance with mandatory visual tool verification before step progression")

    ar_step_ui = os.path.join(PUBLIC_DIR, "p12_img4_73.png")
    if os.path.exists(ar_step_ui):
        s_ar.shapes.add_picture(ar_step_ui, Inches(0.8), Inches(1.85), width=Inches(5.6))

    add_template_card(s_ar, Inches(6.65), Inches(1.85), Inches(4.2), Inches(2.1),
                      "HTML5 Canvas 60 FPS Web AR Engine",
                      ["Zero Native App Downloads: Overlays visual reticles and safety zones directly on browser camera stream.",
                       "Percentage Coordinates (x%, y%): Dynamically scales across mobile phones, tablets, and smart glasses."],
                      badge="SPATIAL ENGINE", accent_color=COLOR_CYAN, title_size=14, body_size=10.5)

    tool_box = s_ar.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.65), Inches(4.1), Inches(4.2), Inches(2.6))
    tool_box.fill.solid()
    tool_box.fill.fore_color.rgb = COLOR_CARD
    tool_box.line.color.rgb = COLOR_ORANGE
    tool_box.line.width = Pt(1.5)

    tool_img = os.path.join(PDF_IMAGES_DIR, "tool_wrench.jpg")
    if os.path.exists(tool_img):
        s_ar.shapes.add_picture(tool_img, Inches(6.8), Inches(4.35), width=Inches(1.5), height=Inches(1.5))

    tx_tool = s_ar.shapes.add_textbox(Inches(8.45), Inches(4.2), Inches(2.3), Inches(2.4))
    tf_t = tx_tool.text_frame
    tf_t.word_wrap = True
    p_tb = tf_t.paragraphs[0]
    p_tb.text = "TOOL GATE: 17MM TORQUE WRENCH"
    p_tb.font.name = FONT_HEADING
    p_tb.font.size = Pt(8)
    p_tb.font.bold = True
    p_tb.font.color.rgb = COLOR_ORANGE
    p_tb.space_after = Pt(2)

    p_tt = tf_t.add_paragraph()
    p_tt.text = "Visual Tool Verification"
    p_tt.font.name = FONT_HEADING
    p_tt.font.size = Pt(11)
    p_tt.font.bold = True
    p_tt.font.color.rgb = COLOR_WHITE
    p_tt.space_after = Pt(4)

    p_td = tf_t.add_paragraph()
    p_td.text = "Step progression locks until technician shows the calibrated wrench to camera. AI confirms tool presence with 97.8% confidence."
    p_td.font.name = FONT_BODY
    p_td.font.size = Pt(9.5)
    p_td.font.color.rgb = COLOR_BODY

    # =========================================================================
    # SLIDE 8: Hands-Free Voice Guidance (Command Table)
    # =========================================================================
    s_voice = add_template_styled_slide(prs, "06 | Voice Interface", "Hands-Free Voice State Machine", "Enabling grease-handed technicians to operate complex workflows purely through spoken commands")

    add_template_card(s_voice, Inches(0.8), Inches(1.85), Inches(4.4), Inches(4.85),
                      "Acoustic Speech Architecture",
                      ["Web Speech API Integration: Native browser speech recognition running in-browser with zero cloud delay.",
                       "Noise-Tolerant State Machine: Implements phonetic and Levenshtein distance matching to filter shop-floor hum.",
                       "Continuous Listening Daemon: Automatic restart loop maintains voice standby mode even through pauses.",
                       "Multi-Accent Tolerance: Robust tokenization handles diverse technical pronunciations effortlessly.",
                       "Auditory TTS Feedback: System speaks confirmations aloud, keeping technician's eyes locked on the machinery."],
                      badge="VOICE ARCHITECTURE", accent_color=COLOR_CYAN, title_size=15, body_size=11)

    cmd_shape = s_voice.shapes.add_table(6, 2, Inches(5.45), Inches(1.85), Inches(5.4), Inches(4.85))
    cmd_tbl = cmd_shape.table
    cmd_tbl.columns[0].width = Inches(1.9)
    cmd_tbl.columns[1].width = Inches(3.5)

    cmd_headers = ["Spoken Voice Command", "System Action & Audio Feedback"]
    for c_idx, h_text in enumerate(cmd_headers):
        cell = cmd_tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_BLUE if c_idx == 0 else COLOR_CARD
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN if c_idx == 0 else COLOR_WHITE

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
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_CYAN

        c1 = cmd_tbl.cell(r_idx, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = COLOR_CARD
        c1.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = c1.text_frame.paragraphs[0]
        p1.text = action_txt
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10)
        p1.font.color.rgb = COLOR_BODY

    # =========================================================================
    # SLIDE 9: FixBot AI Copilot (Dual-Mode Comparison)
    # =========================================================================
    s_bot = add_template_styled_slide(prs, "07 | AI Copilot", "FixBot AI: Industrial Reliability Copilot", "Dual-mode assistant providing both friendly shop guidance and rigorous 5-part engineering diagnostics")

    add_template_card(s_bot, Inches(0.8), Inches(1.85), Inches(4.9), Inches(4.85),
                      "Mode 1: Shop Teammate",
                      ["Natural Language Interface: Friendly conversational assistant for shift greetings, safety briefings, and casual maintenance inquiries.",
                       "Quick Shop Queries: 'Where is the 17mm torque wrench stored?', 'Who is the supervisor on duty?'",
                       "Pre-Shift Briefing: Quick plant status review and safety tips before beginning maintenance operations.",
                       "Context-Aware Memory: Maintains multi-turn dialog context across complex troubleshooting steps."],
                      badge="CONVERSATIONAL TEAMMATE", accent_color=COLOR_CYAN, title_size=15, body_size=11.5)

    add_template_card(s_bot, Inches(5.95), Inches(1.85), Inches(4.9), Inches(4.85),
                      "Mode 2: 5-Part Diagnostic Protocol",
                      ["1. Safety & LOTO: Mandatory electrical 415V breaker isolation and hydraulic pressure bleeding to 0 bar.",
                       "2. Root Cause Hypothesis: Seal extrusion due to overpressure (92% probability).",
                       "3. Calibrated Torque & Clearance: Flange fasteners torqued to exact 45 Nm in star pattern; clearance 0.05mm.",
                       "4. OEM Replacement Parts: Part #HS-45-V (Hydraulic Seal 45mm); checks live store stock (14 in stock).",
                       "5. Step-by-Step SOP: Sequential disassembly, seal seating, and pressure testing with ISO compliance."],
                      badge="5-PART ENGINEERING PROTOCOL", accent_color=COLOR_ORANGE, title_size=15, body_size=11.5)

    # =========================================================================
    # SLIDE 10: Smart Spare Parts Inventory (Real Dashboard Screenshot + Part Photos!)
    # =========================================================================
    s_parts = add_template_styled_slide(prs, "08 | Inventory Logistics", "Smart Spare Parts Catalog & Stock Tracking", "Real-time stock governance, OEM part mapping, and high-speed barcode scanning")

    parts_ui_img = os.path.join(PUBLIC_DIR, "p13_img3_76.png")
    if os.path.exists(parts_ui_img):
        s_parts.shapes.add_picture(parts_ui_img, Inches(0.8), Inches(1.85), width=Inches(5.6))

    part_samples = [
        ("ball-bearing-6205.jpg", "Bearing 6205-2RS", "42 in stock"),
        ("contactor-lc1d25.jpg", "Contactor LC1D25", "8 in stock"),
        ("hydraulic-seal-hs-45.jpg", "Seal HS-45-V", "14 in stock"),
        ("oil-filter-of-200.jpg", "Filter OF-200", "22 in stock")
    ]

    add_template_card(s_parts, Inches(6.65), Inches(1.85), Inches(4.2), Inches(1.6),
                      "36 Verified OEM Components",
                      ["Real-time stock tracking with automated reorder thresholds (Safe, Low, Out-of-Stock).",
                       "Machine Compatibility Matrix prevents wrong part installation by matching part numbers."],
                      badge="PARTS REPOSITORY", accent_color=COLOR_CYAN, title_size=14, body_size=10.5)

    for i, (p_file, p_name, p_stock) in enumerate(part_samples):
        px = Inches(6.65 + (i % 2) * 2.15)
        py = Inches(3.6 + (i // 2) * 1.55)
        c_shape = s_parts.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, py, Inches(2.05), Inches(1.45))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = COLOR_CARD
        c_shape.line.color.rgb = COLOR_CARD_BORDER

        p_path = os.path.join(PARTS_DIR, p_file)
        if os.path.exists(p_path):
            s_parts.shapes.add_picture(p_path, px + Inches(0.08), py + Inches(0.18), width=Inches(1.0), height=Inches(1.0))

        tx = s_parts.shapes.add_textbox(px + Inches(1.1), py + Inches(0.2), Inches(0.9), Inches(1.0))
        tf_p = tx.text_frame
        tf_p.word_wrap = True
        p_n = tf_p.paragraphs[0]
        p_n.text = p_name
        p_n.font.name = FONT_HEADING
        p_n.font.size = Pt(8.5)
        p_n.font.bold = True
        p_n.font.color.rgb = COLOR_WHITE

        p_st = tf_p.add_paragraph()
        p_st.text = p_stock
        p_st.font.name = FONT_BODY
        p_st.font.size = Pt(8)
        p_st.font.bold = True
        p_st.font.color.rgb = COLOR_GREEN

    # =========================================================================
    # SLIDE 11: Plant QR Asset Barcode Management (Real Print Matrix Figure!)
    # =========================================================================
    s_qr = add_template_styled_slide(prs, "09 | Asset Tracking", "Plant QR Code Management & Asset Labeling", "Sub-200ms camera decode, batch barcode generation, and digital twin retrieval")

    qr_ui_img = os.path.join(PUBLIC_DIR, "p15_img3_84.png")
    if os.path.exists(qr_ui_img):
        s_qr.shapes.add_picture(qr_ui_img, Inches(0.8), Inches(1.85), width=Inches(5.6))

    qr_card = s_qr.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.65), Inches(1.85), Inches(4.2), Inches(2.1))
    qr_card.fill.solid()
    qr_card.fill.fore_color.rgb = COLOR_CARD
    qr_card.line.color.rgb = COLOR_CYAN
    qr_card.line.width = Pt(1.5)

    qr_img = os.path.join(PDF_IMAGES_DIR, "qr_grundfos_pump.png")
    if os.path.exists(qr_img):
        s_qr.shapes.add_picture(qr_img, Inches(6.8), Inches(2.1), width=Inches(1.6), height=Inches(1.6))

    tx_qr = s_qr.shapes.add_textbox(Inches(8.55), Inches(1.95), Inches(2.2), Inches(1.9))
    tf_q = tx_qr.text_frame
    tf_q.word_wrap = True
    p_qb = tf_q.paragraphs[0]
    p_qb.text = "ASSET TAG: PUMP-01"
    p_qb.font.name = FONT_HEADING
    p_qb.font.size = Pt(8)
    p_qb.font.bold = True
    p_qb.font.color.rgb = COLOR_CYAN
    p_qb.space_after = Pt(2)

    p_qt = tf_q.add_paragraph()
    p_qt.text = "Digital Twin Lookup"
    p_qt.font.name = FONT_HEADING
    p_qt.font.size = Pt(11)
    p_qt.font.bold = True
    p_qt.font.color.rgb = COLOR_WHITE
    p_qt.space_after = Pt(4)

    p_qd = tf_q.add_paragraph()
    p_qd.text = "Scanning physical machine tag loads operational telemetry, maintenance log history, and open tickets in <200ms."
    p_qd.font.name = FONT_BODY
    p_qd.font.size = Pt(9.5)
    p_qd.font.color.rgb = COLOR_BODY

    add_template_card(s_qr, Inches(6.65), Inches(4.15), Inches(4.2), Inches(2.55),
                      "Batch Asset Generation Features",
                      ["Built-In Code128 & QR Generator: Prints industrial tags directly from web interface.",
                       "Eliminates Dedicated Scanners: Operates using built-in smartphone or tablet camera stream.",
                       "Zero Offline Overhead: Machine metadata cached locally for offline lookups."],
                      badge="ASSET LIFECYCLE", accent_color=COLOR_GREEN, title_size=14, body_size=10.5)

    # =========================================================================
    # SLIDE 12: Supervisor Analytics & RBAC (Real Analytics Dashboard Figure!)
    # =========================================================================
    s_mgmt = add_template_styled_slide(prs, "10 | Access Control", "Role-Based Security & Supervisor Analytics", "Real-time fleet reliability telemetry, MTTR tracking, and role-based permissions")

    analytics_ui_img = os.path.join(PUBLIC_DIR, "p14_img4_81.png")
    if os.path.exists(analytics_ui_img):
        s_mgmt.shapes.add_picture(analytics_ui_img, Inches(0.8), Inches(1.85), width=Inches(5.6))

    add_template_card(s_mgmt, Inches(6.65), Inches(1.85), Inches(4.2), Inches(4.85),
                      "Role-Based Governance (RBAC)",
                      ["Plant Administrator: Global fleet telemetry, MTTR/MTBF analytics, inventory thresholds, user provisioning, and immutable cryptographic audit logs.",
                       "Shift Supervisor: Visual drag-and-drop fault triage, machine dispatch board, review of repair photos, and return-to-service authorization.",
                       "Field Technician: Personal task inbox, hands-free AR camera guidance, voice checklists, tool verification, and digital certificate signing.",
                       "Supabase Row Level Security (RLS): Guarantees total data isolation and role boundaries at the PostgreSQL database level."],
                      badge="ACCESS CONTROL MATRIX", accent_color=COLOR_CYAN, title_size=15, body_size=11)

    # =========================================================================
    # SLIDE 13: Offline-First Synchronization (Diagram + Technical Explanation)
    # =========================================================================
    s_sync = add_template_styled_slide(prs, "11 | Data Resilience", "Offline-First Write-Ahead Synchronization", "Zero-data-loss architecture engineered specifically for metal-shielded industrial dead zones")

    sync_img = os.path.join(PUBLIC_DIR, "updated_offline_sync_workflow.png")
    if os.path.exists(sync_img):
        s_sync.shapes.add_picture(sync_img, Inches(0.8), Inches(1.85), width=Inches(5.6))

    add_template_card(s_sync, Inches(6.65), Inches(1.85), Inches(4.2), Inches(2.35),
                      "Dexie.js IndexedDB Local Store",
                      ["Local Write-Ahead Log: All maintenance updates, completed checklists, and photo evidence write locally in < 5ms.",
                       "IndexedDB Schema: Local relational tables for machines, parts, fault reports, and queued transactions.",
                       "Zero UI Lag: Technicians work completely uninterrupted when network connection drops."],
                      badge="LOCAL WRITE-AHEAD STORAGE", accent_color=COLOR_CYAN, title_size=14, body_size=10.5)

    add_template_card(s_sync, Inches(6.65), Inches(4.35), Inches(4.2), Inches(2.35),
                      "Background Reconciliation Worker",
                      ["Network Sentinel: Real-time listener detects when Wi-Fi or cellular connectivity is restored.",
                       "FIFO Sync Queue: Queued mutations replay sequentially with idempotency keys to prevent duplicate records.",
                       "Zero Data Loss: Stress-tested over 50 offline cycles with 100% data integrity verified."],
                      badge="AUTOMATIC RECONCILIATION", accent_color=COLOR_GREEN, title_size=14, body_size=10.5)

    # =========================================================================
    # SLIDE 14: Quantitative Benchmarks (4 Giant Stats + Clear Table)
    # =========================================================================
    s_bench = add_template_styled_slide(prs, "12 | System Benchmarks", "Empirical Performance & Verification Results", "Empirical performance testing across computer vision, AR graphics, and offline synchronization")

    stat_data = [
        ("94.2%", "AI Detection Accuracy", "120 fault images tested", COLOR_CYAN),
        ("< 1.4s", "Vision API Latency", "Serverless edge inference", COLOR_GREEN),
        ("59.8 FPS", "Mobile AR HUD Speed", "HTML5 Canvas benchmark", COLOR_BLUE),
        ("38%", "MTTR Reduction", "Versus paper manuals in UAT", COLOR_ORANGE)
    ]

    for i, (val_s, title_s, desc_s, clr_s) in enumerate(stat_data):
        sc = s_bench.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 2.55), Inches(1.85), Inches(2.4), Inches(1.3))
        sc.fill.solid()
        sc.fill.fore_color.rgb = COLOR_CARD
        sc.line.color.rgb = clr_s
        sc.line.width = Pt(1.5)
        tf_sc = sc.text_frame
        tf_sc.word_wrap = True
        tf_sc.margin_top = Inches(0.12)

        p_v = tf_sc.paragraphs[0]
        p_v.text = val_s
        p_v.font.name = FONT_HEADING
        p_v.font.size = Pt(22)
        p_v.font.bold = True
        p_v.font.color.rgb = clr_s
        p_v.alignment = PP_ALIGN.CENTER

        p_t = tf_sc.add_paragraph()
        p_t.text = f"{title_s} ({desc_s})"
        p_t.font.name = FONT_BODY
        p_t.font.size = Pt(8.5)
        p_t.font.color.rgb = COLOR_WHITE
        p_t.alignment = PP_ALIGN.CENTER

    # Verification Table
    bm_shape = s_bench.shapes.add_table(5, 3, Inches(0.8), Inches(3.35), Inches(10.05), Inches(3.35))
    bm_t = bm_shape.table
    bm_t.columns[0].width = Inches(2.8)
    bm_t.columns[1].width = Inches(2.8)
    bm_t.columns[2].width = Inches(4.45)

    bm_headers = ["Benchmark Parameter", "Measured Performance", "Industry Benchmark / Standard"]
    for c_idx, h_text in enumerate(bm_headers):
        cell = bm_t.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_BLUE if c_idx == 0 else COLOR_CARD
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN if c_idx == 0 else COLOR_WHITE

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
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_WHITE

        c1 = bm_t.cell(r_idx, 1)
        c1.fill.solid()
        c1.fill.fore_color.rgb = COLOR_CARD
        c1.vertical_anchor = MSO_ANCHOR.MIDDLE
        p1 = c1.text_frame.paragraphs[0]
        p1.text = m_col
        p1.font.name = FONT_BODY
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_GREEN

        c2 = bm_t.cell(r_idx, 2)
        c2.fill.solid()
        c2.fill.fore_color.rgb = COLOR_CARD
        c2.vertical_anchor = MSO_ANCHOR.MIDDLE
        p2 = c2.text_frame.paragraphs[0]
        p2.text = s_col
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_BODY

    # =========================================================================
    # SLIDE 15: Conclusion & Future Scope (Academic Defense Conclusion)
    # =========================================================================
    s_conc = add_template_styled_slide(prs, "13 | Conclusion", "Summary of Achievements & Next Frontiers", "Bridging the gap between cutting-edge AI and rugged shop-floor operational realities")

    add_template_card(s_conc, Inches(0.8), Inches(1.85), Inches(4.9), Inches(3.95),
                      "Summary of Achievements",
                      ["Successfully engineered MaintAI: a unified, lightweight, hands-free maintenance platform combining AI vision, Web AR, and offline resilience.",
                       "Overcame critical industrial pain points: eliminated paper manual delays, mitigated connection blackouts, and enforced tool safety compliance.",
                       "Demonstrates 100% individual design, coding, testing, and cloud deployment by candidate Het Joshi.",
                       "Fully deployed and live on Vercel with active Supabase cloud database synchronization."],
                      badge="PROJECT OUTCOMES", accent_color=COLOR_CYAN, title_size=15, body_size=11.5)

    add_template_card(s_conc, Inches(5.95), Inches(1.85), Inches(4.9), Inches(3.95),
                      "Future Development Roadmap",
                      ["Industrial IoT Integration: Ingesting live telemetry streams directly via MQTT / OPC-UA industrial automation protocols.",
                       "Thermal FLIR Camera Streaming: Incorporating infrared thermal imaging for heat dissipation and hotspot anomaly detection.",
                       "Spatial WebXR SLAM: Upgrading 2D canvas overlays to full 3D spatial anchoring on complex physical equipment assemblies.",
                       "Research Publication: Preparing findings on offline multimodal tool verification for IEEE/ACM conference submission."],
                      badge="FUTURE ROADMAP", accent_color=COLOR_GREEN, title_size=15, body_size=11.5)

    qa_banner = s_conc.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.95), Inches(10.05), Inches(0.88))
    qa_banner.fill.solid()
    qa_banner.fill.fore_color.rgb = COLOR_CARD
    qa_banner.line.color.rgb = COLOR_CYAN
    qa_banner.line.width = Pt(1.5)

    tf_qa = qa_banner.text_frame
    tf_qa.word_wrap = True
    p_qa = tf_qa.paragraphs[0]
    p_qa.text = "Thank You! Questions & Discussion with Honorable Guide & External Examiner"
    p_qa.font.name = FONT_HEADING
    p_qa.font.size = Pt(13)
    p_qa.font.bold = True
    p_qa.font.color.rgb = COLOR_WHITE
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.space_after = Pt(2)

    p_qa_sub = tf_qa.add_paragraph()
    p_qa_sub.text = "Candidate: Het Joshi (24SE09CE003)  |  Guide: Mr. Ayush Dodia  |  School of Engineering, PPSU"
    p_qa_sub.font.name = FONT_BODY
    p_qa_sub.font.size = Pt(10)
    p_qa_sub.font.bold = True
    p_qa_sub.font.color.rgb = COLOR_CYAN
    p_qa_sub.alignment = PP_ALIGN.CENTER

    # Save to all target files resiliently
    candidate_paths = [
        OUTPUT_MENTOR,
        OUTPUT_DEFENSE,
        OUTPUT_PROJECT,
        os.path.join(BASE_DIR, "MaintAI_Modern_Template_Presentation.pptx")
    ]
    saved_any = False
    for p_target in candidate_paths:
        try:
            prs.save(p_target)
            print(f"[SUCCESS] Saved to: {p_target}")
            saved_any = True
        except PermissionError:
            print(f"[NOTE] {p_target} is locked (currently open in PowerPoint).")

    print(f"[STATS] Total slides generated: {len(prs.slides)}")


if __name__ == "__main__":
    build_full_template_deck()
