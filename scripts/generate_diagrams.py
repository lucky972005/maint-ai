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

def wrap_text(text, font, max_width):
    paragraphs = text.split("\n")
    all_lines = []
    for para in paragraphs:
        if not para.strip():
            all_lines.append("")
            continue
        words = para.split(" ")
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word]) if current_line else word
            bbox = font.getbbox(test_line)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    all_lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            all_lines.append(" ".join(current_line))
    return all_lines

def draw_wrapped_text(draw, text, x, y, max_width, font, fill, line_spacing=5):
    lines = wrap_text(text, font, max_width)
    cur_y = y
    for line in lines:
        draw.text((x, cur_y), line, fill=fill, font=font)
        bbox = font.getbbox(line)
        h = bbox[3] - bbox[1]
        cur_y += h + line_spacing
    return cur_y

# ==============================================================================
# Diagram 1: Updated 3-Tier System Architecture Diagram
# ==============================================================================
def create_system_architecture_diagram(out_path):
    W, H = 2200, 1300
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts(sz_title=34, sz_head=22, sz_sub=17, sz_body=13.5, sz_sm=13)

    # Main Header
    draw.rectangle([0, 0, W, 85], fill="#0F172A")
    draw.text((W // 2, 42), "Figure 5.1: MaintAI — 3-Tier System Architecture & Cloud Infrastructure", 
              fill="#FFFFFF", font=fonts["title"], anchor="mm")

    # Column / Tier Dimensions
    tier_w = 640
    tier_h = 1140
    top_y = 120
    x_gap = 90
    x_offset = 60

    # TIER 1: CLIENT PWA
    x1 = x_offset
    draw_rounded_rect(draw, [x1, top_y, x1 + tier_w, top_y + tier_h], radius=16, fill="#F0FDF4", outline="#16A34A", width=3)
    draw_rounded_rect(draw, [x1, top_y, x1 + tier_w, top_y + 65], radius=16, fill="#16A34A")
    draw.text((x1 + tier_w // 2, top_y + 32), "TIER 1: Client Presentation Layer (PWA)", fill="#FFFFFF", font=fonts["head"], anchor="mm")

    boxes_tier1 = [
        ("Next.js 14 App Router & AppShell", "React 18 components, Tailwind CSS styling, responsive layout for mobile & desktop viewports.", "#DCFCE7", "#15803D"),
        ("AR Overlay Engine (HTML5 Canvas)", "Percentage-based pulsing crosshairs, bounding boxes, live camera viewport overlay.", "#DCFCE7", "#15803D"),
        ("Hands-Free Voice Control (Web Speech API)", "Acoustic speech recognition (Next, Previous, Safety, Help), text-to-speech audio feedback.", "#DCFCE7", "#15803D"),
        ("Camera Hardware Integration (MediaDevices)", "html5-qrcode barcode scanning & high-res image capture for AI tool verification gate.", "#DCFCE7", "#15803D"),
        ("Workbox Service Worker Caching", "Precached static bundles, StaleWhileRevalidate strategy for equipment manuals and offline app shell.", "#DCFCE7", "#15803D"),
        ("Dexie.js Client-Side IndexedDB Storage", "Local database: offline machines, procedures, parts, and write-ahead sync queue.", "#FEF08A", "#A16207"),
    ]
    cur_y = top_y + 85
    for title, desc, bg, bdr in boxes_tier1:
        box_h = 145
        draw_rounded_rect(draw, [x1 + 25, cur_y, x1 + tier_w - 25, cur_y + box_h], radius=10, fill=bg, outline=bdr, width=2)
        draw.text((x1 + 45, cur_y + 18), title, fill="#0F172A", font=fonts["sub"])
        draw_wrapped_text(draw, desc, x1 + 45, cur_y + 55, tier_w - 90, fonts["body"], "#334155", line_spacing=4)
        cur_y += 170

    # TIER 2: SERVERLESS API GATEWAY
    x2 = x1 + tier_w + x_gap
    draw_rounded_rect(draw, [x2, top_y, x2 + tier_w, top_y + tier_h], radius=16, fill="#EFF6FF", outline="#2563EB", width=3)
    draw_rounded_rect(draw, [x2, top_y, x2 + tier_w, top_y + 65], radius=16, fill="#2563EB")
    draw.text((x2 + tier_w // 2, top_y + 32), "TIER 2: Serverless Application & API Layer", fill="#FFFFFF", font=fonts["head"], anchor="mm")

    boxes_tier2 = [
        ("Next.js 14 API Route Handlers (/app/api/*)", "Serverless endpoints: /machines, /procedures, /parts, /faults, /verify-tool.", "#DBEAFE", "#1D4ED8"),
        ("Authentication & RBAC Middleware", "Middleware route protection, JWT token validation, role guards (Tech / Supervisor / Admin).", "#DBEAFE", "#1D4ED8"),
        ("Zod Input Validation & Schema Enforcement", "Strict runtime request schema validation for work logs, fault reports & telemetry inputs.", "#DBEAFE", "#1D4ED8"),
        ("Multi-Provider AI Abstraction (lib/ai.ts)", "Unified router connecting OpenAI GPT-4o, Gemini 1.5 Flash, Groq with auto-fallback.", "#DBEAFE", "#1D4ED8"),
        ("Predictive Health Scoring Engine", "Calculates machine health index, failure distribution & MTTR analytics for supervisors.", "#DBEAFE", "#1D4ED8"),
        ("Deterministic Local Mock Fallback", "In-memory demo state guaranteeing 100% uptime during network dropouts or missing keys.", "#FEF08A", "#A16207"),
    ]
    cur_y = top_y + 85
    for title, desc, bg, bdr in boxes_tier2:
        box_h = 145
        draw_rounded_rect(draw, [x2 + 25, cur_y, x2 + tier_w - 25, cur_y + box_h], radius=10, fill=bg, outline=bdr, width=2)
        draw.text((x2 + 45, cur_y + 18), title, fill="#0F172A", font=fonts["sub"])
        draw_wrapped_text(draw, desc, x2 + 45, cur_y + 55, tier_w - 90, fonts["body"], "#334155", line_spacing=4)
        cur_y += 170

    # TIER 3: CLOUD SERVICES & AI BACKEND
    x3 = x2 + tier_w + x_gap
    draw_rounded_rect(draw, [x3, top_y, x3 + tier_w, top_y + tier_h], radius=16, fill="#FAF5FF", outline="#7C3AED", width=3)
    draw_rounded_rect(draw, [x3, top_y, x3 + tier_w, top_y + 65], radius=16, fill="#7C3AED")
    draw.text((x3 + tier_w // 2, top_y + 32), "TIER 3: Cloud Infrastructure & AI Backend", fill="#FFFFFF", font=fonts["head"], anchor="mm")

    boxes_tier3 = [
        ("Supabase PostgreSQL Database", "10 Relational tables: factories, machines, procedures, logs, fault_reports, parts, etc.", "#F3E8FF", "#6D28D9"),
        ("Supabase Row Level Security (RLS)", "Database-enforced multi-tenant isolation scoped strictly by factory tenant & user role.", "#F3E8FF", "#6D28D9"),
        ("Supabase Auth & Session Storage", "JWT issuance, refresh tokens, cookie-based session verification & password encryption.", "#F3E8FF", "#6D28D9"),
        ("Supabase Object Storage", "Encrypted storage buckets for maintenance photo evidence & equipment manual PDFs.", "#F3E8FF", "#6D28D9"),
        ("Google Gemini 1.5 Flash Vision API", "Multimodal high-speed visual tool verification & machine component identification.", "#FCE7F3", "#BE185D"),
        ("OpenAI GPT-4o & Groq Language Engine", "Conversational FixBot troubleshooting assistant & automated procedure step generation.", "#FCE7F3", "#BE185D"),
    ]
    cur_y = top_y + 85
    for title, desc, bg, bdr in boxes_tier3:
        box_h = 145
        draw_rounded_rect(draw, [x3 + 25, cur_y, x3 + tier_w - 25, cur_y + box_h], radius=10, fill=bg, outline=bdr, width=2)
        draw.text((x3 + 45, cur_y + 18), title, fill="#0F172A", font=fonts["sub"])
        draw_wrapped_text(draw, desc, x3 + 45, cur_y + 55, tier_w - 90, fonts["body"], "#334155", line_spacing=4)
        cur_y += 170

    # Connectors between Tier 1 and Tier 2
    draw_arrow(draw, (x1 + tier_w, top_y + 155), (x2, top_y + 155), color="#2563EB", width=4)
    draw_rounded_rect(draw, [x1 + tier_w + 10, top_y + 130, x2 - 10, top_y + 180], radius=6, fill="#FFFFFF", outline="#2563EB", width=2)
    draw.text(((x1 + tier_w + x2) // 2, top_y + 155), "HTTPS REST", fill="#1E40AF", font=fonts["sm_bold"], anchor="mm")

    draw_arrow(draw, (x1 + tier_w, top_y + 1000), (x2, top_y + 1000), color="#D97706", width=4)
    draw_rounded_rect(draw, [x1 + tier_w + 10, top_y + 975, x2 - 10, top_y + 1025], radius=6, fill="#FFFFFF", outline="#D97706", width=2)
    draw.text(((x1 + tier_w + x2) // 2, top_y + 1000), "Sync Queue", fill="#B45309", font=fonts["sm_bold"], anchor="mm")

    # Connectors between Tier 2 and Tier 3
    draw_arrow(draw, (x2 + tier_w, top_y + 155), (x3, top_y + 155), color="#7C3AED", width=4)
    draw_rounded_rect(draw, [x2 + tier_w + 10, top_y + 130, x3 - 10, top_y + 180], radius=6, fill="#FFFFFF", outline="#7C3AED", width=2)
    draw.text(((x2 + tier_w + x3) // 2, top_y + 155), "Postgres / SQL", fill="#6D28D9", font=fonts["sm_bold"], anchor="mm")

    draw_arrow(draw, (x2 + tier_w, top_y + 665), (x3, top_y + 665), color="#BE185D", width=4)
    draw_rounded_rect(draw, [x2 + tier_w + 10, top_y + 640, x3 - 10, top_y + 690], radius=6, fill="#FFFFFF", outline="#BE185D", width=2)
    draw.text(((x2 + tier_w + x3) // 2, top_y + 665), "AI Vision / Text", fill="#9D174D", font=fonts["sm_bold"], anchor="mm")

    img.save(out_path, quality=95)
    print(f"Saved system architecture diagram: {out_path}")

# ==============================================================================
# Diagram 2: Figure 5.2 — End-to-End Maintenance & AR Repair Process Flow
# ==============================================================================
def create_repair_workflow_diagram(out_path):
    W, H = 2200, 1150
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts(sz_title=34, sz_head=17, sz_sub=15, sz_body=13, sz_sm=12)

    # Header
    draw.rectangle([0, 0, W, 85], fill="#0F172A")
    draw.text((W // 2, 42), "Figure 5.2: End-to-End AR-Guided Maintenance & Inspection Process Flow", 
              fill="#FFFFFF", font=fonts["title"], anchor="mm")

    # Workflow Steps across 2 Rows (5 Steps per row)
    box_w, box_h = 370, 245
    y_r1 = 140
    y_r2 = 560
    x_positions = [60, 480, 900, 1320, 1740]

    steps_r1 = [
        ("Step 1: Machine Discovery", 
         "Technician scans physical machine QR tag using camera (/scan) or takes photo for multimodal AI recognition.", 
         "#E0F2FE", "#0284C7"),
        ("Step 2: Record Resolution", 
         "System pulls machine specs, active operational alerts, fault history, and available procedures (/repair/[id]).", 
         "#E0F2FE", "#0284C7"),
        ("Step 3: Procedure Selection", 
         "Technician selects maintenance task (e.g., Oil Change, Belt Replacement) and reviews safety requirements.", 
         "#E0F2FE", "#0284C7"),
        ("Step 4: AR Step Execution", 
         "HTML5 Canvas renders animated pulsing target markers over the live camera feed with visual step instructions.", 
         "#FEF3C7", "#D97706"),
        ("Step 5: Safety Checkpoint", 
         "System prompts lockout/tagout (LOTO) protocol verification before advancing into mechanical components.", 
         "#FEE2E2", "#DC2626"),
    ]

    for idx, (title, desc, bg, bdr) in enumerate(steps_r1):
        x = x_positions[idx]
        draw_rounded_rect(draw, [x, y_r1, x + box_w, y_r1 + box_h], radius=14, fill=bg, outline=bdr, width=3)
        draw_rounded_rect(draw, [x, y_r1, x + box_w, y_r1 + 45], radius=14, fill=bdr)
        draw.text((x + box_w // 2, y_r1 + 22), title, fill="#FFFFFF", font=fonts["head"], anchor="mm")
        
        # Wrapped description inside box body
        draw_wrapped_text(draw, desc, x + 20, y_r1 + 65, box_w - 40, fonts["body"], "#1E293B", line_spacing=5)
        
        if idx < 4:
            draw_arrow(draw, (x + box_w, y_r1 + box_h // 2), (x_positions[idx + 1], y_r1 + box_h // 2), color="#0284C7", width=4)

    # Connector down from Step 5 (Row 1 rightmost) to Step 6 (Row 2 rightmost)
    draw_arrow(draw, (x_positions[4] + box_w // 2, y_r1 + box_h), (x_positions[4] + box_w // 2, y_r2), color="#DC2626", width=4)

    # Row 2: Right-to-Left execution: Step 6 (rightmost) -> Step 7 -> Step 8 -> Step 9 -> Step 10 (leftmost)
    steps_r2 = [
        ("Step 6: AI Tool Verification", 
         "Technician presents required tool (e.g. torque wrench) to camera; AI vision validates correct tool before step unlock.", 
         "#F3E8FF", "#7C3AED"),
        ("Step 7: Voice / Touch Advance", 
         "Technician speaks voice commands ('Next', 'Previous', 'Help') or taps on-screen buttons to navigate.", 
         "#E0F2FE", "#0284C7"),
        ("Step 8: Work Log Completion", 
         "Technician records notes, logs consumed spare parts with barcode validation, and attaches completion photo.", 
         "#E0F2FE", "#0284C7"),
        ("Step 9: Sync & Cloud Commit", 
         "Dexie.js pushes queued log to Supabase PostgreSQL database; uploaded evidence stored in Supabase Storage.", 
         "#DCFCE7", "#16A34A"),
        ("Step 10: Supervisor Analytics", 
         "KPI dashboard recalculates plant MTTR, downtime trends, technician leaderboards, and machine health scores.", 
         "#E0F2FE", "#0284C7"),
    ]

    for idx, (title, desc, bg, bdr) in enumerate(steps_r2):
        pos_idx = 4 - idx # Step 6 at pos 4, Step 7 at pos 3, Step 8 at pos 2, Step 9 at pos 1, Step 10 at pos 0
        x = x_positions[pos_idx]
        draw_rounded_rect(draw, [x, y_r2, x + box_w, y_r2 + box_h], radius=14, fill=bg, outline=bdr, width=3)
        draw_rounded_rect(draw, [x, y_r2, x + box_w, y_r2 + 45], radius=14, fill=bdr)
        draw.text((x + box_w // 2, y_r2 + 22), title, fill="#FFFFFF", font=fonts["head"], anchor="mm")
        
        # Wrapped description inside box body
        draw_wrapped_text(draw, desc, x + 20, y_r2 + 65, box_w - 40, fonts["body"], "#1E293B", line_spacing=5)
        
        if idx < 4:
            # Arrow pointing left towards the next step
            next_pos_idx = 4 - (idx + 1)
            draw_arrow(draw, (x, y_r2 + box_h // 2), (x_positions[next_pos_idx] + box_w, y_r2 + box_h // 2), color="#16A34A", width=4)

    # Next Step Loop: Arrow pointing straight UP from Step 7 (pos 3 in row 2) back to Step 4 (pos 3 in row 1)
    step7_cx = x_positions[3] + box_w // 2
    draw_arrow(draw, (step7_cx, y_r2), (step7_cx, y_r1 + box_h), color="#D97706", width=4)
    # Loop Badge in the middle of the vertical connector
    badge_w, badge_h = 240, 48
    badge_x = step7_cx - badge_w // 2
    badge_y = (y_r1 + box_h + y_r2) // 2 - badge_h // 2
    draw_rounded_rect(draw, [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=8, fill="#FFFBEB", outline="#D97706", width=2)
    draw.text((step7_cx, badge_y + badge_h // 2), "Next Step Loop (Steps 4–7)", fill="#B45309", font=fonts["sm_bold"], anchor="mm")

    # Step loop banner at bottom
    loop_y = 880
    draw_rounded_rect(draw, [60, loop_y, W - 60, loop_y + 80], radius=12, fill="#F8FAFC", outline="#64748B", width=2)
    draw.text((W // 2, loop_y + 40), "Interactive Maintenance Loop: Technicians cycle through Steps 4–7 for each procedure step until all stages are confirmed complete.", 
              fill="#0F172A", font=fonts["sub"], anchor="mm")

    img.save(out_path, quality=95)
    print(f"Saved Figure 5.2 repair workflow diagram: {out_path}")

# ==============================================================================
# Diagram 3: Figure 7.3 — Offline-First Synchronization Architecture
# ==============================================================================
def create_offline_sync_diagram(out_path):
    W, H = 2200, 1150
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts(sz_title=34, sz_head=20, sz_sub=15, sz_body=13.5, sz_sm=12)

    # Header
    draw.rectangle([0, 0, W, 85], fill="#0F172A")
    draw.text((W // 2, 42), "Figure 7.3: MaintAI — Offline-First Architecture & Background Sync Pipeline", 
              fill="#FFFFFF", font=fonts["title"], anchor="mm")

    # Left Container: Device Offline Operations
    container_w = 950
    container_h = 940
    top_y = 120
    draw_rounded_rect(draw, [60, top_y, 60 + container_w, top_y + container_h], radius=16, fill="#FFFBEB", outline="#D97706", width=3)
    draw_rounded_rect(draw, [60, top_y, 60 + container_w, top_y + 60], radius=16, fill="#D97706")
    draw.text((60 + container_w // 2, top_y + 30), "SHOP-FLOOR CLIENT: Offline / Poor Connectivity State", fill="#FFFFFF", font=fonts["head"], anchor="mm")

    off_boxes = [
        ("IndexedDB Local Data Store (Dexie.js)", 
         "• Pre-cached Assets: Stores machine schemas, repair procedures, parts catalog & PDF manuals.\n"
         "• Sub-5ms Queries: Executes instantaneous local lookups with zero reliance on cellular or Wi-Fi signals.\n"
         "• Quota Management: Browser StorageManager API allocates persistent client storage partitions.", 
         "#FEF3C7", "#B45309", "#78350F"),
        ("Write-Ahead Sync Queue (WAL & Dexie Store)", 
         "• Transaction Serialization: Every work log entry and fault report is recorded as an atomic mutation.\n"
         "• Idempotency Keys: Client generates UUID v4 idempotency keys to prevent duplicate cloud records.\n"
         "• Strict FIFO Replay: Pending queue preserves chronological transaction order across shift changes.", 
         "#FEF3C7", "#B45309", "#78350F"),
        ("Offline App Shell & Real-Time Sync Indicator", 
         "• Service Worker Cache: Workbox precaches application shell, icons, and Next.js route bundles.\n"
         "• Ambient Connection Status: UI banner dynamically tracks navigator.onLine and WebSocket heartbeats.\n"
         "• Non-Blocking UX: Maintenance forms allow continuous offline input without loading spinners.", 
         "#FEF3C7", "#B45309", "#78350F"),
    ]
    cur_y = top_y + 85
    box_inner_w = container_w - 70
    box_inner_h = 260
    for title, desc, bg, bdr, text_col in off_boxes:
        bx = 95
        draw_rounded_rect(draw, [bx, cur_y, bx + box_inner_w, cur_y + box_inner_h], radius=12, fill=bg, outline=bdr, width=2)
        draw_rounded_rect(draw, [bx, cur_y, bx + box_inner_w, cur_y + 45], radius=12, fill=bdr)
        draw.text((bx + box_inner_w // 2, cur_y + 22), title, fill="#FFFFFF", font=fonts["head"], anchor="mm")
        
        # Wrapped text cleanly within inner box
        draw_wrapped_text(draw, desc, bx + 25, cur_y + 60, box_inner_w - 50, fonts["body"], text_col, line_spacing=6)
        cur_y += 285

    # Right Container: Online Reconnect & Cloud Reconciliation
    rx = W - 60 - container_w
    draw_rounded_rect(draw, [rx, top_y, rx + container_w, top_y + container_h], radius=16, fill="#F0FDF4", outline="#16A34A", width=3)
    draw_rounded_rect(draw, [rx, top_y, rx + container_w, top_y + 60], radius=16, fill="#16A34A")
    draw.text((rx + container_w // 2, top_y + 30), "CLOUD BACKEND: Background Reconciliation on Reconnect", fill="#FFFFFF", font=fonts["head"], anchor="mm")

    on_boxes = [
        ("Network Reconnection Event Listener", 
         "• Event Triggers: window.addEventListener('online') wakes background synchronization workers.\n"
         "• Connection Verification: Active HTTP ping verifies genuine internet reachability before sync starts.\n"
         "• Debounce Protection: 500ms debounce guard prevents burst re-triggering during spotty signals.", 
         "#DCFCE7", "#15803D", "#14532D"),
        ("Atomic Batch Processor with Exponential Backoff", 
         "• Bulk Mutation Ingestion: Dequeues pending client actions in atomic batches of up to 25 records.\n"
         "• Resilient Retry Policy: Exponential backoff with jitter (1s, 2s, 4s, 8s) recovers from transient 5xx faults.\n"
         "• Payload Validation: Zod schema validators ensure malformed client mutations are quarantined cleanly.", 
         "#DCFCE7", "#15803D", "#14532D"),
        ("Supabase PostgreSQL Commit & Cache Invalidation", 
         "• ACID Data Persistence: Commits maintenance logs, audit timestamps, and inventory stock deductions.\n"
         "• Tenant Boundary Security: PostgreSQL Row Level Security (RLS) strictly enforces factory isolation.\n"
         "• ACK Handshake: Server returns authoritative DB IDs; client acknowledges and purges WAL queue.", 
         "#DCFCE7", "#15803D", "#14532D"),
    ]
    cur_y = top_y + 85
    for title, desc, bg, bdr, text_col in on_boxes:
        bx = rx + 35
        draw_rounded_rect(draw, [bx, cur_y, bx + box_inner_w, cur_y + box_inner_h], radius=12, fill=bg, outline=bdr, width=2)
        draw_rounded_rect(draw, [bx, cur_y, bx + box_inner_w, cur_y + 45], radius=12, fill=bdr)
        draw.text((bx + box_inner_w // 2, cur_y + 22), title, fill="#FFFFFF", font=fonts["head"], anchor="mm")
        
        # Wrapped text cleanly within inner box
        draw_wrapped_text(draw, desc, bx + 25, cur_y + 60, box_inner_w - 50, fonts["body"], text_col, line_spacing=6)
        cur_y += 285

    # Middle Sync Bridge Arrows (Between Left and Right Containers)
    mid_x1 = 60 + container_w
    mid_x2 = rx
    mid_cx = (mid_x1 + mid_x2) // 2

    # Top Arrow: Auto Sync forward
    draw_arrow(draw, (mid_x1, 460), (mid_x2, 460), color="#16A34A", width=5)
    draw_rounded_rect(draw, [mid_cx - 65, 425, mid_cx + 65, 495], radius=8, fill="#FFFFFF", outline="#16A34A", width=2)
    draw.text((mid_cx, 460), "AUTO SYNC", fill="#16A34A", font=fonts["sm_bold"], anchor="mm")

    # Bottom Arrow: Ack / Purge reverse
    draw_arrow(draw, (mid_x2, 760), (mid_x1, 760), color="#2563EB", width=5)
    draw_rounded_rect(draw, [mid_cx - 65, 725, mid_cx + 65, 795], radius=8, fill="#FFFFFF", outline="#2563EB", width=2)
    draw.text((mid_cx, 760), "ACK / PURGE", fill="#2563EB", font=fonts["sm_bold"], anchor="mm")

    img.save(out_path, quality=95)
    print(f"Saved Figure 7.3 offline sync diagram: {out_path}")

if __name__ == "__main__":
    os.makedirs("pdf_images", exist_ok=True)
    create_system_architecture_diagram(r"pdf_images/updated_architecture_diagram.png")
    create_repair_workflow_diagram(r"pdf_images/updated_repair_workflow.png")
    create_offline_sync_diagram(r"pdf_images/updated_offline_sync_workflow.png")
    print("All diagrams regenerated with perfect text wrapping and clean box boundaries!")
