import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import qn
from docx2pdf import convert
import os

TEMPLATE_PATH = r"C:\Users\hetjo\Downloads\Internship_UDP_Training_Report_Template for reporting 2.docx"
OUTPUT_PRO_DOCX = r"C:\dev\pro\MaintAI_Reporting_1_Het_Joshi.docx"
OUTPUT_PRO_PDF = r"C:\dev\pro\MaintAI_Reporting_1_Het_Joshi.pdf"
OUTPUT_DL_DOCX = r"C:\Users\hetjo\Downloads\report\MaintAI_Reporting_1_Het_Joshi.docx"
OUTPUT_DL_PDF = r"C:\Users\hetjo\Downloads\report\MaintAI_Reporting_1_Het_Joshi.pdf"
OUTPUT_R1_PDF = r"C:\Users\hetjo\Downloads\report\report1.pdf"

print("Building fully aligned Report 1 (Monthly Progress Report)...")

doc = docx.Document(TEMPLATE_PATH)

def format_run(run, font_name="Cambria", font_size=11, bold=False, italic=False, color=None):
    if font_name:
        run.font.name = font_name
    if font_size:
        run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color

def set_cell(cell, text, bold=False, italic=False, font_name="Cambria", font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = cell.paragraphs[0]
    p.text = ""
    p.alignment = align
    p.paragraph_format.space_before = Pt(1.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.12
    run = p.add_run(text)
    format_run(run, font_name=font_name, font_size=font_size, bold=bold, italic=italic)

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    if trPr.find(qn('w:cantSplit')) is None:
        trPr.append(parse_xml(r'<w:cantSplit xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))

def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    # remove existing shd if any
    for existing in tcPr.findall(qn('w:shd')):
        tcPr.remove(existing)
    shd = parse_xml(f'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=30, bottom=30, left=50, right=50):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def style_heading_box(p, text):
    p.text = ""
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    format_run(r, font_name="Cambria", font_size=11, bold=True)
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml(r'<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:bottom w:val="single" w:sz="6" w:space="2" w:color="0284C7"/></w:pBdr>')
    pPr.append(pBdr)

def add_bullet(parent_doc, text, bold_prefix="", font_name="Cambria", font_size=9.5, space_before=1.5, space_after=1.5):
    p = parent_doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    r_bullet = p.add_run("•  ")
    format_run(r_bullet, font_name=font_name, font_size=font_size, bold=True, color=RGBColor(2, 132, 199))
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        format_run(r_b, font_name=font_name, font_size=font_size, bold=True)
    r_t = p.add_run(text)
    format_run(r_t, font_name=font_name, font_size=font_size, bold=False)
    return p

# Remove all elements from body except header/footer to build a completely clean Report 1
# We'll keep doc properties, margins, and header intact
body = doc._body._element
for child in list(body):
    if child.tag.endswith('sectPr'):
        continue
    body.remove(child)

# Title paragraph
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(4)
p_title.paragraph_format.space_after = Pt(2)
r1 = p_title.add_run("INTERNSHIP / UDP / TRAINING REPORT\n")
format_run(r1, font_name="Cambria", font_size=13, bold=True)
r2 = p_title.add_run("(Monthly Progress Report)")
format_run(r2, font_name="Cambria", font_size=10.5, italic=True)

# 1. Student Information
p1 = doc.add_paragraph()
style_heading_box(p1, "1. Student Information")

t0 = doc.add_table(rows=6, cols=2)
t0.alignment = WD_TABLE_ALIGNMENT.CENTER
t0_data = [
    ("Student Name", "Het Joshi"),
    ("Enrollment Number", "24SE09CE003"),
    ("Program/Branch", "B.Tech Computer Engineering"),
    ("Semester", "7"),
    ("Contact Number", "9409476665"),
    ("Email ID", "24se09ce003@ppsu.ac.in"),
]
for idx, (lbl, val) in enumerate(t0_data):
    row = t0.rows[idx]
    set_cell(row.cells[0], lbl, bold=True, font_size=9.5)
    set_cell(row.cells[1], val, bold=False, font_size=9.5)
    row.cells[0].width = Inches(2.2)
    row.cells[1].width = Inches(4.3)
    make_row_cant_split(row)

# 2. Internship / UDP / Training Details
p2 = doc.add_paragraph()
style_heading_box(p2, "2. Internship / UDP / Training Details")

t1 = doc.add_table(rows=7, cols=2)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
t1_data = [
    ("Type", "UDP (Undergraduate Design Project)"),
    ("Company/Organization", "P.P. SAVANI UNIVERSITY"),
    ("Department/Domain", "Full-Stack Web Development & Applied AI (Industrial IoT / Maintenance-Tech)"),
    ("Mentor Name (Company)", "P.P. Savani University"),
    ("Mentor Name (Institute)", "Mr. Ayush Dodia"),
    ("Start Date", "08/06/2026"),
    ("End Date", "03/10/2026"),
]
for idx, (lbl, val) in enumerate(t1_data):
    row = t1.rows[idx]
    set_cell(row.cells[0], lbl, bold=True, font_size=9.5)
    set_cell(row.cells[1], val, bold=False, font_size=9.5)
    row.cells[0].width = Inches(2.2)
    row.cells[1].width = Inches(4.3)
    make_row_cant_split(row)

# 3. Work Progress Summary
p3 = doc.add_paragraph()
style_heading_box(p3, "3. Work Progress Summary")

p_t = doc.add_paragraph()
p_t.paragraph_format.space_before = Pt(3)
p_t.paragraph_format.space_after = Pt(4)
r_t_lbl = p_t.add_run("a) Project Title:\n")
format_run(r_t_lbl, font_name="Cambria", font_size=10.5, bold=True)
r_t_val = p_t.add_run("MaintAI — An AI-Powered Progressive Web Application for Industrial Maintenance Assistance")
format_run(r_t_val, font_name="Cambria", font_size=11, bold=True, color=RGBColor(15, 23, 42))

# Page Break for clean section structure
p_b_head = doc.add_paragraph()
p_b_head.paragraph_format.page_break_before = True
p_b_head.paragraph_format.space_before = Pt(4)
p_b_head.paragraph_format.space_after = Pt(3)
r_ps_lbl = p_b_head.add_run("b) Problem Statement:")
format_run(r_ps_lbl, font_name="Cambria", font_size=11, bold=True)

p_ps1 = doc.add_paragraph()
p_ps1.paragraph_format.space_before = Pt(2)
p_ps1.paragraph_format.space_after = Pt(3)
p_ps1.paragraph_format.line_spacing = 1.15
r_ps1 = p_ps1.add_run(
    "Industrial machinery maintenance across manufacturing facilities is traditionally governed by static paper-based operating manuals, disorganized physical binder archives, or unstructured tribal knowledge passed down informally between senior and junior technicians. When mechanical faults, unusual acoustic vibrations, or sudden equipment shutdowns emerge on the factory shop floor, apprentice and junior maintenance personnel routinely struggle with accurate equipment identification, selecting the appropriate tools, locating exact internal components, and executing multi-step repair workflows in strict compliance with plant safety protocols. These operational bottlenecks lead to prolonged Mean Time to Repair (MTTR), inflated machine downtime costs, increased human error, and heightened workplace safety hazards."
)
format_run(r_ps1, font_name="Cambria", font_size=9.5)

p_ps2 = doc.add_paragraph()
p_ps2.paragraph_format.space_before = Pt(2)
p_ps2.paragraph_format.space_after = Pt(4)
p_ps2.paragraph_format.line_spacing = 1.15
r_ps2 = p_ps2.add_run(
    "The proposed project aims to develop MaintAI, an AI-powered, offline-first Progressive Web Application (PWA) that delivers Augmented Reality (AR) interactive repair guidance directly onto industrial machinery without necessitating high-cost proprietary AR headsets. Technicians instantly discover machines through camera QR scanning or multimodal AI image recognition, receive animated canvas overlays pinpointing critical components, navigate steps hands-free via voice recognition, verify tool compliance through computer vision, and cache maintenance records locally with automatic cloud reconciliation."
)
format_run(r_ps2, font_name="Cambria", font_size=9.5)

# Objectives
p_obj_head = doc.add_paragraph()
p_obj_head.paragraph_format.space_before = Pt(4)
p_obj_head.paragraph_format.space_after = Pt(2)
r_obj_head = p_obj_head.add_run("c) Objectives:")
format_run(r_obj_head, font_name="Cambria", font_size=11, bold=True)

objectives = [
    ("Universal Web Application: ", "Develop a responsive Progressive Web Application using Next.js 14, React 18, and TypeScript accessible across smartphones, tablets, and desktops."),
    ("Rapid Equipment Discovery: ", "Identify industrial machines instantly through camera-based QR code scanning and provide automated fallback recognition."),
    ("AI Multimodal Vision Recognition: ", "Integrate vision-based AI classification to recognize machinery when physical QR code tags are damaged, obscured, or missing."),
    ("Interactive AR Maintenance Guidance: ", "Render responsive HTML5 Canvas boundary markers directly over live camera streams to guide component removal and replacement."),
    ("Hands-Free Voice Navigation: ", "Implement hands-free speech recognition (Web Speech API) enabling technicians with soiled gloves to progress steps safely via voice commands."),
    ("AI Tool Verification Guardrail: ", "Deploy real-time computer vision checks verifying that the technician is holding the designated tool before granting procedure progression."),
    ("Offline-First Shop-Floor Continuity: ", "Engineer local caching using Dexie.js (IndexedDB) and Workbox service workers to ensure 100% operational continuity during factory network blackouts."),
    ("Downtime & Failure Analytics: ", "Provide interactive supervisory dashboards with telemetry indicators, MTTR tracking, downtime analytics, and predictive health scoring."),
    ("Digital Work Order & Incident Triage: ", "Streamline fault reporting with camera evidence upload, supervisor dispatching, and technician inbox work order execution."),
    ("Cost-Effective Industry 4.0 Scalability: ", "Offer a low-cost, zero-hardware-install alternative to expensive AR headsets, accelerating workforce training and equipment reliability.")
]
for pfx, txt in objectives:
    add_bullet(doc, txt, bold_prefix=pfx, font_size=9.2, space_before=1.2, space_after=1.2)

# Proposed Methodology
p_meth_head = doc.add_paragraph()
p_meth_head.paragraph_format.space_before = Pt(4)
p_meth_head.paragraph_format.space_after = Pt(2)
r_meth_head = p_meth_head.add_run("d) Proposed Methodology:")
format_run(r_meth_head, font_name="Cambria", font_size=11, bold=True)

methodology_phases = [
    ("Phase 1: Requirement Analysis & Field Study — ", "Analyze shop-floor maintenance workflows, interview plant technicians, and establish functional/non-functional criteria."),
    ("Phase 2: System Architecture & Data Modeling — ", "Architect 3-tier PWA structure, establish PostgreSQL relational schema with Supabase, and configure tenant Row Level Security."),
    ("Phase 3: Machine Identification & Telemetry Portal — ", "Integrate html5-qrcode scanner and build machine specification portals displaying operational status and live alerts."),
    ("Phase 4: AI Multimodal Engine Integration — ", "Implement unified abstraction supporting Google Gemini 1.5 Flash and OpenAI GPT-4o for visual machine and tool classification."),
    ("Phase 5: AR Canvas Overlay & Step Guide — ", "Develop 2D viewport-normalized HTML5 Canvas animation engine to project pulsing boundary boxes onto camera feeds."),
    ("Phase 6: Hands-Free Voice Control Engine — ", "Implement Web Speech recognition with strict command matching ('Next', 'Previous', 'Safety', 'Help') and audio-visual feedback."),
    ("Phase 7: Offline PWA & Sync Pipeline — ", "Configure IndexedDB local stores via Dexie.js, service worker asset caching, and write-ahead sync queue with exponential backoff."),
    ("Phase 8: Comprehensive Testing & Cloud Deployment — ", "Conduct functional testing, cross-device field trials under shop-floor noise, and deploy production build to Vercel with HTTPS.")
]
for pfx, txt in methodology_phases:
    add_bullet(doc, txt, bold_prefix=pfx, font_size=9.2, space_before=1.2, space_after=1.2)

# Expected Outcomes & Future Scope (Page Break for clean presentation)
p_out_head = doc.add_paragraph()
p_out_head.paragraph_format.page_break_before = True
p_out_head.paragraph_format.space_before = Pt(4)
p_out_head.paragraph_format.space_after = Pt(2)
r_out_head = p_out_head.add_run("e) Expected Outcomes:")
format_run(r_out_head, font_name="Cambria", font_size=11, bold=True)

expected_outcomes = [
    ("AI-Powered Maintenance Platform: ", "A fully functional, installable Progressive Web Application tailored for factory technicians and supervisors."),
    ("Sub-Second QR Resolution: ", "Instant machine telemetry and procedure retrieval in under 3 seconds upon QR scanning."),
    ("High-Accuracy Tool & Machine Recognition: ", ">85% classification confidence for machinery and maintenance tools using multimodal vision models."),
    ("Real-Time AR Step-by-Step Overlays: ", "Fluid 60 FPS animated component bounding markers adapting to mobile viewport orientations."),
    ("Hands-Free Speech Operation: ", "Reliable hands-free navigation facilitating safety and speed for technicians wearing protective equipment."),
    ("Zero-Data-Loss Offline Durability: ", "Autonomous offline maintenance logging and fault reporting with automatic background sync reconciliation."),
    ("Measurable Downtime Reduction: ", "Estimated 20–30% reduction in Mean Time to Repair (MTTR) by eliminating manual paper searches and procedural guesswork."),
    ("Accelerated Technician Onboarding: ", "Structured interactive guidance shortening apprentice training cycles by up to 40%."),
    ("Supervisory Fleet Visibility: ", "Real-time visibility into machine downtime trends, parts reorder thresholds, and active technician work orders."),
    ("Standardized Digital Maintenance History: ", "Audit-ready cloud records with timestamped maintenance evidence photos and parts tracking.")
]
for pfx, txt in expected_outcomes:
    add_bullet(doc, txt, bold_prefix=pfx, font_size=9.2, space_before=1.2, space_after=1.2)

# Future Scope
p_fs_head = doc.add_paragraph()
p_fs_head.paragraph_format.space_before = Pt(4)
p_fs_head.paragraph_format.space_after = Pt(2)
r_fs_head = p_fs_head.add_run("Future Scope:")
format_run(r_fs_head, font_name="Cambria", font_size=11, bold=True)

future_scope = [
    ("IoT Telemetry & Vibration Integration: ", "Connect industrial vibration and thermal IoT sensors (MQTT/OPC-UA) for real-time condition-based anomaly alerting."),
    ("Predictive Failure Modeling: ", "Train deep learning time-series models on historical sensor logs to forecast component failure before breakdown occurs."),
    ("Remote Expert Video Assistance: ", "Embed WebRTC real-time audio/video streaming allowing offsite senior engineers to annotate live technician camera feeds."),
    ("Smart AR Glasses & WebXR: ", "Expand canvas AR rendering to WebXR-compliant headsets and wearable monocles (RealWear, Magic Leap) for full stereoscopic guidance."),
    ("Automated Purchase Requisition: ", "Integrate enterprise ERP and supply chain APIs (SAP/Oracle) to trigger automatic purchase orders when spare parts drop below safety stock."),
    ("Digital Twin 3D Visualization: ", "Incorporate interactive 3D Three.js CAD exploded views of complex machine sub-assemblies directly in the browser.")
]
for pfx, txt in future_scope:
    add_bullet(doc, txt, bold_prefix=pfx, font_size=9.2, space_before=1.2, space_after=1.2)

# 4. Tasks Accomplished
p4 = doc.add_paragraph()
style_heading_box(p4, "4. Tasks Accomplished")

accomplished_tasks = [
    ("Industrial Workflow & Domain Investigation: ", "Conducted detailed literature review and shop-floor workflow analysis on machine maintenance procedures (CNC, air compressors, water pumps, diesel generators)."),
    ("System Specification & Architecture Formulation: ", "Architected the 3-tier web application architecture, defined user role boundaries (Technician, Supervisor, Administrator), and finalized the technology stack."),
    ("Technology Stack Benchmarking & Selection: ", "Selected Next.js 14 App Router, TypeScript, and Tailwind CSS for rapid responsive frontend design; Supabase (PostgreSQL) for cloud persistence; and Dexie.js for offline IndexedDB caching."),
    ("AR Feasibility Study & Hardware Abstraction: ", "Evaluated native ARCore vs. web-standard HTML5 Canvas overlay approaches; established that browser-based canvas overlays provide superior cross-platform accessibility without device fragmentation."),
    ("Project Setup & Initial Repository Scaffolding: ", "Created the Git repository, configured TypeScript and ESLint toolchains, and established the development directory structure with modular lib/ abstractions.")
]
for pfx, txt in accomplished_tasks:
    add_bullet(doc, txt, bold_prefix=pfx, font_size=9.2, space_before=1.2, space_after=1.2)

# 5. Tasks in Progress / Next Plan (Page Break for clean presentation)
p5 = doc.add_paragraph()
p5.paragraph_format.page_break_before = True
style_heading_box(p5, "5. Tasks in Progress / Next Plan")

next_tasks = [
    ("User Authentication & Profile Scaffolding: ", "Implement Supabase Auth login, signup, and session state persistence with role-based dashboard redirection."),
    ("Technician Dashboard & Fleet Overview: ", "Develop the primary authenticated dashboard showcasing fleet health, recent repairs, and quick scanner shortcuts."),
    ("Camera QR Scanner Module: ", "Integrate html5-qrcode library with front/back camera selection, viewfinders, and automatic machine route navigation."),
    ("Multimodal AI Machine Classifier: ", "Implement image capture and prompt construction for Google Gemini and OpenAI vision APIs to recognize machinery from camera stills."),
    ("FixBot AI Conversational Assistant: ", "Build chat interface with domain system prompts and knowledge context to assist technicians with torque specs and troubleshooting."),
    ("AR Step Guide & Safety Checkpoints: ", "Prototype the step-by-step guidance interface with safety checklist confirmation before starting procedure steps.")
]
for pfx, txt in next_tasks:
    add_bullet(doc, txt, bold_prefix=pfx, font_size=9.2, space_before=1.2, space_after=1.2)

# Project Timeline Gantt Chart Table
p_gantt_head = doc.add_paragraph()
p_gantt_head.paragraph_format.space_before = Pt(4)
p_gantt_head.paragraph_format.space_after = Pt(2)
r_gh = p_gantt_head.add_run("Project Timeline & Milestone Schedule (16 Weeks):")
format_run(r_gh, font_name="Cambria", font_size=10.5, bold=True)

gantt_tasks = [
    ("Project Planning & Requirement Analysis", [1, 2]),
    ("Literature Survey & Research", [2, 3, 4]),
    ("Feasibility Study & Tech Selection", [3, 4]),
    ("SRS & Architecture Design", [4, 5]),
    ("UI/UX Design & Component System", [5, 6]),
    ("Supabase Database Schema & RLS", [6, 7]),
    ("QR Code Scanner Integration", [7, 8]),
    ("AI Dataset & Vision Model Setup", [8, 9]),
    ("AI Machine Identification Engine", [9, 10]),
    ("HTML5 Canvas AR Overlay Engine", [10, 11, 12]),
    ("Web Speech Voice Control Engine", [11, 12]),
    ("Dexie.js Offline Cache & Sync Queue", [12, 13]),
    ("Supervisor Analytics & Reports", [13, 14]),
    ("Multi-Device Testing & Bug Fixing", [14, 15]),
    ("Production Cloud Deployment (Vercel)", [15, 16]),
    ("Final Documentation & Demonstration", [15, 16])
]

t_gantt = doc.add_table(rows=len(gantt_tasks)+1, cols=17)
t_gantt.alignment = WD_TABLE_ALIGNMENT.CENTER

# Header row
set_cell(t_gantt.rows[0].cells[0], "Task / Activity", bold=True, font_size=8, align=WD_ALIGN_PARAGRAPH.LEFT)
t_gantt.rows[0].cells[0].width = Inches(2.2)
set_cell_margins(t_gantt.rows[0].cells[0], top=20, bottom=20, left=30, right=30)
set_cell_shading(t_gantt.rows[0].cells[0], "0F172A")
t_gantt.rows[0].cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

for w in range(1, 17):
    cell = t_gantt.rows[0].cells[w]
    cell.width = Inches(0.26)
    set_cell(cell, f"W{w}", bold=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_margins(cell, top=20, bottom=20, left=10, right=10)
    set_cell_shading(cell, "0F172A")
    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
make_row_cant_split(t_gantt.rows[0])

for idx, (tname, active_weeks) in enumerate(gantt_tasks):
    row = t_gantt.rows[idx + 1]
    set_cell(row.cells[0], tname, bold=False, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
    row.cells[0].width = Inches(2.2)
    set_cell_margins(row.cells[0], top=15, bottom=15, left=30, right=30)
    for w in range(1, 17):
        c = row.cells[w]
        c.width = Inches(0.26)
        set_cell(c, "", font_size=7)
        set_cell_margins(c, top=15, bottom=15, left=5, right=5)
        if w in active_weeks:
            set_cell_shading(c, "0284C7")  # Beautiful PPSU theme blue
        else:
            set_cell_shading(c, "F8FAFC")
    make_row_cant_split(row)

# 6. Learnings / Skills Acquired
p6 = doc.add_paragraph()
style_heading_box(p6, "6. Learnings / Skills Acquired")

p_tech_head = doc.add_paragraph()
p_tech_head.paragraph_format.space_before = Pt(3)
p_tech_head.paragraph_format.space_after = Pt(2)
r_th = p_tech_head.add_run("Technical Skills Learned:")
format_run(r_th, font_name="Cambria", font_size=10, bold=True)

tech_skills = [
    ("Progressive Web Application Architecture: ", "Understanding service worker lifecycles, Web App Manifests, and browser client storage mechanisms."),
    ("Modern React & Next.js 14 App Router: ", "Leveraging server and client components, modular directory routing, and layout nesting."),
    ("Cloud Database Engineering (Supabase): ", "Designing relational schemas, setting primary/foreign key constraints, and applying Row Level Security (RLS) policies."),
    ("Multimodal Computer Vision APIs: ", "Structuring image base64 payloads and engineering strict JSON extraction prompts for Google Gemini and OpenAI vision models."),
    ("Browser Hardware API Integration: ", "Accessing camera video streams via navigator.mediaDevices.getUserMedia() and microphone input via Web Speech API.")
]
for pfx, txt in tech_skills:
    add_bullet(doc, txt, bold_prefix=pfx, font_size=9.2, space_before=1.2, space_after=1.2)

p_prof_head = doc.add_paragraph()
p_prof_head.paragraph_format.space_before = Pt(3)
p_prof_head.paragraph_format.space_after = Pt(2)
r_prh = p_prof_head.add_run("Professional Skills Learned:")
format_run(r_prh, font_name="Cambria", font_size=10, bold=True)

prof_skills = [
    ("Requirements Elicitation: ", "Translating real-world industrial plant pain points into rigorous technical requirements."),
    ("Agile Milestone Planning: ", "Decomposing complex engineering epics into structured sprint deliverables spanning 16 weeks."),
    ("Technical Documentation & Diagrams: ", "Formulating comprehensive Software Requirement Specifications (SRS) and UML architectural diagrams."),
    ("Version Control Best Practices: ", "Managing Git repositories with feature branches, semantic commits, and clean issue tracking.")
]
for pfx, txt in prof_skills:
    add_bullet(doc, txt, bold_prefix=pfx, font_size=9.2, space_before=1.2, space_after=1.2)

# Evaluation (Page Break for clean official grading sheet)
p_eval_head = doc.add_paragraph()
p_eval_head.paragraph_format.page_break_before = True
style_heading_box(p_eval_head, "Evaluation (To be filled by Mentor (Institute))")

t_eval = doc.add_table(rows=7, cols=7)
t_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_eval = ["Criteria", "Bloom's Level", "Excellent (20)", "Good (15)", "Average (10)", "Poor (5)", "Marks Obtained (Out of 20)"]
for c_idx, h in enumerate(headers_eval):
    set_cell(t_eval.rows[0].cells[c_idx], h, bold=True, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_shading(t_eval.rows[0].cells[c_idx], "F1F5F9")
make_row_cant_split(t_eval.rows[0])

eval_criteria_data = [
    ("Problem Definition", "L4–Analyze", "Clearly defined, justified real-world problem", "Defined but lacks depth", "Vague problem", "No clear problem", ""),
    ("Project Title Relevance", "L2–Understand", "Highly precise and aligned", "Mostly relevant", "Partially relevant", "Misleading", ""),
    ("Scope of Work", "L5–Evaluate", "Well-defined scope, deliverables, constraints", "Defined with minor gaps", "Broad/unclear", "No scope", ""),
    ("Literature Study", "L4–Analyze", "3–5 sources analyzed critically", "Sources listed", "Minimal references", "No study", ""),
    ("Clarity & Presentation", "L3–Apply", "Structured, professional", "Minor issues", "Some confusion", "Poor", "")
]
for r_idx, r_data in enumerate(eval_criteria_data):
    row = t_eval.rows[r_idx + 1]
    for c_idx, val in enumerate(r_data):
        align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [1, 6] else WD_ALIGN_PARAGRAPH.LEFT
        set_cell(row.cells[c_idx], val, bold=(c_idx==0), font_size=8, align=align)
    make_row_cant_split(row)

# Total marks row
r_total = t_eval.rows[6]
set_cell(r_total.cells[0], "Total Marks", bold=True, font_size=9, align=WD_ALIGN_PARAGRAPH.RIGHT)
for i in range(1, 6):
    set_cell(r_total.cells[i], "", font_size=9)
set_cell(r_total.cells[6], "", font_size=9)
make_row_cant_split(r_total)

# Evaluation Signatures
p_sig_head = doc.add_paragraph()
p_sig_head.paragraph_format.space_before = Pt(8)
p_sig_head.paragraph_format.space_after = Pt(3)
r_sh = p_sig_head.add_run("Evaluation Signatures")
format_run(r_sh, font_name="Cambria", font_size=10.5, bold=True)

t_sig = doc.add_table(rows=2, cols=3)
t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
sig_titles = ["Student Signature", "Mentor (Company) Signature", "Mentor (Institute) Signature"]
for c_idx, st in enumerate(sig_titles):
    set_cell(t_sig.rows[0].cells[c_idx], st, bold=True, font_size=9, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_shading(t_sig.rows[0].cells[c_idx], "F8FAFC")
    set_cell(t_sig.rows[1].cells[c_idx], "\n\n\n", font_size=9)
make_row_cant_split(t_sig.rows[0])
make_row_cant_split(t_sig.rows[1])

# Mentor Remarks (Page Break for dedicated remarks sheet)
p_rem_head = doc.add_paragraph()
p_rem_head.paragraph_format.page_break_before = True
style_heading_box(p_rem_head, "Mentor (Institute) Remarks")

for _ in range(10):
    p_line = doc.add_paragraph()
    p_line.paragraph_format.space_before = Pt(8)
    p_line.paragraph_format.space_after = Pt(8)
    r_l = p_line.add_run("_________________________________________________________________________________________________________")
    format_run(r_l, font_name="Cambria", font_size=9, color=RGBColor(148, 163, 184))

os.makedirs(os.path.dirname(OUTPUT_DL_DOCX), exist_ok=True)
doc.save(OUTPUT_PRO_DOCX)
doc.save(OUTPUT_DL_DOCX)
print("Saved Report 1 Word documents successfully!")

print("Converting Report 1 to PDF...")
convert(OUTPUT_PRO_DOCX, OUTPUT_PRO_PDF)
import shutil
shutil.copy2(OUTPUT_PRO_PDF, OUTPUT_DL_PDF)
shutil.copy2(OUTPUT_PRO_PDF, OUTPUT_R1_PDF)
print("Report 1 generated and converted successfully!")
