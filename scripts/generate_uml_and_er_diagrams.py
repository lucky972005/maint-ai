import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_PATH_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_PATH_SEMI = r"C:\Windows\Fonts\segoeuisl.ttf"

def get_fonts(sz_title=32, sz_head=20, sz_sub=15, sz_body=13, sz_sm=11, sz_badge=10):
    return {
        "title": ImageFont.truetype(FONT_PATH_BOLD, sz_title),
        "head": ImageFont.truetype(FONT_PATH_BOLD, sz_head),
        "sub": ImageFont.truetype(FONT_PATH_BOLD, sz_sub),
        "body": ImageFont.truetype(FONT_PATH_REG, sz_body),
        "body_bold": ImageFont.truetype(FONT_PATH_BOLD, sz_body),
        "sm": ImageFont.truetype(FONT_PATH_REG, sz_sm),
        "sm_bold": ImageFont.truetype(FONT_PATH_BOLD, sz_sm),
        "badge": ImageFont.truetype(FONT_PATH_BOLD, sz_badge),
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
        # Approximate angle
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - arrow_size * 1.5 * math.cos(angle - 0.5), y2 - arrow_size * 1.5 * math.sin(angle - 0.5))
        p2 = (x2 - arrow_size * 1.5 * math.cos(angle + 0.5), y2 - arrow_size * 1.5 * math.sin(angle + 0.5))
        points = [(x2, y2), p1, p2]
    draw.polygon(points, fill=color)

def draw_dashed_arrow(draw, start, end, color="#475569", width=2, dash_len=8, arrow_size=8):
    import math
    x1, y1 = start
    x2, y2 = end
    dist = math.hypot(x2 - x1, y2 - y1)
    if dist == 0:
        return
    dashes = int(dist / (dash_len * 2))
    dx = (x2 - x1) / dist
    dy = (y2 - y1) / dist
    for i in range(dashes):
        sx = x1 + (2 * i) * dash_len * dx
        sy = y1 + (2 * i) * dash_len * dy
        ex = x1 + (2 * i + 1) * dash_len * dx
        ey = y1 + (2 * i + 1) * dash_len * dy
        draw.line([sx, sy, ex, ey], fill=color, width=width)
    # Arrow head at end
    angle = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - arrow_size * 1.5 * math.cos(angle - 0.5), y2 - arrow_size * 1.5 * math.sin(angle - 0.5))
    p2 = (x2 - arrow_size * 1.5 * math.cos(angle + 0.5), y2 - arrow_size * 1.5 * math.sin(angle + 0.5))
    draw.polygon([(x2, y2), p1, p2], fill=color)

def draw_stick_actor(draw, cx, cy, name, role_desc, fonts, color="#0F2A5C"):
    # Head
    r = 22
    draw.ellipse([cx - r, cy - 45, cx + r, cy - 1], outline=color, width=3, fill="#F8FAFC")
    # Body
    draw.line([cx, cy, cx, cy + 50], fill=color, width=3)
    # Arms
    draw.line([cx - 30, cy + 18, cx + 30, cy + 18], fill=color, width=3)
    # Legs
    draw.line([cx, cy + 50, cx - 25, cy + 95], fill=color, width=3)
    draw.line([cx, cy + 50, cx + 25, cy + 95], fill=color, width=3)
    # Label
    draw.text((cx, cy + 110), name, fill=color, font=fonts["head"], anchor="mm")
    draw.text((cx, cy + 132), role_desc, fill="#64748B", font=fonts["sm"], anchor="mm")

def draw_use_case_oval(draw, cx, cy, w, h, text, fonts, bg="#F0FDF4", bdr="#16A34A"):
    draw.ellipse([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], fill=bg, outline=bdr, width=2)
    lines = text.split("\n")
    if len(lines) == 1:
        draw.text((cx, cy), lines[0], fill="#0F172A", font=fonts["body_bold"], anchor="mm")
    elif len(lines) == 2:
        draw.text((cx, cy - 10), lines[0], fill="#0F172A", font=fonts["body_bold"], anchor="mm")
        draw.text((cx, cy + 10), lines[1], fill="#1E293B", font=fonts["body"], anchor="mm")
    elif len(lines) == 3:
        draw.text((cx, cy - 18), lines[0], fill="#0F172A", font=fonts["body_bold"], anchor="mm")
        draw.text((cx, cy), lines[1], fill="#1E293B", font=fonts["body"], anchor="mm")
        draw.text((cx, cy + 18), lines[2], fill="#475569", font=fonts["sm"], anchor="mm")

# ==============================================================================
# 1. UML USE CASE DIAGRAM (Figure 5.3)
# ==============================================================================
def create_uml_use_case_diagram(out_path):
    W, H = 2200, 1450
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts(sz_title=34, sz_head=20, sz_sub=16, sz_body=13.5, sz_sm=12, sz_badge=11)

    # Main Header
    draw.rectangle([0, 0, W, 85], fill="#0F172A")
    draw.text((W // 2, 42), "Figure 5.3: MaintAI — UML Use Case Diagram (Actors, System Boundary & Operational Interactions)", 
              fill="#FFFFFF", font=fonts["title"], anchor="mm")

    # Actors Coordinates
    # Left: Field Technician
    draw_stick_actor(draw, 140, 480, "Field Technician", "Frontline Shop-Floor User", fonts, color="#0284C7")
    
    # Right: Supervisor (top-right), Admin (middle-right), Gemini AI (bottom-right external)
    draw_stick_actor(draw, 2060, 320, "Plant Supervisor", "Maintenance Operations Manager", fonts, color="#16A34A")
    draw_stick_actor(draw, 2060, 780, "System Admin", "Security & Tenant Manager", fonts, color="#7C3AED")
    
    # External Actor: Gemini AI
    cx_ai, cy_ai = 2060, 1180
    draw_rounded_rect(draw, [cx_ai - 100, cy_ai - 50, cx_ai + 100, cy_ai + 50], radius=12, fill="#FEF2F2", outline="#DC2626", width=2)
    draw.text((cx_ai, cy_ai - 22), "<<External AI>>", fill="#DC2626", font=fonts["sm_bold"], anchor="mm")
    draw.text((cx_ai, cy_ai), "Google Gemini 1.5", fill="#0F172A", font=fonts["head"], anchor="mm")
    draw.text((cx_ai, cy_ai + 22), "Multimodal Vision API", fill="#64748B", font=fonts["sm"], anchor="mm")

    # System Boundary Box
    sb_x1, sb_y1, sb_x2, sb_y2 = 300, 110, 1920, 1370
    draw_rounded_rect(draw, [sb_x1, sb_y1, sb_x2, sb_y2], radius=16, fill="#F8FAFC", outline="#475569", width=3)
    draw_rounded_rect(draw, [sb_x1, sb_y1, sb_x2, sb_y1 + 50], radius=16, fill="#334155")
    draw.text(((sb_x1 + sb_x2) // 2, sb_y1 + 25), "MaintAI Progressive Web Application (PWA) System Boundary", fill="#FFFFFF", font=fonts["head"], anchor="mm")

    # Sub-boundary Sections (Visual grouping)
    # Section 1: Technician & AR Guidance (Left-Center)
    # Section 2: AI & Safety Verification (Center)
    # Section 3: Data & Offline Sync (Bottom-Center)
    # Section 4: Supervisor & Management (Right-Center)

    # Use Case Ovals:
    # Column 1 (x = 560): Tech core actions
    # Column 2 (x = 1000): AR, Voice & AI Gate
    # Column 3 (x = 1440): Faults, Inventory & Logs
    # Column 4 (x = 1720): Supervisor / Admin actions

    use_cases = [
        # (ID, cx, cy, w, h, text, bg, bdr)
        # Technician Use Cases
        ("UC1", 560, 220, 360, 90, "Scan Machine QR Code\n(Camera MediaDevices)", "#EFF6FF", "#2563EB"),
        ("UC2", 560, 360, 360, 90, "View Machine Specs\n& Active Health Index", "#EFF6FF", "#2563EB"),
        ("UC3", 560, 520, 380, 100, "Execute AR Step Inspection\n(HTML5 Canvas Overlays)", "#EFF6FF", "#2563EB"),
        ("UC4", 1040, 430, 360, 90, "Hands-Free Voice Navigation\n(Web Speech API)", "#FEF3C7", "#D97706"),
        ("UC5", 1040, 610, 380, 100, "Multimodal AI Tool Verification\n(Visual Gatekeeper)", "#FDF2F8", "#DB2777"),
        ("UC6", 560, 710, 360, 90, "Deduct Consumed Parts\n& Barcode Scan", "#EFF6FF", "#2563EB"),
        ("UC7", 560, 870, 370, 95, "Offline Write-Ahead Logging\n& Auto-Reconnection Sync", "#EFF6FF", "#2563EB"),
        ("UC8", 560, 1030, 360, 90, "Submit Machine Fault Report\n& Photo Evidence", "#EFF6FF", "#2563EB"),
        ("UC9", 1040, 1180, 380, 95, "Offline IndexedDB Cache\nManagement (Dexie.js)", "#FEF3C7", "#D97706"),
        
        # Supervisor Use Cases
        ("UC10", 1540, 240, 360, 90, "Author & Update Standard\nOperating Procedures (SOPs)", "#F0FDF4", "#16A34A"),
        ("UC11", 1540, 390, 380, 95, "Triage Fault Incident Tickets\n& Dispatch Technicians", "#F0FDF4", "#16A34A"),
        ("UC12", 1540, 540, 380, 95, "Monitor Plant MTTR, MTBF\n& Machine Health Telemetry", "#F0FDF4", "#16A34A"),
        ("UC13", 1540, 690, 360, 90, "Manage Spare Parts Catalog\n& Low-Stock Alerts", "#F0FDF4", "#16A34A"),
        
        # Administrator Use Cases
        ("UC14", 1540, 860, 380, 95, "Manage Factory Tenancies\n& Multi-Tenant Boundaries", "#FAF5FF", "#7C3AED"),
        ("UC15", 1540, 1010, 380, 95, "Enforce Row Level Security\n& RBAC Auth Policies", "#FAF5FF", "#7C3AED"),
    ]

    for ucid, cx, cy, w, h, text, bg, bdr in use_cases:
        draw_use_case_oval(draw, cx, cy, w, h, text, fonts, bg=bg, bdr=bdr)

    # Actor Associations (Solid Lines)
    # Tech (140, 480) to UC1, UC2, UC3, UC6, UC7, UC8
    tech_pt = (175, 480)
    draw.line([tech_pt, (380, 220)], fill="#0284C7", width=2)
    draw.line([tech_pt, (380, 360)], fill="#0284C7", width=2)
    draw.line([tech_pt, (370, 520)], fill="#0284C7", width=2)
    draw.line([tech_pt, (380, 710)], fill="#0284C7", width=2)
    draw.line([tech_pt, (375, 870)], fill="#0284C7", width=2)
    draw.line([tech_pt, (380, 1030)], fill="#0284C7", width=2)

    # Supervisor (2060, 320) to UC10, UC11, UC12, UC13
    sup_pt = (2020, 320)
    draw.line([sup_pt, (1720, 240)], fill="#16A34A", width=2)
    draw.line([sup_pt, (1730, 390)], fill="#16A34A", width=2)
    draw.line([sup_pt, (1730, 540)], fill="#16A34A", width=2)
    draw.line([sup_pt, (1720, 690)], fill="#16A34A", width=2)

    # Admin (2060, 780) to UC14, UC15
    adm_pt = (2020, 780)
    draw.line([adm_pt, (1730, 860)], fill="#7C3AED", width=2)
    draw.line([adm_pt, (1730, 1010)], fill="#7C3AED", width=2)

    # Gemini AI (2060, 1180) to UC5
    draw.line([(1960, 1180), (1230, 610)], fill="#DC2626", width=2)
    draw.text((1600, 930), "Provides Visual Inspection JSON", fill="#DC2626", font=fonts["sm_bold"], anchor="mm")

    # Stereotypes <<include>> and <<extend>> (Dashed Arrows)
    # UC3 (AR Inspection) -> UC4 (Voice Control): <<include>>
    draw_dashed_arrow(draw, (750, 500), (860, 460), color="#D97706", width=2, arrow_size=8)
    draw.text((800, 465), "<<include>>", fill="#B45309", font=fonts["sm_bold"], anchor="mm")

    # UC3 (AR Inspection) -> UC5 (AI Tool Verifier): <<extend>>
    draw_dashed_arrow(draw, (860, 590), (750, 540), color="#DB2777", width=2, arrow_size=8)
    draw.text((805, 580), "<<extend>>", fill="#9D174D", font=fonts["sm_bold"], anchor="mm")

    # UC7 (Offline Sync) -> UC9 (IndexedDB Cache): <<include>>
    draw_dashed_arrow(draw, (745, 900), (870, 1150), color="#2563EB", width=2, arrow_size=8)
    draw.text((820, 1010), "<<include>>", fill="#1E40AF", font=fonts["sm_bold"], anchor="mm")

    # Bottom Legend / Methodology Note
    leg_y = 1270
    draw_rounded_rect(draw, [sb_x1 + 20, leg_y, sb_x2 - 20, leg_y + 80], radius=10, fill="#FFFFFF", outline="#CBD5E1", width=1)
    draw.text((sb_x1 + 40, leg_y + 25), "UML Stereotype Legend:  • <<include>> : Mandatory sub-flow executed automatically during primary use case.", fill="#334155", font=fonts["sm_bold"])
    draw.text((sb_x1 + 40, leg_y + 50), "• <<extend>> : Conditional extension activated only when procedural step requires certified safety tool validation.  • RLS : PostgreSQL tenant isolation.", fill="#64748B", font=fonts["sm"])

    img.save(out_path, quality=95)
    print(f"Saved UML Use Case Diagram: {out_path}")

# ==============================================================================
# 2. UML CLASS DIAGRAM (Figure 5.4)
# ==============================================================================
def create_uml_class_diagram(out_path):
    W, H = 2200, 1450
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts(sz_title=34, sz_head=19, sz_sub=15, sz_body=13, sz_sm=11.5, sz_badge=10)

    # Main Header
    draw.rectangle([0, 0, W, 85], fill="#0F172A")
    draw.text((W // 2, 42), "Figure 5.4: MaintAI — UML Class Diagram (Domain Model, Entities & Subsystems)", 
              fill="#FFFFFF", font=fonts["title"], anchor="mm")

    # 3-Row Class Layout
    # Row 1 (Core Assets & Procedures): Machine, RepairProcedure, RepairStep
    # Row 2 (Execution, Safety & Verification): ToolVerificationGate, MaintenanceLog, FaultReport
    # Row 3 (Inventory & Sync Queue): Part, PartUsage, SyncQueueItem

    def draw_uml_class(draw, x, y, w, title, stereotype, attributes, methods, header_bg="#0F2A5C"):
        # Calculate heights
        h_head = 45 if not stereotype else 58
        h_attr = len(attributes) * 25 + 14
        h_meth = len(methods) * 25 + 14
        total_h = h_head + h_attr + h_meth

        # Box border & background
        draw_rounded_rect(draw, [x, y, x + w, y + total_h], radius=10, fill="#FFFFFF", outline=header_bg, width=2)
        
        # Header
        draw_rounded_rect(draw, [x, y, x + w, y + h_head], radius=10, fill=header_bg)
        if stereotype:
            draw.text((x + w // 2, y + 16), stereotype, fill="#E2E8F0", font=fonts["sm_bold"], anchor="mm")
            draw.text((x + w // 2, y + 38), title, fill="#FFFFFF", font=fonts["head"], anchor="mm")
        else:
            draw.text((x + w // 2, y + h_head // 2), title, fill="#FFFFFF", font=fonts["head"], anchor="mm")

        # Attributes section
        attr_y = y + h_head
        draw.line([x, attr_y, x + w, attr_y], fill=header_bg, width=2)
        cur_y = attr_y + 8
        for attr in attributes:
            draw.text((x + 14, cur_y), attr, fill="#1E293B", font=fonts["body"])
            cur_y += 25

        # Methods section
        meth_y = attr_y + h_attr
        draw.line([x, meth_y, x + w, meth_y], fill=header_bg, width=2)
        cur_y = meth_y + 8
        for meth in methods:
            draw.text((x + 14, cur_y), meth, fill="#0F172A", font=fonts["body_bold"])
            cur_y += 25

        return total_h

    # ROW 1 (y = 120)
    # Machine Class
    mach_attrs = [
        "- id: UUID",
        "- factoryId: UUID",
        "- name: string",
        "- model: string",
        "- qrCode: string",
        "- status: MachineStatus",
        "- healthScore: integer"
    ]
    mach_meths = [
        "+ getTelemetry(): TelemetryData",
        "+ updateHealthScore(delta: int): void",
        "+ getActiveAlerts(): Alert[]",
        "+ fetchProcedures(): Procedure[]"
    ]
    draw_uml_class(draw, 60, 120, 480, "Machine", "<<Entity>>", mach_attrs, mach_meths, header_bg="#0284C7")

    # RepairProcedure Class
    proc_attrs = [
        "- id: UUID",
        "- machineId: UUID",
        "- title: string",
        "- category: string",
        "- estimatedTimeMins: int",
        "- stepsCount: int"
    ]
    proc_meths = [
        "+ getSteps(): RepairStep[]",
        "+ validatePrerequisites(): boolean",
        "+ calculateTotalDuration(): int"
    ]
    draw_uml_class(draw, 620, 120, 440, "RepairProcedure", "<<Entity>>", proc_attrs, proc_meths, header_bg="#0284C7")

    # RepairStep Class
    step_attrs = [
        "- stepNumber: int",
        "- title: string",
        "- instruction: string",
        "- requiredTool: string",
        "- targetCoords: Point2D",
        "- isLOTORequired: boolean"
    ]
    step_meths = [
        "+ renderARMarker(ctx: Canvas2D): void",
        "+ verifyToolPrerequisite(): boolean",
        "+ markCompleted(): void"
    ]
    draw_uml_class(draw, 1140, 120, 460, "RepairStep", "<<Value Object>>", step_attrs, step_meths, header_bg="#D97706")

    # ToolVerificationGate Class (Top-Right)
    gate_attrs = [
        "- targetTool: string",
        "- minConfidence: float = 0.70",
        "- isVerified: boolean",
        "- detectedBoxes: BoundingBox[]"
    ]
    gate_meths = [
        "+ evaluateFrame(blob: Blob): Promise<Result>",
        "+ parseGeminiResponse(json: string): void",
        "+ triggerSpeechAlert(reason: string): void"
    ]
    draw_uml_class(draw, 1680, 120, 460, "ToolVerificationGate", "<<AI Subsystem>>", gate_attrs, gate_meths, header_bg="#DB2777")

    # ROW 2 (y = 560)
    # MaintenanceLog Class
    log_attrs = [
        "- id: UUID",
        "- procedureId: UUID",
        "- machineId: UUID",
        "- technicianId: UUID",
        "- status: WorkOrderStatus",
        "- durationSeconds: int",
        "- startedAt: DateTime",
        "- completedAt: DateTime"
    ]
    log_meths = [
        "+ addPartUsage(part: Part, qty: int): void",
        "+ attachPhotoEvidence(url: string): void",
        "+ signOffTechnician(pin: string): void",
        "+ commitSession(): Promise<boolean>"
    ]
    draw_uml_class(draw, 620, 530, 460, "MaintenanceLog", "<<Aggregate Root>>", log_attrs, log_meths, header_bg="#7C3AED")

    # FaultReport Class
    fault_attrs = [
        "- id: UUID",
        "- factoryId: UUID",
        "- machineId: UUID",
        "- reportedBy: UUID",
        "- assignedTo: UUID",
        "- severity: SeverityLevel",
        "- status: ReportStatus"
    ]
    fault_meths = [
        "+ assignTechnician(techId: UUID): void",
        "+ updateSeverity(lvl: SeverityLevel): void",
        "+ resolveFault(logId: UUID): void"
    ]
    draw_uml_class(draw, 60, 550, 480, "FaultReport", "<<Entity>>", fault_attrs, fault_meths, header_bg="#DC2626")

    # SyncQueueItem Class
    sync_attrs = [
        "- id: UUID",
        "- timestamp: long",
        "- entityType: string",
        "- action: MutationType",
        "- payload: JsonRecord",
        "- retryCount: int",
        "- status: SyncState"
    ]
    sync_meths = [
        "+ serializeToWAL(): string",
        "+ replayToSupabase(): Promise<boolean>",
        "+ markAcknowledged(): void",
        "+ calculateBackoff(): int"
    ]
    draw_uml_class(draw, 1680, 530, 460, "SyncQueueItem", "<<Offline WAL>>", sync_attrs, sync_meths, header_bg="#B45309")

    # ROW 3 (y = 1000)
    # Part Class
    part_attrs = [
        "- id: UUID",
        "- factoryId: UUID",
        "- partNumber: string",
        "- name: string",
        "- stockQuantity: int",
        "- minStockLevel: int",
        "- barcode: string"
    ]
    part_meths = [
        "+ isLowStock(): boolean",
        "+ decrementStock(qty: int): boolean",
        "+ triggerRestockAlert(): void"
    ]
    draw_uml_class(draw, 620, 990, 460, "Part", "<<Entity>>", part_attrs, part_meths, header_bg="#16A34A")

    # PartUsage Class
    usage_attrs = [
        "- id: UUID",
        "- logId: UUID",
        "- partId: UUID",
        "- quantityUsed: int"
    ]
    usage_meths = [
        "+ validateAvailability(): boolean",
        "+ computeCost(): decimal"
    ]
    draw_uml_class(draw, 1160, 990, 420, "PartUsage", "<<Junction>>", usage_attrs, usage_meths, header_bg="#16A34A")

    # CONNECTORS & MULTIPLICITY
    # 1. Machine (1) to RepairProcedure (0..*)
    draw_arrow(draw, (540, 240), (620, 240), color="#0284C7", width=3)
    draw.text((550, 220), "1", fill="#0F172A", font=fonts["sm_bold"])
    draw.text((600, 220), "0..*", fill="#0F172A", font=fonts["sm_bold"])
    draw.text((580, 255), "has", fill="#64748B", font=fonts["sm"], anchor="mm")

    # 2. RepairProcedure (1) to RepairStep (1..*) - COMPOSITION (filled diamond)
    # Diamond at (1060, 240)
    draw.polygon([(1060, 240), (1075, 230), (1090, 240), (1075, 250)], fill="#0284C7")
    draw_arrow(draw, (1090, 240), (1140, 240), color="#0284C7", width=3)
    draw.text((1095, 220), "1", fill="#0F172A", font=fonts["sm_bold"])
    draw.text((1125, 220), "1..*", fill="#0F172A", font=fonts["sm_bold"])
    draw.text((1115, 255), "contains", fill="#64748B", font=fonts["sm"], anchor="mm")

    # 3. RepairStep to ToolVerificationGate - DEPENDENCY (dashed arrow)
    draw_dashed_arrow(draw, (1600, 240), (1680, 240), color="#DB2777", width=3)
    draw.text((1640, 220), "<<uses>>", fill="#DB2777", font=fonts["sm_bold"], anchor="mm")

    # 4. Machine (1) to FaultReport (0..*)
    draw_arrow(draw, (240, 500), (240, 550), color="#DC2626", width=3)
    draw.text((250, 510), "1", fill="#0F172A", font=fonts["sm_bold"])
    draw.text((250, 535), "0..*", fill="#0F172A", font=fonts["sm_bold"])

    # 5. Machine (1) to MaintenanceLog (0..*)
    draw_arrow(draw, (440, 500), (620, 620), color="#7C3AED", width=3)
    draw.text((460, 510), "1", fill="#0F172A", font=fonts["sm_bold"])
    draw.text((580, 600), "0..*", fill="#0F172A", font=fonts["sm_bold"])

    # 6. RepairProcedure (1) to MaintenanceLog (0..*)
    draw_arrow(draw, (840, 480), (840, 530), color="#7C3AED", width=3)
    draw.text((850, 490), "1", fill="#0F172A", font=fonts["sm_bold"])
    draw.text((850, 515), "0..*", fill="#0F172A", font=fonts["sm_bold"])

    # 7. MaintenanceLog (1) to PartUsage (0..*) - COMPOSITION
    draw.polygon([(840, 930), (830, 945), (840, 960), (850, 945)], fill="#7C3AED")
    draw_arrow(draw, (840, 960), (1160, 1080), color="#7C3AED", width=3)
    draw.text((860, 965), "1", fill="#0F172A", font=fonts["sm_bold"])
    draw.text((1130, 1060), "0..*", fill="#0F172A", font=fonts["sm_bold"])

    # 8. Part (1) to PartUsage (0..*)
    draw_arrow(draw, (1080, 1080), (1160, 1080), color="#16A34A", width=3)
    draw.text((1090, 1060), "1", fill="#0F172A", font=fonts["sm_bold"])
    draw.text((1140, 1060), "0..*", fill="#0F172A", font=fonts["sm_bold"])

    # 9. MaintenanceLog to SyncQueueItem - Queues mutations
    draw_dashed_arrow(draw, (1080, 710), (1680, 710), color="#B45309", width=3)
    draw.text((1380, 690), "<<enqueues mutations>>", fill="#B45309", font=fonts["sm_bold"], anchor="mm")

    # Bottom notes
    draw_rounded_rect(draw, [60, 1370, W - 60, 1430], radius=8, fill="#F8FAFC", outline="#CBD5E1", width=1)
    draw.text((W // 2, 1400), "UML Class Notation:  • Filled Diamond = Strong Composition (Lifecycle dependent)  • Dashed Arrow = Dependency / Service Usage  • Multiplicities indicate relational cardinalities.", 
              fill="#334155", font=fonts["sm_bold"], anchor="mm")

    img.save(out_path, quality=95)
    print(f"Saved UML Class Diagram: {out_path}")

# ==============================================================================
# 3. UML ACTIVITY DIAGRAM (Figure 5.5)
# ==============================================================================
def create_uml_activity_diagram(out_path):
    W, H = 2200, 1450
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts(sz_title=34, sz_head=18, sz_sub=15, sz_body=13, sz_sm=11.5, sz_badge=10)

    # Main Header
    draw.rectangle([0, 0, W, 85], fill="#0F172A")
    draw.text((W // 2, 42), "Figure 5.5: MaintAI — UML Activity Diagram (AI Vision Tool Verification & AR Repair Workflow)", 
              fill="#FFFFFF", font=fonts["title"], anchor="mm")

    # 3 Swimlanes
    # Lane 1: Technician & Mobile Client PWA (x: 60 to 760)
    # Lane 2: HTML5 AR Engine & Web Speech Runtime (x: 760 to 1460)
    # Lane 3: Gemini 1.5 Flash Vision & Supabase Cloud (x: 1460 to 2140)

    sw1_x1, sw1_x2 = 60, 760
    sw2_x1, sw2_x2 = 760, 1460
    sw3_x1, sw3_x2 = 1460, 2140
    top_y, bot_y = 100, 1370

    # Draw swimlane backgrounds
    draw.rectangle([sw1_x1, top_y, sw1_x2, bot_y], fill="#F8FAFC", outline="#CBD5E1", width=2)
    draw.rectangle([sw2_x1, top_y, sw2_x2, bot_y], fill="#FFFBEB", outline="#CBD5E1", width=2)
    draw.rectangle([sw3_x1, top_y, sw3_x2, bot_y], fill="#F0FDF4", outline="#CBD5E1", width=2)

    # Swimlane Headers
    draw.rectangle([sw1_x1, top_y, sw1_x2, top_y + 45], fill="#0284C7")
    draw.text(((sw1_x1 + sw1_x2) // 2, top_y + 22), "Swimlane 1: Technician & Mobile Client PWA", fill="#FFFFFF", font=fonts["head"], anchor="mm")

    draw.rectangle([sw2_x1, top_y, sw2_x2, top_y + 45], fill="#D97706")
    draw.text(((sw2_x1 + sw2_x2) // 2, top_y + 22), "Swimlane 2: AR Canvas & Web Speech Runtime", fill="#FFFFFF", font=fonts["head"], anchor="mm")

    draw.rectangle([sw3_x1, top_y, sw3_x2, top_y + 45], fill="#16A34A")
    draw.text(((sw3_x1 + sw3_x2) // 2, top_y + 22), "Swimlane 3: Gemini Vision & Supabase Cloud", fill="#FFFFFF", font=fonts["head"], anchor="mm")

    def draw_activity_state(draw, cx, cy, w, h, text, bg="#FFFFFF", bdr="#0284C7"):
        draw_rounded_rect(draw, [cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], radius=16, fill=bg, outline=bdr, width=2)
        lines = text.split("\n")
        if len(lines) == 1:
            draw.text((cx, cy), lines[0], fill="#0F172A", font=fonts["body_bold"], anchor="mm")
        elif len(lines) == 2:
            draw.text((cx, cy - 10), lines[0], fill="#0F172A", font=fonts["body_bold"], anchor="mm")
            draw.text((cx, cy + 10), lines[1], fill="#334155", font=fonts["body"], anchor="mm")
        elif len(lines) == 3:
            draw.text((cx, cy - 16), lines[0], fill="#0F172A", font=fonts["body_bold"], anchor="mm")
            draw.text((cx, cy), lines[1], fill="#334155", font=fonts["body"], anchor="mm")
            draw.text((cx, cy + 16), lines[2], fill="#64748B", font=fonts["sm"], anchor="mm")

    def draw_decision_diamond(draw, cx, cy, w, h, text):
        half_w = w // 2
        half_h = h // 2
        pts = [(cx, cy - half_h), (cx + half_w, cy), (cx, cy + half_h), (cx - half_w, cy)]
        draw.polygon(pts, fill="#EFF6FF", outline="#2563EB")
        lines = text.split("\n")
        if len(lines) == 1:
            draw.text((cx, cy), lines[0], fill="#1E40AF", font=fonts["sm_bold"], anchor="mm")
        elif len(lines) == 2:
            draw.text((cx, cy - 8), lines[0], fill="#1E40AF", font=fonts["sm_bold"], anchor="mm")
            draw.text((cx, cy + 8), lines[1], fill="#1E40AF", font=fonts["sm_bold"], anchor="mm")

    # Initial State (Solid Circle)
    c1 = (sw1_x1 + sw1_x2) // 2
    c2 = (sw2_x1 + sw2_x2) // 2
    c3 = (sw3_x1 + sw3_x2) // 2

    start_y = 180
    draw.ellipse([c1 - 18, start_y - 18, c1 + 18, start_y + 18], fill="#0F172A")
    draw_arrow(draw, (c1, start_y + 18), (c1, 230), color="#0F172A", width=3)

    # State 1: Scan QR Tag
    draw_activity_state(draw, c1, 260, 360, 60, "Scan Machine QR Tag\n(html5-qrcode video feed)", bg="#FFFFFF", bdr="#0284C7")
    draw_arrow(draw, (c1, 290), (c1, 340), color="#0284C7", width=3)

    # Decision 1: Cached in Dexie?
    draw_decision_diamond(draw, c1, 380, 260, 75, "Cached locally in\nDexie.js store?")
    
    # Branch No -> Fetch from Supabase (Lane 3)
    draw_arrow(draw, (c1 + 130, 380), (c3 - 180, 380), color="#2563EB", width=3)
    draw.text((c1 + 180, 365), "[No: Cache Miss]", fill="#DC2626", font=fonts["sm_bold"])
    draw_activity_state(draw, c3, 380, 360, 60, "Fetch Machine & SOP JSON\nvia Supabase Edge REST", bg="#FFFFFF", bdr="#16A34A")
    
    # Return from Supabase back to Lane 1
    draw_arrow(draw, (c3, 410), (c3, 460), color="#16A34A", width=3)
    draw_arrow(draw, (c3, 460), (c1 + 180, 460), color="#16A34A", width=3)
    draw_arrow(draw, (c1 + 180, 460), (c1 + 180, 490), color="#16A34A", width=3)

    # Branch Yes -> Direct down
    draw_arrow(draw, (c1, 418), (c1, 490), color="#16A34A", width=3)
    draw.text((c1 + 10, 440), "[Yes: Hit]", fill="#16A34A", font=fonts["sm_bold"])

    # State 2: Load SOP Step Viewer
    draw_activity_state(draw, c1, 520, 360, 60, "Mount AR Step Viewer HUD\n& Initialize Video Stream", bg="#FFFFFF", bdr="#0284C7")

    # Fork Bar (Lane 2)
    draw_arrow(draw, (c1 + 180, 520), (c2 - 180, 520), color="#D97706", width=3)
    fork_y = 520
    draw.rectangle([c2 - 180, fork_y - 6, c2 + 180, fork_y + 6], fill="#0F172A")

    # Parallel Sub-activities in Lane 2
    draw_arrow(draw, (c2 - 90, fork_y + 6), (c2 - 90, 570), color="#D97706", width=3)
    draw_activity_state(draw, c2 - 90, 600, 240, 60, "Render 60fps Canvas\nPulsing Target Markers", bg="#FFFFFF", bdr="#D97706")

    draw_arrow(draw, (c2 + 90, fork_y + 6), (c2 + 90, 570), color="#D97706", width=3)
    draw_activity_state(draw, c2 + 90, 600, 240, 60, "Listen for Hands-Free\nWeb Speech Commands", bg="#FFFFFF", bdr="#D97706")

    # Join Bar (Lane 2)
    join_y = 665
    draw.rectangle([c2 - 180, join_y - 6, c2 + 180, join_y + 6], fill="#0F172A")
    draw_arrow(draw, (c2 - 90, 630), (c2 - 90, join_y - 6), color="#D97706", width=3)
    draw_arrow(draw, (c2 + 90, 630), (c2 + 90, join_y - 6), color="#D97706", width=3)

    # From Join -> Decision: Tool Verification Required?
    draw_arrow(draw, (c2, join_y + 6), (c2, 730), color="#0F172A", width=3)
    draw_decision_diamond(draw, c2, 770, 280, 80, "Does Step Demand AI\nTool Verification?")

    # Branch No -> Directly advance to execution
    draw_arrow(draw, (c2 - 140, 770), (c1, 770), color="#16A34A", width=3)
    draw_arrow(draw, (c1, 770), (c1, 840), color="#16A34A", width=3)
    draw.text((c2 - 190, 750), "[No: Standard Step]", fill="#16A34A", font=fonts["sm_bold"])

    # Branch Yes -> Tool Verification Gate (Lane 3)
    draw_arrow(draw, (c2 + 140, 770), (c3, 770), color="#DB2777", width=3)
    draw.text((c2 + 150, 750), "[Yes: Tool Required]", fill="#DB2777", font=fonts["sm_bold"])
    draw_activity_state(draw, c3, 770, 360, 65, "Capture 640x480 Frame\n& Dispatch to Gemini API", bg="#FFFFFF", bdr="#DB2777")

    draw_arrow(draw, (c3, 803), (c3, 840), color="#DB2777", width=3)
    draw_decision_diamond(draw, c3, 880, 260, 75, "Tool Matched &\nConfidence ≥ 0.70?")

    # AI Verification No -> Audio Warning & Loop Back
    draw_arrow(draw, (c3 + 130, 880), (c3 + 200, 880), color="#DC2626", width=3)
    draw_arrow(draw, (c3 + 200, 880), (c3 + 200, 770), color="#DC2626", width=3)
    draw_arrow(draw, (c3 + 200, 770), (c3 + 180, 770), color="#DC2626", width=3)
    draw.text((c3 + 135, 860), "[No]", fill="#DC2626", font=fonts["sm_bold"])
    draw.text((c3 + 205, 825), "Voice Alert: 'Wrong Tool'", fill="#DC2626", font=fonts["sm"])

    # AI Verification Yes -> Merge into Execution
    draw_arrow(draw, (c3 - 130, 880), (c1 + 180, 880), color="#16A34A", width=3)
    draw_arrow(draw, (c1 + 180, 880), (c1 + 180, 840), color="#16A34A", width=3)
    draw.text((c3 - 190, 860), "[Yes: Verified]", fill="#16A34A", font=fonts["sm_bold"])

    # State 3: Execute Assembly & Speak Next
    draw_activity_state(draw, c1, 870, 360, 60, "Perform Physical Repair\n& Speak 'NEXT STEP'", bg="#FFFFFF", bdr="#0284C7")
    draw_arrow(draw, (c1, 900), (c1, 950), color="#0284C7", width=3)

    # State 4: Record Parts & Duration
    draw_activity_state(draw, c1, 980, 360, 60, "Scan Consumed Parts\n& Deduct Stock Quantity", bg="#FFFFFF", bdr="#0284C7")
    draw_arrow(draw, (c1, 1010), (c1, 1055), color="#0284C7", width=3)

    # Decision 3: All Steps Complete?
    draw_decision_diamond(draw, c1, 1090, 260, 70, "Are all SOP\nsteps finished?")

    # Not complete -> Loop back to step execution
    draw_arrow(draw, (c1 - 130, 1090), (sw1_x1 + 30, 1090), color="#D97706", width=3)
    draw_arrow(draw, (sw1_x1 + 30, 1090), (sw1_x1 + 30, 520), color="#D97706", width=3)
    draw_arrow(draw, (sw1_x1 + 30, 520), (c1 - 180, 520), color="#D97706", width=3)
    draw.text((sw1_x1 + 35, 800), "[No: Next Step]", fill="#D97706", font=fonts["sm_bold"])

    # Complete Yes -> Network Online Check
    draw_arrow(draw, (c1, 1125), (c1, 1175), color="#16A34A", width=3)
    draw.text((c1 + 10, 1145), "[Yes: Complete]", fill="#16A34A", font=fonts["sm_bold"])

    draw_decision_diamond(draw, c1, 1210, 260, 70, "Network Connection\nAvailable?")

    # Offline -> Dexie Write-Ahead Queue
    draw_arrow(draw, (c1 - 130, 1210), (sw1_x1 + 80, 1210), color="#B45309", width=3)
    draw_arrow(draw, (sw1_x1 + 80, 1210), (sw1_x1 + 80, 1290), color="#B45309", width=3)
    draw_arrow(draw, (sw1_x1 + 80, 1290), (c1 - 180, 1290), color="#B45309", width=3)
    draw_activity_state(draw, c1, 1290, 360, 60, "Enqueue Transaction in\nDexie.js Write-Ahead Log", bg="#FFFFFF", bdr="#B45309")
    draw.text((sw1_x1 + 85, 1240), "[Offline]", fill="#B45309", font=fonts["sm_bold"])

    # Online -> Commit to Supabase
    draw_arrow(draw, (c1 + 130, 1210), (c3 - 180, 1210), color="#16A34A", width=3)
    draw.text((c1 + 140, 1190), "[Online]", fill="#16A34A", font=fonts["sm_bold"])
    draw_activity_state(draw, c3, 1210, 360, 60, "Post Work Order to Supabase\n& Update Plant MTTR Telemetry", bg="#FFFFFF", bdr="#16A34A")

    # Final Join & End Node
    draw_arrow(draw, (c3, 1240), (c3, 1290), color="#16A34A", width=3)
    draw_arrow(draw, (c1 + 180, 1290), (c2 - 30, 1290), color="#0F172A", width=3)
    draw_arrow(draw, (c3 - 180, 1290), (c2 + 30, 1290), color="#0F172A", width=3)

    # End State (Bullseye)
    end_cx, end_cy = c2, 1290
    draw.ellipse([end_cx - 22, end_cy - 22, end_cx + 22, end_cy + 22], outline="#0F172A", width=3, fill="#FFFFFF")
    draw.ellipse([end_cx - 14, end_cy - 14, end_cx + 14, end_cy + 14], fill="#0F172A")
    draw.text((end_cx, end_cy + 35), "Maintenance Completed", fill="#0F172A", font=fonts["head"], anchor="mm")

    # Bottom notes
    draw_rounded_rect(draw, [60, 1380, W - 60, 1435], radius=8, fill="#F8FAFC", outline="#CBD5E1", width=1)
    draw.text((W // 2, 1408), "UML Activity Semantics:  • Horizontal Solid Bars = Fork (Parallel execution) and Join (Synchronization)  • Rhombus = Decision Diamonds  • Bullseye = Final Activity State.", 
              fill="#334155", font=fonts["sm_bold"], anchor="mm")

    img.save(out_path, quality=95)
    print(f"Saved UML Activity Diagram: {out_path}")

# ==============================================================================
# 4. DATABASE ER DIAGRAM (Figure 5.6)
# ==============================================================================
def create_database_er_diagram(out_path):
    W, H = 2200, 1450
    img = Image.new("RGB", (W, H), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    fonts = get_fonts(sz_title=34, sz_head=19, sz_sub=15, sz_body=13, sz_sm=11.5, sz_badge=10)

    # Main Header
    draw.rectangle([0, 0, W, 85], fill="#0F172A")
    draw.text((W // 2, 42), "Figure 5.6: MaintAI — Relational Database Entity-Relationship (ER) Diagram (Supabase PostgreSQL)", 
              fill="#FFFFFF", font=fonts["title"], anchor="mm")

    # 10 Relational Tables arranged cleanly with clear domain color coding
    # Row 1: factories (Blue), profiles (Blue), machines (Green), repair_procedures (Green)
    # Row 2: fault_reports (Red), maintenance_logs (Purple), maintenance_evidence (Purple), preventive_schedules (Cyan)
    # Row 3: parts (Amber), parts_used (Amber), RLS Security Notes

    def draw_er_table(draw, x, y, w, title, fields, header_bg="#2563EB"):
        h_head = 44
        h_fields = len(fields) * 26 + 12
        total_h = h_head + h_fields

        # Border
        draw_rounded_rect(draw, [x, y, x + w, y + total_h], radius=10, fill="#FFFFFF", outline=header_bg, width=2)
        # Header
        draw_rounded_rect(draw, [x, y, x + w, y + h_head], radius=10, fill=header_bg)
        draw.text((x + 18, y + h_head // 2), title, fill="#FFFFFF", font=fonts["head"], anchor="lm")

        # Fields
        cur_y = y + h_head + 8
        for badge, name, dtype in fields:
            # Badge
            if badge == "PK":
                draw_rounded_rect(draw, [x + 14, cur_y - 2, x + 44, cur_y + 18], radius=4, fill="#FEF08A", outline="#CA8A04", width=1)
                draw.text((x + 29, cur_y + 8), "PK", fill="#854D0E", font=fonts["badge"], anchor="mm")
            elif badge == "FK":
                draw_rounded_rect(draw, [x + 14, cur_y - 2, x + 44, cur_y + 18], radius=4, fill="#DBEAFE", outline="#2563EB", width=1)
                draw.text((x + 29, cur_y + 8), "FK", fill="#1E40AF", font=fonts["badge"], anchor="mm")
            elif badge == "PFK":
                draw_rounded_rect(draw, [x + 14, cur_y - 2, x + 48, cur_y + 18], radius=4, fill="#F3E8FF", outline="#7C3AED", width=1)
                draw.text((x + 31, cur_y + 8), "PFK", fill="#6D28D9", font=fonts["badge"], anchor="mm")
            else:
                draw_rounded_rect(draw, [x + 14, cur_y - 2, x + 44, cur_y + 18], radius=4, fill="#F1F5F9", outline="#94A3B8", width=1)
                draw.text((x + 29, cur_y + 8), "•", fill="#475569", font=fonts["badge"], anchor="mm")

            # Field Name
            draw.text((x + 56, cur_y + 8), name, fill="#0F172A", font=fonts["body_bold"], anchor="lm")
            # Data Type
            draw.text((x + w - 16, cur_y + 8), dtype, fill="#64748B", font=fonts["sm"], anchor="rm")

            cur_y += 26

        return total_h

    # ROW 1 (y = 120)
    # 1. factories
    f_factories = [
        ("PK", "id", "UUID"),
        ("", "name", "VARCHAR(100)"),
        ("", "location", "VARCHAR(100)"),
        ("", "created_at", "TIMESTAMPTZ"),
    ]
    draw_er_table(draw, 50, 120, 440, "factories (Tenant Root)", f_factories, header_bg="#1D4ED8")

    # 2. profiles
    f_profiles = [
        ("PFK", "id", "UUID (auth.users)"),
        ("FK", "factory_id", "UUID (factories)"),
        ("", "full_name", "VARCHAR(100)"),
        ("", "email", "VARCHAR(100)"),
        ("", "role", "tech | supervisor | admin"),
    ]
    draw_er_table(draw, 540, 120, 480, "profiles (User Accounts)", f_profiles, header_bg="#1D4ED8")

    # 3. machines
    f_machines = [
        ("PK", "id", "UUID"),
        ("FK", "factory_id", "UUID (factories)"),
        ("", "name", "VARCHAR(100)"),
        ("", "model", "VARCHAR(50)"),
        ("", "qr_code", "VARCHAR(100)"),
        ("", "status", "operational | down"),
        ("", "health_score", "INTEGER (0–100)"),
    ]
    draw_er_table(draw, 1070, 120, 500, "machines (Equipment Catalog)", f_machines, header_bg="#16A34A")

    # 4. repair_procedures
    f_procedures = [
        ("PK", "id", "UUID"),
        ("FK", "machine_id", "UUID (machines)"),
        ("", "title", "VARCHAR(150)"),
        ("", "category", "VARCHAR(50)"),
        ("", "estimated_time_mins", "INTEGER"),
        ("", "steps_json", "JSONB (AR coords)"),
    ]
    draw_er_table(draw, 1620, 120, 530, "repair_procedures (SOP Library)", f_procedures, header_bg="#16A34A")

    # ROW 2 (y = 520)
    # 5. fault_reports
    f_faults = [
        ("PK", "id", "UUID"),
        ("FK", "factory_id", "UUID (factories)"),
        ("FK", "machine_id", "UUID (machines)"),
        ("FK", "reported_by", "UUID (profiles)"),
        ("FK", "assigned_to", "UUID (profiles)"),
        ("", "severity", "low | med | high"),
        ("", "status", "pending | in_progress | closed"),
    ]
    draw_er_table(draw, 50, 520, 460, "fault_reports (Breakdowns)", f_faults, header_bg="#DC2626")

    # 6. maintenance_logs
    f_logs = [
        ("PK", "id", "UUID"),
        ("FK", "procedure_id", "UUID (procedures)"),
        ("FK", "machine_id", "UUID (machines)"),
        ("FK", "technician_id", "UUID (profiles)"),
        ("", "status", "in_progress | completed"),
        ("", "duration_seconds", "INTEGER"),
        ("", "notes", "TEXT"),
        ("", "created_at", "TIMESTAMPTZ"),
    ]
    draw_er_table(draw, 560, 520, 500, "maintenance_logs (Work Orders)", f_logs, header_bg="#7C3AED")

    # 7. maintenance_evidence
    f_evidence = [
        ("PK", "id", "UUID"),
        ("FK", "log_id", "UUID (logs)"),
        ("", "image_url", "TEXT (Supabase S3)"),
        ("", "caption", "VARCHAR(255)"),
        ("", "created_at", "TIMESTAMPTZ"),
    ]
    draw_er_table(draw, 1110, 520, 480, "maintenance_evidence (Photos)", f_evidence, header_bg="#7C3AED")

    # 8. preventive_schedules
    f_schedules = [
        ("PK", "id", "UUID"),
        ("FK", "machine_id", "UUID (machines)"),
        ("FK", "procedure_id", "UUID (procedures)"),
        ("", "interval_days", "INTEGER"),
        ("", "next_due_date", "DATE"),
    ]
    draw_er_table(draw, 1640, 520, 510, "preventive_schedules (Rules)", f_schedules, header_bg="#0891B2")

    # ROW 3 (y = 920)
    # 9. parts
    f_parts = [
        ("PK", "id", "UUID"),
        ("FK", "factory_id", "UUID (factories)"),
        ("", "part_number", "VARCHAR(50)"),
        ("", "name", "VARCHAR(100)"),
        ("", "stock_quantity", "INTEGER"),
        ("", "min_stock_level", "INTEGER"),
        ("", "barcode", "VARCHAR(100)"),
    ]
    draw_er_table(draw, 1070, 920, 500, "parts (Spare Parts Inventory)", f_parts, header_bg="#D97706")

    # 10. parts_used
    f_parts_used = [
        ("PK", "id", "UUID"),
        ("FK", "log_id", "UUID (logs)"),
        ("FK", "part_id", "UUID (parts)"),
        ("", "quantity_used", "INTEGER"),
    ]
    draw_er_table(draw, 1620, 920, 530, "parts_used (Part Consumption)", f_parts_used, header_bg="#D97706")

    # Crow's Foot Relationship Connectors
    # 1. factories (1) to profiles (N)
    draw_arrow(draw, (490, 200), (540, 200), color="#1D4ED8", width=3)
    draw.text((515, 180), "1 : N", fill="#1D4ED8", font=fonts["sm_bold"], anchor="mm")

    # 2. profiles / factories to machines (1 : N)
    draw_arrow(draw, (1020, 200), (1070, 200), color="#16A34A", width=3)
    draw.text((1045, 180), "1 : N", fill="#16A34A", font=fonts["sm_bold"], anchor="mm")

    # 3. machines (1) to repair_procedures (N)
    draw_arrow(draw, (1570, 200), (1620, 200), color="#16A34A", width=3)
    draw.text((1595, 180), "1 : N", fill="#16A34A", font=fonts["sm_bold"], anchor="mm")

    # 4. machines (1) to fault_reports (N)
    draw_arrow(draw, (1070, 280), (510, 580), color="#DC2626", width=3)
    draw.text((790, 430), "1 : N (Machine Breakdowns)", fill="#DC2626", font=fonts["sm_bold"], anchor="mm")

    # 5. machines & procedures to maintenance_logs (1 : N)
    draw_arrow(draw, (1320, 360), (950, 520), color="#7C3AED", width=3)
    draw.text((1150, 440), "1 : N (Work Orders)", fill="#7C3AED", font=fonts["sm_bold"], anchor="mm")

    # 6. maintenance_logs (1) to maintenance_evidence (N)
    draw_arrow(draw, (1060, 620), (1110, 620), color="#7C3AED", width=3)
    draw.text((1085, 600), "1 : N", fill="#7C3AED", font=fonts["sm_bold"], anchor="mm")

    # 7. maintenance_logs (1) to parts_used (N)
    draw_arrow(draw, (810, 800), (810, 1020), color="#D97706", width=3)
    draw_arrow(draw, (810, 1020), (1620, 1020), color="#D97706", width=3)
    draw.text((1200, 1000), "1 : N (Consumed Parts)", fill="#D97706", font=fonts["sm_bold"], anchor="mm")

    # 8. parts (1) to parts_used (N)
    draw_arrow(draw, (1570, 1020), (1620, 1020), color="#D97706", width=3)
    draw.text((1595, 1000), "1 : N", fill="#D97706", font=fonts["sm_bold"], anchor="mm")

    # 9. machines & procedures to preventive_schedules (1 : N)
    draw_arrow(draw, (1885, 330), (1885, 520), color="#0891B2", width=3)
    draw.text((1920, 420), "1 : N", fill="#0891B2", font=fonts["sm_bold"], anchor="mm")

    # Bottom Multi-Tenant Row Level Security Architecture Box
    rls_y = 920
    draw_rounded_rect(draw, [50, rls_y, 980, rls_y + 360], radius=14, fill="#F8FAFC", outline="#475569", width=2)
    draw_rounded_rect(draw, [50, rls_y, 980, rls_y + 45], radius=14, fill="#334155")
    draw.text((515, rls_y + 22), "PostgreSQL Row Level Security (RLS) Tenant Boundaries", fill="#FFFFFF", font=fonts["head"], anchor="mm")

    rls_bullets = [
        ("• Mandatory Tenant Isolation:", "All queries automatically append: WHERE factory_id = (auth.jwt() ->> 'factory_id')::uuid"),
        ("• Role-Based Access Control (RBAC):", "Technicians can INSERT maintenance_logs and parts_used; Supervisors can UPDATE procedures."),
        ("• Offline Write-Ahead Replay:", "Replayed mutation payloads are verified against client-side JWT claims before atomic DB commit."),
        ("• Foreign Key Integrity:", "Strict ON DELETE RESTRICT guarantees that completed audit logs can never be orphaned or deleted."),
        ("• Storage S3 Bucket Isolation:", "Equipment photos in /evidence bucket are prefixed by tenant UUID to enforce storage privacy.")
    ]
    cur_ry = rls_y + 65
    for btitle, bdesc in rls_bullets:
        draw.text((75, cur_ry), btitle, fill="#0F172A", font=fonts["body_bold"])
        draw.text((75, cur_ry + 22), bdesc, fill="#475569", font=fonts["sm"])
        cur_ry += 54

    # Bottom footer notes
    draw_rounded_rect(draw, [50, 1370, W - 50, 1430], radius=8, fill="#F8FAFC", outline="#CBD5E1", width=1)
    draw.text((W // 2, 1400), "Relational Conventions:  • [PK] = Primary Key  • [FK] = Foreign Key  • [PFK] = Primary Foreign Key (Supabase Auth link)  • Arrows indicate 1-to-Many foreign key references.", 
              fill="#334155", font=fonts["sm_bold"], anchor="mm")

    img.save(out_path, quality=95)
    print(f"Saved Database ER Diagram: {out_path}")

if __name__ == "__main__":
    os.makedirs("pdf_images", exist_ok=True)
    create_uml_use_case_diagram(r"pdf_images/fig_5_3_use_case_diagram.png")
    create_uml_class_diagram(r"pdf_images/fig_5_4_class_diagram.png")
    create_uml_activity_diagram(r"pdf_images/fig_5_5_activity_diagram.png")
    create_database_er_diagram(r"pdf_images/fig_5_6_database_er.png")
    print("All 4 UML and ER diagrams generated successfully!")
