#!/usr/bin/env python3
"""
MaintAI - Tailwind Traders Style Academic Presentation Generator (V2 Enhanced)
Faithfully replicates the exact design, layout, color palette, and typography of the
uploaded Tailwind Traders brochure/presentation:
- Color palette: Deep Corporate Navy (#152F4E), Crisp Pure White (#FFFFFF), Electric Cyan (#38BDF8)
- Alternating editorial layout:
    * Hero Cover (Slide 1 & 14): Panoramic digital telemetry banner + 3 bottom color blocks
    * Pattern A (Slide 2, 4, 6, 8, 10, 12): Top Image / Bottom Navy, Top White / Bottom Image, Top Image / Bottom Navy Callout Quote (Page 2 Style)
    * Pattern B (Slide 3, 5, 7, 9, 11, 13): Top Navy / Bottom Image, Top Image / Bottom White Callout Quote, Top Navy Bullets / Bottom Image (Page 4 Style)
- Non-stretched, aspect-ratio-fitted industrial images and UI screenshots
- Human-crafted typography (Century Gothic geometric sans, large cozy quotes, clean hierarchy)

Candidate: Het Joshi (Enrollment No. 24SE09CE003)
Internal Guide: Mr. Ayush Dodia (Assistant Professor)
Institute: Department of Computer Engineering, School of Engineering, P P Savani University
"""

import os
import sys
from PIL import Image, ImageOps
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
ASSET_CACHE_DIR = os.path.join(BASE_DIR, "preview_tailwind_slides", "fitted_assets")
os.makedirs(ASSET_CACHE_DIR, exist_ok=True)

# Target output files
OUTPUT_MENTOR = os.path.join(BASE_DIR, "MaintAI_Mentor_Presentation.pptx")
OUTPUT_DEFENSE = os.path.join(BASE_DIR, "MaintAI_Defense_Presentation.pptx")
OUTPUT_PROJECT = os.path.join(BASE_DIR, "MaintAI_Project_Presentation.pptx")
OUTPUT_TAILWIND = os.path.join(BASE_DIR, "MaintAI_Tailwind_Style_Presentation.pptx")

# Exact Tailwind Traders Palette
COLOR_NAVY = RGBColor(21, 47, 78)          # #152F4E Deep Corporate Navy
COLOR_NAVY_DARK = RGBColor(15, 34, 58)     # #0F223A Darker Navy
COLOR_WHITE = RGBColor(255, 255, 255)      # #FFFFFF Pure Crisp White
COLOR_OFFWHITE = RGBColor(248, 250, 252)   # #F8FAFC
COLOR_TEXT_NAVY = RGBColor(21, 47, 78)     # #152F4E Text on white
COLOR_TEXT_MUTED = RGBColor(71, 85, 105)   # #475569 Slate text on white
COLOR_TEXT_WHITE = RGBColor(255, 255, 255) # Pure White text on navy
COLOR_TEXT_ICE = RGBColor(226, 232, 240)   # #E2E8F0 Ice text on navy
COLOR_CYAN = RGBColor(56, 189, 248)        # #38BDF8 Accent Cyan

FONT_SANS = "Century Gothic"               # Matches the rounded geometric sans in PDF
FONT_FALLBACK = "Segoe UI"


def fit_image_to_frame(src_path, target_w=1333, target_h=1080, bg_color=(255, 255, 255)):
    """
    Fits any image nicely into (target_w, target_h) preserving its aspect ratio.
    If the image has a transparent background, flattens onto bg_color.
    Returns path to preprocessed image.
    """
    if not os.path.exists(src_path):
        return None

    filename = os.path.splitext(os.path.basename(src_path))[0] + f"_fitted_{target_w}x{target_h}.jpg"
    out_path = os.path.join(ASSET_CACHE_DIR, filename)
    if os.path.exists(out_path):
        return out_path

    try:
        with Image.open(src_path) as img:
            img = img.convert("RGBA")
            iw, ih = img.size

            # If aspect ratio is close to target (within 15%), crop & fill
            target_aspect = target_w / target_h
            img_aspect = iw / ih

            if abs(target_aspect - img_aspect) < 0.2:
                # Slight crop to fill
                img_fitted = ImageOps.fit(img, (target_w, target_h), Image.Resampling.LANCZOS)
                canvas = Image.new("RGB", (target_w, target_h), bg_color)
                canvas.paste(img_fitted, (0, 0), mask=img_fitted.split()[3])
            else:
                # Contain inside with white canvas padding
                ratio = min((target_w - 40) / iw, (target_h - 40) / ih)
                new_w = max(1, int(iw * ratio))
                new_h = max(1, int(ih * ratio))
                img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                canvas = Image.new("RGB", (target_w, target_h), bg_color)
                offset_x = (target_w - new_w) // 2
                offset_y = (target_h - new_h) // 2
                canvas.paste(img_resized, (offset_x, offset_y), mask=img_resized.split()[3])

            canvas.save(out_path, "JPEG", quality=95)
            return out_path
    except Exception as e:
        print(f"Warning: Failed to fit image {src_path}: {e}")
        return src_path


def create_blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def add_cover_slide(prs, banner_img_path, title_1, vision_text_1, vision_text_2, title_2, cand_details, brand_title, brand_tag):
    """
    Slide 1 & 14 (Matching Page 1 of Tailwind Traders reference):
    - Top 48%: Digital telemetry banner with glowing histogram & binary digits
    - Bottom 52%: 3 panels:
      * Left: Deep Navy panel ('Our vision' / 'Our impact')
      * Center: Deep Navy panel ('Contact us' / 'Academic Defense' / 'Future Roadmap')
      * Right: Crisp White panel (University crest + Brand title + tracked subtitle)
    """
    slide = create_blank_slide(prs)

    # Top Panoramic Telemetry Banner
    if os.path.exists(banner_img_path):
        slide.shapes.add_picture(banner_img_path, Inches(0), Inches(0), width=Inches(13.333), height=Inches(3.6))
    else:
        top_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(3.6))
        top_rect.fill.solid()
        top_rect.fill.fore_color.rgb = COLOR_NAVY_DARK
        top_rect.line.fill.background()

    # Bottom Left Panel (Navy Blue, width = 4.444 in, height = 3.9 in)
    p1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(3.6), Inches(4.444), Inches(3.9))
    p1.fill.solid()
    p1.fill.fore_color.rgb = COLOR_NAVY
    p1.line.fill.background()

    tf1 = p1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = Inches(0.45)
    tf1.margin_top = Inches(0.4)

    p1_h = tf1.paragraphs[0]
    p1_h.text = title_1
    p1_h.font.name = FONT_SANS
    p1_h.font.size = Pt(25)
    p1_h.font.color.rgb = COLOR_TEXT_WHITE
    p1_h.space_after = Pt(14)

    p1_b1 = tf1.add_paragraph()
    p1_b1.text = vision_text_1
    p1_b1.font.name = FONT_SANS
    p1_b1.font.size = Pt(11)
    p1_b1.font.color.rgb = COLOR_TEXT_ICE
    p1_b1.line_spacing = 1.2
    p1_b1.space_after = Pt(12)

    p1_b2 = tf1.add_paragraph()
    p1_b2.text = vision_text_2
    p1_b2.font.name = FONT_SANS
    p1_b2.font.size = Pt(11)
    p1_b2.font.color.rgb = COLOR_TEXT_ICE
    p1_b2.line_spacing = 1.2

    # Bottom Center Panel (Navy Blue, left = 4.444 in, width = 4.444 in)
    p2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.444), Inches(3.6), Inches(4.444), Inches(3.9))
    p2.fill.solid()
    p2.fill.fore_color.rgb = COLOR_NAVY
    p2.line.fill.background()

    tf2 = p2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = Inches(0.45)
    tf2.margin_top = Inches(0.4)

    p2_h = tf2.paragraphs[0]
    p2_h.text = title_2
    p2_h.font.name = FONT_SANS
    p2_h.font.size = Pt(25)
    p2_h.font.color.rgb = COLOR_TEXT_WHITE
    p2_h.space_after = Pt(14)

    for line in cand_details:
        p_c = tf2.add_paragraph()
        p_c.text = line
        p_c.font.name = FONT_SANS
        p_c.font.size = Pt(11)
        p_c.font.color.rgb = COLOR_TEXT_ICE
        p_c.space_after = Pt(6)

    # Bottom Right Panel (Crisp Pure White, left = 8.888 in, width = 4.445 in)
    p3 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.888), Inches(3.6), Inches(4.445), Inches(3.9))
    p3.fill.solid()
    p3.fill.fore_color.rgb = COLOR_WHITE
    p3.line.fill.background()

    # Circular / Official PPSU NAAC A+ Crest
    ppsu_logo = os.path.join(PUBLIC_DIR, "official_ppsu_naac.png")
    if os.path.exists(ppsu_logo):
        slide.shapes.add_picture(ppsu_logo, Inches(10.3), Inches(4.15), height=Inches(0.95))

    # Brand Title in Deep Navy
    tx_brand = slide.shapes.add_textbox(Inches(9.0), Inches(5.3), Inches(4.2), Inches(1.8))
    tf3 = tx_brand.text_frame
    tf3.word_wrap = True
    p3_t = tf3.paragraphs[0]
    p3_t.text = brand_title
    p3_t.font.name = FONT_SANS
    p3_t.font.size = Pt(28)
    p3_t.font.bold = True
    p3_t.font.color.rgb = COLOR_TEXT_NAVY
    p3_t.alignment = PP_ALIGN.CENTER
    p3_t.space_after = Pt(8)

    p3_sub = tf3.add_paragraph()
    p3_sub.text = brand_tag
    p3_sub.font.name = FONT_SANS
    p3_sub.font.size = Pt(10)
    p3_sub.font.bold = True
    p3_sub.font.color.rgb = COLOR_NAVY
    p3_sub.alignment = PP_ALIGN.CENTER

    return slide


def add_pattern_a_slide(prs, col1_img, col1_title, col1_paras,
                        col2_title, col2_paras, col2_img,
                        col3_img, col3_quote):
    """
    Pattern A (Faithfully matches Page 2 of the reference):
    - Col 1: Top Image (4.444 x 3.6 in) + Bottom Navy Block (4.444 x 3.9 in, 'Our services' style)
    - Col 2: Top White Block (4.444 x 3.6 in, 'Our team' style) + Bottom Image (4.444 x 3.9 in)
    - Col 3: Top Image (4.444 x 3.6 in) + Bottom Navy Block (4.444 x 3.9 in with Large White Callout Quote!)
    """
    slide = create_blank_slide(prs)
    col_w = Inches(4.444)
    top_h = Inches(3.6)
    bot_h = Inches(3.9)

    # ---------------- COLUMN 1 (Left) ----------------
    # Top Image
    c1_fitted = fit_image_to_frame(col1_img)
    if c1_fitted and os.path.exists(c1_fitted):
        slide.shapes.add_picture(c1_fitted, Inches(0), Inches(0), width=col_w, height=top_h)
    else:
        c1_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), col_w, top_h)
        c1_top.fill.solid()
        c1_top.fill.fore_color.rgb = COLOR_NAVY_DARK
        c1_top.line.fill.background()

    # Bottom Navy Block
    c1_bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), top_h, col_w, bot_h)
    c1_bot.fill.solid()
    c1_bot.fill.fore_color.rgb = COLOR_NAVY
    c1_bot.line.fill.background()

    tf1 = c1_bot.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = Inches(0.4)
    tf1.margin_top = Inches(0.4)

    p1_h = tf1.paragraphs[0]
    p1_h.text = col1_title
    p1_h.font.name = FONT_SANS
    p1_h.font.size = Pt(23)
    p1_h.font.color.rgb = COLOR_TEXT_WHITE
    p1_h.space_after = Pt(12)

    for para in col1_paras:
        p = tf1.add_paragraph()
        p.text = para
        p.font.name = FONT_SANS
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_ICE
        p.line_spacing = 1.15
        p.space_after = Pt(8)

    # ---------------- COLUMN 2 (Center) ----------------
    # Top White Block
    c2_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_w, Inches(0), col_w, top_h)
    c2_top.fill.solid()
    c2_top.fill.fore_color.rgb = COLOR_WHITE
    c2_top.line.fill.background()

    tf2 = c2_top.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = Inches(0.4)
    tf2.margin_top = Inches(0.4)

    p2_h = tf2.paragraphs[0]
    p2_h.text = col2_title
    p2_h.font.name = FONT_SANS
    p2_h.font.size = Pt(23)
    p2_h.font.color.rgb = COLOR_TEXT_NAVY
    p2_h.space_after = Pt(12)

    for para in col2_paras:
        p = tf2.add_paragraph()
        p.text = para
        p.font.name = FONT_SANS
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.line_spacing = 1.15
        p.space_after = Pt(8)

    # Bottom Image
    c2_fitted = fit_image_to_frame(col2_img)
    if c2_fitted and os.path.exists(c2_fitted):
        slide.shapes.add_picture(c2_fitted, col_w, top_h, width=col_w, height=bot_h)
    else:
        c2_bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_w, top_h, col_w, bot_h)
        c2_bot.fill.solid()
        c2_bot.fill.fore_color.rgb = COLOR_OFFWHITE
        c2_bot.line.fill.background()

    # ---------------- COLUMN 3 (Right) ----------------
    # Top Image
    c3_fitted = fit_image_to_frame(col3_img)
    if c3_fitted and os.path.exists(c3_fitted):
        slide.shapes.add_picture(c3_fitted, col_w * 2, Inches(0), width=col_w, height=top_h)
    else:
        c3_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_w * 2, Inches(0), col_w, top_h)
        c3_top.fill.solid()
        c3_top.fill.fore_color.rgb = COLOR_NAVY_DARK
        c3_top.line.fill.background()

    # Bottom Navy Block with Large White Callout Quote!
    c3_bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_w * 2, top_h, col_w, bot_h)
    c3_bot.fill.solid()
    c3_bot.fill.fore_color.rgb = COLOR_NAVY
    c3_bot.line.fill.background()

    tf3 = c3_bot.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = Inches(0.45)
    tf3.margin_top = Inches(0.55)

    p3_q = tf3.paragraphs[0]
    p3_q.text = col3_quote
    p3_q.font.name = FONT_SANS
    p3_q.font.size = Pt(17.5)
    p3_q.font.color.rgb = COLOR_TEXT_WHITE
    p3_q.line_spacing = 1.35

    return slide


def add_pattern_b_slide(prs, col1_title, col1_paras, col1_img,
                        col2_img, col2_quote,
                        col3_title, col3_bullets, col3_img):
    """
    Pattern B (Faithfully matches Page 4 of the reference):
    - Col 1: Top Navy Block (4.444 x 3.6 in) + Bottom Image (4.444 x 3.9 in)
    - Col 2: Top Image (4.444 x 3.6 in) + Bottom White Block (4.444 x 3.9 in with Large Navy Callout Quote!)
    - Col 3: Top Navy Block with Bullets (4.444 x 3.6 in) + Bottom Image (4.444 x 3.9 in)
    """
    slide = create_blank_slide(prs)
    col_w = Inches(4.444)
    top_h = Inches(3.6)
    bot_h = Inches(3.9)

    # ---------------- COLUMN 1 (Left) ----------------
    # Top Navy Block
    c1_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), col_w, top_h)
    c1_top.fill.solid()
    c1_top.fill.fore_color.rgb = COLOR_NAVY
    c1_top.line.fill.background()

    tf1 = c1_top.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = Inches(0.4)
    tf1.margin_top = Inches(0.4)

    p1_h = tf1.paragraphs[0]
    p1_h.text = col1_title
    p1_h.font.name = FONT_SANS
    p1_h.font.size = Pt(23)
    p1_h.font.color.rgb = COLOR_TEXT_WHITE
    p1_h.space_after = Pt(12)

    for para in col1_paras:
        p = tf1.add_paragraph()
        p.text = para
        p.font.name = FONT_SANS
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_ICE
        p.line_spacing = 1.15
        p.space_after = Pt(8)

    # Bottom Image
    c1_fitted = fit_image_to_frame(col1_img)
    if c1_fitted and os.path.exists(c1_fitted):
        slide.shapes.add_picture(c1_fitted, Inches(0), top_h, width=col_w, height=bot_h)
    else:
        c1_bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), top_h, col_w, bot_h)
        c1_bot.fill.solid()
        c1_bot.fill.fore_color.rgb = COLOR_OFFWHITE
        c1_bot.line.fill.background()

    # ---------------- COLUMN 2 (Center) ----------------
    # Top Image
    c2_fitted = fit_image_to_frame(col2_img)
    if c2_fitted and os.path.exists(c2_fitted):
        slide.shapes.add_picture(c2_fitted, col_w, Inches(0), width=col_w, height=top_h)
    else:
        c2_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_w, Inches(0), col_w, top_h)
        c2_top.fill.solid()
        c2_top.fill.fore_color.rgb = COLOR_OFFWHITE
        c2_top.line.fill.background()

    # Bottom White Block with Large Navy Callout Quote!
    c2_bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_w, top_h, col_w, bot_h)
    c2_bot.fill.solid()
    c2_bot.fill.fore_color.rgb = COLOR_WHITE
    c2_bot.line.fill.background()

    tf2 = c2_bot.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = Inches(0.45)
    tf2.margin_top = Inches(0.55)

    p2_q = tf2.paragraphs[0]
    p2_q.text = col2_quote
    p2_q.font.name = FONT_SANS
    p2_q.font.size = Pt(17.5)
    p2_q.font.color.rgb = COLOR_TEXT_NAVY
    p2_q.line_spacing = 1.35

    # ---------------- COLUMN 3 (Right) ----------------
    # Top Navy Block with Bullet Points
    c3_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_w * 2, Inches(0), col_w, top_h)
    c3_top.fill.solid()
    c3_top.fill.fore_color.rgb = COLOR_NAVY
    c3_top.line.fill.background()

    tf3 = c3_top.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = Inches(0.4)
    tf3.margin_top = Inches(0.4)

    p3_h = tf3.paragraphs[0]
    p3_h.text = col3_title
    p3_h.font.name = FONT_SANS
    p3_h.font.size = Pt(23)
    p3_h.font.color.rgb = COLOR_TEXT_WHITE
    p3_h.space_after = Pt(12)

    for bullet in col3_bullets:
        p = tf3.add_paragraph()
        p.text = f"•  {bullet}"
        p.font.name = FONT_SANS
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_ICE
        p.line_spacing = 1.15
        p.space_after = Pt(6)

    # Bottom Image
    c3_fitted = fit_image_to_frame(col3_img)
    if c3_fitted and os.path.exists(c3_fitted):
        slide.shapes.add_picture(c3_fitted, col_w * 2, top_h, width=col_w, height=bot_h)
    else:
        c3_bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_w * 2, top_h, col_w, bot_h)
        c3_bot.fill.solid()
        c3_bot.fill.fore_color.rgb = COLOR_OFFWHITE
        c3_bot.line.fill.background()

    return slide


def build_tailwind_style_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Curated Asset Paths
    banner_img = os.path.join(PUBLIC_DIR, "tailwind_style_banner.png")
    cnc_img = os.path.join(MACHINES_DIR, "cnc-machine.jpg")
    pump_img = os.path.join(MACHINES_DIR, "water-pump.jpg")
    robot_img = os.path.join(MACHINES_DIR, "milling-machine.jpg")
    diesel_img = os.path.join(MACHINES_DIR, "diesel-generator.jpg")
    compressor_img = os.path.join(MACHINES_DIR, "air-compressor.jpeg")
    boiler_img = os.path.join(MACHINES_DIR, "boiler-system.jpg")
    motor_img = os.path.join(MACHINES_DIR, "electric-motor.jpg")
    press_img = os.path.join(MACHINES_DIR, "hydraulic-press.jpg")
    conveyor_img = os.path.join(MACHINES_DIR, "conveyor-belt.jpg")
    cooling_img = os.path.join(MACHINES_DIR, "cooling-tower.jpg")
    chiller_img = os.path.join(MACHINES_DIR, "chiller-unit.jpg")
    molding_img = os.path.join(MACHINES_DIR, "forklift.jpg")
    schuler_press = os.path.join(PDF_IMAGES_DIR, "mach_schuler_press.jpg")

    # Real Tools and Spares
    wrench_img = os.path.join(PDF_IMAGES_DIR, "tool_wrench.jpg")
    allen_key_img = os.path.join(PDF_IMAGES_DIR, "tool_allen_key.jpg")
    multimeter_img = os.path.join(PDF_IMAGES_DIR, "tool_multimeter.jpg")
    pliers_img = os.path.join(PDF_IMAGES_DIR, "tool_pliers.jpg")
    bearing_img = os.path.join(PARTS_DIR, "ball-bearing-6205.jpg")
    contactor_img = os.path.join(PARTS_DIR, "contactor-lc1d25.jpg")
    seal_img = os.path.join(PARTS_DIR, "hydraulic-seal-hs-45.jpg")
    sensor_img = os.path.join(PARTS_DIR, "pressure-switch-ps-100.jpg")

    # Real UI and Architecture
    ar_step_ui = os.path.join(PUBLIC_DIR, "p12_img4_73.png")
    ar_hud_crop = os.path.join(PDF_IMAGES_DIR, "crop_ar_hud.png")
    gemini_gate_crop = os.path.join(PDF_IMAGES_DIR, "crop_gemini_gate.png")
    fault_report_ui = os.path.join(PDF_IMAGES_DIR, "screenshot7_fault_report.png")
    fixbot_ui = os.path.join(PDF_IMAGES_DIR, "fig_A_6_fixbot_ai.jpeg")
    dispatch_ui = os.path.join(PDF_IMAGES_DIR, "fig_A_8_technician_assign.jpeg")
    parts_inventory_ui = os.path.join(PUBLIC_DIR, "p13_img3_76.png")
    analytics_ui = os.path.join(PUBLIC_DIR, "p14_img4_81.png")
    qr_matrix_ui = os.path.join(PUBLIC_DIR, "p15_img3_84.png")
    qr_tag_img = os.path.join(PDF_IMAGES_DIR, "qr_grundfos_pump.png")
    arch_img = os.path.join(PUBLIC_DIR, "updated_architecture_diagram.png")
    sync_img = os.path.join(PUBLIC_DIR, "updated_offline_sync_workflow.png")
    use_case_img = os.path.join(PDF_IMAGES_DIR, "fig_5_3_use_case_diagram.png")
    repair_flow_img = os.path.join(PDF_IMAGES_DIR, "updated_repair_workflow.png")

    print("[INFO] Building 14 Tailwind-Style Presentation Slides...")

    # =========================================================================
    # SLIDE 1: Cover Slide (Exact Match to Page 1)
    # =========================================================================
    add_cover_slide(
        prs,
        banner_img,
        title_1="Our vision",
        vision_text_1="At MaintAI, our vision is to empower manufacturing plants and industrial reliability teams to navigate complex machinery operations with confidence.",
        vision_text_2="We strive to be a trusted partner, providing multimodal AI diagnostics, in-situ AR guidance, and offline-first resilience that helps industrial plants achieve zero unplanned downtime.",
        title_2="Contact us",
        cand_details=[
            "Candidate: Het Joshi",
            "Enrollment No: 24SE09CE003",
            "B.Tech Computer Engineering (7th Sem)",
            "Guide: Mr. Ayush Dodia (Asst. Prof.)",
            "Department of Computer Engineering",
            "School of Engineering, PPSU"
        ],
        brand_title="MAINTAI\nPLATFORM",
        brand_tag="I N T E L L I G E N T  I N D U S T R I A L  A I"
    )

    # =========================================================================
    # SLIDE 2: Problem Statement & Shop Dilemma (Pattern A - Page 2 Style)
    # =========================================================================
    add_pattern_a_slide(
        prs,
        col1_img=cnc_img,
        col1_title="The dilemma",
        col1_paras=[
            "Unplanned manufacturing downtime costs heavy industries an average of $260,000+ per hour across automotive and process lines.",
            "A single mechanical breakdown halts entire sequential assembly operations.",
            "Manual dispatching incurs 40 to 90 minute response lags before technicians arrive on site."
        ],
        col2_title="Shop vulnerabilities",
        col2_paras=[
            "Technicians navigate cumbersome 300+ page paper binders or static PDF manuals.",
            "Extreme cognitive friction finding torque specs and clearances with dirty hands.",
            "Zero digital verification or immutable audit proof of executed maintenance steps."
        ],
        col2_img=pump_img,
        col3_img=wrench_img,
        col3_quote="Traditional maintenance relies on slow, paper-based workflows; MaintAI delivers real-time, spatial guidance directly on plant equipment."
    )

    # =========================================================================
    # SLIDE 3: Our Solution & Engineering Scope (Pattern B - Page 4 Style)
    # =========================================================================
    add_pattern_b_slide(
        prs,
        col1_title="Our solution",
        col1_paras=[
            "MaintAI delivers a comprehensive hands-free maintenance platform combining multimodal computer vision, lightweight Web AR, and offline write-ahead synchronization.",
            "Engineered as an edge-native Progressive Web App (PWA) with zero native app installation friction."
        ],
        col1_img=ar_step_ui,
        col2_img=robot_img,
        col2_quote="Empowering frontline technicians with in-situ AI diagnostics, hands-free voice controls, and automated tool verification.",
        col3_title="Core capabilities",
        col3_bullets=[
            "Real-time computer vision defect diagnostics in <1.4s.",
            "Lightweight HTML5 Canvas Web AR HUD operating at 59.8 FPS.",
            "Continuous hands-free voice state machine with Levenshtein phonetic matching.",
            "38% reduction in Mean Time to Repair (MTTR) demonstrated during shop-floor validation."
        ],
        col3_img=allen_key_img
    )

    # =========================================================================
    # SLIDE 4: System Architecture & 3-Tier Edge Topology (Pattern A - Page 2 Style)
    # =========================================================================
    add_pattern_a_slide(
        prs,
        col1_img=arch_img,
        col1_title="Presentation tier",
        col1_paras=[
            "Built on Next.js 14 App Router, React 18, and Tailwind CSS design system.",
            "HTML5 Canvas 60 FPS spatial visual overlay engine.",
            "PWA Service Worker caches the application shell for instant offline boot."
        ],
        col2_title="Local edge runtime",
        col2_paras=[
            "Dexie.js IndexedDB local write-ahead log ensures <5ms task save latency.",
            "Web Speech API STT/TTS engine executes in-browser with zero cloud round-trip delay."
        ],
        col2_img=diesel_img,
        col3_img=parts_inventory_ui,
        col3_quote="A resilient 3-tier architecture ensuring continuous shop-floor productivity even through complete network blackouts."
    )

    # =========================================================================
    # SLIDE 5: Multimodal AI Defect Diagnostics (Pattern B - Page 4 Style)
    # =========================================================================
    add_pattern_b_slide(
        prs,
        col1_title="Vision engine",
        col1_paras=[
            "1080p camera feed ingested via browser WebRTC media stream with client-side canvas downsampling.",
            "Adaptive JPEG compression preserves bandwidth while maintaining fine defect resolution.",
            "Sub-1.4s average inference latency on standard plant network connections."
        ],
        col1_img=fault_report_ui,
        col2_img=compressor_img,
        col2_quote="Transforming noisy shop-floor camera frames into actionable, ISO-compliant engineering diagnostics in under 1.4 seconds.",
        col3_title="Defect taxonomy",
        col3_bullets=[
            "Identifies bearing spalling, gear pitting, oil/hydraulic leaks, and belt wear with 94.2% accuracy.",
            "Automated incident ticket creation with pre-filled OEM spare part requirements.",
            "ISO 10816 vibration classification & ISO 898-1 fastener mechanical property lookup.",
            "Automated supervisor notification with severity rating (Critical, Warning, Nominal)."
        ],
        col3_img=multimeter_img
    )

    # =========================================================================
    # SLIDE 6: Augmented Reality HUD & Spatial Guidance (Pattern A - Page 2 Style)
    # =========================================================================
    add_pattern_a_slide(
        prs,
        col1_img=ar_hud_crop,
        col1_title="In-situ AR HUD",
        col1_paras=[
            "Lightweight HTML5 Canvas engine overlays animated reticles and inspection zones directly on live camera feed.",
            "Normalized percentage coordinates (x%, y%) dynamically scale across mobile phones, tablets, and smart glasses.",
            "Sustained 59.8 FPS mobile rendering rate."
        ],
        col2_title="Quality assurance",
        col2_paras=[
            "Replaces paper binders with spatial, step-by-step visual guidance.",
            "Pulsing crosshairs focus technician attention onto exact fastener sequences and lubrication ports."
        ],
        col2_img=boiler_img,
        col3_img=gemini_gate_crop,
        col3_quote="Step progression remains locked until the technician visually presents the required calibrated torque wrench."
    )

    # =========================================================================
    # SLIDE 7: Hands-Free Voice State Machine (Pattern B - Page 4 Style)
    # =========================================================================
    add_pattern_b_slide(
        prs,
        col1_title="Voice interface",
        col1_paras=[
            "Browser-native Web Speech API speech recognition running directly in-browser with zero latency.",
            "Noise-tolerant state machine implements phonetic and Levenshtein distance matching to filter shop-floor hum.",
            "Continuous listening daemon with auto-restart loop maintains standby mode through pauses."
        ],
        col1_img=motor_img,
        col2_img=press_img,
        col2_quote="Enabling grease-handed technicians to operate complex workflows purely through spoken voice commands.",
        col3_title="Acoustic pipeline",
        col3_bullets=[
            "Robust phonetic tokenization handles varied regional technical pronunciations effortlessly.",
            "Auditory TTS feedback speaks confirmations and torque ratings aloud.",
            "Spoken commands: 'Next Step', 'Repeat Step', 'Previous Step'.",
            "'Toggle Torch' activates camera LED for dark cavities; 'Safety Checklist' reads mandatory LOTO rules."
        ],
        col3_img=pliers_img
    )

    # =========================================================================
    # SLIDE 8: FixBot AI Industrial Copilot (Pattern A - Page 2 Style)
    # =========================================================================
    add_pattern_a_slide(
        prs,
        col1_img=fixbot_ui,
        col1_title="Shop teammate",
        col1_paras=[
            "Friendly natural-language interface for shift greetings, safety briefings, and casual maintenance inquiries.",
            "Answers workshop queries: 'Where is the 17mm torque wrench stored?', 'Who is the shift supervisor on duty?'",
            "Maintains conversation context across multi-turn dialogs."
        ],
        col2_title="Engineering rigor",
        col2_paras=[
            "Seamlessly transitions into an authoritative 5-part engineering diagnostic protocol for mechanical troubleshooting.",
            "Provides root-cause hypotheses with probability ratings."
        ],
        col2_img=schuler_press,
        col3_img=dispatch_ui,
        col3_quote="Dual-mode AI copilot that bridges friendly shift communication with authoritative ISO engineering diagnostic rigor."
    )

    # =========================================================================
    # SLIDE 9: Smart Spare Parts & Machine Compatibility Matrix (Pattern B - Page 4 Style)
    # =========================================================================
    add_pattern_b_slide(
        prs,
        col1_title="Parts repository",
        col1_paras=[
            "Complete catalog of 36 verified OEM components spanning electrical, mechanical, and hydraulic assemblies.",
            "Real-time stock tracking with automated reorder thresholds (Safe, Low, Out-of-Stock).",
            "1-click purchase order requisition directly to maintenance store."
        ],
        col1_img=parts_inventory_ui,
        col2_img=bearing_img,
        col2_quote="Machine Compatibility Matrix prevents wrong part installation by matching part numbers to machine serials.",
        col3_title="Inventory control",
        col3_bullets=[
            "Ball Bearing 6205-2RS (Mechanical, 42 in stock).",
            "Contactor LC1D25 (Electrical, 8 in stock).",
            "Hydraulic Seal HS-45-V (Hydraulics, 14 in stock).",
            "Instant barcode lookup integration prevents assembly errors."
        ],
        col3_img=contactor_img
    )

    # =========================================================================
    # SLIDE 10: Plant QR Asset Barcode Management (Pattern A - Page 2 Style)
    # =========================================================================
    add_pattern_a_slide(
        prs,
        col1_img=qr_matrix_ui,
        col1_title="Asset tracking",
        col1_paras=[
            "Sub-200ms camera barcode scanner decoding Code128, QR Code, and DataMatrix industrial formats.",
            "Instant digital twin retrieval upon scanning physical machine tag.",
            "Eliminates need for costly specialized handheld laser terminals."
        ],
        col2_title="Batch generation",
        col2_paras=[
            "Built-in Code128 barcode generator prints industrial tags directly from the web interface.",
            "Seamless asset onboarding for newly received machinery and spare parts inventory."
        ],
        col2_img=qr_tag_img,
        col3_img=conveyor_img,
        col3_quote="Scanning physical machine tag loads operational telemetry, maintenance log history, and open tickets in under 200ms."
    )

    # =========================================================================
    # SLIDE 11: Supervisor Analytics & Plant Governance (Pattern B - Page 4 Style)
    # =========================================================================
    add_pattern_b_slide(
        prs,
        col1_title="Plant analytics",
        col1_paras=[
            "Real-time fleet reliability telemetry, MTTR, and MTBF tracking dashboards.",
            "Visual drag-and-drop fault triage and technician assignment dispatch board.",
            "Live monitoring of ongoing repairs and pending work order approvals."
        ],
        col1_img=analytics_ui,
        col2_img=cooling_img,
        col2_quote="Supabase PostgreSQL Row Level Security (RLS) guarantees total multi-tenant data isolation and role boundaries.",
        col3_title="Role matrix",
        col3_bullets=[
            "Plant Administrator: Global plant telemetry, user onboarding, safety stock thresholds, cryptographic audit logs.",
            "Shift Supervisor: Dispatch board, shift scheduling, work order triage, return-to-service sign-off.",
            "Field Technician: Mobile AR HUD, voice checklists, tool verification, digital certificate signing.",
            "Sign-off authority: Supervisors review technician completion photos."
        ],
        col3_img=chiller_img
    )

    # =========================================================================
    # SLIDE 12: Offline-First Synchronization Engine (Pattern A - Page 2 Style)
    # =========================================================================
    add_pattern_a_slide(
        prs,
        col1_img=sync_img,
        col1_title="Write-ahead log",
        col1_paras=[
            "All maintenance updates, completed checklists, and photo evidence write locally to Dexie.js IndexedDB in <5ms.",
            "IndexedDB local relational tables for machines, parts, fault reports, and queued transactions.",
            "Technicians continue working completely uninterrupted when network drops."
        ],
        col2_title="Reconciliation",
        col2_paras=[
            "Network sentinel detects when Wi-Fi or cellular connectivity is restored.",
            "FIFO background sync worker replays queued mutations sequentially with idempotency keys to prevent duplicates."
        ],
        col2_img=sensor_img,
        col3_img=repair_flow_img,
        col3_quote="Zero data loss verified across 50 simulated disconnect/reconnect cycles with 500+ mutations."
    )

    # =========================================================================
    # SLIDE 13: Quantitative System Benchmarks (Pattern B - Page 4 Style)
    # =========================================================================
    add_pattern_b_slide(
        prs,
        col1_title="Key benchmarks",
        col1_paras=[
            "AI Vision Accuracy: 94.2% top-1 defect detection accuracy across 120 fault images.",
            "Vision API Latency: <1.4s serverless edge inference response time.",
            "AR HUD Frame Rate: 59.8 FPS sustained mobile canvas rendering.",
            "MTTR Reduction: 38% reduction in Mean Time to Repair compared to paper manuals."
        ],
        col1_img=use_case_img,
        col2_img=molding_img,
        col2_quote="Rigorous empirical benchmarks demonstrate production-ready performance across all industrial reliability criteria.",
        col3_title="Compliance norms",
        col3_bullets=[
            "Zero Data Loss: 50 offline disconnect/reconnect simulation cycles with 500+ mutations passed with 0 dropped packets.",
            "Barcode Decode Speed: Average 180ms decode time on standard 1080p camera stream.",
            "Google Lighthouse PWA Score: Performance 96/100, PWA 100/100, Accessibility 98/100.",
            "ISO 10816, ISO 898-1, and OSHA 1910.147 (LOTO) visual checklist gate."
        ],
        col3_img=seal_img
    )

    # =========================================================================
    # SLIDE 14: Conclusion & Academic Defense (Exact Match to Page 3 / 4)
    # =========================================================================
    add_cover_slide(
        prs,
        banner_img,
        title_1="Our impact",
        vision_text_1="MaintAI successfully bridges multimodal AI computer vision, in-situ Web AR guidance, and offline-first data resilience into a unified industrial platform.",
        vision_text_2="Demonstrating 100% individual engineering effort by candidate Het Joshi across full-stack Next.js, AR canvas math, Gemini AI prompts, Dexie.js offline store, and Supabase database architecture.",
        title_2="Academic defense",
        cand_details=[
            "Future Roadmap:",
            "• Industrial IoT MQTT / OPC-UA integration",
            "• Thermal FLIR infrared camera streaming",
            "• Spatial WebXR 3D SLAM tracking",
            "Candidate: Het Joshi (24SE09CE003)",
            "Guide: Mr. Ayush Dodia (Asst. Prof.)",
            "School of Engineering, PPSU"
        ],
        brand_title="MAINTAI\nDEFENSE",
        brand_tag="T H A N K  Y O U  •  Q & A  S E S S I O N"
    )

    # Save to all target paths
    candidate_paths = [
        OUTPUT_TAILWIND,
        OUTPUT_MENTOR,
        OUTPUT_DEFENSE,
        OUTPUT_PROJECT
    ]
    for p_target in candidate_paths:
        try:
            prs.save(p_target)
            print(f"[SUCCESS] Saved presentation to: {p_target}")
        except PermissionError:
            print(f"[NOTE] {p_target} is locked (currently open in PowerPoint).")

    print(f"[STATS] Total slides generated: {len(prs.slides)}")


if __name__ == "__main__":
    build_tailwind_style_presentation()
