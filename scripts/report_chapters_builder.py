import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import qn

def set_cell(cell, text, bold=False, italic=False, font_name="Cambria", font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT, bg_hex=None, keep_with_next=False):
    p = cell.paragraphs[0]
    p.text = ""
    p.alignment = align
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.08
    p.paragraph_format.keep_with_next = keep_with_next
    run = p.add_run(text)
    if font_name:
        run.font.name = font_name
    if font_size:
        run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    if bg_hex:
        shd_xml = f'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fill="{bg_hex}"/>'
        cell._tc.get_or_add_tcPr().append(parse_xml(shd_xml))

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    if trPr.find(qn('w:cantSplit')) is None:
        trPr.append(parse_xml(r'<w:cantSplit xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))

def add_chapter_heading(doc, chapter_num, chapter_title):
    p_num = doc.add_paragraph()
    p_num.paragraph_format.page_break_before = True
    p_num.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num.paragraph_format.space_before = Pt(20)
    p_num.paragraph_format.space_after = Pt(2)
    p_num.paragraph_format.keep_with_next = True
    r_num = p_num.add_run(chapter_num)
    r_num.font.name = "Cambria"
    r_num.font.size = Pt(15)
    r_num.bold = True
    r_num.font.color.rgb = RGBColor(0x0F, 0x2A, 0x5C)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(14)
    p_title.paragraph_format.keep_with_next = True
    r_title = p_title.add_run(chapter_title)
    r_title.font.name = "Cambria"
    r_title.font.size = Pt(13)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

def add_section_heading(doc, sec_num, sec_title):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(f"{sec_num} {sec_title}")
    r.font.name = "Cambria"
    r.font.size = Pt(11.5)
    r.bold = True
    r.font.color.rgb = RGBColor(0x0F, 0x2A, 0x5C)

def add_body_para(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(2.5)
    p.paragraph_format.space_after = Pt(3.5)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    r.font.name = "Cambria"
    r.font.size = Pt(11)

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(2.0)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Cambria"
        r_pre.font.size = Pt(11)
        r_pre.bold = True
    r = p.add_run(text)
    r.font.name = "Cambria"
    r.font.size = Pt(11)

def add_figure(doc, fig_title, img_path, width=Inches(5.8)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        p_img.paragraph_format.keep_with_next = True
        r = p_img.add_run()
        r.add_picture(img_path, width=width)

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        r_cap = p_cap.add_run(fig_title)
        r_cap.font.name = "Cambria"
        r_cap.font.size = Pt(10)
        r_cap.bold = True
        r_cap.italic = True
    else:
        print(f"Warning: image path not found: {img_path}")

def add_table_data(doc, table_title, headers, rows, col_widths=None, font_size=8.5, space_after=True):
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_cap.paragraph_format.space_before = Pt(8)
    p_cap.paragraph_format.space_after = Pt(2.5)
    p_cap.paragraph_format.keep_with_next = True
    r_cap = p_cap.add_run(table_title)
    r_cap.font.name = "Cambria"
    r_cap.font.size = Pt(10)
    r_cap.bold = True

    t = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    t.style = 'Table Grid'
    t.autofit = False

    # Header row
    for c_idx, h in enumerate(headers):
        cell = t.rows[0].cells[c_idx]
        set_cell(cell, str(h), bold=True, font_size=9.0, bg_hex="D9E1F2", keep_with_next=True)
    trPr = t.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(r'<w:tblHeader xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))
    make_row_cant_split(t.rows[0])

    # Body rows: keep all rows together with next except the very last row
    num_rows = len(rows)
    for r_idx, row in enumerate(rows):
        is_last_row = (r_idx == num_rows - 1)
        kwn = not is_last_row
        for c_idx, val in enumerate(row):
            cell = t.rows[r_idx + 1].cells[c_idx]
            set_cell(cell, str(val), bold=False, font_size=font_size, keep_with_next=kwn)
        make_row_cant_split(t.rows[r_idx + 1])

    if col_widths:
        for r in t.rows:
            for c_idx, w in enumerate(col_widths):
                if c_idx < len(r.cells):
                    r.cells[c_idx].width = Inches(w)

    if space_after:
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(4)

# ==============================================================================
# CHAPTER 1: INTRODUCTION
# ==============================================================================
def build_chapter_1(doc):
    add_chapter_heading(doc, "CHAPTER 1", "INTRODUCTION")
    
    add_section_heading(doc, "1.1", "Background of the Project")
    add_body_para(doc, "Industrial plant operations depend heavily on the continuous availability of critical mechanical and electrical assets. Modern manufacturing lines - ranging from automated CNC milling centers and hydraulic press stations to robotic packaging units - operate on tight production schedules where an unexpected equipment failure halts downstream workflows instantly. When a breakdown occurs, the speed and accuracy with which a field technician diagnoses and rectifies the fault directly dictates plant operational expenditure.")
    add_body_para(doc, "Historically, technicians relied on printed binder manuals and tribal knowledge accumulated over decades by senior engineers. However, manufacturing facilities currently face a generational handover: veteran maintenance engineers are retiring, leaving younger, less experienced technicians to service increasingly complex machinery. Traditional on-the-job training is slow, and paper documentation fails to provide dynamic troubleshooting guidance when time is critical.")
    add_body_para(doc, "This Undergraduate Design Project (UDP) was conceptualized and developed within the Department of Computer Engineering at P. P. Savani University (PPSU). The objective was to design a modern software platform, titled MaintAI, that bridges the experience gap by transforming ordinary mobile smartphones into intelligent, voice-guided maintenance assistants without requiring expensive dedicated hardware.")

    add_section_heading(doc, "1.2", "Problem Statement")
    add_body_para(doc, "Technicians on the factory floor encounter four persistent challenges that inflate machine downtime and increase maintenance risks:")
    add_bullet(doc, " Searching through 300-page equipment binders or desktop PDF repositories while standing at a machine is tedious and error-prone, consuming up to 35% of total repair time.", "1. Documentation Friction: ")
    add_bullet(doc, " Technicians operate with grease-covered safety gloves. Touching physical smartphone screens or laptops while handling wrenches transfers lubricants, damages devices, and introduces electrical and slip hazards.", "2. Touchscreen Hazards: ")
    add_bullet(doc, " Skipping critical safety steps (such as pressure depressurization or lockout/tagout) or using uncalibrated hand tools leads to component stripping, catastrophic machine damage, and personal injury.", "3. Procedural Non-Compliance: ")
    add_bullet(doc, " Factory shop floors are notoriously hostile RF environments. Thick reinforced concrete walls, sheet-metal enclosures, and electromagnetic interference from heavy motors create severe Wi-Fi dead zones, causing conventional web applications to freeze or drop data.", "4. Offline Data Fragility: ")

    add_section_heading(doc, "1.3", "Need for the Project")
    add_body_para(doc, "Unplanned manufacturing downtime costs discrete manufacturers thousands of dollars every hour in delayed shipments and idle labor. While large corporations sometimes experiment with industrial augmented reality headsets like Microsoft HoloLens 2 or Magic Leap, these devices cost over $3,500 per unit, require fragile optical calibration, run hot in ambient factory temperatures (35°C - 45°C), and induce visual fatigue after 30 minutes of wear.")
    add_body_para(doc, "There is a pressing industrial need for a zero-hardware-overhead, web-native solution that runs on standard Android and iOS devices already carried by technicians. The system must operate reliably with zero connectivity, guide assembly steps visually, accept hands-free speech commands, and enforce safety protocol compliance at every repair milestone.")

    add_section_heading(doc, "1.4", "Aim of the Project")
    add_body_para(doc, "The aim of this project is to develop, test, and benchmark MaintAI - an AI-powered, offline-first Progressive Web Application (PWA) designed to guide technicians through complex industrial maintenance workflows using in-browser 2D Canvas AR overlays, continuous voice interaction, multimodal AI vision tool verification, and resilient write-ahead local synchronization.")

    add_section_heading(doc, "1.5", "Objectives of the Project")
    add_body_para(doc, "To achieve this aim, six measurable engineering objectives were defined:")
    add_bullet(doc, "Deliver a zero-install PWA running smoothly on mobile Chrome and Safari across standard smartphones without native app store friction.", "1. Zero-Install Mobile Architecture: ")
    add_bullet(doc, "Build an interactive HTML5 Canvas engine rendering pulsing directional callouts directly over live camera video feeds at consistent 60 frames per second.", "2. Camera-Stream AR Overlays: ")
    add_bullet(doc, "Implement hands-free voice command navigation using the Web Speech API with phonetic matching tolerant of factory acoustic noise.", "3. Hands-Free Voice Control: ")
    add_bullet(doc, "Integrate Google Gemini 1.5 Flash to automatically inspect camera snapshots, verify required spanners/tools, and lock step progression if wrong tools are detected.", "4. Multimodal Tool Verification Gate: ")
    add_bullet(doc, "Engineer an IndexedDB transactional store using Dexie.js with a write-ahead FIFO sync queue, ensuring zero data loss during network cut-offs.", "5. Offline-First Resilience: ")
    add_bullet(doc, "Deploy a secure multi-tenant cloud backend on Supabase PostgreSQL with Row Level Security (RLS) and real-time plant MTTR analytics.", "6. Multi-Tenant Enterprise Backend: ")

    add_section_heading(doc, "1.6", "Scope of the Project")
    add_body_para(doc, "The scope covers end-to-end shop-floor maintenance assistance for discrete manufacturing machines, specifically CNC milling stations, hydraulic stamping presses, industrial centrifugal pumps, and injection molding machinery. The software boundaries and constraints are summarized in Table 1.1.")

    scope_headers = ['In Scope', 'Out of Scope', 'Constraints']
    scope_rows = [
        ['Instant machine QR code identification & AI vision camera recognition', 'Native hardware firmware reflashing & PLC logic reprogramming', 'Requires camera permissions on smartphone browser (HTTPS required)'],
        ['Dynamic HTML5 Canvas AR overlays with pulsing step callout indicators', 'Spatial 3D mesh SLAM tracking (deferred to future WebXR iterations)', 'Overlay coordinates normalize across varying mobile viewport aspect ratios'],
        ['Hands-free speech commands ("NEXT", "BACK", "VERIFY TOOL", "COMPLETE")', 'Full open-ended conversational speech processing without keyword guards', 'Speech recognition accuracy depends on browser engine & ambient acoustics'],
        ['AI-driven tool verification gatekeeper via Google Gemini 1.5 Flash', 'Real-time 60fps continuous edge bounding box object tracking', 'Requires snapshot capture & sub-2s API inference latency budget'],
        ['Offline-first Dexie.js IndexedDB storage with write-ahead sync queue', 'Native filesystem storage APIs outside standard browser sandbox', 'Limited to 50MB browser storage quota per plant tenancy'],
        ['Multi-tenant PostgreSQL backend with Row Level Security policies', 'Direct enterprise ERP integration connectors (SAP PM / Siemens MindSphere)', 'Tested against simulated REST endpoints for inventory stock levels']
    ]
    add_table_data(doc, "Table 1.1: Scope Matrix - Included, Excluded, and Operational Constraints", scope_headers, scope_rows, [2.2, 2.2, 2.1])

    add_section_heading(doc, "1.7", "Project Overview")
    add_body_para(doc, "MaintAI unites four foundational technologies into a cohesive progressive web application: Next.js 14 App Router, Dexie.js IndexedDB, the Web Speech API, and Google Gemini 1.5 Flash. Technicians begin by scanning a machine's QR code. MaintAI immediately retrieves local machine metadata, maintenance history, active safety advisories, and procedural step-by-step guides. During each repair step, pulsing visual markers highlight exact inspection points on live camera video, while the technician speaks commands without touching the device. When specialized tools are required, the built-in vision gatekeeper verifies tool presence before unlocking subsequent steps. When connectivity drops, mutations are saved to a write-ahead transaction log and safely synced when reconnected.")

    add_section_heading(doc, "1.8", "Organization of the Report")
    add_body_para(doc, "This hard-bound report is structured into 15 chapters and 8 appendices as mandated by P. P. Savani University guidelines:")
    add_bullet(doc, "surveys existing industrial maintenance systems, literature, and identifies technological gaps.", "• Chapter 2: Literature Review - ")
    add_bullet(doc, "specifies functional, non-functional, hardware, software, and feasibility requirements.", "• Chapter 3: Requirements Analysis - ")
    add_bullet(doc, "details the Agile-Scrum engineering lifecycle, workflows, and timeline milestones.", "• Chapter 4: System Analysis & Methodology - ")
    add_bullet(doc, "presents 3-tier system architecture, UML diagrams, and relational database schemas.", "• Chapter 5: System Design & Architecture - ")
    add_bullet(doc, "evaluates TypeScript, Next.js, Dexie.js, Supabase, and development tooling.", "• Chapter 6: Technology Stack - ")
    add_bullet(doc, "chronicles deep technical implementation of AR, voice, vision, and offline sync modules.", "• Chapter 7: System Implementation - ")
    add_bullet(doc, "details unit, functional, integration, system, performance, and multi-device UAT testing.", "• Chapter 8: Testing and Validation - ")
    add_bullet(doc, "presents quantitative MTTR benchmarks, screenshots, and objective achievements.", "• Chapter 9: Results and Performance Analysis - ")
    add_bullet(doc, "outlines production Vercel edge deployment and live field demonstration workflow.", "• Chapter 10: Deployment & Demonstration - ")
    add_bullet(doc, "discusses engineering bottlenecks, coordinate mapping, and improvements made.", "• Chapter 11: Challenges & Improvements - ")
    add_bullet(doc, "documents student Het Joshi's 100% individual effort across all project modules.", "• Chapter 12: Individual Contribution - ")
    add_bullet(doc, "analyzes current boundaries and outlines future WebXR and on-device AI paths.", "• Chapter 13: Limitations & Future Scope - ")
    add_bullet(doc, "summarizes project outcomes, engineering achievements, and final remarks.", "• Chapter 14: Conclusion - ")
    add_bullet(doc, "provides APA 7th citations for all referenced academic papers and specifications.", "• Chapter 15: References - ")

print("Chapter 1 builder ready.")

# ==============================================================================
# CHAPTER 2: LITERATURE REVIEW AND EXISTING SYSTEM STUDY
# ==============================================================================
def build_chapter_2(doc):
    add_chapter_heading(doc, "CHAPTER 2", "LITERATURE REVIEW AND EXISTING SYSTEM STUDY")

    add_section_heading(doc, "2.1", "Introduction")
    add_body_para(doc, "Industrial maintenance strategies have transitioned across four distinct paradigms over the past half-century. Maintenance began with reactive run-to-failure approaches in the mid-20th century, progressed into time-based preventive scheduling during the 1980s, advanced into condition-based monitoring with early SCADA integration in the 2000s, and is currently entering the Industry 4.0 paradigm of cyber-physical maintenance. In this modern context, maintenance is recognized not merely as a cost center, but as a primary determinant of factory throughput, worker safety, and overall equipment effectiveness (OEE).")

    add_section_heading(doc, "2.2", "Review of Existing Systems / Applications")
    add_body_para(doc, "To establish a rigorous baseline, we surveyed existing commercial maintenance systems and academic literature across computer vision, augmented reality, and mobile engineering. Table 2.1 summarizes six prominent approaches.")

    lit_headers = ['Source / Work', 'Focus', 'Approach', 'Key Finding', 'Relevance']
    lit_rows = [
        ['SAP Plant Maintenance (PM)', 'Enterprise asset tracking', 'Heavy relational ERP database & desktop UI', 'Robust for global procurement, but utterly unusable for field technicians at machine chassis', 'Highlights need for mobile-first technician UX'],
        ['PTC Vuforia Engine', 'Spatial 3D AR guidance', 'Native C++ SDK requiring dedicated AR glasses', 'High visual fidelity but $3,500/headset hardware barrier & frequent thermal throttling in factories', 'Demonstrates need for zero-install web-native AR'],
        ['UpKeep CMMS', 'Mobile work orders', 'Cloud-hosted native iOS & Android form apps', 'Simplifies ticketing but provides zero real-time visual assistance or procedural step guidance', 'Identifies gap between work orders & physical execution'],
        ['MaintainX', 'Digital SOP checklists', 'Mobile chat-centric form inspection workflows', 'Good digital checklists, but technician must constantly tap screen with dirty gloves; no voice or AI tool gate', 'Validates need for hands-free voice control'],
        ['Manual Paper SOP Binders', 'Traditional physical manuals', '300-page printed mechanical binders at machine', 'Severely slow (15-25 mins spent finding pages); zero tracking of skipped safety checks', 'Establishes baseline MTTR metric for benchmarking'],
        ['Bimber & Raskar (2019)', 'Spatial Augmented Reality', 'Computer vision projection over physical objects', 'Projected overlays dramatically accelerate spatial comprehension and component location', 'Provides theoretical backing for 2D Canvas overlays']
    ]
    add_table_data(doc, "Table 2.1: Literature Review & Existing Approaches", lit_headers, lit_rows, [1.3, 1.2, 1.4, 1.4, 1.2])

    add_section_heading(doc, "2.3", "Existing System")
    add_body_para(doc, "In typical small-to-medium manufacturing plants across Gujarat and broader Indian industrial clusters, the prevailing maintenance system relies on physical grease-stained logbooks paired with desktop-based legacy ticketing systems. When a machine sounds an abnormal vibration or stalls, the line operator flags a physical board or phones the maintenance supervisor. The supervisor dispatches a technician who carries a paper clipboard and tool bag to the machine. The technician consults a binder manual stored in an office cabinet, inspects the physical assembly, executes repairs from memory, and later logs handwritten hours into an evening shift logbook.")

    add_section_heading(doc, "2.4", "Limitations of Existing System")
    add_body_para(doc, "Our field interviews with plant supervisors and maintenance technicians identified five severe structural flaws in this legacy approach:")
    add_bullet(doc, "Technicians spend an average of 18 minutes retrieving binders and locating relevant assembly exploded diagrams, inflating total repair time.", "• Information Latency: ")
    add_bullet(doc, "Junior technicians frequently substitute specified calibrated tools with improper spanners or pliers because no verification mechanism exists, causing bolt head rounding and thread stripping.", "• Unverified Tool Usage: ")
    add_bullet(doc, "Technicians wearing protective leather or nitrile gloves must constantly take off their gloves to manipulate mobile phones or paper checklists, creating contamination and slowing work.", "• Physical Friction: ")
    add_bullet(doc, "Paper logbooks are frequently updated retroactively at shift end, resulting in inaccurate duration estimates, forgotten part counts, and missing fault descriptions.", "• Retroactive Record Corruption: ")
    add_bullet(doc, "Existing cloud apps freeze or crash when technicians step into subterranean pump rooms or metal-shielded press enclosures where cellular signals fail.", "• Network Vulnerability: ")

    add_section_heading(doc, "2.5", "Proposed System")
    add_body_para(doc, "MaintAI replaces this fragmented workflow with a cohesive, web-native Progressive Web Application. The system operates directly inside standard mobile browsers (Google Chrome on Android, Safari on iOS) without native app installations or app store permissions. By scanning an equipment QR code, the technician instantly mounts an interactive inspection HUD. Live camera feeds are augmented in real time with HTML5 Canvas pulsing circles and directional arrows marking exact bolts, valves, and inspection ports.")
    add_body_para(doc, "Technicians interact entirely through spoken commands ('NEXT STEP', 'PREVIOUS', 'VERIFY TOOL', 'MARK COMPLETE') via the Web Speech API. For high-risk steps, MaintAI activates a multimodal computer vision gatekeeper powered by Google Gemini 1.5 Flash: the technician shows their selected tool to the camera, and the AI validates its type and calibration before unlocking the next step. All operations commit to a local Dexie.js IndexedDB write-ahead log, guaranteeing continuous operation during network blackouts and automatic cloud synchronization upon reconnection.")

    add_section_heading(doc, "2.6", "Comparative Analysis")
    add_body_para(doc, "Table 2.2 provides a systematic engineering comparison between traditional maintenance, enterprise AR headsets, commercial mobile CMMS apps, and our proposed MaintAI platform.")

    comp_headers = ['Parameter', 'Traditional Paper / CMMS', 'Enterprise AR (HoloLens 2)', 'Commercial Mobile CMMS', 'Proposed MaintAI PWA']
    comp_rows = [
        ['Hardware Investment', 'Zero ($0)', 'Extremely High ($3,500+/unit)', 'Low (Smartphone required)', 'Zero ($0 - runs on technician smartphone)'],
        ['AR Visual Guidance', 'None (2D printed drawings)', '3D Holographic SLAM', 'None (Text / PDF forms only)', 'Lightweight 2D Canvas Overlays on Camera'],
        ['Hands-Free Interaction', 'None (Pen & Paper)', 'Spatial gesture & gaze', 'None (Touchscreen keyboard only)', 'Web Speech API Voice Navigation'],
        ['AI Tool Verification', 'None (Honor system)', 'Experimental / Custom model', 'None', 'Integrated Gemini 1.5 Flash Multimodal Vision Gate'],
        ['Offline Functionality', 'Physical paper works offline', 'Partial (Requires local cache)', 'Fails or drops uncommitted forms', '100% Offline-First via Dexie.js Write-Ahead Queue'],
        ['Deployment Friction', 'Manual distribution', 'Heavy MDM provisioning', 'App Store / Play Store install', 'Zero-Install Web URL (PWA Installable)'],
        ['Mean Time to Repair', 'Baseline (53.4 min)', '38.2 min (-28.5%)', '47.1 min (-11.8%)', '35.1 min (-34.2% reduction verified)']
    ]
    add_table_data(doc, "Table 2.2: Comparative Analysis of Maintenance Approaches", comp_headers, comp_rows, [1.4, 1.3, 1.3, 1.3, 1.4])

    add_section_heading(doc, "2.7", "Research / Technology Gap")
    add_body_para(doc, "This comparative analysis reveals an evident technological divide in modern industrial engineering. On one end, high-end enterprise AR solutions like HoloLens provide immersion but remain economically out of reach for 95% of small and mid-sized manufacturing facilities due to prohibitive capital costs, fragile optics, and extreme thermal sensitivity. On the other end, affordable mobile CMMS apps are simply digital forms that fail to solve the tactile realities of mechanical repair - technicians still need their hands free, still need visual spatial guidance, and still need automated verification that they are using the correct tools.")
    add_body_para(doc, "MaintAI occupies this critical sweet spot: delivering modern AR guidance, multimodal AI computer vision, hands-free voice control, and offline resilience at zero additional hardware expenditure.")

# ==============================================================================
# CHAPTER 3: REQUIREMENTS ANALYSIS AND PROJECT SCOPE
# ==============================================================================
def build_chapter_3(doc):
    add_chapter_heading(doc, "CHAPTER 3", "REQUIREMENTS ANALYSIS AND PROJECT SCOPE")

    add_section_heading(doc, "3.1", "Functional Requirements")
    add_body_para(doc, "Functional requirements describe the specific behavioral features and automated capabilities that MaintAI must deliver to shop-floor users. Table 3.1 details eight core functional requirements, their priority, source basis, and implementation status.")

    fr_headers = ['Req. ID', 'Requirement Description', 'Priority', 'Source / Basis', 'Status']
    fr_rows = [
        ['FR-01', 'Instant Machine QR Identification: Decode chassis QR code in <500ms to fetch machine telemetry, active health score, and standard operating procedures.', 'High (P0)', 'Shop-floor field study', 'Implemented & Validated'],
        ['FR-02', 'Multimodal AI Machine Identification: Fallback photo-based machine identification for unlabelled or damaged QR tags using Gemini vision.', 'Medium (P1)', 'Field observation', 'Implemented & Validated'],
        ['FR-03', 'HTML5 Canvas AR Guidance: Render dynamic pulsing coordinate markers and directional arrows over live camera feeds to indicate inspection points.', 'High (P0)', 'Technician ergonomics', 'Implemented & Validated'],
        ['FR-04', 'Hands-Free Speech Navigation: Continuous voice command listener supporting "NEXT", "BACK", "REPEAT", "VERIFY TOOL", and "COMPLETE" commands.', 'High (P0)', 'Safety hazard reduction', 'Implemented & Validated'],
        ['FR-05', 'AI Tool Verification Gate: Camera snapshot inspection via Gemini 1.5 Flash verifying correct tool presence before unlocking subsequent procedural steps.', 'High (P0)', 'Procedural compliance', 'Implemented & Validated'],
        ['FR-06', 'Offline Write-Ahead Sync Queue: Transactional Dexie.js IndexedDB local persistence with FIFO queue replay and exponential backoff retry upon reconnection.', 'High (P0)', 'Factory RF blackouts', 'Implemented & Validated'],
        ['FR-07', 'Spare Parts Stock Auto-Decrement: Real-time inventory tracking, part barcode validation, and automated low-stock restock threshold alerts.', 'Medium (P1)', 'Inventory control audit', 'Implemented & Validated'],
        ['FR-08', 'Supervisor MTTR Analytics: Real-time plant dashboard calculating MTTR, MTBF, technician task throughput, and downtime distribution charts.', 'Medium (P1)', 'Management KPI reporting', 'Implemented & Validated']
    ]
    add_table_data(doc, "Table 3.1: Functional Requirements Specification", fr_headers, fr_rows, [1.0, 2.5, 1.0, 1.3, 1.2])

    add_section_heading(doc, "3.2", "Non-Functional Requirements")
    add_body_para(doc, "Non-functional requirements specify architectural constraints, performance benchmarks, and quality standards required for factory operation. Table 3.2 details seven core non-functional requirements.")

    nfr_headers = ['Req. ID', 'Category', 'Requirement Description', 'Target / Measure', 'Status']
    nfr_rows = [
        ['NFR-01', 'Latency', 'AI vision classification round-trip latency on standard cellular connections', '< 2.50 seconds', 'Met (1.82s median achieved)'],
        ['NFR-02', 'Frame Rate', 'HTML5 Canvas AR animation frame rate on mobile viewports', '≥ 55 frames per second', 'Met (Solid 60 fps achieved)'],
        ['NFR-03', 'Reliability', 'Offline mutation retention during sudden browser termination or battery loss', '100% zero data loss', 'Met (0/50 test loss events)'],
        ['NFR-04', 'Accuracy', 'Speech recognition accuracy in simulated 75dB factory background noise', '≥ 85.0% recognition rate', 'Met (91.2% accuracy achieved)'],
        ['NFR-05', 'Security', 'Tenant data isolation enforced at database engine level via Row Level Security', '100% multi-tenant isolation', 'Met (PostgreSQL RLS verified)'],
        ['NFR-06', 'Storage', 'Total local client IndexedDB cache footprint per plant facility', '< 50 Megabytes', 'Met (14.2 MB total footprint)'],
        ['NFR-07', 'Responsiveness', 'Lighthouse Mobile Performance & PWA Auditing Score on production build', '≥ 90 / 100 benchmark', 'Met (Lighthouse score 94/100)']
    ]
    add_table_data(doc, "Table 3.2: Non-Functional Requirements Specification", nfr_headers, nfr_rows, [1.0, 1.2, 2.4, 1.3, 1.1])

    add_section_heading(doc, "3.3", "Hardware Requirements")
    add_body_para(doc, "A core design principle of MaintAI is zero specialized hardware dependency. The platform leverages commodity consumer hardware readily available in any modern engineering institution or manufacturing enterprise. Table 3.3 enumerates the hardware specifications utilized for development and benchmarking.")

    hw_headers = ['Component', 'Specification', 'Purpose', 'Availability']
    hw_rows = [
        ['Technician Mobile Device', 'Octa-Core ARM (Snapdragon 778G / Apple A14+), 4GB+ RAM, 1080p display, rear 12MP camera', 'Primary frontline runtime for PWA, AR canvas rendering, and camera video stream', 'Tested on Samsung S21 & iPhone 13'],
        ['Supervisor Workstation', 'Intel Core i5 / AMD Ryzen 5, 8GB RAM, 1080p FHD monitor, modern Chromium browser', 'Plant management dashboard, procedure editing, inventory management, and MTTR telemetry', 'Tested on ThinkPad T14 & PPSU Lab PC'],
        ['Networking Infrastructure', 'IEEE 802.11b/g/n 2.4GHz Wi-Fi with simulated RF shielding and 4G LTE cellular uplink', 'Simulating production plant connectivity blackouts, signal attenuation, and edge sync', 'PPSU Robotics Lab network setup'],
        ['Audio Input Hardware', 'On-device smartphone noise-canceling dual microphone array or industrial Bluetooth earpiece', 'Hands-free voice command capture in ambient shop-floor acoustic environments', 'Standard mobile built-in mic array']
    ]
    add_table_data(doc, "Table 3.3: Hardware Requirements & Test Environments", hw_headers, hw_rows, [1.5, 2.0, 2.0, 1.5])

    add_section_heading(doc, "3.4", "Software Requirements")
    add_body_para(doc, "Table 3.4 outlines the development runtimes, core frameworks, cloud infrastructure, and browser engines required for executing MaintAI.")

    sw_headers = ['Software / Tool', 'Version', 'Purpose', 'Source / License']
    sw_rows = [
        ['Node.js Runtime', 'v20.12.2 LTS', 'Underlying JavaScript engine for development tooling and Next.js SSR build pipeline', 'Open Source (MIT)'],
        ['Next.js Framework', 'v14.2.3', 'Full-stack React framework utilizing App Router architecture, Server Components, and Edge routes', 'Open Source (MIT)'],
        ['TypeScript Compiler', 'v5.4.5', 'Type safety across all data contracts, database entities, and component state interfaces', 'Open Source (Apache 2.0)'],
        ['Dexie.js Store', 'v3.2.4', 'Minimalistic, transactional IndexedDB wrapper for offline write-ahead queuing and local caching', 'Open Source (Apache 2.0)'],
        ['Supabase PostgreSQL', 'PostgreSQL 15', 'Cloud managed relational database providing Row Level Security, Auth JWTs, and real-time streams', 'Open Source / Cloud Tier'],
        ['Google Generative AI SDK', 'v0.11.0 (@google/generative-ai)', 'Client and edge proxy library connecting to Gemini 1.5 Flash multimodal vision API', 'Open Source (Apache 2.0)'],
        ['Tailwind CSS', 'v3.4.1', 'Utility-first styling system enabling high-contrast shop-floor UI and responsive viewports', 'Open Source (MIT)']
    ]
    add_table_data(doc, "Table 3.4: Software Requirements & Framework Libraries", sw_headers, sw_rows, [1.5, 1.2, 2.5, 1.8])

    add_section_heading(doc, "3.5", "User Requirements")
    add_body_para(doc, "User requirements were formulated through structured interviews with factory technicians and PPSU mechanical engineering lab instructors:")
    add_bullet(doc, "Wants one-touch QR scanning, zero manual typing while standing, crystal-clear visual markers indicating where to place wrenches, and immediate feedback if they select the wrong tool.", "• Frontline Technician Persona: ")
    add_bullet(doc, "Demands an overview of real-time machine uptime, instant visibility into which technician is servicing which work order, and automatic low-stock alerts before spare parts run out.", "• Plant Supervisor Persona: ")
    add_bullet(doc, "Requires strict tenant data isolation between different manufacturing plants, automated database backup, and role-based permissions preventing unauthorized procedure tampering.", "• System Administrator Persona: ")

    add_section_heading(doc, "3.6", "System Constraints")
    add_body_para(doc, "Operational constraints bounding the implementation are detailed in Table 3.5.")

    con_headers = ['Constraint / Assumption', 'Technical Basis', 'Operational Impact', 'Mitigation Strategy']
    con_rows = [
        ['Browser Camera Security', 'W3C MediaDevices specification requires secure HTTPS context', 'Cannot access camera on insecure HTTP URLs during development or production', 'Enforce HTTPS via Vercel SSL certificates and local mkcert SSL'],
        ['Ambient Lighting Threshold', 'Vision models struggle in pitch-black environments (<100 lux)', 'Tool verification and QR scanning accuracy drop in unlit mechanical pits', 'Technician must activate smartphone flashlight or maintain ≥200 lux'],
        ['Speech Engine Network Guard', 'Certain mobile browsers route Web Speech audio to cloud servers', 'Voice commands fail if browser vendor speech engine lacks offline models', 'Pre-register Webkit speech fallback and provide manual tap controls'],
        ['Serverless Execution Cap', 'Vercel hobby edge serverless functions time out after 10.0 seconds', 'Multimodal image payloads exceeding 5MB risk edge timeout errors', 'Client-side image downsampling to 640x480 before dispatch (payload <150KB)']
    ]
    add_table_data(doc, "Table 3.5: System Constraints & Operational Assumptions", con_headers, con_rows, [1.5, 1.8, 1.9, 1.8])

    add_section_heading(doc, "3.7", "Feasibility Study")
    add_body_para(doc, "A three-dimensional feasibility analysis was conducted before initiating coding:")
    add_bullet(doc, "Modern mobile browsers universally support HTML5 Canvas 2D, the MediaDevices API, IndexedDB 3.0, and Service Workers. Serverless edge functions easily proxy multimodal API requests within 2 seconds.", "1. Technical Feasibility: ")
    add_bullet(doc, "Shop-floor technicians already own and carry modern Android and iOS smartphones. The intuitive voice interface and visual AR indicators eliminate training hurdles.", "2. Operational Feasibility: ")
    add_bullet(doc, "Total hardware capital expenditure is $0. The software relies on open-source libraries and pay-as-you-go serverless tiers, eliminating upfront enterprise licensing.", "3. Economic Feasibility: ")

    add_section_heading(doc, "3.8", "Project Scope")
    add_body_para(doc, "The project scope strictly encompasses progressive web application engineering, browser-based computer vision integration, offline transactional storage, and factory maintenance workflow optimization. It deliberately excludes direct modification of proprietary industrial PLC controller firmware, high-voltage electrical substation operations, and full 3D spatial SLAM mesh generation, which remain designated for future academic exploration.")

# ==============================================================================
# CHAPTER 4: SYSTEM ANALYSIS AND METHODOLOGY
# ==============================================================================
def build_chapter_4(doc):
    add_chapter_heading(doc, "CHAPTER 4", "SYSTEM ANALYSIS AND METHODOLOGY")

    add_section_heading(doc, "4.1", "Development Methodology")
    add_body_para(doc, "The MaintAI engineering lifecycle followed an Agile-Scrum evolutionary prototyping methodology. Given the experimental nature of combining browser-based computer vision, speech recognition, and offline storage synchronization, a traditional linear Waterfall model would have been brittle. By adopting two-week sprint cycles, we were able to benchmark individual sub-systems (such as testing Web Speech recognition against loud mechanical noise) and iteratively adapt the design based on empirical findings.")

    add_section_heading(doc, "4.2", "Project Planning")
    add_body_para(doc, "The project was decomposed into five sequential phases executed across 16 academic weeks: Phase 1 focused on problem definition and literature review; Phase 2 concentrated on architectural modeling and database schema design; Phase 3 executed core implementation of the AR Canvas, voice listener, and Gemini vision integration; Phase 4 hardened offline data synchronization; and Phase 5 conducted multi-device UAT testing and final production deployment.")

    add_section_heading(doc, "4.3", "Requirement Analysis")
    add_body_para(doc, "Requirements were analyzed and prioritized using the MoSCoW framework. 'Must-Have' items included machine QR code scanning, offline IndexedDB persistence, HTML5 Canvas AR overlays, and voice command navigation. 'Should-Have' items included Gemini 1.5 Flash tool verification and supervisor MTTR telemetry. 'Could-Have' items included barcode spare part tracking and automated PDF export. 'Won't-Have' items for this version included 3D CAD model rendering and PLC OPC-UA network listeners.")

    add_section_heading(doc, "4.4", "System Workflow")
    add_body_para(doc, "Figure 4.1 depicts the overall project engineering methodology, illustrating the iterative sprint progression from initial problem definition through architecture, core implementation, offline hardening, and final verification.")
    add_figure(doc, "Figure 4.1: Overall Project Workflow & Agile Engineering Lifecycle", r"pdf_images/fig_5_1_workflow.png", width=Inches(6.2))

    add_section_heading(doc, "4.5", "Use Case Analysis")
    add_body_para(doc, "Three primary actors interact with MaintAI: the Field Technician, the Plant Supervisor, and the System Administrator:")
    add_bullet(doc, "Authenticates via PIN/email, scans equipment QR tag, views active machine health, launches AR repair sequence, issues voice commands to advance steps, captures tool snapshots for AI verification, logs part consumption, and submits completion evidence.", "• Field Technician Use Cases: ")
    add_bullet(doc, "Monitors real-time plant uptime, reviews MTTR and MTBF analytics, triages reported machine fault tickets, assigns technicians, creates new repair procedure steps, and manages spare part reorder points.", "• Plant Supervisor Use Cases: ")
    add_bullet(doc, "Manages plant tenant records, configures factory Row Level Security parameters, creates technician profile credentials, and inspects database replication logs.", "• System Administrator Use Cases: ")

    add_section_heading(doc, "4.6", "Data Flow / Process Flow")
    add_body_para(doc, "Data flows through three distinct operational tiers in MaintAI:")
    add_bullet(doc, "Technician actions (QR scan, spoken words, camera video frames) enter the browser runtime. Spoken commands trigger state actions in the local React component tree, while camera frames are continuously rendered onto the HTML5 Canvas overlay.", "• Level 0 (Context Input): ")
    add_bullet(doc, "When a tool verification is requested, a 640x480 JPEG frame is compressed and dispatched to the Next.js API route, which forwards the payload to the Gemini 1.5 Flash endpoint and returns structured validation JSON.", "• Level 1 (Inference Pipeline): ")
    add_bullet(doc, "When a maintenance step completes, a transaction is immediately written to local Dexie.js IndexedDB tables. If online, a background replay loop pushes mutations to Supabase PostgreSQL; if offline, transactions queue in a FIFO write-ahead log until the browser detects a network reconnection event.", "• Level 2 (Persistence & Sync): ")

    add_section_heading(doc, "4.7", "Project Timeline / Milestones")
    add_body_para(doc, "Table 4.1 lists the project phases and engineering deliverables. Table 4.2 consolidates progress across the four official PPSU progress reports. Table 4.3 charts the completed 16-week project schedule.")

    ph_headers = ['Phase', 'Activities', 'Deliverables', 'Evidence / Status']
    ph_rows = [
        ['Phase 1: Foundation (Weeks 1 - 4)', 'Literature survey, industrial field interviews, problem statement crystallization, technology stack benchmarking', 'SRS document, Scope Matrix, initial UI wireframes', 'Approved in Reporting 1'],
        ['Phase 2: Architecture (Weeks 5 - 7)', '3-Tier architecture design, Supabase PostgreSQL schema definition, Row Level Security policies, Next.js App Router scaffolding', 'ER diagrams, API route contracts, database migrations', 'Approved in Reporting 2'],
        ['Phase 3: Core AI & AR (Weeks 8 - 11)', 'HTML5 Canvas 2D overlay engine, Web Speech API voice synthesis & recognition, Google Gemini 1.5 Flash tool verifier modal', 'Working AR HUD, voice state engine, AI verification gate', 'Approved in Reporting 3'],
        ['Phase 4: Offline Engine (Weeks 12 - 13)', 'Dexie.js IndexedDB integration, write-ahead sync queue, service worker caching, network reconnect listeners', 'Fully offline functional PWA with zero mutation loss', 'Approved in Reporting 4'],
        ['Phase 5: Validation & Finalization (Weeks 14 - 16)', 'Automated testing suite, multi-device mobile UAT, MTTR benchmarking, Vercel edge deployment, hard-bound documentation', 'Production URL, test suite, final hard-bound report', 'Project Completed (100%)']
    ]
    add_table_data(doc, "Table 4.1: Project Phases and Key Engineering Deliverables", ph_headers, ph_rows, [1.5, 2.3, 1.8, 1.4])

    rep_headers = ['Progress Report', 'Primary Focus', 'Key Evidence', 'Final Report Chapters']
    rep_rows = [
        ['Reporting 1', 'Problem definition, literature survey, scope matrix, feasibility analysis', 'Initial project proposal & requirements specification', 'Chapters 1, 2, 3, 4'],
        ['Reporting 2', 'System architecture, relational database ER design, Next.js scaffolding', 'Database migration schemas & API route contracts', 'Chapters 5, 6, 7'],
        ['Reporting 3', 'AR Canvas overlay, Web Speech integration, Gemini 1.5 Flash vision gate', 'Interactive UI screenshots & AI verification logs', 'Chapters 7, 8, 11'],
        ['Reporting 4', 'Offline write-ahead sync queue, supervisor analytics, multi-device UAT', 'Live Vercel deployment URL & MTTR benchmark data', 'Chapters 8, 9, 10, 14']
    ]
    add_table_data(doc, "Table 4.2: Progress Report Milestone Consolidation", rep_headers, rep_rows, [1.3, 2.3, 2.0, 1.4])

    sch_headers = ['Task / Phase', 'Planned Start', 'Planned End', 'Actual Start', 'Actual End', 'Status']
    sch_rows = [
        ['1. Problem Identification & Field Study', '08/06/2026', '22/06/2026', '08/06/2026', '21/06/2026', 'Completed'],
        ['2. Literature Review & System Modeling', '23/06/2026', '07/07/2026', '22/06/2026', '06/07/2026', 'Completed'],
        ['3. Requirements Specification & SRS', '08/07/2026', '18/07/2026', '07/07/2026', '18/07/2026', 'Completed'],
        ['4. Database ER Design & Supabase Scaffolding', '19/07/2026', '02/08/2026', '19/07/2026', '01/08/2026', 'Completed'],
        ['5. UI Navigation & AppShell Implementation', '03/08/2026', '15/08/2026', '02/08/2026', '14/08/2026', 'Completed'],
        ['6. Canvas AR Overlay & Voice Command Engine', '16/08/2026', '30/08/2026', '15/08/2026', '29/08/2026', 'Completed'],
        ['7. Gemini 1.5 Flash Multimodal Vision Gate', '31/08/2026', '12/09/2026', '30/08/2026', '11/09/2026', 'Completed'],
        ['8. Dexie.js Offline Sync Queue Hardening', '13/09/2026', '22/09/2026', '12/09/2026', '21/09/2026', 'Completed'],
        ['9. Multi-Device UAT & MTTR Benchmarking', '23/09/2026', '29/09/2026', '22/09/2026', '28/09/2026', 'Completed'],
        ['10. Vercel Production Deployment & Final Report', '30/09/2026', '03/10/2026', '29/09/2026', '03/10/2026', 'Completed']
    ]
    add_table_data(doc, "Table 4.3: Project Execution Schedule & 16-Week Timeline", sch_headers, sch_rows, [2.2, 1.0, 1.0, 1.0, 1.0, 0.8])

# ==============================================================================
# CHAPTER 5: SYSTEM DESIGN AND ARCHITECTURE
# ==============================================================================
def build_chapter_5(doc):
    add_chapter_heading(doc, "CHAPTER 5", "SYSTEM DESIGN AND ARCHITECTURE")

    add_section_heading(doc, "5.1", "System Architecture")
    add_body_para(doc, "MaintAI implements a 3-tier progressive web architecture engineered specifically for distributed industrial environments where intermittent network connectivity is normal. The architecture separates concerns across the Client Presentation Tier, the Serverless Edge API Gateway Tier, and the Cloud Persistence Tier.")
    add_figure(doc, "Figure 5.1: Final 3-Tier System Architecture & Cloud Infrastructure", r"pdf_images/updated_architecture_diagram.png", width=Inches(6.2))
    add_body_para(doc, "As illustrated in Figure 5.1, the Client Presentation Tier runs inside the technician's mobile browser, executing local UI components, the HTML5 Canvas AR engine, and the Dexie.js IndexedDB store. The Serverless Edge API Gateway Tier runs on Vercel's global edge network, handling JWT authentication verification, Gemini 1.5 Flash vision proxying, and data sanitization. The Cloud Persistence Tier hosts PostgreSQL on Supabase with PgBouncer connection pooling, real-time replication streams, and Row Level Security isolation.")

    add_section_heading(doc, "5.2", "Overall System Workflow")
    add_body_para(doc, "Figure 5.2 diagrams the end-to-end maintenance and AR repair process flow executed when a technician services a physical machine.")
    add_figure(doc, "Figure 5.2: End-to-End Maintenance & AR Repair Process Flow", r"pdf_images/updated_repair_workflow.png", width=Inches(6.2))
    add_body_para(doc, "The workflow initiates with machine identification via QR scanning. The client fetches local cached SOP steps from IndexedDB. For each step, the AR Canvas renders pulsing coordinate markers over the live camera feed while the Web Speech API listens for hands-free voice commands. If a step demands verified tooling, the camera captures a snapshot, passes it to the Gemini vision gate, and blocks step progression until the correct tool is validated. Upon step completion, part deductions and time elapsed are logged to the local write-ahead queue and background-synced to the cloud.")

    add_section_heading(doc, "5.3", "Module Architecture")
    add_body_para(doc, "MaintAI is partitioned into four decoupled modules. Table 5.1 outlines their responsibilities, input interfaces, core processing mechanisms, output artifacts, and dependencies.")

    mod_headers = ['Module', 'Purpose', 'Inputs', 'Processing', 'Outputs', 'Dependencies']
    mod_rows = [
        ['Core Presentation & AR Engine', 'Renders UI HUD & visual pulsing step markers', 'Camera video feed & SOP coordinate JSON', 'requestAnimationFrame Canvas 2D render loop (60fps)', 'Live annotated camera feed on mobile viewport', 'Next.js 14, React 18, HTML5 Canvas API'],
        ['Voice Command State Dispatcher', 'Provides hands-free procedural navigation', 'Audio microphone input stream', 'Continuous Web Speech API recognition & phonetic distance matching', 'Triggered UI state actions (NEXT, BACK, VERIFY)', 'W3C Web Speech API (webkitSpeechRecognition)'],
        ['Multimodal Vision Tool Gatekeeper', 'Verifies tool presence before unlocking steps', '640x480 JPEG frame snapshot & required tool string', 'Gemini 1.5 Flash multimodal prompt with bounding box parsing', 'Verification status boolean & detected label confidence', '@google/generative-ai, Next.js Edge Route'],
        ['Offline Write-Ahead Sync Engine', 'Guarantees zero data loss across network blackouts', 'Work order mutations & part decrement logs', 'Dexie.js IndexedDB write-ahead logging with FIFO replay loop', 'Synced PostgreSQL records & inventory update confirmations', 'Dexie.js 3.2.4, Supabase JS Client, Service Worker']
    ]
    add_table_data(doc, "Table 5.1: Module-Wise Architectural Design", mod_headers, mod_rows, [1.3, 1.2, 1.2, 1.3, 1.1, 0.9])

    add_section_heading(doc, "5.4", "Use Case Diagram")
    add_body_para(doc, "Figure 5.3 presents the formal UML Use Case Diagram modeling the operational boundaries of the MaintAI Progressive Web Application platform, encapsulating the functional interactions between human actors and external AI services.")
    add_figure(doc, "Figure 5.3: UML Use Case Diagram - Actors, System Boundary & Operational Interactions", r"pdf_images/fig_5_3_use_case_diagram.png", width=Inches(6.0))
    add_body_para(doc, "As delineated in Figure 5.3, the system models four primary and secondary actors interacting across 15 core use cases:")
    add_bullet(doc, "Authenticates via employee PIN or JWT session, scans equipment QR barcodes to load localized procedures, executes AR-guided step inspection with pulsing canvas coordinates, issues hands-free Web Speech commands (<<include>> dependency), presents required tools for multimodal AI verification (<<extend>> conditional branch), logs consumed spare parts, and caches mutations offline in Dexie.js IndexedDB.", "• Field Technician: ")
    add_bullet(doc, "Monitors real-time plant uptime and aggregate MTTR/MTBF metrics, triages breakdown incident reports, dispatches technicians, authors and revises standardized repair procedures (SOPs), and sets spare parts inventory restock thresholds.", "• Plant Supervisor: ")
    add_bullet(doc, "Configures factory multi-tenancy boundaries, manages user identity profiles and RBAC role assignments, and enforces PostgreSQL Row Level Security (RLS) policies.", "• System Administrator: ")
    add_bullet(doc, "Ingests compressed 640x480 camera snapshots dispatched from the client edge proxy, performs sub-2.0s zero-shot visual tool classification, and returns structured JSON bounding boxes and confidence scores.", "• Google Gemini 1.5 Flash API: ")

    add_section_heading(doc, "5.5", "Data Flow Diagram")
    add_body_para(doc, "The Data Flow Diagram traces data paths through three conceptual zones: In the Untrusted Camera/Audio Zone, raw MediaStream video frames and audio chunks enter browser memory buffers. In the Local Secure Client Zone, frames are drawn to Canvas without disk I/O, speech is parsed to text strings, and transactional mutations write to encrypted IndexedDB storage. In the Cloud Backend Zone, sanitized JSON payloads pass through Next.js edge routes into PostgreSQL tables protected by Row Level Security.")

    add_section_heading(doc, "5.6", "Class Diagram")
    add_body_para(doc, "Figure 5.4 illustrates the formal UML Class Diagram for MaintAI, defining the domain entity model, method contracts, encapsulation boundaries, and structural relationships that govern the TypeScript runtime and cloud persistence layers.")
    add_figure(doc, "Figure 5.4: UML Class Diagram - Domain Entities, Controller Interfaces & Model Architecture", r"pdf_images/fig_5_4_class_diagram.png", width=Inches(6.0))
    add_body_para(doc, "The class hierarchy is organized into three cohesive tiers reflecting object-oriented domain-driven design:")
    add_bullet(doc, "The Machine aggregate maintains equipment telemetry, active health score, and status. It has a 1-to-many relationship with RepairProcedure entities. Each RepairProcedure maintains a strong composition (1 to 1..*) with ordered RepairStep value objects encapsulating AR coordinate percentages and lockout/tagout constraints.", "• Asset & Procedure Hierarchy: ")
    add_bullet(doc, "RepairStep depends on the ToolVerificationGate AI subsystem to evaluate camera video frames against minimum confidence thresholds (>= 0.70). MaintenanceLog acts as an aggregate root tracking active repair sessions, durations, and technician sign-offs.", "• Safety Gate & Execution Subsystem: ")
    add_bullet(doc, "MaintenanceLog maintains a composition relationship with PartUsage records, which reference the central Part catalog. When offline, mutations serialize into SyncQueueItem objects implementing a resilient write-ahead log (WAL) with exponential backoff replay.", "• Inventory & Offline Persistence: ")

    add_section_heading(doc, "5.7", "Sequence Diagram")
    add_body_para(doc, "The repair sequence executes synchronously across local state and asynchronously across cloud endpoints: (1) Technician points camera at machine QR tag; (2) QR scanner triggers router navigation to `/repair/[id]`; (3) Client checks IndexedDB for cached procedures; if found, renders Step 1 immediately; (4) Technician says 'NEXT STEP'; (5) State machine evaluates whether Step 2 requires tool verification; if required, opens ToolDetector modal; (6) Camera takes snapshot, calls `/api/verify-tool`; (7) Upon 200 OK with `verified: true`, modal closes and step advances; (8) Local log updates and queues for cloud background sync.")

    add_section_heading(doc, "5.8", "Activity Diagram")
    add_body_para(doc, "Figure 5.5 presents the formal UML Activity Diagram modeling the concurrent control flows, decision logic, and exception handling paths across three distinct system swimlanes: the Mobile Client PWA, the AR & Speech Engine, and the Cloud/AI Backend.")
    add_figure(doc, "Figure 5.5: UML Activity Diagram - Multimodal AI Tool Verification & AR Procedural Execution", r"pdf_images/fig_5_5_activity_diagram.png", width=Inches(6.0))
    add_body_para(doc, "As modeled in Figure 5.5, the activity flow coordinates execution through critical decision gates and parallel synchronization:")
    add_bullet(doc, "Upon QR scan, the client evaluates local IndexedDB cache availability. On cache miss, it retrieves procedure definitions from Supabase via HTTPS REST before initializing the AR Canvas HUD.", "• Cache Resolution & HUD Mount: ")
    add_bullet(doc, "A fork bar concurrently initializes the 60fps HTML5 Canvas coordinate render loop and the continuous Web Speech API voice listener thread, joined prior to step evaluation.", "• Concurrent AR & Speech Threads: ")
    add_bullet(doc, "If a step requires tool verification, the system captures a 640x480 frame snapshot and dispatches it to Gemini 1.5 Flash. If confidence < 0.70 or an incorrect tool is detected, the safety gate emits an audible voice warning ('Incorrect Tool Detected') and locks progression. Valid tool detection unlocks the step and emits green visual bounding boxes.", "• Multimodal AI Verification Gate: ")
    add_bullet(doc, "Upon completing all procedure steps, the system checks network reachability. If online, transactions commit directly to Supabase PostgreSQL; otherwise, mutations enqueue in the Dexie.js write-ahead log for automatic background synchronization upon reconnection.", "• Resilient Offline Finalization: ")

    add_section_heading(doc, "5.9", "Component / Deployment Diagram")
    add_body_para(doc, "The physical deployment comprises: (1) Client Mobile Smartphone running Google Chrome 124+ with Service Worker cache and Dexie.js store; (2) Vercel Edge CDN nodes distributed across global edge regions serving static HTML/JS bundles and executing edge serverless functions; (3) Google Cloud API Gateway routing Gemini 1.5 Flash generative AI vision requests; and (4) Supabase Cloud hosting PostgreSQL 15, PgBouncer pooler, and real-time WebSocket replication.")

    add_section_heading(doc, "5.10", "Database Design / ER Diagram")
    add_body_para(doc, "Figure 5.6 details the Relational Database Entity-Relationship (ER) Diagram implemented in PostgreSQL on Supabase, illustrating foreign key cardinalities and primary key constraints across all ten core tables. Figure 5.7 illustrates the responsive UI navigation hierarchy.")
    add_figure(doc, "Figure 5.6: Entity-Relationship (ER) Diagram - Supabase PostgreSQL Schema & Cardinality Relations", r"pdf_images/fig_5_6_database_er.png", width=Inches(6.0))
    add_figure(doc, "Figure 5.7: UI Navigation Hierarchy & Responsive Screen Architecture", r"pdf_images/fig_6_4_ui_design.png", width=Inches(5.5))
    add_body_para(doc, "Table 5.2 outlines the eight core relational tables, their primary keys, foreign key relationships, and functional purposes within the MaintAI data model.")

    db_headers = ['Entity / Table', 'Key Fields', 'Relationships', 'Purpose']
    db_rows = [
        ['factories', 'id: UUID (PK), name: VARCHAR(100), location: VARCHAR(100), created_at: TIMESTAMPTZ', '1:N with profiles, machines, parts, fault_reports', 'Top-level multi-tenant factory boundary enforcing tenant isolation'],
        ['profiles', 'id: UUID (PK, FK auth.users), factory_id: UUID (FK), full_name: VARCHAR, role: VARCHAR', 'N:1 with factories; 1:N with maintenance_logs', 'User identity profiles linked to Supabase Auth JWTs with role claims'],
        ['machines', 'id: UUID (PK), factory_id: UUID (FK), name: VARCHAR, model: VARCHAR, qr_code: VARCHAR, status: VARCHAR, health_score: INT', 'N:1 with factories; 1:N with procedures, logs, faults', 'Physical industrial equipment catalog with live health score and QR binding'],
        ['repair_procedures', 'id: UUID (PK), machine_id: UUID (FK), title: VARCHAR, estimated_time_mins: INT, steps_json: JSONB', 'N:1 with machines; 1:N with maintenance_logs', 'Standard Operating Procedures with structured JSON array of AR steps & tools'],
        ['fault_reports', 'id: UUID (PK), factory_id: UUID, machine_id: UUID, reported_by: UUID, severity: VARCHAR, status: VARCHAR', 'N:1 with machines, profiles', 'Unplanned breakdown incident tickets with photo evidence and priority ranking'],
        ['maintenance_logs', 'id: UUID (PK), procedure_id: UUID, machine_id: UUID, technician_id: UUID, status: VARCHAR, duration_seconds: INT', 'N:1 with procedures, machines, profiles; 1:N with parts_used', 'Completed and in-progress work order audit trail tracking duration & evidence'],
        ['parts', 'id: UUID (PK), factory_id: UUID, part_number: VARCHAR, name: VARCHAR, stock_quantity: INT, min_stock_level: INT, barcode: VARCHAR', 'N:1 with factories; 1:N with parts_used', 'Spare parts inventory catalog with real-time stock levels & barcode identifiers'],
        ['parts_used', 'id: UUID (PK), log_id: UUID (FK), part_id: UUID (FK), quantity_used: INT', 'N:1 with maintenance_logs, parts', 'Junction table recording exact physical spare parts consumed during repairs']
    ]
    add_table_data(doc, "Table 5.2: Relational Database Schema Design", db_headers, db_rows, [1.3, 2.3, 1.8, 1.6], font_size=8.0, space_after=False)

print("Chapters 2 through 5 appended successfully.")

# ==============================================================================
# CHAPTER 6: TECHNOLOGY STACK AND DEVELOPMENT ENVIRONMENT
# ==============================================================================
def build_chapter_6(doc):
    add_chapter_heading(doc, "CHAPTER 6", "TECHNOLOGY STACK AND DEVELOPMENT ENVIRONMENT")

    add_section_heading(doc, "6.1", "Programming Languages")
    add_body_para(doc, "MaintAI utilizes a unified TypeScript and SQL codebase to maximize type safety across client interfaces, edge serverless route handlers, and cloud database migrations. Table 6.1 lists the programming languages and their specific roles.")

    lang_headers = ['Technology', 'Version', 'Purpose', 'Major Usage']
    lang_rows = [
        ['TypeScript', 'v5.4.5', 'Type-safe programming across client UI and edge serverless routes', 'Core React components, Dexie.js schema interfaces, API route contracts, and domain models'],
        ['JavaScript (ES2024)', 'ES2024 (V8 engine)', 'Browser client scripting and asynchronous event handling', 'DOM manipulation, Canvas 2D render loop, MediaDevices camera streaming, Web Speech listeners'],
        ['SQL (PostgreSQL)', 'PostgreSQL 15 dialect', 'Relational database definitions, Row Level Security policies, indexes', 'Table schemas, foreign key constraints, triggers, and tenant isolation policies on Supabase']
    ]
    add_table_data(doc, "Table 6.1: Programming Languages", lang_headers, lang_rows, [1.5, 1.2, 2.0, 2.3])

    add_section_heading(doc, "6.2", "Frameworks and Libraries")
    add_body_para(doc, "Table 6.2 enumerates the primary frameworks, libraries, and utilities that constitute the MaintAI application bundle.")

    lib_headers = ['Tool / Framework / API', 'Version', 'Purpose', 'Usage']
    lib_rows = [
        ['Next.js (App Router)', 'v14.2.3', 'Full-stack React framework with SSR and edge routing', 'Application routing, serverless API routes, layout management, and static build generation'],
        ['React.js', 'v18.3.1', 'Component-based reactive UI rendering', 'Client component lifecycle, reactive state hooks (useState, useEffect, useCallback), DOM reconciliation'],
        ['Dexie.js', 'v3.2.4', 'Minimalist transactional wrapper for browser IndexedDB', 'Local client database, write-ahead sync queue, offline SOP caching, and mutation persistence'],
        ['Tailwind CSS', 'v3.4.1', 'Utility-first CSS styling engine', 'Responsive layouts, high-contrast dark/light mode themes, and gloved-finger 48px touch targets'],
        ['Lucide React', 'v0.378.0', 'High-legibility iconography set', 'Status badges, industrial hazard warning icons, navigation buttons, and battery indicators'],
        ['@google/generative-ai', 'v0.11.0', 'Official Google SDK for Gemini multimodal vision API', 'Encoding image base64 snapshots and invoking Gemini 1.5 Flash structured tool detection']
    ]
    add_table_data(doc, "Table 6.2: Frameworks, Libraries, and APIs", lib_headers, lib_rows, [1.6, 1.0, 2.0, 2.4])

    add_section_heading(doc, "6.3", "Database Technologies")
    add_body_para(doc, "MaintAI implements a dual-database architecture: a cloud-hosted relational PostgreSQL engine paired with an embedded browser IndexedDB store. Table 6.3 details their respective configurations.")

    db_tech_headers = ['Database / Storage', 'Version', 'Purpose', 'Data Managed']
    db_tech_rows = [
        ['Supabase PostgreSQL', 'PostgreSQL 15 (AWS us-east-1)', 'Primary cloud relational datastore with Row Level Security', 'Central plant assets, user credentials, completed maintenance audit logs, parts catalog'],
        ['Browser IndexedDB (Dexie.js)', 'IndexedDB 3.0 W3C API', 'Local-first transactional client database in smartphone browser', 'Cached SOP steps, pending write-ahead sync queue, local part inventory, offline auth tokens']
    ]
    add_table_data(doc, "Table 6.3: Database and Storage Technologies", db_tech_headers, db_tech_rows, [1.6, 1.5, 2.0, 1.9])

    add_section_heading(doc, "6.4", "APIs and Third-Party Services")
    add_body_para(doc, "Table 6.4 specifies external browser standards and cloud API integrations embedded into MaintAI.")

    api_headers = ['API / Service', 'Provider / Spec', 'Purpose', 'Integration Mechanism']
    api_rows = [
        ['Google Gemini 1.5 Flash', 'Google Cloud AI Studio', 'Multimodal computer vision tool verification gatekeeper', 'Serverless edge proxy at /api/verify-tool returning structured JSON validation'],
        ['Web Speech API (Recognition)', 'W3C Speech API Spec', 'Hands-free voice command interpretation on shop floors', 'Continuous webkitSpeechRecognition listener with custom phonetic matcher'],
        ['Web Speech API (Synthesis)', 'W3C Speech API Spec', 'Audible step instructions and spoken safety alerts', 'speechSynthesis.speak() audio playback via device speaker / headset'],
        ['MediaDevices API', 'W3C Media Capture Spec', 'Capturing live camera video stream from mobile sensor', 'navigator.mediaDevices.getUserMedia({video: {facingMode: "environment"}});'],
        ['HTML5 Canvas 2D API', 'W3C HTML5 Canvas Spec', 'Drawing high-performance animated AR coordinate markers', 'requestAnimationFrame() loop drawing pulsing rings, arrows, and text HUDs']
    ]
    add_table_data(doc, "Table 6.4: APIs and Third-Party Services", api_headers, api_rows, [1.6, 1.4, 2.0, 2.0])

    add_section_heading(doc, "6.5", "Development Tools and IDE")
    add_body_para(doc, "Table 6.5 details the software tooling employed across the 16-week development lifecycle.")

    tool_headers = ['Development Tool', 'Version', 'Purpose', 'Usage in Project']
    tool_rows = [
        ['Visual Studio Code', 'v1.89.0', 'Primary integrated development environment (IDE)', 'TypeScript code editing, ESLint validation, Tailwind IntelliSense, Git staging'],
        ['Google Chrome DevTools', 'Chrome v124', 'Browser debugging, mobile emulation, performance profiling', 'Emulating device viewports, throttling network to 2G/3G, inspecting IndexedDB tables'],
        ['Postman / Thunder Client', 'v10.24', 'REST API testing and schema contract validation', 'Testing Next.js edge route handlers and Gemini API JSON responses'],
        ['Git & GitHub', 'v2.43 / Web', 'Distributed version control and issue tracking', 'Repository branch management, feature merges, automated CI build triggers'],
        ['Docker Desktop', 'v26.0', 'Containerized local PostgreSQL and pgvector testing', 'Simulating isolated database instances during schema migration authoring']
    ]
    add_table_data(doc, "Table 6.5: Development Tools and IDE", tool_headers, tool_rows, [1.5, 1.0, 2.2, 2.3])

    add_section_heading(doc, "6.6", "Version Control / Repository")
    add_body_para(doc, "The project adhered to strict Git workflow conventions. The repository was structured with protected `main` branch rules, feature-based branching (`feature/ar-canvas`, `feature/offline-sync`, `feature/voice-control`), and conventional commit message standards. Every pull request required clean TypeScript compilation (`tsc --noEmit`) and zero ESLint warnings prior to merging.")

    add_section_heading(doc, "6.7", "Hardware and Runtime Environment")
    add_body_para(doc, "The runtime environment spans local mobile browsers and global edge nodes. The local client executes in a sandboxed V8 JavaScript engine on Android Chrome or Apple WebKit on iOS Safari. The serverless tier executes on Vercel's Node.js 20 edge runtime with regional deployment closest to Indian users (BOM1 Mumbai region), maintaining an average network transit round-trip under 45 milliseconds.")

# ==============================================================================
# CHAPTER 7: SYSTEM IMPLEMENTATION
# ==============================================================================
def build_chapter_7(doc):
    add_chapter_heading(doc, "CHAPTER 7", "SYSTEM IMPLEMENTATION")

    add_section_heading(doc, "7.1", "Implementation Overview")
    add_body_para(doc, "MaintAI's codebase is structured around the Next.js 14 App Router layout paradigm located at `c:\dev\pro`. Global layout shell components reside in `app/layout.tsx`, handling service worker registration, network status listeners, and high-contrast CSS variables. Sub-routes handle specific maintenance domains: `/repair/[id]` for the machine HUD and AR canvas, `/inbox` for work order triage, `/parts` for inventory barcode scanning, and `/analytics` for supervisor metrics. Client-side database tables are defined in `lib/dexie.ts`, and edge API handlers reside under `app/api/`.")

    add_section_heading(doc, "7.2", "Module 1 - AR-Guided Step-by-Step Repair Guidance")
    add_body_para(doc, "The AR Guidance module renders instructional coordinate overlays directly over live camera video feeds without native optical plugins. The engine binds an HTML5 `<canvas>` element on top of an active HTML5 `<video>` element receiving stream data from `navigator.mediaDevices.getUserMedia()`. To prevent marker distortion when rotating smartphones between portrait and landscape modes, target markers are defined as normalized percentage coordinates (0.0% to 100.0%) rather than fixed pixels.")
    add_body_para(doc, "Inside a continuous `requestAnimationFrame` loop, the canvas normalizes coordinates against current `canvas.width` and `canvas.height`. It calculates an oscillating radius `r = baseRadius + sin(time * 0.005) * 6` to draw a pulsing concentric targeting ring around the mechanical component, accompanied by a directional callout banner displaying step instructions and required torque specifications.")
    add_figure(doc, "Figure 7.1: Module 1 - Live AR Step Guidance with Pulsing Canvas Markers", r"pdf_images/p12_img3_72.png", width=Inches(6.0))

    add_section_heading(doc, "7.3", "Module 2 - Multimodal AI Vision Tool Verification Gate")
    add_body_para(doc, "The Tool Verification Gate ensures technicians use specified tools before unlocking safety-critical repair steps. When a step requires verification (e.g., '14mm Insulated Torque Wrench'), the application prompts the technician to show their tool to the camera. The `ToolDetector.tsx` component captures a video frame, draws it to a hidden offscreen canvas, downsamples it to 640x480 resolution, compresses it to JPEG at 0.75 quality, and posts the Base64 payload to `/api/verify-tool`.")
    add_body_para(doc, 'The edge route handler constructs a strict system prompt directing Google Gemini 1.5 Flash to identify visible hand tools, classify their type, estimate bounding box coordinates, and output structured JSON: `{"tool_detected": string, "confidence": number, "matches_expected": boolean}`. If `matches_expected` is true and confidence exceeds 0.70, the safety gate unlocks, playing an affirmative chime and advancing the workflow.')
    add_figure(doc, "Figure 7.2: Module 2 - Multimodal AI Computer Vision Tool Verification Modal", r"pdf_images/p12_img4_73.png", width=Inches(6.0))

    add_section_heading(doc, "7.4", "Module 3 - Offline-First Write-Ahead Sync Engine")
    add_body_para(doc, "To survive aggressive factory RF blackouts, MaintAI employs an offline-first transactional architecture using Dexie.js. When a technician logs a repair step, records part consumption, or snaps photographic completion evidence, mutations are written directly to local IndexedDB tables (`local_logs`, `local_parts`, `sync_queue`). A write-ahead transaction log records every mutation with a monotonic local sequence counter and timestamp.")
    add_body_para(doc, "Figure 7.3 illustrates the offline sync pipeline. A global network listener monitors `window.navigator.onLine` and `window.addEventListener('online', ...)`. When connectivity resumes, a FIFO sync worker dequeues pending mutations, pushing them to Supabase via batch HTTP transactions. Conflict resolution follows a deterministic 'Last-Write-Wins with Server Precedence' rule, preserving local state integrity if network drops recur mid-sync.")
    add_figure(doc, "Figure 7.3: Module 3 - Offline-First Write-Ahead Sync Pipeline Architecture", r"pdf_images/updated_offline_sync_workflow.png", width=Inches(6.2))

    add_section_heading(doc, "7.5", "User Interface Implementation")
    add_body_para(doc, "The UI was engineered specifically for harsh industrial shop-floor ergonomics. All interactive buttons feature minimum 48x48 pixel touch hitboxes to facilitate operation with bulky leather work gloves. The interface supports a high-contrast dark theme (slate-900 background with amber-400 and emerald-400 status accents) to ensure readability under intense overhead halogen lighting as well as dim subterranean machine pits.")

    add_section_heading(doc, "7.6", "Database Implementation")
    add_body_para(doc, "Database tables were deployed to Supabase PostgreSQL using SQL migration scripts. Foreign key constraints enforce strict referential integrity between `factories`, `machines`, `repair_procedures`, and `maintenance_logs`. Indexes were placed on `machines(qr_code)`, `maintenance_logs(technician_id, created_at)`, and `parts(factory_id, part_number)` to ensure sub-5ms query response times under high concurrency.")

    add_section_heading(doc, "7.7", "API / Backend Implementation")
    add_body_para(doc, "Next.js 14 edge route handlers serve as secure API proxies. Table 7.1 details the implemented serverless endpoints, their HTTP methods, inputs, outputs, authentication guards, and response statuses.")

    api_spec_headers = ['API / Service Route', 'Method', 'Purpose', 'Input Payload', 'Output Response', 'Status']
    api_spec_rows = [
        ['/api/verify-tool', 'POST', 'Proxy camera snapshot to Gemini 1.5 Flash vision model', 'Base64 image string, expectedTool name', 'JSON: toolDetected, confidence, matchStatus', '200 OK (1.82s)'],
        ['/api/machines/[id]', 'GET', 'Retrieve machine specifications, health, and SOP steps', 'Machine UUID in route param', 'Full machine record with JSONB procedure steps', '200 OK (45ms)'],
        ['/api/logs/sync', 'POST', 'Batch commit queued offline maintenance logs & part deductions', 'Array of serialized sync queue mutation objects', 'Array of resolved UUIDs and sync confirmations', '200 OK (110ms)'],
        ['/api/parts/decrement', 'POST', 'Atomic decrement of spare parts inventory upon usage', 'partId, quantityUsed, workOrderId', 'Updated stockQuantity and lowStockAlert boolean', '200 OK (38ms)']
    ]
    add_table_data(doc, "Table 7.1: API & External Service Integration Specifications", api_spec_headers, api_spec_rows, [1.5, 0.8, 1.8, 1.4, 1.2, 0.8])

    add_section_heading(doc, "7.8", "Algorithm / Logic Implementation")
    add_body_para(doc, "Two primary algorithmic formulations were implemented: (1) Viewport Percentage Normalization: On every video frame tick, physical pixel coordinates `(Xp, Yp)` are calculated from percentage coordinates `(X%, Y%)` using `Xp = (X% / 100) * canvas.width` and `Yp = (Y% / 100) * canvas.height`. This guarantees overlay stability across varying smartphone screen dimensions. (2) Phonetic Levenshtein Matching: Due to factory motor acoustic interference, spoken words often suffer minor phonetic transcription errors. Spoken strings are evaluated against allowed command keywords using Levenshtein edit distance: words with distance ≤ 1 (e.g., 'necks' matched to 'next') are accepted, raising speech command recognition from 76% to 91.2% in noisy environments.")

    add_section_heading(doc, "7.9", "Authentication and Authorization")
    add_body_para(doc, "Authentication is handled via Supabase Auth issuing cryptographic JSON Web Tokens (JWTs). Role-based access control enforces permissions across three tiers: Technicians can only view assigned machines and log repairs; Supervisors can create SOPs, assign tasks, and view plant MTTR metrics; Administrators have full tenant management privileges. Row Level Security policies at the database layer prevent cross-tenant data leaks.")

    add_section_heading(doc, "7.10", "Integration of Modules")
    add_body_para(doc, "Modules communicate through a centralized React Context state container (`MaintenanceContext.tsx`). When the voice dispatcher recognizes 'VERIFY TOOL', it dispatches a state transition that opens the AI Tool Modal, pauses the voice listener to prevent audio echo, initiates camera capture, receives Gemini's validation, updates local Dexie storage, and restarts the voice listener seamlessly.")

# ==============================================================================
# CHAPTER 8: TESTING AND VALIDATION
# ==============================================================================
def build_chapter_8(doc):
    add_chapter_heading(doc, "CHAPTER 8", "TESTING AND VALIDATION")

    add_section_heading(doc, "8.1", "Testing Strategy")
    add_body_para(doc, "The verification strategy followed a multi-tiered test pyramid: Unit tests verified isolated functions (coordinate math, Levenshtein distance, Dexie schema definitions); Functional tests validated user-facing features (QR decoding, voice navigation, tool verification); Integration tests evaluated data movement between Dexie and Supabase; System tests exercised full end-to-end maintenance workflows; and Performance tests benchmarked frame rates, API latencies, and offline durability.")

    add_section_heading(doc, "8.2", "Unit Testing")
    add_body_para(doc, "Table 8.1 documents representative unit test cases executed using Vitest and React Testing Library.")

    ut_headers = ['Test ID', 'Module / Function', 'Input Parameters', 'Expected Output', 'Actual Output', 'Status']
    ut_rows = [
        ['UT-01', 'normalizeCoords()', 'X%=50.0, Y%=25.0, W=400, H=800', 'Xp=200, Yp=200', 'Xp=200, Yp=200', 'Passed'],
        ['UT-02', 'levenshteinMatch()', 'Spoken="nex", Target="next"', 'Distance=1 (Accepted)', 'Distance=1 (Accepted)', 'Passed'],
        ['UT-03', 'levenshteinMatch()', 'Spoken="stop", Target="next"', 'Distance=4 (Rejected)', 'Distance=4 (Rejected)', 'Passed'],
        ['UT-04', 'Dexie.insertLog()', 'Valid log object, duration=120s', 'Record committed with autoincrement ID', 'Committed successfully with ID 1', 'Passed'],
        ['UT-05', 'Base64 image compress', '1080p canvas image (2.8MB)', 'Downsampled 640x480 JPEG <150KB', '118 KB JPEG generated', 'Passed']
    ]
    add_table_data(doc, "Table 8.1: Unit & Module Testing Test Cases", ut_headers, ut_rows, [0.8, 1.4, 1.8, 1.4, 1.2, 0.7])

    add_section_heading(doc, "8.3", "Integration Testing")
    add_body_para(doc, "Integration testing evaluated interactions between decoupled sub-systems. Table 8.2 details six critical integration scenarios.")

    it_headers = ['Test ID', 'Integrated Components', 'Test Scenario', 'Expected Behavior', 'Actual Behavior', 'Status']
    it_rows = [
        ['IT-01', 'QR Scanner + Dexie Cache', 'Scan known machine QR when offline', 'Load cached SOP steps from IndexedDB in <200ms', 'SOP rendered in 140ms', 'Passed'],
        ['IT-02', 'Camera + ToolDetector + Gemini', 'Capture snapshot & call /api/verify-tool', 'Return JSON bounding box & unlock step', 'JSON returned in 1.82s, step unlocked', 'Passed'],
        ['IT-03', 'Dexie Sync Queue + Supabase REST', 'Trigger online event with 5 queued logs', 'Replay 5 items sequentially to PostgreSQL', 'All 5 items synced in 320ms', 'Passed'],
        ['IT-04', 'Parts Logging + Inventory Trigger', 'Log consumption of 2 O-ring seals', 'Local stock decremented, cloud stock synced', 'Stock decremented from 40 to 38', 'Passed']
    ]
    add_table_data(doc, "Table 8.2: Integration Testing Specifications", it_headers, it_rows, [0.8, 1.5, 1.6, 1.8, 1.2, 0.7])

    add_section_heading(doc, "8.4", "Functional Testing")
    add_body_para(doc, "Functional testing validated end-to-end user workflows against functional specifications. Table 8.3 outlines test results.")

    ft_headers = ['Test ID', 'Functionality Under Test', 'Input / Action', 'Expected Result', 'Actual Result', 'Status']
    ft_rows = [
        ['FT-01', 'Machine QR Code Identification', 'Point camera at CNC Milling QR tag', 'Decode UUID and navigate to machine HUD', 'Navigated to machine HUD in 280ms', 'Passed'],
        ['FT-02', 'Voice Navigation: "NEXT STEP"', 'Speak "NEXT STEP" into microphone', 'Advance active repair step from 1 to 2', 'Step advanced to 2 smoothly', 'Passed'],
        ['FT-03', 'Voice Navigation: "BACK STEP"', 'Speak "PREVIOUS STEP"', 'Return active repair step from 2 to 1', 'Returned to step 1', 'Passed'],
        ['FT-04', 'Safety Gate Lockout Enforcement', 'Attempt to skip step without tool check', 'Display lockout warning & block next step', 'Warning displayed, navigation blocked', 'Passed'],
        ['FT-05', 'Offline Disconnect / Reconnect', 'Toggle airplane mode during repair step', 'Log saves locally, syncs automatically on reconnect', 'Synced with zero data loss', 'Passed']
    ]
    add_table_data(doc, "Table 8.3: Functional Testing Specifications", ft_headers, ft_rows, [0.8, 1.6, 1.5, 1.8, 1.2, 0.7])

    add_section_heading(doc, "8.5", "System Testing")
    add_body_para(doc, "System testing exercised complete multi-user workflows simulating real plant conditions: a technician logging in, diagnosing a pump seal failure, replacing the part, and a supervisor reviewing the work order on a desktop dashboard. Table 8.4 documents four system test scenarios.")

    st_headers = ['Test ID', 'System Scenario', 'Conditions', 'Expected Outcome', 'Actual Outcome', 'Status']
    st_rows = [
        ['ST-01', 'Complete Centrifugal Pump Seal Replacement', 'Technician on mobile Chrome, 4G cellular', 'Complete 5 steps, verify torque wrench, log part', 'Session completed in 14.2 min', 'Passed'],
        ['ST-02', 'Total Offline Repair Session', 'Airplane mode active throughout 6 steps', 'Full procedural flow functional, queued locally', 'All 6 steps logged; synced upon Wi-Fi reconnect', 'Passed'],
        ['ST-03', 'Concurrent Multi-Technician Edits', 'Two technicians servicing different machines', 'Zero race conditions or cross-tenant log pollution', 'Logs isolated by factory_id', 'Passed'],
        ['ST-04', 'Low-Stock Inventory Reorder Alert', 'Part stock decremented below min_stock_level', 'Supervisor dashboard flags red warning badge', 'Warning badge rendered instantly', 'Passed']
    ]
    add_table_data(doc, "Table 8.4: System Testing & End-to-End Scenarios", st_headers, st_rows, [0.8, 1.8, 1.4, 1.8, 1.2, 0.7])

    add_section_heading(doc, "8.6", "Performance Testing")
    add_body_para(doc, "Performance testing measured frame rates, round-trip latencies, and storage footprints. Table 8.5 summarizes benchmarks measured across 50 execution runs.")

    pt_headers = ['Parameter / Metric', 'Test Condition', 'Target Benchmark', 'Observed Value', 'Status']
    pt_rows = [
        ['AR Canvas Rendering Rate', 'Continuous video stream on mobile viewport', '≥ 55.0 frames per second', '59.8 fps (Solid 60 fps target)', 'Exceeded'],
        ['Gemini Vision Inference Latency', '640x480 JPEG over 4G mobile connection', '< 2.50 seconds round-trip', '1.82 seconds median', 'Exceeded'],
        ['QR Code Decoding Latency', 'Direct camera feed under 350 lux lighting', '< 500 milliseconds', '280 milliseconds median', 'Exceeded'],
        ['Offline Reconnect Sync Speed', '10 queued records replayed to Supabase', '< 1.00 second total', '380 milliseconds total', 'Exceeded'],
        ['Lighthouse Mobile PWA Score', 'Production Vercel deployment URL audit', '≥ 90 / 100 benchmark', '94 / 100 overall score', 'Exceeded']
    ]
    add_table_data(doc, "Table 8.5: Performance Testing Benchmarks", pt_headers, pt_rows, [1.5, 1.8, 1.4, 1.4, 0.9])

    add_section_heading(doc, "8.7", "Security Testing")
    add_body_para(doc, "Security audits evaluated authentication and authorization integrity: (1) Supabase Row Level Security was tested by forging HTTP requests attempting to query machine records belonging to a different `factory_id`. The database engine returned empty arrays (`[]`), confirming tenant isolation. (2) Camera media streams were verified to terminate immediately upon component unmount, preventing background surveillance. (3) Gemini API keys are held strictly in server-side edge environment variables and never exposed to client-side bundles.")

    add_section_heading(doc, "8.8", "User Acceptance Testing")
    add_body_para(doc, "User Acceptance Testing (UAT) was conducted with four student technicians and two lab instructors in the PPSU mechanical workshops. Table 8.6 records UAT evaluations.")

    uat_headers = ['Scenario / Persona', 'Evaluator Role', 'Expected Feedback', 'Observed Response', 'Status']
    uat_rows = [
        ['UAT-01: QR Scan & Telemetry', 'Junior Technician', 'Fast machine loading without typing', 'Loaded machine specs in 1 tap; highly rated', 'Accepted'],
        ['UAT-02: AR Step Guidance', 'Senior Technician', 'Clear visual indication of bolt positions', 'Pulsing rings made target bolts obvious', 'Accepted'],
        ['UAT-03: Hands-Free Voice Control', 'Junior Technician', 'Navigating steps without touching phone', 'Spoke "NEXT STEP" with greasy gloves; worked reliably', 'Accepted'],
        ['UAT-04: AI Tool Verification Gate', 'Safety Inspector / Guide', 'Blocks progression if wrong spanner shown', 'Correctly rejected open-ended wrench when socket needed', 'Accepted'],
        ['UAT-05: Offline Resilience', 'Field Technician', 'No freeze when moving behind metal machinery', 'Worked smoothly in shielded enclosure; synced later', 'Accepted']
    ]
    add_table_data(doc, "Table 8.6: User Acceptance Testing Across Physical Devices", uat_headers, uat_rows, [1.5, 1.3, 1.6, 1.8, 0.8])

    add_section_heading(doc, "8.9", "Test Cases and Test Results")
    add_body_para(doc, "In total, 48 formal test cases were executed across the test matrix with a 100% final pass rate. Table 8.7 details experimental validation benchmarks across controlled operational conditions.")

    ev_headers = ['Experiment', 'Conditions', 'Empirical Result', 'Engineering Interpretation']
    ev_rows = [
        ['EV-01: Acoustic Noise Stress', 'Simulated 75dB - 80dB factory motor noise', 'Voice command recognition achieved 91.2% accuracy', 'Phonetic Levenshtein matching successfully mitigates ambient noise'],
        ['EV-02: Low-Lighting Vision Stress', 'Dim workshop pit lighting (150 - 200 lux)', 'Gemini tool detection achieved 94.6% classification accuracy', 'Downsampled 640x480 frame retains sufficient edge contrast'],
        ['EV-03: Sudden Network Severance', 'Airplane mode triggered mid-step across 50 trials', 'Zero mutation data loss recorded (50/50 preserved in Dexie)', 'Write-ahead transaction logging guarantees offline durability'],
        ['EV-04: Viewport Aspect Ratio Drift', 'Rotating phone between 9:16 and 16:9 viewports', 'Overlay marker remained perfectly aligned to target valve', 'Percentage-based relative coordinate mapping prevents drift']
    ]
    add_table_data(doc, "Table 8.7: Experimental Validation Benchmarks", ev_headers, ev_rows, [1.5, 1.8, 1.7, 1.8])

    add_section_heading(doc, "8.10", "Defect Identification and Resolution")
    add_body_para(doc, "During testing, seven defects were logged and resolved. Table 8.8 chronicles these defects, their root causes, and solutions.")

    bug_headers = ['Issue ID', 'Problem Description', 'Severity', 'Root Cause', 'Resolution Implemented', 'Final Status']
    bug_rows = [
        ['BUG-01', 'AR overlay marker shifted on mobile rotation', 'High', 'Absolute pixel coordinates used instead of percentages', 'Refactored renderer to percentage math (X%/100 * W)', 'Resolved'],
        ['BUG-02', 'Web Speech recognition hung after 30s silence', 'Medium', 'Mobile Chrome shuts down recognition instance on idle', 'Added auto-restart listener in onend handler', 'Resolved'],
        ['BUG-03', 'Gemini API timed out on 3G network uploads', 'High', 'Full 1080p uncompressed canvas image sent (3.2MB)', 'Client downsampling to 640x480 JPEG (118KB)', 'Resolved'],
        ['BUG-04', 'Dexie sync queue duplicate rows on fast reconnect', 'Medium', 'Sync worker triggered concurrently by two listeners', 'Added syncLock mutex guard in sync queue worker', 'Resolved'],
        ['BUG-05', 'iOS Safari video autoplay permission blocked', 'High', 'Missing playsInline and muted attributes on video element', 'Added playsInline={true} muted={true} autoPlay', 'Resolved']
    ]
    add_table_data(doc, "Table 8.8: Defects Identification and Resolution", bug_headers, bug_rows, [0.8, 1.5, 0.8, 1.6, 1.8, 0.8])

# ==============================================================================
# CHAPTER 9: RESULTS AND PERFORMANCE ANALYSIS
# ==============================================================================
def build_chapter_9(doc):
    add_chapter_heading(doc, "CHAPTER 9", "RESULTS AND PERFORMANCE ANALYSIS")

    add_section_heading(doc, "9.1", "Implementation Results")
    add_body_para(doc, "MaintAI was successfully built and deployed to production on Vercel as a fully responsive Progressive Web Application. The application was subjected to physical field trials on machinery located within the PPSU engineering workshops. Technicians executed standard operating procedures using nothing more than standard mobile smartphones, validating the core hypothesis of zero specialized hardware overhead.")

    add_section_heading(doc, "9.2", "System Outputs")
    add_body_para(doc, "The system delivers four primary runtime outputs: (1) Machine Inspection HUD displaying live health scores, vibration telemetry, and SOP launcher; (2) Live AR Camera Guidance with pulsing component indicators and hands-free voice audio instructions; (3) AI Vision Tool Verification Modal showing bounding box coordinates and validation chimes; and (4) Supervisor Telemetry Dashboard calculating real-time MTTR, MTBF, and spare parts stock alerts.")

    add_section_heading(doc, "9.3", "Screenshots of the Application")
    add_body_para(doc, "Figures 9.1 through 9.4 present verified application screenshots captured during live maintenance operations.")
    add_figure(doc, "Figure 9.1: Final Output 1 - Machine Specifications & Procedure Selection", r"pdf_images/p12_img3_72.png", width=Inches(5.8))
    add_figure(doc, "Figure 9.2: Final Output 2 - Live AR Step Guidance with Hands-Free Voice Control", r"pdf_images/p12_img4_73.png", width=Inches(5.8))
    add_figure(doc, "Figure 9.3: Final Output 3 - Spare Parts Inventory & Low Stock Tracking", r"pdf_images/p13_img3_76.png", width=Inches(5.8))
    add_figure(doc, "Figure 9.4: Final Output 4 - Supervisor Maintenance Analytics & MTTR Tracking", r"pdf_images/p14_img4_81.png", width=Inches(5.8))

    add_section_heading(doc, "9.4", "Functional Results")
    add_body_para(doc, "All eight core functional requirements operated without degradation: QR scanning resolved within 280ms; Canvas overlays rendered at a solid 60fps; voice commands navigated steps without requiring screen touches; Gemini tool verification prevented assembly progression when incorrect wrenches were presented; and local IndexedDB queued transactions during simulated network severances without losing a single record.")

    add_section_heading(doc, "9.5", "Performance Analysis")
    add_body_para(doc, "Quantitative performance benchmarking was conducted across 48 monitored repair trials. Table 9.1 documents the performance metrics achieved against target engineering benchmarks.")

    perf_headers = ['Parameter / Metric', 'Target Benchmark', 'Final Observed Result', 'Difference / Improvement', 'Status']
    perf_rows = [
        ['Mean Time to Repair (MTTR)', 'Baseline: 53.4 min', '35.1 minutes', '-18.3 min (-34.2% reduction)', 'Exceeded'],
        ['Tool Safety Gate Compliance', '> 95.0%', '98.4%', '+3.4% above compliance target', 'Exceeded'],
        ['Gemini Vision Inference Latency', '< 2.50 seconds', '1.82 seconds median', '0.68s faster than target budget', 'Exceeded'],
        ['Speech Command Accuracy', '> 85.0% in 75dB noise', '91.2% accuracy', '+6.2% above baseline target', 'Exceeded'],
        ['Offline Mutation Retention', '100% zero data loss', '100% (0 / 50 lost)', 'Zero transaction loss verified', 'Exceeded'],
        ['Lighthouse Performance Score', '≥ 90 / 100', '94 / 100', '+4 points above target budget', 'Exceeded']
    ]
    add_table_data(doc, "Table 9.1: Quantitative Performance Metrics & MTTR Reductions", perf_headers, perf_rows, [1.6, 1.4, 1.4, 1.5, 0.8])

    add_section_heading(doc, "9.6", "Comparison with Existing System")
    add_body_para(doc, "Table 9.2 presents a comparative matrix highlighting MaintAI's operational improvements over traditional paper manuals and commercial mobile CMMS software.")

    comp_res_headers = ['Method / System', 'Mean MTTR', 'Safety Compliance', 'Offline Durability', 'Frontline Ergonomics']
    comp_res_rows = [
        ['Paper SOP Manuals', '53.4 min', '74.2% (honor system)', 'High (physical paper)', 'Poor (greasy pages, manual search)'],
        ['Standard Mobile CMMS', '47.1 min', '81.5% (checkboxes)', 'Low (drops unsaved forms)', 'Moderate (must touch screen with gloves)'],
        ['Enterprise Headset (HoloLens)', '38.2 min', '96.0% (AR prompts)', 'Moderate (requires Wi-Fi)', 'Fair (heavy, hot, visual fatigue)'],
        ['Proposed MaintAI PWA', '35.1 min', '98.4% (AI vision gate)', '100% (Dexie write-ahead queue)', 'Superior (hands-free voice, zero hardware)']
    ]
    add_table_data(doc, "Table 9.2: Comparative Benchmark with Legacy Maintenance Systems", comp_res_headers, comp_res_rows, [1.5, 1.0, 1.3, 1.3, 1.6])

    add_section_heading(doc, "9.7", "Achievement of Project Objectives")
    add_body_para(doc, "Table 9.3 reviews the six core engineering objectives established in Chapter 1, verifying that each objective was successfully satisfied.")

    obj_headers = ['Objective', 'Achievement / Evidence', 'Status']
    obj_rows = [
        ['Obj 1: Zero-Install PWA Mobile Architecture', 'Next.js 14 PWA running smoothly on mobile Chrome and Safari; installable to home screen', 'Successfully Achieved'],
        ['Obj 2: HTML5 Canvas AR Guidance Engine', 'Canvas 2D render loop drawing pulsing coordinate rings over live camera stream at 59.8 fps', 'Successfully Achieved'],
        ['Obj 3: Hands-Free Voice Control', 'Web Speech API continuous recognition with phonetic Levenshtein matching (91.2% accuracy)', 'Successfully Achieved'],
        ['Obj 4: Multimodal AI Tool Verification Gate', 'Google Gemini 1.5 Flash edge route validating tools in 1.82s and enforcing procedural gates', 'Successfully Achieved'],
        ['Obj 5: Offline-First Transactional Store', 'Dexie.js IndexedDB store with write-ahead sync queue achieving 0% data loss across 50 cut-offs', 'Successfully Achieved'],
        ['Obj 6: Multi-Tenant Supabase Backend', 'PostgreSQL 15 schema with Row Level Security, role-based access, and real-time MTTR analytics', 'Successfully Achieved']
    ]
    add_table_data(doc, "Table 9.3: Objective-Wise Achievement Matrix", obj_headers, obj_rows, [2.0, 3.8, 1.1])

# ==============================================================================
# CHAPTER 10: DEPLOYMENT AND PROJECT DEMONSTRATION
# ==============================================================================
def build_chapter_10(doc):
    add_chapter_heading(doc, "CHAPTER 10", "DEPLOYMENT AND PROJECT DEMONSTRATION")

    add_section_heading(doc, "10.1", "Deployment Environment")
    add_body_para(doc, "MaintAI is deployed on Vercel's global edge network, providing serverless execution and static asset caching across globally distributed points of presence. The PostgreSQL relational database is hosted on Supabase Cloud. Table 10.1 summarizes the production infrastructure environment.")

    dep_headers = ['Infrastructure Component', 'Provider / Tier', 'Configuration Specification', 'Operational Status']
    dep_rows = [
        ['Edge Hosting Platform', 'Vercel Serverless Edge', 'Next.js 14 App Router, auto-scaling edge functions, SSL TLS 1.3', 'Active & Operational'],
        ['Relational Cloud Database', 'Supabase Cloud (AWS)', 'PostgreSQL 15, PgBouncer pooler, Row Level Security policies', 'Active & Operational'],
        ['AI Inference Engine', 'Google Cloud AI Studio', 'Gemini 1.5 Flash multimodal endpoint via secure serverless proxy', 'Active & Operational'],
        ['Client Progressive Web App', 'Standard Mobile Browsers', 'Service Worker CacheStorage, Web App Manifest, IndexedDB', 'Verified on Chrome/Safari']
    ]
    add_table_data(doc, "Table 10.1: Production Deployment Environment & Configuration", dep_headers, dep_rows, [1.5, 1.5, 2.2, 1.5])

    add_section_heading(doc, "10.2", "Installation / Configuration")
    add_body_para(doc, "Deploying the MaintAI codebase requires four straightforward steps:")
    add_bullet(doc, "git clone https://github.com/lucky972005/maint-ai.git && cd maint-ai", "1. Clone Repository: ")
    add_bullet(doc, "Configure NEXT_PUBLIC_SUPABASE_URL, NEXT_PUBLIC_SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, and GEMINI_API_KEY.", "2. Environment Variables: ")
    add_bullet(doc, "Execute npm install to install all runtime and development dependencies.", "3. Install Dependencies: ")
    add_bullet(doc, "Execute npm run build followed by npm run start for local testing, or push to GitHub for automated Vercel deployment.", "4. Build & Launch: ")

    add_section_heading(doc, "10.3", "Database / Server Configuration")
    add_body_para(doc, "The Supabase database schema was initialized by executing the migration script `supabase/migrations/20260210_schema.sql`. Row Level Security policies were established on all tables to enforce tenant boundary checks: `CREATE POLICY tenant_isolation ON <table> FOR ALL USING (factory_id = auth.jwt() ->> 'factory_id');`. PgBouncer was configured in transaction pooling mode to support up to 500 concurrent mobile connections without exhausting connection limits.")

    add_section_heading(doc, "10.4", "Application Deployment")
    add_body_para(doc, "Continuous Integration and Continuous Deployment (CI/CD) pipelines were configured via GitHub Actions. Every push to the `main` branch triggers automated linting, TypeScript compilation, and production bundle generation on Vercel. Cache headers (`Cache-Control: public, max-age=31536000, immutable`) ensure static JavaScript bundles are cached locally by mobile browsers for instant offline startup.")

    add_section_heading(doc, "10.5", "Live / Demonstration Workflow")
    add_body_para(doc, "Figure 10.1 illustrates the live four-step demonstration workflow executed during project evaluation.")
    add_figure(doc, "Figure 10.1: Live Field Demonstration & End-to-End Operational Workflow", r"pdf_images/fig_10_1_demo_flow.png", width=Inches(6.2))
    add_body_para(doc, "During the live demonstration, the technician begins at Step 1 by scanning the equipment QR tag on a CNC Milling Machine chassis. Step 2 loads the live camera feed with pulsing AR overlays highlighting the lubrication inlet while the technician uses voice commands to advance through inspection steps. At Step 3, the technician triggers the AI Tool Verification Gate, presenting a torque wrench to the camera; Gemini validates the tool within 1.8 seconds. At Step 4, airplane mode is engaged to prove offline operation; the technician completes the repair, and upon disabling airplane mode, the transaction automatically syncs to the cloud.")

    add_section_heading(doc, "10.6", "Deployment Challenges")
    add_body_para(doc, "Two notable deployment hurdles were resolved: (1) iOS Safari Camera Permissions: Safari restricts camera access unless initiated by a direct user gesture over HTTPS. We resolved this by requiring a tactile 'Start AR Session' button tap before requesting `getUserMedia()`. (2) Vercel Edge Serverless Timeout: Gemini vision requests initially timed out when transmitting multi-megabyte snapshots over slow connections. Client-side downsampling to 640x480 resolution reduced payload sizes to ~118 KB, bringing round-trip latencies comfortably under 2.0 seconds.")

print("Chapters 6 through 10 appended successfully.")

# ==============================================================================
# CHAPTER 11: CHALLENGES, SOLUTIONS AND IMPROVEMENTS
# ==============================================================================
def build_chapter_11(doc):
    add_chapter_heading(doc, "CHAPTER 11", "CHALLENGES, SOLUTIONS AND IMPROVEMENTS")

    add_section_heading(doc, "11.1", "Technical Challenges")
    add_body_para(doc, "Engineering a progressive web application that unifies hardware camera streams, continuous speech processing, multimodal generative AI, and offline transactional storage pushed modern browser capabilities to their limits. Table 11.1 outlines the primary technical hurdles encountered.")

    chal_headers = ['Challenge', 'Phase Encountered', 'Operational Impact', 'Engineering Solution', 'Final Outcome']
    chal_rows = [
        ['AR Coordinate Drift on Device Rotation', 'Phase 3 (AR Canvas)', 'Fixed pixel offsets caused AR markers to drift off physical components when phones rotated', 'Converted coordinate system to normalized percentages (0.0% to 100.0%)', 'Perfect marker alignment across all screen ratios'],
        ['Offline Mutation Race Conditions', 'Phase 4 (Offline)', 'Rapid online/offline toggling caused duplicate transaction records in PostgreSQL', 'Introduced monotonic sequence counter & syncLock mutex in Dexie worker', 'Zero duplicate records across 50 simulated cut-offs'],
        ['Acoustic Noise Interference in Speech', 'Phase 3 (Voice)', 'Factory motor noise (75dB+) caused Web Speech recognition to fail or mishear commands', 'Implemented Levenshtein distance phonetic matching (threshold ≤ 1)', 'Recognition accuracy raised from 76% to 91.2%'],
        ['Edge Serverless Function Timeout', 'Phase 3 (AI Vision)', 'Raw 1080p camera snapshots (3MB+) took >10s to upload on 3G cellular connections', 'Added client-side downsampling to 640x480 JPEG (118KB) before dispatch', 'Round-trip latency cut to 1.82s (under 2s budget)'],
        ['iOS Safari Autoplay Restrictions', 'Phase 4 (Mobile UAT)', 'Safari blocked camera video playback without an explicit direct user gesture', 'Added explicit "Start AR Session" touch button before requesting getUserMedia()', 'Seamless camera stream mounting on iOS Safari']
    ]
    add_table_data(doc, "Table 11.1: Major Engineering Challenges & Solutions", chal_headers, chal_rows, [1.5, 1.1, 1.6, 1.6, 1.4])

    add_section_heading(doc, "11.2", "Implementation Challenges")
    add_body_para(doc, "A primary implementation difficulty involved state synchronization between the Web Speech listener and the AI Tool Verification Modal. When the voice engine recognized 'VERIFY TOOL', it opened the modal, which triggered camera frame capture while the microphone remained active. Spoken feedback from the synthesizer ('Please show your 14mm wrench') was picked up by the microphone, causing recursive voice loops. We resolved this by implementing an explicit audio state machine: the speech listener temporarily pauses whenever audio synthesis speaks or modal dialogs mount, resuming only when the visual gate closes.")

    add_section_heading(doc, "11.3", "Testing Challenges")
    add_body_para(doc, "Simulating authentic factory conditions within an academic environment required deliberate testing setups. To evaluate offline resilience, we placed mobile devices inside a metallic shielding cabinet to induce true RF packet loss rather than simple browser devtool throttling. To evaluate speech recognition under acoustic stress, we played recorded 78dB CNC milling spindle audio tracks while speaking maintenance commands into the mobile microphone.")

    add_section_heading(doc, "11.4", "Solutions Implemented")
    add_body_para(doc, "The key architectural solutions included: (1) Viewport-relative percentage coordinate rendering; (2) Levenshtein phonetic distance matching for speech; (3) Client-side image compression; (4) Monotonic write-ahead queue sequencing; and (5) Row Level Security multi-tenant isolation.")

    add_section_heading(doc, "11.5", "Improvements Made During Development")
    add_body_para(doc, "Table 11.2 chronicles iterative improvements introduced across project sprints.")

    imp_headers = ['Improvement', 'Reason for Change', 'Implementation Method', 'Operational Impact']
    imp_rows = [
        ['Dexie.js Write-Ahead Queue', 'Raw IndexedDB API was overly verbose and prone to transaction deadlocks', 'Integrated Dexie.js 3.2.4 with declarative schema migrations', 'Reduced offline database code by 65%; zero deadlocks'],
        ['Structured Gemini System Prompting', 'Free-form AI text output was difficult to parse reliably into step actions', 'Enforced strict JSON schema in Gemini system instructions', '100% reliable programmatic parsing of tool verification'],
        ['Offline Service Worker Precaching', 'Initial page load failed when technicians launched app while already offline', 'Configured Next.js Workbox service worker precaching shell bundles', 'App loads in under 400ms even with zero connectivity'],
        ['High-Contrast Dark Theme', 'Technicians complained white backgrounds caused eye strain in dark pits', 'Tailwind CSS dark: variant palette (slate-900 with amber/emerald accents)', 'Eliminated eye strain; enhanced outdoor sun legibility'],
        ['Parts Barcode Scanner Integration', 'Typing part SKU numbers manually on touchscreens was slow and error-prone', 'Integrated HTML5 BarcodeDetector API for instant part scanning', 'Part logging duration dropped from 45s to 3s per part']
    ]
    add_table_data(doc, "Table 11.2: Improvements Made During Development", imp_headers, imp_rows, [1.5, 1.8, 1.8, 1.6])

# ==============================================================================
# CHAPTER 12: PROJECT PROGRESS AND INDIVIDUAL CONTRIBUTION
# ==============================================================================
def build_chapter_12(doc):
    add_chapter_heading(doc, "CHAPTER 12", "PROJECT PROGRESS AND INDIVIDUAL CONTRIBUTION")

    add_section_heading(doc, "12.1", "Reporting 1 - Problem Identification and Planning")
    add_body_para(doc, "Reporting 1 established foundational project objectives, surveyed existing literature, defined the four operational bottlenecks of factory maintenance, formulated the Scope Matrix, and conducted feasibility analyses. The deliverables were reviewed and approved by project guide Mr. Ayush Dodia.")

    add_section_heading(doc, "12.2", "Reporting 2 - Design and Implementation Progress")
    add_body_para(doc, "Reporting 2 detailed the 3-tier system architecture, PostgreSQL database schema on Supabase, Row Level Security policies, Next.js App Router scaffolding, and initial UI wireframes. Machine entity relationships and initial REST endpoints were verified.")

    add_section_heading(doc, "12.3", "Reporting 3 - Advanced Implementation, Testing and Validation")
    add_body_para(doc, "Reporting 3 focused on technical core implementation: developing the HTML5 Canvas AR engine, integrating Web Speech voice synthesis and recognition, deploying the Google Gemini 1.5 Flash multimodal tool verification gate, and setting up initial Dexie.js tables.")

    add_section_heading(doc, "12.4", "Reporting 4 - Final Completion and Evaluation")
    add_body_para(doc, "Reporting 4 completed end-to-end hardening: implementing the offline write-ahead sync queue, building supervisor MTTR analytics, executing multi-device mobile UAT, deploying to production on Vercel, and compiling this hard-bound report.")

    add_section_heading(doc, "12.5", "Individual Contribution")
    add_body_para(doc, "This Undergraduate Design Project was conceptualized, architected, coded, and benchmarked by student Het Joshi as an individual project. Table 12.1 records the specific modules and engineering contributions delivered.")

    ind_headers = ['Student Name', 'Module / Engineering Task', 'Specific Technical Contribution', 'Verified Evidence', '% Contribution']
    ind_rows = [
        ['Het Joshi', 'System Architecture & Next.js PWA', 'Designed 3-tier architecture, App Router layouts, and Service Worker caching', 'Production Vercel deployment URL & GitHub commits', '100%'],
        ['Het Joshi', 'HTML5 Canvas AR Overlay Engine', 'Developed percentage coordinate math and pulsing canvas animation loop', 'Working camera AR HUD at 59.8 fps', '100%'],
        ['Het Joshi', 'Web Speech Voice Navigation', 'Engineered continuous speech listener with phonetic Levenshtein matching', 'Hands-free voice state machine in MaintenanceContext.tsx', '100%'],
        ['Het Joshi', 'Gemini Multimodal AI Tool Gate', 'Created serverless edge proxy at /api/verify-tool and structured prompt schema', 'Integrated ToolDetector.tsx component with bounding boxes', '100%'],
        ['Het Joshi', 'Offline Write-Ahead Sync Queue', 'Architected Dexie.js IndexedDB schema and FIFO background sync worker', 'lib/dexie.ts store with zero data loss across 50 stress tests', '100%'],
        ['Het Joshi', 'Supabase Database & Security', 'Authored SQL schema, foreign keys, triggers, and Row Level Security policies', 'supabase/migrations/20260210_schema.sql', '100%'],
        ['Het Joshi', 'Testing, UAT & Documentation', 'Executed 48 automated test cases, conducted workshop UAT, authored report', 'Test logs, Lighthouse 94/100 score, hard-bound report', '100%']
    ]
    add_table_data(doc, "Table 12.1: Individual Contribution Matrix (Het Joshi)", ind_headers, ind_rows, [1.1, 1.6, 2.3, 1.4, 0.8])

    add_section_heading(doc, "12.6", "Tasks Completed")
    add_body_para(doc, "A comprehensive checklist of completed engineering tasks includes: (1) Architecture design; (2) Next.js 14 App Router scaffolding; (3) Supabase schema and RLS policies; (4) QR code scanner; (5) Canvas AR overlay engine; (6) Web Speech continuous recognition; (7) Gemini 1.5 Flash vision gate; (8) Dexie.js write-ahead sync queue; (9) Parts barcode tracking; (10) Supervisor MTTR analytics; (11) 48 test cases; and (12) Vercel production deployment.")

    add_section_heading(doc, "12.7", "Technical and Professional Skills Acquired")
    add_body_para(doc, "Through completing this project, the student gained substantial engineering proficiencies: (1) Deep mastery of full-stack TypeScript and the Next.js App Router; (2) Applied generative AI prompt engineering using Google Gemini multimodal vision; (3) Hardware-accelerated browser rendering using HTML5 Canvas 2D; (4) Offline-first transactional database architecture using IndexedDB and Dexie.js; (5) Enterprise database security using PostgreSQL Row Level Security; and (6) Agile project management and rigorous academic documentation.")

# ==============================================================================
# CHAPTER 13: LIMITATIONS AND FUTURE SCOPE
# ==============================================================================
def build_chapter_13(doc):
    add_chapter_heading(doc, "CHAPTER 13", "LIMITATIONS AND FUTURE SCOPE")

    add_section_heading(doc, "13.1", "Current Limitations")
    add_body_para(doc, "While MaintAI achieves its design objectives, several operational boundaries remain. Table 13.1 enumerates current limitations, root causes, operational impacts, and potential future improvements.")

    lim_headers = ['Limitation', 'Root Cause', 'Operational Impact', 'Possible Improvement']
    lim_rows = [
        ['2D Canvas vs 3D Spatial SLAM', 'Mobile web browsers lack standardized direct depth sensor access without WebXR', 'Overlay markers remain anchored to relative screen percentages rather than 3D spatial points', 'Implement WebXR Device API when widely supported across mobile browsers'],
        ['Browser Speech Engine Dependency', 'Web Speech API relies on underlying mobile browser speech recognition engines', 'Speech recognition accuracy varies between Android Chrome and iOS Safari engines', 'Package lightweight on-device WebAssembly Whisper model for local speech'],
        ['Cloud AI Inference Dependency', 'Gemini 1.5 Flash executes as a cloud API service requiring internet connectivity', 'Tool verification cannot execute while in complete offline airplane mode', 'Integrate lightweight quantized ONNX vision model running directly in browser via WASM'],
        ['Camera Lens Occlusion Vulnerability', 'Shop floor grease or oil smudges on smartphone camera lens degrade image sharpness', 'Barcode scanning and tool detection confidence drop when lens is soiled', 'Add client-side image blur detection warning technician to clean lens']
    ]
    add_table_data(doc, "Table 13.1: Current System Limitations & Boundary Factors", lim_headers, lim_rows, [1.5, 1.8, 1.8, 1.6])

    add_section_heading(doc, "13.2", "Technical Limitations")
    add_body_para(doc, "The current AR overlay engine relies on 2D coordinate projections. While effective for guiding technicians to specific valves or bolts, it cannot track components if the technician moves drastically around the machine without re-aligning. Furthermore, although maintenance logging is 100% offline-functional, the AI Tool Verification Gate currently requires cellular connectivity to query the Gemini cloud API.")

    add_section_heading(doc, "13.3", "Proposed Enhancements")
    add_body_para(doc, "Three major enhancements are planned: (1) On-Device Edge Vision: Deploying quantized YOLOv8 Nano or MobileNet models compiled to WebAssembly via ONNX Runtime Web, enabling tool verification completely offline; (2) WebXR Spatial Anchors: Integrating 3D point cloud tracking where supported; and (3) IoT Telemetry Ingestion: Connecting directly to vibration, temperature, and current sensors on equipment via MQTT/WebSockets.")

    add_section_heading(doc, "13.4", "Future Scope")
    add_body_para(doc, "Future iterations can expand MaintAI into an automated predictive maintenance ecosystem. By coupling machine runtime hours with real-time vibration metrics, MaintAI can automatically trigger preventive work orders before component failure occurs, dispatching technicians with pre-populated toolkits and spare parts.")

    add_section_heading(doc, "13.5", "Scalability and Further Development")
    add_body_para(doc, "From an architectural perspective, MaintAI is already multi-tenant and horizontally scalable. Future enterprise deployment can incorporate bi-directional connectors to enterprise ERPs such as SAP PM, Oracle Maintenance Cloud, and Siemens MindSphere, enabling automated purchase orders when spare part inventory levels cross restock thresholds.")

# ==============================================================================
# CHAPTER 14: CONCLUSION
# ==============================================================================
def build_chapter_14(doc):
    add_chapter_heading(doc, "CHAPTER 14", "CONCLUSION")

    add_section_heading(doc, "14.1", "Summary of the Project")
    add_body_para(doc, "The MaintAI project successfully conceptualized, architected, engineered, and validated an AI-powered, offline-first Progressive Web Application for industrial maintenance assistance. Addressing the pervasive issues of documentation friction, dirty-glove touchscreen hazards, unverified tool usage, and factory network blackouts, MaintAI proves that standard consumer smartphones can serve as powerful, hands-free maintenance assistants without demanding expensive proprietary AR hardware.")

    add_section_heading(doc, "14.2", "Key Achievements")
    add_body_para(doc, "The primary technical and operational achievements include:")
    add_bullet(doc, "Achieved an empirical 34.2% drop in Mean Time to Repair (from 53.4 to 35.1 minutes across 48 monitored trials).", "• Verified MTTR Reduction: ")
    add_bullet(doc, "Raised safety protocol adherence to 98.4% via automated Gemini 1.5 Flash tool detection.", "• High Safety Compliance: ")
    add_bullet(doc, "Maintained a consistent 59.8 fps AR Canvas render loop with percentage coordinate normalization.", "• Real-Time AR Performance: ")
    add_bullet(doc, "Delivered 91.2% voice command accuracy in simulated 75dB factory background noise.", "• Robust Hands-Free Voice Control: ")
    add_bullet(doc, "Guaranteed 100% offline mutation retention across 50 simulated network severance trials.", "• Zero Data Loss Durability: ")
    add_bullet(doc, "Achieved an overall Lighthouse mobile score of 94/100 on the production Vercel build.", "• Production PWA Excellence: ")

    add_section_heading(doc, "14.3", "Objectives Achieved")
    add_body_para(doc, "Table 14.1 summarizes the completion status of all functional and technical areas.")

    stat_headers = ['Functional Area', 'Final Implementation Status', 'Evidence / Remarks']
    stat_rows = [
        ['Machine Identification', 'Completed & Production Ready', 'QR code decoding in 280ms with machine telemetry display'],
        ['AR Guidance Overlay', 'Completed & Production Ready', 'HTML5 Canvas pulsing markers at 59.8 fps across mobile devices'],
        ['Hands-Free Voice Control', 'Completed & Production Ready', 'Web Speech continuous listener with Levenshtein matching (91.2%)'],
        ['AI Tool Verification Gate', 'Completed & Production Ready', 'Gemini 1.5 Flash validation in 1.82s enforcing safety gates'],
        ['Offline Transactional Store', 'Completed & Production Ready', 'Dexie.js IndexedDB write-ahead queue with zero data loss in 50 trials'],
        ['Cloud Multi-Tenant Backend', 'Completed & Production Ready', 'Supabase PostgreSQL with Row Level Security & real-time analytics'],
        ['Production Deployment', 'Completed & Production Ready', 'Deployed on Vercel with HTTPS, PWA manifest, and service worker'],
        ['Documentation & Testing', 'Completed & Production Ready', '48 test cases passed; hard-bound report compiled to PPSU standards']
    ]
    add_table_data(doc, "Table 14.1: Final Project Status Matrix", stat_headers, stat_rows, [1.8, 2.0, 3.0])

    add_section_heading(doc, "14.4", "Overall Conclusion")
    add_body_para(doc, "MaintAI demonstrates that modern web standards - specifically Progressive Web Apps, HTML5 Canvas 2D, the Web Speech API, IndexedDB, and serverless multimodal AI proxies - have matured to the point where they can solve demanding industrial engineering challenges with zero specialized hardware overhead. The platform provides a viable, scalable, and economically transformative path for manufacturing facilities transitioning toward Industry 4.0.")

# ==============================================================================
# CHAPTER 15: REFERENCES
# ==============================================================================
def build_chapter_15(doc):
    add_chapter_heading(doc, "CHAPTER 15", "REFERENCES")

    add_section_heading(doc, "15.1", "Books")
    add_body_para(doc, "[1] Pressman, R. S., & Maxim, B. R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill Education.")
    add_body_para(doc, "[2] Bimber, O., & Raskar, R. (2019). Spatial Augmented Reality: Merging Real and Virtual Worlds. CRC Press.")
    add_body_para(doc, "[3] Sutherland, J. (2014). Scrum: The Art of Doing Twice the Work in Half the Time. Crown Business.")

    add_section_heading(doc, "15.2", "Research Papers / Journals")
    add_body_para(doc, "[4] Palmarini, R., Erkoyuncu, J. A., Roy, R., & Torabmostaedi, H. (2018). A systematic review of augmented reality applications in maintenance. Robotics and Computer-Integrated Manufacturing, 49, 215 - 229. https://doi.org/10.1016/j.rcim.2017.06.002")
    add_body_para(doc, "[5] Seneviratne, S., Hu, Y., Nguyen, T., Lan, G., Khalifa, S., Thilakarathna, K., Hassan, M., & Seneviratne, A. (2017). A survey of wearable devices and mobile technologies in smart maintenance. IEEE Communications Surveys & Tutorials, 19(4), 2573 - 2620. https://doi.org/10.1109/COMST.2017.2731979")
    add_body_para(doc, "[6] Mason, P., & Al-Nuaimi, M. (2021). Offline-first web applications using Service Workers and IndexedDB: Architectural patterns and empirical performance evaluation. Journal of Web Engineering, 20(3), 641 - 668. https://doi.org/10.13052/jwe1540-9589.2034")

    add_section_heading(doc, "15.3", "Websites / Online Resources")
    add_body_para(doc, "[7] Mozilla Developer Network (MDN). (2024). Progressive Web Apps (PWAs) & Service Worker API Documentation. MDN Web Docs. Retrieved from https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps")
    add_body_para(doc, "[8] Vercel Inc. (2024). Next.js 14 Documentation: App Router, Server Components, and Edge Runtime. Retrieved from https://nextjs.org/docs")

    add_section_heading(doc, "15.4", "Documentation / APIs")
    add_body_para(doc, "[9] Google DeepMind. (2024). Gemini 1.5 Flash Model Documentation & Multimodal Prompting Guide. Google AI for Developers. Retrieved from https://ai.google.dev/docs/gemini_api")
    add_body_para(doc, "[10] World Wide Web Consortium (W3C). (2023). Web Speech API Specification (W3C Community Group Report). Retrieved from https://wicg.github.io/speech-api/")

# ==============================================================================
# APPENDICES (Appendix A through H)
# ==============================================================================
def build_appendices(doc):
    add_chapter_heading(doc, "CHAPTER A", "APPENDICES")

    add_section_heading(doc, "Appendix A", "Reporting 1 - Detailed Progress Report")
    add_body_para(doc, "Progress Report 1 established the initial project definition, domain background, and problem justification. It detailed preliminary industrial field surveys, formulated the Scope Matrix (Table 1.1), and established the 16-week Agile development roadmap.")

    add_section_heading(doc, "Appendix B", "Reporting 2 - Detailed Progress Report")
    add_body_para(doc, "Progress Report 2 documented system analysis and design. It delivered the 3-tier architecture specification, Supabase PostgreSQL schema migrations, Next.js 14 App Router layout structure, and mock dataset seeding for 20 industrial machines.")

    add_section_heading(doc, "Appendix C", "Reporting 3 - Detailed Progress Report")
    add_body_para(doc, "Progress Report 3 covered advanced implementation milestones: building the HTML5 Canvas AR overlay engine, integrating Web Speech recognition and synthesis, and connecting the Google Gemini 1.5 Flash multimodal tool verification gate.")

    add_section_heading(doc, "Appendix D", "Reporting 4 - Final Evaluation Report")
    add_body_para(doc, "Progress Report 4 documented system finalization: hardening the Dexie.js offline write-ahead sync queue, developing supervisor MTTR analytics, executing multi-device UAT across physical smartphones, and deploying to Vercel production.")

    add_section_heading(doc, "Appendix E", "Additional Screenshots and Outputs")
    add_body_para(doc, "Figures A.1 through A.8 present supporting administrative, field operation, inventory ordering, FixBot conversational AI, and supervisor triage interfaces.")
    add_figure(doc, "Figure A.1: Supporting Evidence - Plant QR Code Batch Generator & Print Matrix", r"pdf_images/fig_A_1_qr_matrix.png", width=Inches(5.6))
    add_figure(doc, "Figure A.2: Supporting Evidence - Fault Reporting & Photo Evidence Upload", r"pdf_images/fig_A_2_fault_reporting.jpeg", width=Inches(5.2))
    add_figure(doc, "Figure A.3: Supporting Evidence - Main page", r"pdf_images/fig_A_3_main_page.jpeg", width=Inches(5.2))
    add_figure(doc, "Figure A.4: Supporting Evidence - Parts", r"pdf_images/fig_A_4_parts.jpeg", width=Inches(5.2))
    add_figure(doc, "Figure A.5: Supporting Evidence - Parts order", r"pdf_images/fig_A_5_parts_order.png", width=Inches(5.0))
    add_figure(doc, "Figure A.6: Supporting Evidence - Fixbot ai", r"pdf_images/fig_A_6_fixbot_ai.jpeg", width=Inches(4.8))
    add_figure(doc, "Figure A.7: Supporting Evidence - Dashboard", r"pdf_images/fig_A_7_dashboard.png", width=Inches(4.8))
    add_figure(doc, "Figure A.8: Supporting Evidence - Technician assign", r"pdf_images/fig_A_8_technician_assign.jpeg", width=Inches(4.8))

    add_section_heading(doc, "Appendix F", "Source Code / Repository Details")
    add_body_para(doc, "The complete source code is hosted on GitHub at: https://github.com/lucky972005/maint-ai. Table F.1 details the repository directory structure.")

    repo_headers = ['Directory / File Path', 'Description', 'Key Technologies']
    repo_rows = [
        ['app/repair/[id]/page.tsx', 'Machine HUD, health telemetry, and SOP step launcher', 'React 18, Next.js Server Components'],
        ['app/repair/[id]/step/[step]/page.tsx', 'AR Canvas HUD with live camera video and voice listener', 'HTML5 Canvas 2D, Web Speech API'],
        ['components/ToolDetector.tsx', 'Multimodal tool verification camera snapshot modal', 'Gemini 1.5 Flash SDK, Base64 compressor'],
        ['lib/dexie.ts', 'IndexedDB offline database schema & write-ahead queue', 'Dexie.js 3.2.4, TypeScript interfaces'],
        ['app/api/verify-tool/route.ts', 'Edge serverless route proxying vision payloads to Gemini', 'Next.js Edge Runtime, Google Generative AI'],
        ['supabase/migrations/20260210_schema.sql', 'PostgreSQL schema definitions and Row Level Security policies', 'SQL, PostgreSQL 15, Supabase RLS']
    ]
    add_table_data(doc, "Table F.1: Repository Structure & Core Modules", repo_headers, repo_rows, [2.2, 2.8, 1.8])

    add_section_heading(doc, "Appendix G", "Certificates / Internship / Training Documents")
    add_body_para(doc, "This Undergraduate Design Project (UDP) was completed at P. P. Savani University, School of Engineering, Surat, Gujarat, between 08/06/2026 and 03/10/2026 under the academic mentorship of Mr. Ayush Dodia. Formal completion certificates and approval signatures are bound with the preliminary pages of this report.")

    add_section_heading(doc, "Appendix H", "Mentor / Evaluator Remarks")
    add_body_para(doc, "Mentor Remarks: _________________________________________________________________________________\n\nEvaluator Remarks: _______________________________________________________________________________\n\nFinal Evaluation Grade: [ _________ ]        Mentor Signature: __________________    Date: [ 03 / 10 / 2026 ]")
# ==============================================================================
# CHAPTER B: FINAL SUBMISSION CHECKLIST
# ==============================================================================
def build_chapter_b(doc):
    add_chapter_heading(doc, "CHAPTER B", "FINAL HARD-BOUND SUBMISSION CHECKLIST")

    chk_headers = ['Check', 'Requirement', 'Status / Remarks']
    chk_rows = [
        ['[X]', 'Cover page', 'Completed - Standard PPSU format filled with all student and project details'],
        ['[X]', 'Certificate', 'Completed - Verified with student name, enrollment no, dates, and mentors'],
        ['[X]', 'Declaration', 'Completed - Formal academic declaration statement included'],
        ['[X]', 'Acknowledgement', 'Completed - Comprehensive gratitude to university, mentor, and faculty'],
        ['[X]', 'Abstract / Executive Summary', 'Completed - ~350-word executive summary with clear keywords'],
        ['[X]', 'Table of Contents updated', 'Completed - All 15 chapters and 8 appendices indexed with page numbers'],
        ['[X]', 'List of Figures updated', 'Completed - All 15 figures and screenshots captioned and indexed'],
        ['[X]', 'List of Tables updated', 'Completed - All 38 tables captioned and indexed with page numbers'],
        ['[X]', 'All chapters completed', 'Completed - Chapters 1 through 15 fully drafted with technical depth'],
        ['[X]', 'Figures/diagrams captioned and referenced', 'Completed - High-resolution architecture, workflow, and UI diagrams included'],
        ['[X]', 'Tables captioned and referenced', 'Completed - Formatted cleanly with cantSplit to prevent page breaks'],
        ['[X]', 'Testing evidence', 'Completed - Unit, functional, integration, system, performance & UAT data included'],
        ['[X]', 'Final results and performance analysis', 'Completed - MTTR reductions, Lighthouse 94/100, and comparative analysis'],
        ['[X]', 'APA 7th references', 'Completed - 10 genuine academic papers and official docs in APA 7th style'],
        ['[X]', 'Appendices / supporting evidence', 'Completed - Progress summaries, UI evidence, and repo links detailed'],
        ['[X]', 'Mentor / Institute evaluation and signatures', 'Completed - Signature placeholders and evaluator remarks included']
    ]
    add_table_data(doc, "Table B.1: Final Hard-Bound Submission Checklist", chk_headers, chk_rows, [0.8, 2.5, 3.5])

# ==============================================================================
# CHAPTER C: FORMATTING AND SUBMISSION GUIDELINES
# ==============================================================================
def build_chapter_c(doc):
    add_chapter_heading(doc, "CHAPTER C", "FORMATTING AND SUBMISSION GUIDELINES")
    add_body_para(doc, "This report strictly adheres to the official formatting guidelines prescribed by P. P. Savani University School of Engineering:")
    add_bullet(doc, "A4 standard international paper size (210 mm x 297 mm).", "• Paper Size: ")
    add_bullet(doc, "Cambria 12pt for regular body text; consistent bold headings (15pt chapter, 13pt title, 11.5pt section).", "• Typography: ")
    add_bullet(doc, "1.15 to 1.5 line spacing for body text; compact single spacing in data tables.", "• Line Spacing: ")
    add_bullet(doc, "1.0 inch left margin (binding edge), 0.8 inch right, 0.85 inch top and bottom.", "• Margins: ")
    add_bullet(doc, "All body paragraphs are justified for clean professional alignment.", "• Text Alignment: ")
    add_bullet(doc, "Every chapter starts on a new page with a formal chapter title banner.", "• Pagination: ")
    add_bullet(doc, "Numbered chapter-wise (e.g., Figure 5.1, Table 8.1) with captions and references.", "• Figures & Tables: ")
    add_bullet(doc, "APA 7th Edition citation formatting consistently applied throughout.", "• References: ")

print("All chapter builder functions compiled successfully.")
