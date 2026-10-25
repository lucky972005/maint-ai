#!/usr/bin/env python3
"""
MaintAI - Cyberpunk AR/AI Pitch Deck Presentation Generator
Faithfully replicates the exact design, layout, color palette, typography, and visual assets of the
uploaded 19-page pitch deck template:
- Holographic AR/VR cyberpunk aesthetic (Cyan #00F0FF, Magenta #C026D3, Coral #FF4B4B, Solid Cyan #00C2CB)
- True hollow/outlined titles using OpenXML DrawingML outline + transparency
- Extracted original high-resolution background gradients and photography
- Tracked uppercase typography (Century Gothic / Segoe UI)
- All 19 signature slides:
  1. Pitch Deck Cover (Smart AR visor + outlined title + academic credentials)
  2. About Us (Solid Cyan card + neon VR headset photo)
  3. Problem (Holographic iris HUD + 5-point grid)
  4. Solution (Outlined vertical title + 2x2 grid)
  5. Product Overview (4 hollow cyan pillar cards)
  6. Product Benefits (Light ice gray card + VR user)
  7. System Architecture (Creation of Adam cybernetic hands transition)
  8. Edge Runtime (Solid Cyan card + engineer with holographic data)
  9. Key Benchmarks (Giant glowing cyan metrics $260K, 94.2%, 38%)
  10. Industrial Standards (3 hollow cyan square frames)
  11. Platform Comparison (Vertical hands + 2-column comparison)
  12. Competition 2x2 Matrix (Convenient/Affordable quadrant graph with MaintAI badge)
  13. Growth Strategy (3 hollow cyan timeline boxes)
  14. Two-Year Action Plan (Two parallel horizontal milestone tracks)
  15. Financials & ROI (Glowing cyan data table + iris HUD)
  16. Meet The Team (Light glass card + 4 framed portraits)
  17. The Full Stack (8 architectural technology pillars)
  18. Executive Summary (Solid Coral/Red card + holographic engineer)
  19. Thank You (Neon VR user + candidate/guide contact info & Q&A)

Candidate: Het Joshi (Enrollment No. 24SE09CE003)
Internal Guide: Mr. Ayush Dodia (Assistant Professor)
Institute: Department of Computer Engineering, School of Engineering, P P Savani University
"""

import os
import sys
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")
ASSETS_DIR = os.path.join(BASE_DIR, "cyber_template_assets")

OUTPUT_CYBER = os.path.join(BASE_DIR, "MaintAI_Cyber_Pitch_Deck.pptx")
OUTPUT_MENTOR = os.path.join(BASE_DIR, "MaintAI_Mentor_Presentation.pptx")
OUTPUT_DEFENSE = os.path.join(BASE_DIR, "MaintAI_Defense_Presentation.pptx")
OUTPUT_PROJECT = os.path.join(BASE_DIR, "MaintAI_Project_Presentation.pptx")

# Palette
COLOR_BLACK = RGBColor(7, 7, 9)             # #070709 Midnight Black
COLOR_CYAN_OUTLINE = "00F0FF"               # Glowing Cyan outline hex
COLOR_WHITE_OUTLINE = "FFFFFF"              # White outline hex
COLOR_NAVY_OUTLINE = "0B1B38"               # Navy outline hex
COLOR_CYAN_SOLID = RGBColor(0, 194, 203)    # #00C2CB Solid Cyan Card
COLOR_CORAL_SOLID = RGBColor(255, 75, 75)   # #FF4B4B Solid Coral Card
COLOR_ICE_CARD = RGBColor(226, 232, 240)    # #E2E8F0 Light Ice Gray Card
COLOR_TEXT_CYAN = RGBColor(0, 240, 255)     # #00F0FF
COLOR_TEXT_WHITE = RGBColor(255, 255, 255)  # Pure White
COLOR_TEXT_ICE = RGBColor(226, 232, 240)    # Ice White
COLOR_TEXT_NAVY = RGBColor(11, 27, 56)      # Deep Navy for Cyan/Ice Cards
COLOR_TEXT_MUTED = RGBColor(148, 163, 184)  # Slate for subtext

FONT_TITLE = "Century Gothic"
FONT_BODY = "Segoe UI"


def create_blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def set_slide_background(slide, bg_path):
    """Sets slide background image filling 13.333 x 7.5 inches."""
    if bg_path and os.path.exists(bg_path):
        slide.shapes.add_picture(bg_path, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))
    else:
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BLACK
        bg.line.fill.background()


def add_footer(slide, slide_num, label="PITCH DECK"):
    """Adds small tracked footer 'PITCH DECK' and slide number."""
    txBox = slide.shapes.add_textbox(Inches(0), Inches(7.05), Inches(13.333), Inches(0.4))
    tf = txBox.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.5)
    tf.margin_right = Inches(0.5)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)

    p = tf.paragraphs[0]
    p.text = f"{' '.join(label.upper())}"
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_TEXT_MUTED
    p.alignment = PP_ALIGN.CENTER

    if slide_num:
        tx_num = slide.shapes.add_textbox(Inches(12.2), Inches(7.05), Inches(0.8), Inches(0.4))
        tf_num = tx_num.text_frame
        tf_num.margin_right = Inches(0.4)
        p_num = tf_num.paragraphs[0]
        p_num.text = str(slide_num)
        p_num.font.name = FONT_BODY
        p_num.font.size = Pt(8.5)
        p_num.font.color.rgb = COLOR_TEXT_MUTED
        p_num.alignment = PP_ALIGN.RIGHT


def add_outlined_title(slide, left, top, width, height, text, size_pt=46, outline_hex="00F0FF", line_width=28000, align=PP_ALIGN.LEFT):
    """
    Creates the signature hollow outlined typography from the pitch deck.
    Uses OpenXML DrawingML line outline + transparent scheme fill.
    """
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.alignment = align

    # Spaced uppercase letters for tracking
    spaced_text = " ".join(text.strip().upper())
    run = p.add_run()
    run.text = spaced_text
    run.font.name = FONT_TITLE
    run.font.size = Pt(size_pt)
    run.font.bold = True

    # OpenXML outline formatting
    rPr = run._r.get_or_add_rPr()
    outline_xml = parse_xml(
        f'<a:ln xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="{line_width}">'
        f'<a:solidFill><a:srgbClr val="{outline_hex}"/></a:solidFill>'
        f'</a:ln>'
    )
    rPr.append(outline_xml)

    nofill_xml = parse_xml(
        '<a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:schemeClr val="tx1"><a:alpha val="0"/></a:schemeClr>'
        '</a:solidFill>'
    )
    rPr.append(nofill_xml)

    return txBox


# =============================================================================
# SLIDE BUILDERS (19 SLIDES)
# =============================================================================

def build_slide_1_cover(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p1_img0_7.jpeg"))

    # Hero Image: Person wearing smart AR glasses visor (left side 0 to 8.2 inches)
    hero_img = os.path.join(ASSETS_DIR, "p1_img1_9.jpeg")
    if os.path.exists(hero_img):
        slide.shapes.add_picture(hero_img, Inches(0.8), Inches(0.9), width=Inches(7.5), height=Inches(5.7))

    # Right dark panel
    panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.9), Inches(1.8), Inches(6.433), Inches(2.8))
    panel.fill.solid()
    panel.fill.fore_color.rgb = RGBColor(14, 27, 56) # Deep Navy translucent
    panel.line.fill.background()

    # Outlined title
    add_outlined_title(slide, Inches(7.5), Inches(2.2), Inches(5.6), Inches(1.1), "PITCH DECK", size_pt=52, outline_hex="00F0FF", line_width=32000)

    # Subtitle / Author details
    tx = slide.shapes.add_textbox(Inches(7.5), Inches(3.45), Inches(5.6), Inches(1.8))
    tf = tx.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Het Joshi  •  Enrollment: 24SE09CE003"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(13)
    p1.font.color.rgb = COLOR_TEXT_CYAN
    p1.space_after = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = "Guide: Mr. Ayush Dodia (Assistant Professor)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_TEXT_ICE
    p2.space_after = Pt(4)

    p3 = tf.add_paragraph()
    p3.text = "Department of Computer Engineering, School of Engineering\nP P Savani University (PPSU, NAAC A+)"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10)
    p3.font.color.rgb = COLOR_TEXT_MUTED

    # Official PPSU Logo
    logo = os.path.join(PUBLIC_DIR, "official_ppsu_naac.png")
    if os.path.exists(logo):
        slide.shapes.add_picture(logo, Inches(11.5), Inches(0.4), height=Inches(0.75))

    return slide


def build_slide_2_about_us(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p2_img0_20.jpeg"))

    # Left Solid Cyan Card
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.9), Inches(6.6), Inches(3.9))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CYAN_SOLID
    card.line.fill.background()

    # Outlined title on Cyan
    add_outlined_title(slide, Inches(0.7), Inches(2.4), Inches(5.2), Inches(0.9), "ABOUT US", size_pt=38, outline_hex="071B38", line_width=25000)

    # Body text
    tx = slide.shapes.add_textbox(Inches(0.7), Inches(3.5), Inches(5.2), Inches(2.1))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = (
        "At MaintAI, we empower industrial manufacturing plants to foster intelligent maintenance "
        "and drive shop-floor reliability. By closing the loop on real-time computer vision defect diagnostics, "
        "lightweight Web AR in-situ guidance, and offline write-ahead synchronization, we help frontline teams "
        "eliminate unplanned machine downtime and guarantee OSHA audit compliance."
    )
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = COLOR_TEXT_NAVY
    p.line_spacing = 1.35

    # Right Hero Image: Person with VR headset
    right_img = os.path.join(ASSETS_DIR, "p2_img1_22.jpeg")
    if os.path.exists(right_img):
        slide.shapes.add_picture(right_img, Inches(7.1), Inches(0.6), height=Inches(6.4))

    add_footer(slide, 2)
    return slide


def build_slide_3_problem(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p3_img0_27.jpeg"))

    # Left Iris / Biometric HUD circle
    iris_img = os.path.join(ASSETS_DIR, "p3_img1_29.jpeg")
    if os.path.exists(iris_img):
        slide.shapes.add_picture(iris_img, Inches(0), Inches(0.8), width=Inches(3.9), height=Inches(5.9))

    # Right Outlined Title
    add_outlined_title(slide, Inches(4.5), Inches(1.4), Inches(8.0), Inches(0.9), "PROBLEM", size_pt=42, outline_hex="00F0FF")

    # 3-Column / 2-Row Problem Matrix
    problems = [
        ("MARKET GAP", "Heavy manufacturing loses an average of $260,000+ per hour during unplanned mechanical breakdowns."),
        ("CUSTOMERS", "Technicians struggle navigating 300+ page paper binders with oily, grease-covered hands."),
        ("FINANCIALS", "Manual dispatching incurs 40 to 90 min lag before specialist maintenance personnel arrive on site."),
        ("COSTS", "Skipping torque wrench calibration leads to bolt shearing and catastrophic OSHA safety hazards."),
        ("USABILITY", "Plant basements and steel EMI shields block Wi-Fi; standard cloud maintenance software crashes completely.")
    ]

    col_w = Inches(2.7)
    row_h = Inches(2.0)
    start_x = Inches(4.5)
    start_y = Inches(2.6)

    for idx, (head, body) in enumerate(problems):
        r = idx // 3
        c = idx % 3
        x = start_x + c * (col_w + Inches(0.25))
        y = start_y + r * row_h

        tx = slide.shapes.add_textbox(x, y, col_w, row_h)
        tf = tx.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = " ".join(head.upper())
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_CYAN
        p1.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.line_spacing = 1.25

    add_footer(slide, 3)
    return slide


def build_slide_4_solution(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p4_img0_37.jpeg"))

    # Left Outlined Title
    add_outlined_title(slide, Inches(1.4), Inches(3.2), Inches(4.0), Inches(1.2), "SOLUTION", size_pt=46, outline_hex="00F0FF")

    # Right 2x2 Grid
    solutions = [
        ("CLOSE THE GAP", "In-situ HTML5 Canvas Web AR HUD overlays live spatial visual inspection markers and tool reticles directly onto camera feed at 59.8 FPS."),
        ("TARGET AUDIENCE", "Frontline maintenance technicians, shop-floor supervisors, and plant reliability engineering teams across heavy industry."),
        ("COST SAVINGS", "38% reduction in Mean Time to Repair (MTTR) demonstrated during shop-floor validation tests; zero data loss guaranteed."),
        ("EASY TO USE", "Continuous hands-free voice state machine with Levenshtein phonetic matching; zero native app installation friction (PWA).")
    ]

    col_w = Inches(3.4)
    start_x = Inches(5.8)

    # Row 1
    for c, (head, body) in enumerate(solutions[:2]):
        x = start_x + c * (col_w + Inches(0.4))
        tx = slide.shapes.add_textbox(x, Inches(1.8), col_w, Inches(2.2))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = " ".join(head.upper())
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_CYAN
        p1.space_after = Pt(8)
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.line_spacing = 1.25

    # Row 2
    for c, (head, body) in enumerate(solutions[2:]):
        x = start_x + c * (col_w + Inches(0.4))
        tx = slide.shapes.add_textbox(x, Inches(4.2), col_w, Inches(2.2))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = " ".join(head.upper())
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_CYAN
        p1.space_after = Pt(8)
        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.line_spacing = 1.25

    add_footer(slide, 4)
    return slide


def build_slide_5_product_overview(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p5_img0_40.jpeg"))

    # Centered Outlined Title
    add_outlined_title(slide, Inches(1.5), Inches(1.5), Inches(10.333), Inches(0.9), "PRODUCT OVERVIEW", size_pt=42, outline_hex="00F0FF", align=PP_ALIGN.CENTER)

    pillars = [
        ("UNIQUE", "Multimodal Google Gemini 1.5 Flash Vision serverless proxy classifies bearing, gear, and fluid defects in <1.4s."),
        ("FIRST TO MARKET", "In-situ Web AR running in-browser on standard HTML5 canvas without requiring ARCore or native app store downloads."),
        ("TESTED", "Empirically validated across 50 offline disconnect/reconnect cycles with 500+ mutations passed with 0 dropped packets."),
        ("AUTHENTIC", "Engineered with Next.js 14 App Router, Dexie.js IndexedDB write-ahead log, and Supabase Row Level Security.")
    ]

    col_w = Inches(2.6)
    start_x = Inches(1.0)
    gap = Inches(0.4)

    for idx, (title, desc) in enumerate(pillars):
        x = start_x + idx * (col_w + gap)

        # Hollow Cyan Icon Frame (Square outline)
        icon_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.9), Inches(3.0), Inches(0.8), Inches(0.8))
        icon_box.fill.background()
        icon_box.line.color.rgb = COLOR_TEXT_CYAN
        icon_box.line.width = Pt(1.5)

        tx = slide.shapes.add_textbox(x, Inches(4.1), col_w, Inches(2.2))
        tf = tx.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = " ".join(title.upper())
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_CYAN
        p1.alignment = PP_ALIGN.CENTER
        p1.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.alignment = PP_ALIGN.CENTER
        p2.line_spacing = 1.25

    add_footer(slide, 5)
    return slide


def build_slide_6_product_benefits(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p6_img0_48.jpeg"))

    # Left Hero: Woman wearing VR headset
    vr_img = os.path.join(ASSETS_DIR, "p6_img1_50.jpeg")
    if os.path.exists(vr_img):
        slide.shapes.add_picture(vr_img, Inches(0.7), Inches(0.8), width=Inches(6.8), height=Inches(5.9))

    # Right Light Ice Card
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.2), Inches(1.9), Inches(6.133), Inches(3.6))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_ICE_CARD
    card.line.fill.background()

    # Outlined Title on Ice Card
    add_outlined_title(slide, Inches(7.6), Inches(2.3), Inches(5.3), Inches(0.9), "PRODUCT BENEFITS", size_pt=34, outline_hex="071B38", line_width=24000)

    # Bullet points
    benefits = [
        "Simple, hands-free voice-directed maintenance workflows",
        "AI Tool Gatekeeper enforces mandatory torque wrench checks",
        "Continuous offline operation in zero-connectivity plant basements",
        "Cryptographically verifiable digital return-to-service certificates"
    ]

    tx = slide.shapes.add_textbox(Inches(7.6), Inches(3.4), Inches(5.3), Inches(1.9))
    tf = tx.text_frame
    tf.word_wrap = True

    for idx, b in enumerate(benefits):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"•  {b}"
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_NAVY
        p.line_spacing = 1.25
        p.space_after = Pt(6)

    add_footer(slide, 6)
    return slide


def build_slide_7_architecture_hands(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, None) # Pure Black

    # Centered Outlined Title
    add_outlined_title(slide, Inches(1.5), Inches(1.2), Inches(10.333), Inches(1.0), "SYSTEM ARCHITECTURE", size_pt=42, outline_hex="00F0FF", align=PP_ALIGN.CENTER)

    # Center Hero: Cybernetic robot hand touching human hand (p7_img0_54.jpeg)
    hands_img = os.path.join(ASSETS_DIR, "p7_img0_54.jpeg")
    if os.path.exists(hands_img):
        slide.shapes.add_picture(hands_img, Inches(0.5), Inches(2.2), width=Inches(12.333), height=Inches(4.4))

    # Subtitle
    tx = slide.shapes.add_textbox(Inches(2.0), Inches(6.4), Inches(9.333), Inches(0.5))
    tf = tx.text_frame
    p = tf.paragraphs[0]
    p.text = "Edge-Native Progressive Web Architecture with Multimodal Cloud AI Synergy"
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_TEXT_ICE
    p.alignment = PP_ALIGN.CENTER

    add_footer(slide, 7)
    return slide


def build_slide_8_edge_runtime(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p8_img0_57.jpeg"))

    # Left Solid Cyan Card
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.4), Inches(5.6), Inches(5.0))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CYAN_SOLID
    card.line.fill.background()

    # Outlined Title on Cyan Card
    add_outlined_title(slide, Inches(0.7), Inches(1.8), Inches(4.5), Inches(0.8), "EDGE RUNTIME", size_pt=34, outline_hex="071B38", line_width=24000)

    pillars = [
        ("PRESENTATION TIER", "Next.js 14 App Router, React 18, and Tailwind CSS system with 60 FPS HTML5 Canvas engine."),
        ("LOCAL CACHE STORE", "Dexie.js IndexedDB write-ahead log ensures <5ms task save latency during complete offline blackouts."),
        ("VOICE STT / TTS", "Browser-native Web Speech API with Levenshtein phonetic matching running with zero cloud round-trip delay.")
    ]

    tx = slide.shapes.add_textbox(Inches(0.7), Inches(2.7), Inches(4.5), Inches(3.4))
    tf = tx.text_frame
    tf.word_wrap = True

    for idx, (title, desc) in enumerate(pillars):
        p1 = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p1.text = " ".join(title.upper())
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_NAVY
        p1.space_after = Pt(3)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_NAVY
        p2.line_spacing = 1.2
        p2.space_after = Pt(10)

    # Right Hero Image: Engineer with holographic bokeh
    right_img = os.path.join(ASSETS_DIR, "p8_img1_59.jpeg")
    if os.path.exists(right_img):
        slide.shapes.add_picture(right_img, Inches(5.6), Inches(0.8), width=Inches(7.733), height=Inches(5.8))

    add_footer(slide, 8)
    return slide


def build_slide_9_key_benchmarks(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p9_img0_62.jpeg"))

    # Centered Outlined Title
    add_outlined_title(slide, Inches(1.5), Inches(1.3), Inches(10.333), Inches(0.9), "KEY BENCHMARKS", size_pt=42, outline_hex="00F0FF", align=PP_ALIGN.CENTER)

    metrics = [
        ("$260K", ["Manufacturing downtime cost/hr", "Zero data loss in 50 offline tests", "100% digital audit compliance"]),
        ("94.2%", ["Top-1 AI vision detection accuracy", "<1.4s serverless inference latency", "ISO 10816 vibration classification"]),
        ("38%", ["Demonstrated MTTR reduction", "59.8 FPS mobile Web AR rendering", "Sub-200ms camera barcode decode"])
    ]

    col_w = Inches(3.2)
    start_x = Inches(1.5)
    gap = Inches(0.8)

    for idx, (big_num, bullets) in enumerate(metrics):
        x = start_x + idx * (col_w + gap)

        # Big Cyan Metric
        tx_num = slide.shapes.add_textbox(x, Inches(2.6), col_w, Inches(1.1))
        tf_num = tx_num.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.text = big_num
        p_num.font.name = FONT_TITLE
        p_num.font.size = Pt(54)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_TEXT_CYAN
        p_num.alignment = PP_ALIGN.CENTER

        # Cyan Divider Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x + Inches(0.3), Inches(3.85), col_w - Inches(0.6), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_TEXT_CYAN
        line.line.fill.background()

        # Bullets
        tx_b = slide.shapes.add_textbox(x, Inches(4.1), col_w, Inches(1.8))
        tf_b = tx_b.text_frame
        tf_b.word_wrap = True

        for b_idx, bullet in enumerate(bullets):
            p = tf_b.paragraphs[0] if b_idx == 0 else tf_b.add_paragraph()
            p.text = bullet
            p.font.name = FONT_BODY
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_TEXT_WHITE
            p.alignment = PP_ALIGN.CENTER
            p.line_spacing = 1.2
            p.space_after = Pt(4)

    add_footer(slide, 9)
    return slide


def build_slide_10_industrial_standards(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p10_img0_66.jpeg"))

    # Left Hero: VR Headset
    left_img = os.path.join(ASSETS_DIR, "p10_img1_68.jpeg")
    if os.path.exists(left_img):
        slide.shapes.add_picture(left_img, Inches(0.5), Inches(0.6), width=Inches(5.2), height=Inches(6.4))

    # Right Outlined Title
    add_outlined_title(slide, Inches(6.0), Inches(1.3), Inches(7.0), Inches(0.9), "STANDARDS & NORMS", size_pt=38, outline_hex="00F0FF")

    standards = [
        ("ISO 10816 VIBRATION NORMS", "Mechanical vibration severity grading (Class I to IV zones) to predict bearing degradation before catastrophic breakdown."),
        ("ISO 898-1 FASTENER RATINGS", "Automated bolt property and calibrated torque lookup preventing bolt shearing and vibration-induced loosening."),
        ("OSHA 1910.147 LOTO GATES", "Mandatory Lockout/Tagout visual gate requiring physical zero-energy verification before AR repair steps unlock.")
    ]

    start_y = Inches(2.5)
    row_h = Inches(1.4)

    for idx, (title, desc) in enumerate(standards):
        y = start_y + idx * row_h

        # Hollow Cyan Square Frame
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.0), y + Inches(0.1), Inches(0.9), Inches(0.9))
        box.fill.background()
        box.line.color.rgb = RGBColor(255, 75, 75) if idx == 0 else COLOR_TEXT_CYAN
        box.line.width = Pt(2.0)

        tx = slide.shapes.add_textbox(Inches(7.2), y, Inches(5.6), Inches(1.2))
        tf = tx.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_CYAN
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.line_spacing = 1.2

    add_footer(slide, 10)
    return slide


def build_slide_11_competition_columns(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, None) # Pure Black

    # Left Vertical Hands Hero Image
    left_img = os.path.join(ASSETS_DIR, "p11_img0_71.jpeg")
    if os.path.exists(left_img):
        slide.shapes.add_picture(left_img, Inches(0.4), Inches(0.5), width=Inches(2.5), height=Inches(6.5))

    # Center/Right Outlined Title
    add_outlined_title(slide, Inches(3.2), Inches(1.3), Inches(9.5), Inches(0.9), "OUR COMPETITION", size_pt=42, outline_hex="00F0FF")

    # Column 1: MaintAI Platform
    tx1 = slide.shapes.add_textbox(Inches(3.2), Inches(2.6), Inches(4.5), Inches(3.8))
    tf1 = tx1.text_frame
    tf1.word_wrap = True

    p1_h = tf1.paragraphs[0]
    p1_h.text = "MAINTAI PLATFORM"
    p1_h.font.name = FONT_TITLE
    p1_h.font.size = Pt(14)
    p1_h.font.bold = True
    p1_h.font.color.rgb = COLOR_TEXT_CYAN
    p1_h.space_after = Pt(12)

    maint_points = [
        "Edge-native PWA: Zero app store downloads or proprietary scanner hardware needed.",
        "In-situ HTML5 Web AR: 60 FPS spatial visual overlays on standard mobile browser.",
        "Hands-free Voice Machine: Noise-tolerant Levenshtein distance phonetic matching.",
        "Dexie.js Offline Sync: 100% data preservation during basement network blackouts."
    ]
    for pt in maint_points:
        p = tf1.add_paragraph()
        p.text = pt
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_WHITE
        p.line_spacing = 1.2
        p.space_after = Pt(8)

    # Column 2: Legacy Competitors
    tx2 = slide.shapes.add_textbox(Inches(8.2), Inches(2.6), Inches(4.5), Inches(3.8))
    tf2 = tx2.text_frame
    tf2.word_wrap = True

    p2_h = tf2.paragraphs[0]
    p2_h.text = "LEGACY COMPETITORS"
    p2_h.font.name = FONT_TITLE
    p2_h.font.size = Pt(14)
    p2_h.font.bold = True
    p2_h.font.color.rgb = COLOR_TEXT_CYAN
    p2_h.space_after = Pt(12)

    comp_points = [
        "Legacy CMMS Tools (Maximo, SAP): Extremely expensive, complex, slow training curve.",
        "Static PDF Readers: Technicians must pinch-to-zoom dirty screens while repairing.",
        "Cloud-Only Web Portals: Crash immediately when technician enters basement rooms.",
        "Paper Manual Binders: Prone to grease damage, zero cryptographic audit logging."
    ]
    for pt in comp_points:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_WHITE
        p.line_spacing = 1.2
        p.space_after = Pt(8)

    add_footer(slide, 11)
    return slide


def build_slide_12_competition_matrix(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p12_img0_74.jpeg"))

    # Outlined Title Top Left
    add_outlined_title(slide, Inches(1.0), Inches(0.9), Inches(5.0), Inches(0.9), "COMPETITION", size_pt=38, outline_hex="00F0FF")

    # Center Coordinate Crosshair (Axes)
    cx = Inches(6.666)
    cy = Inches(4.1)
    axis_len = Inches(4.8)

    # Horizontal Axis (Expensive -> Affordable)
    h_axis = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx - axis_len / 2, cy, axis_len, Inches(0.02))
    h_axis.fill.solid()
    h_axis.fill.fore_color.rgb = COLOR_TEXT_CYAN
    h_axis.line.fill.background()

    # Vertical Axis (Convenient -> Inconvenient)
    v_axis = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, cy - axis_len / 2 + Inches(0.3), Inches(0.02), axis_len - Inches(0.6))
    v_axis.fill.solid()
    v_axis.fill.fore_color.rgb = COLOR_TEXT_CYAN
    v_axis.line.fill.background()

    # Axis Labels
    labels = [
        ("CONVENIENT", cx - Inches(1.0), cy - axis_len / 2 + Inches(0.05), Inches(2.0), PP_ALIGN.CENTER),
        ("INCONVENIENT", cx - Inches(1.0), cy + axis_len / 2 - Inches(0.4), Inches(2.0), PP_ALIGN.CENTER),
        ("EXPENSIVE", cx - axis_len / 2 - Inches(1.4), cy - Inches(0.15), Inches(1.3), PP_ALIGN.RIGHT),
        ("AFFORDABLE", cx + axis_len / 2 + Inches(0.1), cy - Inches(0.15), Inches(1.4), PP_ALIGN.LEFT)
    ]
    for text, lx, ly, lw, align in labels:
        tx = slide.shapes.add_textbox(lx, ly, lw, Inches(0.35))
        tf = tx.text_frame
        p = tf.paragraphs[0]
        p.text = text
        p.font.name = FONT_TITLE
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_CYAN
        p.alignment = align

    # Competitor Badges (A, B, C, D, E)
    comp_badges = [
        ("A: SAP CMMS", cx - Inches(1.5), cy - Inches(1.2), RGBColor(147, 51, 234)),
        ("B: Spreadsheets", cx + Inches(0.8), cy + Inches(0.6), RGBColor(192, 38, 211)),
        ("C: Basic Apps", cx + Inches(2.2), cy + Inches(1.3), RGBColor(236, 72, 153)),
        ("D: Paper Binders", cx - Inches(2.3), cy + Inches(1.1), RGBColor(100, 116, 139)),
        ("E: Static PDFs", cx - Inches(1.2), cy + Inches(0.8), RGBColor(100, 116, 139))
    ]
    for b_text, bx, by, col in comp_badges:
        badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, by, Inches(1.1), Inches(0.35))
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(15, 23, 42)
        badge.line.color.rgb = col
        badge.line.width = Pt(1.5)
        tf = badge.text_frame
        p = tf.paragraphs[0]
        p.text = b_text
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER

    # MaintAI Champion Badge (Highlighted Top-Right Quadrant!)
    m_badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx + Inches(0.7), cy - Inches(1.3), Inches(2.2), Inches(0.7))
    m_badge.fill.solid()
    m_badge.fill.fore_color.rgb = RGBColor(11, 27, 56)
    m_badge.line.color.rgb = COLOR_TEXT_WHITE
    m_badge.line.width = Pt(2.5)

    tf_m = m_badge.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = "MAINTAI"
    p_m.font.name = FONT_TITLE
    p_m.font.size = Pt(18)
    p_m.font.bold = True
    p_m.font.color.rgb = COLOR_TEXT_WHITE
    p_m.alignment = PP_ALIGN.CENTER

    add_footer(slide, 12)
    return slide


def build_slide_13_growth_strategy(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p13_img0_27.jpeg"))

    # Centered Outlined Title & Subtitle
    add_outlined_title(slide, Inches(1.5), Inches(1.4), Inches(10.333), Inches(0.8), "GROWTH STRATEGY", size_pt=42, outline_hex="00F0FF", align=PP_ALIGN.CENTER)

    tx_sub = slide.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.333), Inches(0.4))
    tf_sub = tx_sub.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "How we'll scale across heavy industrial plant operations"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = COLOR_TEXT_ICE
    p_sub.alignment = PP_ALIGN.CENTER

    phases = [
        ("PHASE 1 (MVP)", "Deploy core multimodal AI defect diagnostics, lightweight Web AR HUD, and Dexie.js offline store for early shop pilots."),
        ("PHASE 2 (PILOT)", "Integrate hands-free voice state machine, AI tool gatekeeper verification, QR batch tags, and Supabase RLS security."),
        ("PHASE 3 (SCALE)", "Connect industrial IoT telemetry via MQTT / OPC-UA, FLIR thermal imaging cameras, and spatial WebXR 3D SLAM tracking.")
    ]

    col_w = Inches(3.2)
    start_x = Inches(1.5)
    gap = Inches(0.7)

    for idx, (head, desc) in enumerate(phases):
        x = start_x + idx * (col_w + gap)

        # Hollow Cyan Box
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(3.2), col_w, Inches(0.9))
        box.fill.background()
        box.line.color.rgb = COLOR_TEXT_CYAN
        box.line.width = Pt(2.0)

        tf_box = box.text_frame
        p_box = tf_box.paragraphs[0]
        p_box.text = head
        p_box.font.name = FONT_TITLE
        p_box.font.size = Pt(13)
        p_box.font.bold = True
        p_box.font.color.rgb = COLOR_TEXT_CYAN
        p_box.alignment = PP_ALIGN.CENTER

        tx_d = slide.shapes.add_textbox(x, Inches(4.4), col_w, Inches(1.8))
        tf_d = tx_d.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = COLOR_TEXT_WHITE
        p_d.alignment = PP_ALIGN.CENTER
        p_d.line_spacing = 1.25

    add_footer(slide, 13)
    return slide


def build_slide_14_action_plan(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p14_img0_85.jpeg"))

    # Centered Outlined Title
    add_outlined_title(slide, Inches(1.5), Inches(1.3), Inches(10.333), Inches(0.8), "TWO-YEAR ACTION PLAN", size_pt=42, outline_hex="00F0FF", align=PP_ALIGN.CENTER)

    track1_milestones = [
        ("Supply volunteers", 1), # Feb
        ("Run focus groups", 4), # May
        ("Gather feedback", 9)   # Oct
    ]
    track2_milestones = [
        ("Test with start ups", 1), # Feb
        ("Regional launch", 6),     # Jul (highlighted cyan)
        ("Deliver to consumers", 11) # Dec
    ]

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    start_x = Inches(2.0)
    step_x = Inches(0.82)

    # Track 1 (Year 1)
    y1 = Inches(3.1)
    tx_yr1 = slide.shapes.add_textbox(Inches(0.8), y1 - Inches(0.15), Inches(1.0), Inches(0.4))
    p_yr1 = tx_yr1.text_frame.paragraphs[0]
    p_yr1.text = "YEAR 1"
    p_yr1.font.name = FONT_TITLE
    p_yr1.font.size = Pt(12)
    p_yr1.font.bold = True
    p_yr1.font.color.rgb = COLOR_TEXT_WHITE

    # Track 1 Line
    line1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, start_x, y1, step_x * 11 + Inches(0.3), Inches(0.02))
    line1.fill.solid()
    line1.fill.fore_color.rgb = COLOR_TEXT_MUTED
    line1.line.fill.background()

    for m_idx, m_name in enumerate(months):
        mx = start_x + m_idx * step_x
        # Node
        node = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, mx, y1 - Inches(0.08), Inches(0.18), Inches(0.18))
        node.fill.solid()
        node.fill.fore_color.rgb = COLOR_TEXT_WHITE if any(m[1] == m_idx for m in track1_milestones) else RGBColor(15, 23, 42)
        node.line.color.rgb = COLOR_TEXT_WHITE
        node.line.width = Pt(1)

        # Month label
        tx_m = slide.shapes.add_textbox(mx - Inches(0.2), y1 + Inches(0.15), Inches(0.6), Inches(0.3))
        p_m = tx_m.text_frame.paragraphs[0]
        p_m.text = m_name
        p_m.font.name = FONT_BODY
        p_m.font.size = Pt(8.5)
        p_m.font.color.rgb = COLOR_TEXT_MUTED
        p_m.alignment = PP_ALIGN.CENTER

    for label, m_idx in track1_milestones:
        mx = start_x + m_idx * step_x
        tx_l = slide.shapes.add_textbox(mx - Inches(0.8), y1 - Inches(0.85), Inches(1.8), Inches(0.6))
        tf_l = tx_l.text_frame
        tf_l.word_wrap = True
        p_l = tf_l.paragraphs[0]
        p_l.text = label
        p_l.font.name = FONT_BODY
        p_l.font.size = Pt(9.5)
        p_l.font.color.rgb = COLOR_TEXT_WHITE
        p_l.alignment = PP_ALIGN.CENTER

    # Track 2 (Year 2)
    y2 = Inches(5.0)
    tx_yr2 = slide.shapes.add_textbox(Inches(0.8), y2 - Inches(0.15), Inches(1.0), Inches(0.4))
    p_yr2 = tx_yr2.text_frame.paragraphs[0]
    p_yr2.text = "YEAR 2"
    p_yr2.font.name = FONT_TITLE
    p_yr2.font.size = Pt(12)
    p_yr2.font.bold = True
    p_yr2.font.color.rgb = COLOR_TEXT_WHITE

    line2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, start_x, y2, step_x * 11 + Inches(0.3), Inches(0.02))
    line2.fill.solid()
    line2.fill.fore_color.rgb = COLOR_TEXT_MUTED
    line2.line.fill.background()

    for m_idx, m_name in enumerate(months):
        mx = start_x + m_idx * step_x
        is_cyan = (m_idx == 6)
        is_active = any(m[1] == m_idx for m in track2_milestones)

        node = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, mx, y2 - Inches(0.08), Inches(0.18), Inches(0.18))
        node.fill.solid()
        node.fill.fore_color.rgb = COLOR_TEXT_CYAN if is_cyan else (COLOR_TEXT_WHITE if is_active else RGBColor(15, 23, 42))
        node.line.color.rgb = COLOR_TEXT_CYAN if is_cyan else COLOR_TEXT_WHITE
        node.line.width = Pt(1)

        tx_m = slide.shapes.add_textbox(mx - Inches(0.2), y2 + Inches(0.15), Inches(0.6), Inches(0.3))
        p_m = tx_m.text_frame.paragraphs[0]
        p_m.text = m_name
        p_m.font.name = FONT_BODY
        p_m.font.size = Pt(8.5)
        p_m.font.color.rgb = COLOR_TEXT_MUTED
        p_m.alignment = PP_ALIGN.CENTER

    for label, m_idx in track2_milestones:
        mx = start_x + m_idx * step_x
        tx_l = slide.shapes.add_textbox(mx - Inches(0.8), y2 - Inches(0.85), Inches(1.8), Inches(0.6))
        tf_l = tx_l.text_frame
        tf_l.word_wrap = True
        p_l = tf_l.paragraphs[0]
        p_l.text = label
        p_l.font.name = FONT_BODY
        p_l.font.size = Pt(9.5)
        p_l.font.bold = (m_idx == 6)
        p_l.font.color.rgb = COLOR_TEXT_CYAN if m_idx == 6 else COLOR_TEXT_WHITE
        p_l.alignment = PP_ALIGN.CENTER

    add_footer(slide, 14)
    return slide


def build_slide_15_financials(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p15_img0_90.jpeg"))

    # Right Iris HUD Image
    iris_img = os.path.join(ASSETS_DIR, "p15_img1_93.jpeg")
    if os.path.exists(iris_img):
        slide.shapes.add_picture(iris_img, Inches(7.8), Inches(0.0), width=Inches(5.533), height=Inches(7.5))

    # Left Outlined Title
    add_outlined_title(slide, Inches(0.8), Inches(1.0), Inches(5.0), Inches(0.8), "FINANCIALS", size_pt=38, outline_hex="00F0FF")

    # Financial Data Table
    table_shape = slide.shapes.add_table(11, 4, Inches(0.8), Inches(1.9), Inches(6.8), Inches(4.8))
    table = table_shape.table

    table.columns[0].width = Inches(2.4)
    table.columns[1].width = Inches(1.4)
    table.columns[2].width = Inches(1.4)
    table.columns[3].width = Inches(1.6)

    table_data = [
        ("METRIC / COST DRIVER", "YEAR 1", "YEAR 2", "YEAR 3"),
        ("Active Plant Deployments", "5", "40", "160"),
        ("Frontline Tech Users", "50", "400", "1,600"),
        ("Inspected Machine Units", "500", "4,000", "16,000"),
        ("Avg Downtime Cost/Hour", "$260,000", "$260,000", "$260,000"),
        ("Prevented Breakdown Hrs", "42 hrs", "380 hrs", "1,620 hrs"),
        ("GROSS CLIENT SAVINGS", "$10.92M", "$98.80M", "$421.2M"),
        ("Cloud & Vision API Cost", "$24,000", "$160,000", "$640,000"),
        ("Engineering & Support", "$85,000", "$380,000", "$1,450,000"),
        ("Local Store Hardware", "$12,000", "$95,000", "$380,000"),
        ("TOTAL OPERATING EXP", "$121,000", "$635,000", "$2,470,000")
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5)

            # Colors & Borders
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_TEXT_CYAN
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(14, 27, 56)
            elif r_idx in [6, 10]:
                p.font.bold = True
                p.font.color.rgb = COLOR_TEXT_CYAN if r_idx == 6 else COLOR_TEXT_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(11, 23, 44)
            else:
                p.font.color.rgb = COLOR_TEXT_ICE
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(7, 15, 30)

    add_footer(slide, 15)
    return slide


def build_slide_16_meet_the_team(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p16_img0_96.jpeg"))

    # Centered Outlined Title
    add_outlined_title(slide, Inches(1.5), Inches(1.3), Inches(10.333), Inches(0.8), "MEET THE TEAM", size_pt=42, outline_hex="071B38", line_width=26000, align=PP_ALIGN.CENTER)

    # Light Glass Panel Card
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.2), Inches(11.333), Inches(4.3))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(241, 245, 249) # Light Slate Glass
    card.line.fill.background()

    team_members = [
        ("HET JOSHI", "Lead Software Architect\nEnrollment: 24SE09CE003\nB.Tech Computer Engineering", os.path.join(ASSETS_DIR, "p16_img1_98.jpeg")),
        ("MR. AYUSH DODIA", "Internal Project Guide\nAssistant Professor\nDept. of Computer Engineering", os.path.join(ASSETS_DIR, "p16_img2_99.jpeg")),
        ("DR. NEERAJ SHARMA", "Head of Department\nSchool of Engineering\nP P Savani University", os.path.join(ASSETS_DIR, "p16_img3_100.jpeg")),
        ("P P SAVANI UNIV", "Department of Computer Engg.\nSchool of Engineering\nNAAC A+ Accredited", os.path.join(PUBLIC_DIR, "official_ppsu_naac.png"))
    ]

    col_w = Inches(2.3)
    start_x = Inches(1.6)
    gap = Inches(0.6)

    for idx, (name, role, img_path) in enumerate(team_members):
        x = start_x + idx * (col_w + gap)

        # Portrait Box with Blue Border
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(2.6), col_w, Inches(2.0))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_TEXT_WHITE
        box.line.color.rgb = RGBColor(14, 50, 120)
        box.line.width = Pt(2.0)

        if img_path and os.path.exists(img_path):
            slide.shapes.add_picture(img_path, x + Inches(0.1), Inches(2.7), width=col_w - Inches(0.2), height=Inches(1.8))

        # Member Name & Title
        tx = slide.shapes.add_textbox(x - Inches(0.1), Inches(4.75), col_w + Inches(0.2), Inches(1.5))
        tf = tx.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = name
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(14, 50, 120)
        p1.alignment = PP_ALIGN.CENTER
        p1.space_after = Pt(3)

        p2 = tf.add_paragraph()
        p2.text = role
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = RGBColor(71, 85, 105)
        p2.alignment = PP_ALIGN.CENTER
        p2.line_spacing = 1.2

    add_footer(slide, 16)
    return slide


def build_slide_17_full_stack(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p17_img0_96.jpeg"))

    # Centered Outlined Title
    add_outlined_title(slide, Inches(1.5), Inches(1.1), Inches(10.333), Inches(0.8), "THE FULL STACK", size_pt=42, outline_hex="071B38", line_width=26000, align=PP_ALIGN.CENTER)

    # Light Glass Panel Card
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.9), Inches(11.733), Inches(5.0))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(241, 245, 249)
    card.line.fill.background()

    stack_items = [
        ("NEXT.JS 14 APP ROUTER", "Core Web Framework", os.path.join(ASSETS_DIR, "p17_img1_105.jpeg")),
        ("REACT 18 & CANVAS", "Spatial AR HUD Engine", os.path.join(ASSETS_DIR, "p17_img2_106.jpeg")),
        ("TAILWIND CSS", "Industrial Design System", os.path.join(ASSETS_DIR, "p17_img3_107.jpeg")),
        ("WEB SPEECH API", "Hands-Free Voice STT/TTS", os.path.join(ASSETS_DIR, "p17_img4_108.jpeg")),
        ("DEXIE.JS INDEXEDDB", "Local Write-Ahead Store", os.path.join(ASSETS_DIR, "p17_img5_109.jpeg")),
        ("SUPABASE POSTGRES", "Row Level Security (RLS)", os.path.join(ASSETS_DIR, "p17_img6_110.jpeg")),
        ("GEMINI 1.5 FLASH", "Multimodal Vision AI", os.path.join(ASSETS_DIR, "p17_img7_111.jpeg")),
        ("PWA SERVICE WORKER", "Zero-Install Offline App", os.path.join(ASSETS_DIR, "p17_img8_112.jpeg"))
    ]

    col_w = Inches(2.4)
    start_x = Inches(1.2)
    start_y = Inches(2.2)

    for idx, (title, sub, icon_path) in enumerate(stack_items):
        r = idx // 4
        c = idx % 4
        x = start_x + c * (col_w + Inches(0.45))
        y = start_y + r * Inches(2.2)

        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, col_w, Inches(1.2))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_TEXT_WHITE
        box.line.color.rgb = RGBColor(14, 50, 120)
        box.line.width = Pt(1.5)

        if icon_path and os.path.exists(icon_path):
            slide.shapes.add_picture(icon_path, x + Inches(0.7), y + Inches(0.1), width=Inches(1.0), height=Inches(1.0))

        tx = slide.shapes.add_textbox(x - Inches(0.1), y + Inches(1.25), col_w + Inches(0.2), Inches(0.8))
        tf = tx.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(14, 50, 120)
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = RGBColor(100, 116, 139)
        p2.alignment = PP_ALIGN.CENTER

    add_footer(slide, 17)
    return slide


def build_slide_18_executive_summary(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, os.path.join(ASSETS_DIR, "p8_img0_57.jpeg"))

    # Right Hero Image: Engineer with Holographic HUD
    right_img = os.path.join(ASSETS_DIR, "p18_img0_115.jpeg")
    if os.path.exists(right_img):
        slide.shapes.add_picture(right_img, Inches(5.6), Inches(0.0), width=Inches(7.733), height=Inches(7.5))

    # Left Solid Coral Card
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.6), Inches(6.2), Inches(4.5))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CORAL_SOLID
    card.line.fill.background()

    # Outlined Title on Coral Card
    add_outlined_title(slide, Inches(0.7), Inches(2.1), Inches(4.8), Inches(0.8), "SUMMARY", size_pt=38, outline_hex="FFFFFF", line_width=24000)

    # White Body Text
    tx = slide.shapes.add_textbox(Inches(0.7), Inches(3.1), Inches(4.8), Inches(2.7))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = (
        "At MaintAI, we believe in giving 100% individual engineering effort. By closing the loop on "
        "real-time computer vision defect diagnostics, in-situ Web AR spatial guidance, and offline write-ahead "
        "data synchronization, we help industrial manufacturing plants achieve zero unplanned downtime. "
        "Demonstrated with rigorous validation by candidate Het Joshi, delivering a 38% reduction in MTTR, "
        "zero data loss, and unmatched frontline convenience."
    )
    p.font.name = FONT_BODY
    p.font.size = Pt(11.5)
    p.font.color.rgb = COLOR_TEXT_WHITE
    p.line_spacing = 1.35

    add_footer(slide, 18)
    return slide


def build_slide_19_thank_you(prs):
    slide = create_blank_slide(prs)
    set_slide_background(slide, None) # Pure Black

    # Left Hero: Neon VR User
    left_img = os.path.join(ASSETS_DIR, "p19_img0_119.jpeg")
    if os.path.exists(left_img):
        slide.shapes.add_picture(left_img, Inches(0.5), Inches(0.6), width=Inches(7.5), height=Inches(6.4))

    # Right Outlined Title
    add_outlined_title(slide, Inches(8.0), Inches(2.0), Inches(4.8), Inches(0.9), "THANK YOU", size_pt=42, outline_hex="00F0FF")

    # Candidate & Defense Info
    tx = slide.shapes.add_textbox(Inches(8.0), Inches(3.2), Inches(4.8), Inches(2.6))
    tf = tx.text_frame
    tf.word_wrap = True

    details = [
        ("Candidate", "Het Joshi (24SE09CE003)"),
        ("Guide", "Mr. Ayush Dodia (Assistant Professor)"),
        ("Department", "Department of Computer Engineering"),
        ("Institute", "School of Engineering, PPSU"),
        ("Project Web", "https://maint-ai.tech"),
        ("Contact", "hetjoshi@maint-ai.tech")
    ]

    for idx, (label, val) in enumerate(details):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"{val}"
        p.font.name = FONT_BODY
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_TEXT_ICE if idx > 1 else COLOR_TEXT_WHITE
        p.font.bold = (idx == 0)
        p.space_after = Pt(5)

    add_footer(slide, 19)
    return slide


# =============================================================================
# MAIN ORCHESTRATOR
# =============================================================================

def build_all_slides():
    print("[INFO] Creating 19-Slide Cyberpunk AR/AI Pitch Deck Presentation...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    build_slide_1_cover(prs)
    build_slide_2_about_us(prs)
    build_slide_3_problem(prs)
    build_slide_4_solution(prs)
    build_slide_5_product_overview(prs)
    build_slide_6_product_benefits(prs)
    build_slide_7_architecture_hands(prs)
    build_slide_8_edge_runtime(prs)
    build_slide_9_key_benchmarks(prs)
    build_slide_10_industrial_standards(prs)
    build_slide_11_competition_columns(prs)
    build_slide_12_competition_matrix(prs)
    build_slide_13_growth_strategy(prs)
    build_slide_14_action_plan(prs)
    build_slide_15_financials(prs)
    build_slide_16_meet_the_team(prs)
    build_slide_17_full_stack(prs)
    build_slide_18_executive_summary(prs)
    build_slide_19_thank_you(prs)

    candidate_paths = [
        OUTPUT_CYBER,
        OUTPUT_MENTOR,
        OUTPUT_DEFENSE,
        OUTPUT_PROJECT
    ]

    saved_count = 0
    for target in candidate_paths:
        try:
            prs.save(target)
            print(f"[SUCCESS] Saved presentation to: {target}")
            saved_count += 1
        except PermissionError:
            print(f"[NOTE] {target} is locked (currently open in PowerPoint).")

    print(f"[DONE] Successfully generated {len(prs.slides)} slides in cyber pitch deck style!")


if __name__ == "__main__":
    build_all_slides()
