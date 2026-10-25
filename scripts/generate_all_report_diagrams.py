import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_PATH_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"

def get_fonts(sz_title=28, sz_head=20, sz_sub=16, sz_body=14, sz_sm=12):
    return {
        "title": ImageFont.truetype(FONT_PATH_BOLD, sz_title),
        "head": ImageFont.truetype(FONT_PATH_BOLD, sz_head),
        "sub": ImageFont.truetype(FONT_PATH_BOLD, sz_sub),
        "body": ImageFont.truetype(FONT_PATH_REG, sz_body),
        "body_bold": ImageFont.truetype(FONT_PATH_BOLD, sz_body),
        "sm": ImageFont.truetype(FONT_PATH_REG, sz_sm),
        "sm_bold": ImageFont.truetype(FONT_PATH_BOLD, sz_sm),
    }

def draw_rounded_rect(draw, xy, radius=12, fill=None, outline=None, width=2):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, color="#475569", width=3, arrow_size=10):
    x1, y1 = start
    x2, y2 = end
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    if x1 == x2: # Vertical
        if y2 > y1: # Down
            points = [(x2, y2), (x2 - arrow_size, y2 - arrow_size * 1.5), (x2 + arrow_size, y2 - arrow_size * 1.5)]
        else: # Up
            points = [(x2, y2), (x2 - arrow_size, y2 + arrow_size * 1.5), (x2 + arrow_size, y2 + arrow_size * 1.5)]
    elif y1 == y2: # Horizontal
        if x2 > x1: # Right
            points = [(x2, y2), (x2 - arrow_size * 1.5, y2 - arrow_size), (x2 - arrow_size * 1.5, y2 + arrow_size)]
        else: # Left
            points = [(x2, y2), (x2 + arrow_size * 1.5, y2 - arrow_size), (x2 + arrow_size * 1.5, y2 + arrow_size)]
    else:
        points = [(x2, y2), (x2 - 8, y2 - 8), (x2 + 8, y2 - 8)]
    draw.polygon(points, fill=color)

# ==============================================================================
# Diagram: Figure 5.1 Project Methodology & Engineering Lifecycle Workflow
# ==============================================================================
def create_fig_5_1_workflow(out_path):
    W, H = 2200, 1100
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts(sz_title=34, sz_head=20, sz_sub=15, sz_body=13, sz_sm=12)

    # Header
    draw.rectangle([0, 0, W, 85], fill="#0F172A")
    draw.text((W // 2, 42), "Figure 5.1: MaintAI Engineering Methodology & Iterative Project Lifecycle", 
              fill="#FFFFFF", font=fonts["title"], anchor="mm")

    phases = [
        ("Phase 1: Problem & Planning", "• Domain Literature Review\n• Shop-floor field pain-points\n• Scope & Feasibility study\n• Tech stack benchmarking", "#EFF6FF", "#2563EB"),
        ("Phase 2: System Architecture", "• 3-Tier PWA Architecture\n• PostgreSQL Schema & RLS\n• API Contract Specification\n• Initial UI/UX Wireframing", "#F0FDF4", "#16A34A"),
        ("Phase 3: Core Implementation", "• Next.js 14 App Router\n• HTML5 Canvas AR Engine\n• Web Speech Voice Control\n• Gemini AI Vision Tool Gate", "#FEF3C7", "#D97706"),
        ("Phase 4: Offline Resilience", "• Dexie.js IndexedDB Store\n• Write-Ahead Sync Queue\n• Service Worker Precaching\n• Conflict Resolution Rules", "#FAF5FF", "#7C3AED"),
        ("Phase 5: Verification & UAT", "• Automated API testing\n• Multi-device mobile UAT\n• Factory noise benchmarking\n• Final Production Deployment", "#FDF2F8", "#DB2777"),
    ]

    box_w = 380
    box_h = 320
    top_y = 160
    x_starts = [60, 480, 900, 1320, 1740]

    for idx, (title, content, bg, bdr) in enumerate(phases):
        x = x_starts[idx]
        draw_rounded_rect(draw, [x, top_y, x + box_w, top_y + box_h], radius=14, fill=bg, outline=bdr, width=3)
        draw_rounded_rect(draw, [x, top_y, x + box_w, top_y + 55], radius=14, fill=bdr)
        draw.text((x + box_w // 2, top_y + 27), title, fill="#FFFFFF", font=fonts["head"], anchor="mm")
        draw.text((x + 25, top_y + 80), content, fill="#1E293B", font=fonts["sub"], spacing=10)
        
        if idx < 4:
            draw_arrow(draw, (x + box_w, top_y + box_h // 2), (x_starts[idx + 1], top_y + box_h // 2), color="#475569", width=4)

    # Bottom Agile Feedback & Continuous Integration Loop
    loop_y = 560
    draw_rounded_rect(draw, [60, loop_y, W - 60, loop_y + 440], radius=16, fill="#F8FAFC", outline="#64748B", width=2)
    draw.text((W // 2, loop_y + 40), "Agile Scrum Sprint Iterations & Progress Milestone Alignment (Reporting 1 → 2 → 3 → 4)", 
              fill="#0F172A", font=fonts["head"], anchor="mm")

    sprint_boxes = [
        ("Reporting 1: Foundation", "Problem Definition\nLiterature Survey\nScope Matrix\nReq. Specification", "#DBEAFE", "#1E40AF"),
        ("Reporting 2: Architecture", "Database ER Design\nNext.js API Routes\nAppShell & Layout\nMock Data Seed", "#DCFCE7", "#15803D"),
        ("Reporting 3: Core & AI", "AR Canvas Engine\nVoice Recognition\nVision Tool Verifier\nDexie.js Sync Engine", "#FEF08A", "#A16207"),
        ("Reporting 4: Finalization", "Supervisor Analytics\nAutomated Testing\nMulti-Device UAT\nProduction Deployment", "#FCE7F3", "#9D174D"),
    ]

    sb_w = 460
    sb_h = 240
    sb_y = loop_y + 90
    sb_xs = [110, 610, 1110, 1610]

    for idx, (stitle, scontent, sbg, sbdr) in enumerate(sprint_boxes):
        sx = sb_xs[idx]
        draw_rounded_rect(draw, [sx, sb_y, sx + sb_w, sb_y + sb_h], radius=12, fill=sbg, outline=sbdr, width=2)
        draw.text((sx + sb_w // 2, sb_y + 35), stitle, fill="#0F172A", font=fonts["head"], anchor="mm")
        draw.text((sx + 40, sb_y + 80), scontent, fill="#334155", font=fonts["body"], spacing=8)
        if idx < 3:
            draw_arrow(draw, (sx + sb_w, sb_y + sb_h // 2), (sb_xs[idx + 1], sb_y + sb_h // 2), color="#64748B", width=3)

    img.save(out_path, quality=95)
    print(f"Saved Figure 5.1: {out_path}")

# ==============================================================================
# Diagram: Figure 6.3 Relational Database Schema & Class UML Diagram
# ==============================================================================
def create_fig_6_3_er_uml(out_path):
    W, H = 2200, 1300
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts(sz_title=34, sz_head=20, sz_sub=16, sz_body=13, sz_sm=11)

    # Header
    draw.rectangle([0, 0, W, 85], fill="#0F172A")
    draw.text((W // 2, 42), "Figure 6.3: Relational Database Schema (PostgreSQL/Supabase) & Entity Relationships", 
              fill="#FFFFFF", font=fonts["title"], anchor="mm")

    tables = [
        # (title, fields, x, y, w, h, header_color)
        ("factories", ["id: UUID (PK)", "name: VARCHAR(100)", "location: VARCHAR(100)", "created_at: TIMESTAMPTZ"], 60, 130, 420, 240, "#2563EB"),
        ("profiles", ["id: UUID (PK, FK auth.users)", "factory_id: UUID (FK factories)", "full_name: VARCHAR(100)", "email: VARCHAR(100)", "role: 'tech'|'supervisor'|'admin'"], 540, 130, 480, 260, "#2563EB"),
        ("machines", ["id: UUID (PK)", "factory_id: UUID (FK factories)", "name: VARCHAR(100)", "model: VARCHAR(50)", "qr_code: VARCHAR(100)", "status: 'operational'|'maintenance'", "health_score: INTEGER"], 1080, 130, 500, 290, "#16A34A"),
        ("repair_procedures", ["id: UUID (PK)", "machine_id: UUID (FK machines)", "title: VARCHAR(150)", "category: VARCHAR(50)", "estimated_time_mins: INT", "steps_json: JSONB"], 1640, 130, 500, 270, "#16A34A"),
        
        ("fault_reports", ["id: UUID (PK)", "factory_id: UUID (FK)", "machine_id: UUID (FK)", "reported_by: UUID (FK)", "assigned_to: UUID (FK)", "severity: 'low'|'med'|'high'", "status: 'pending'|'in_progress'|'closed'"], 60, 520, 460, 310, "#DC2626"),
        ("maintenance_logs", ["id: UUID (PK)", "procedure_id: UUID (FK)", "machine_id: UUID (FK)", "technician_id: UUID (FK)", "status: 'in_progress'|'completed'", "duration_seconds: INTEGER", "notes: TEXT", "created_at: TIMESTAMPTZ"], 580, 520, 480, 320, "#7C3AED"),
        ("maintenance_evidence", ["id: UUID (PK)", "log_id: UUID (FK maintenance_logs)", "image_url: TEXT", "caption: VARCHAR(255)", "created_at: TIMESTAMPTZ"], 1120, 520, 460, 240, "#7C3AED"),
        ("parts", ["id: UUID (PK)", "factory_id: UUID (FK)", "part_number: VARCHAR(50)", "name: VARCHAR(100)", "stock_quantity: INTEGER", "min_stock_level: INTEGER", "barcode: VARCHAR(100)"], 1640, 520, 500, 280, "#D97706"),
        ("parts_used", ["id: UUID (PK)", "log_id: UUID (FK logs)", "part_id: UUID (FK parts)", "quantity_used: INTEGER"], 1640, 880, 500, 220, "#D97706"),
        ("preventive_schedules", ["id: UUID (PK)", "machine_id: UUID (FK)", "procedure_id: UUID (FK)", "interval_days: INTEGER", "next_due_date: DATE"], 580, 920, 480, 220, "#0891B2"),
    ]

    for title, fields, x, y, w, h, color in tables:
        draw_rounded_rect(draw, [x, y, x + w, y + h], radius=10, fill="#FFFFFF", outline=color, width=2)
        draw_rounded_rect(draw, [x, y, x + w, y + 45], radius=10, fill=color)
        draw.text((x + 20, y + 22), title, fill="#FFFFFF", font=fonts["head"], anchor="lm")
        
        fy = y + 60
        for fld in fields:
            draw.text((x + 20, fy), fld, fill="#1E293B", font=fonts["body"])
            fy += 32

    # Draw Relationship Lines
    draw_arrow(draw, (480, 210), (540, 210), color="#2563EB", width=3) # factory -> profiles
    draw_arrow(draw, (1020, 210), (1080, 210), color="#16A34A", width=3) # profiles/factory -> machines
    draw_arrow(draw, (1580, 210), (1640, 210), color="#16A34A", width=3) # machines -> procedures
    draw_arrow(draw, (820, 450), (820, 520), color="#7C3AED", width=3) # profiles/machines -> maintenance_logs
    draw_arrow(draw, (1060, 620), (1120, 620), color="#7C3AED", width=3) # logs -> evidence
    draw_arrow(draw, (1890, 800), (1890, 880), color="#D97706", width=3) # parts -> parts_used
    draw_arrow(draw, (520, 650), (580, 650), color="#DC2626", width=3) # faults -> logs

    # Bottom notes
    draw.rectangle([60, 1180, W - 60, 1260], fill="#F1F5F9", outline="#CBD5E1", width=1)
    draw.text((W // 2, 1220), "Row Level Security (RLS) policies enforce factory tenant boundaries: CREATE POLICY factory_isolation ON <table> FOR ALL USING (factory_id = auth.jwt() ->> 'factory_id');", 
              fill="#334155", font=fonts["sub"], anchor="mm")

    img.save(out_path, quality=95)
    print(f"Saved Figure 6.3: {out_path}")

# ==============================================================================
# Diagram: Figure 6.4 Major Interface Architecture & UI Hierarchy
# ==============================================================================
def create_fig_6_4_ui_design(out_path):
    W, H = 2200, 1100
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts(sz_title=34, sz_head=20, sz_sub=16, sz_body=13, sz_sm=12)

    # Header
    draw.rectangle([0, 0, W, 85], fill="#0F172A")
    draw.text((W // 2, 42), "Figure 6.4: MaintAI UI Navigation Hierarchy & Responsive Screen Architecture", 
              fill="#FFFFFF", font=fonts["title"], anchor="mm")

    screens = [
        ("AppShell & Navigation", "Persistent TopBar & BottomBar\n• Role-based access badges\n• Live network offline status\n• Quick QR scanner launcher", 60, 140, 380, 240, "#1E293B"),
        ("Machine Scanner & Specs", "/scan & /repair/[id]\n• Live video viewfinder\n• Machine specs & health\n• Active operational alerts\n• Procedure picker list", 480, 140, 380, 240, "#0284C7"),
        ("AR Repair Step Viewer", "/repair/[id]/step/[step]\n• Pulsing canvas overlays\n• Voice control listener\n• Lockout safety checklists\n• Next / Prev controls", 900, 140, 380, 240, "#D97706"),
        ("AI Tool Verifier Modal", "ToolDetector Component\n• Camera still snapshot\n• Gemini 1.5 Flash Vision\n• Bounding box overlay\n• Step unlocking gate", 1320, 140, 380, 240, "#7C3AED"),
        ("Supervisor Dashboard", "/analytics & /dashboard\n• Plant MTTR & MTBF cards\n• Downtime distribution chart\n• Technician leaderboard\n• Health index rankings", 1740, 140, 380, 240, "#16A34A"),
        
        ("Fault Triage & Inbox", "/inbox & /fault-report\n• Priority severity tags\n• Photo evidence viewer\n• One-click tech assignment\n• Direct repair jump link", 270, 460, 440, 240, "#DC2626"),
        ("Parts Inventory & Scan", "/parts\n• Real-time stock counts\n• Low stock warning badges\n• Barcode verification\n• Auto-restock requests", 880, 460, 440, 240, "#CA8A04"),
        ("Manuals & FixBot AI", "/manuals & /chat\n• Client PDF rendering\n• Offline document cache\n• Contextual chat assistant\n• Symptom troubleshooting", 1490, 460, 440, 240, "#0D9488"),
    ]

    for title, desc, x, y, w, h, color in screens:
        draw_rounded_rect(draw, [x, y, x + w, y + h], radius=14, fill="#FFFFFF", outline=color, width=3)
        draw_rounded_rect(draw, [x, y, x + w, y + 50], radius=14, fill=color)
        draw.text((x + w // 2, y + 25), title, fill="#FFFFFF", font=fonts["head"], anchor="mm")
        draw.text((x + 30, y + 80), desc, fill="#334155", font=fonts["sub"], spacing=8)

    # Bottom responsive annotations
    draw_rounded_rect(draw, [60, 780, W - 60, 1020], radius=16, fill="#F8FAFC", outline="#94A3B8", width=2)
    draw.text((W // 2, 825), "Responsive Viewport Adaptation & Field Usability Design System", fill="#0F172A", font=fonts["head"], anchor="mm")
    
    notes = [
        "• Mobile Optimized: 48px+ touch targets for gloved shop-floor operation and high-contrast dark/light UI themes.",
        "• Hands-Free Ergonomics: Web Speech API voice control eliminates touchscreen contact during messy mechanical tasks.",
        "• Viewport Scaling: Canvas overlays dynamically normalize coordinate percentages (0–100%) to prevent aspect ratio drift."
    ]
    ny = 875
    for note in notes:
        draw.text((120, ny), note, fill="#334155", font=fonts["sub"])
        ny += 42

    img.save(out_path, quality=95)
    print(f"Saved Figure 6.4: {out_path}")

if __name__ == "__main__":
    os.makedirs("pdf_images", exist_ok=True)
    create_fig_5_1_workflow(r"pdf_images/fig_5_1_workflow.png")
    create_fig_6_3_er_uml(r"pdf_images/fig_6_3_er_uml.png")
    create_fig_6_4_ui_design(r"pdf_images/fig_6_4_ui_design.png")
    print("All additional figures generated successfully!")
