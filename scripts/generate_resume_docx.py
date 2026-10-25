import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def add_p_border_bottom(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = parse_xml(r'<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                     r'<w:bottom w:val="single" w:sz="6" w:space="1" w:color="000000"/>'
                     r'</w:pBdr>')
    pPr.append(pBdr)

doc = docx.Document()

# Page setup: Letter, 0.5 in top/bottom, 0.55 in left/right
section = doc.sections[0]
section.page_width = Inches(8.5)
section.page_height = Inches(11.0)
section.top_margin = Inches(0.5)
section.bottom_margin = Inches(0.45)
section.left_margin = Inches(0.55)
section.right_margin = Inches(0.55)

# Style defaults
style = doc.styles['Normal']
style.font.name = 'Arial'
style.font.size = Pt(8.4)
style.font.color.rgb = RGBColor(0x11, 0x11, 0x11)

# Header
p_name = doc.add_paragraph()
p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_name.paragraph_format.space_before = Pt(0)
p_name.paragraph_format.space_after = Pt(2)
run_name = p_name.add_run("HET JOSHI")
run_name.bold = True
run_name.font.size = Pt(19.5)
run_name.font.name = 'Arial'

p_c1 = doc.add_paragraph()
p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c1.paragraph_format.space_before = Pt(0)
p_c1.paragraph_format.space_after = Pt(1)
run_c1 = p_c1.add_run("Bharuch, India  |  +91 9409476665  |  hetjoshi535@gmail.com")
run_c1.font.size = Pt(8.4)
run_c1.font.name = 'Arial'

p_c2 = doc.add_paragraph()
p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c2.paragraph_format.space_before = Pt(0)
p_c2.paragraph_format.space_after = Pt(5)
run_c2 = p_c2.add_run("linkedin.com/in/het-joshi-6b4649256  |  github.com/lucky972005")
run_c2.font.size = Pt(8.4)
run_c2.font.name = 'Arial'

def add_section_header(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(2)
    add_p_border_bottom(p)
    run = p.add_run(title)
    run.bold = True
    run.font.size = Pt(10.2)
    run.font.name = 'Arial'
    return p

def add_bullet(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.first_line_indent = Inches(-0.14)
    p.paragraph_format.space_before = Pt(0.5)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.15
    run_bullet = p.add_run("•  ")
    run_bullet.font.size = Pt(8.2)
    run_bullet.font.name = 'Arial'
    run_text = p.add_run(text)
    run_text.font.size = Pt(8.2)
    run_text.font.name = 'Arial'
    return p

# 1. PROFESSIONAL SUMMARY
add_section_header("PROFESSIONAL SUMMARY")
p_sum = doc.add_paragraph()
p_sum.paragraph_format.space_before = Pt(2)
p_sum.paragraph_format.space_after = Pt(3)
p_sum.paragraph_format.line_spacing = 1.18
run_sum = p_sum.add_run(
    "Final-year Computer Engineering student with practical experience in SQL, database fundamentals, Python, data "
    "visualization, and application data handling, supported by internship and academic project experience. Comfortable "
    "working with structured data, building dashboards, troubleshooting technical issues, and learning new technologies "
    "quickly. Strong communicator with a methodical approach to data accuracy, problem solving, and team collaboration."
)
run_sum.font.size = Pt(8.3)
run_sum.font.name = 'Arial'

# 2. TECHNICAL SKILLS
add_section_header("TECHNICAL SKILLS")
skills_data = [
    ("Database & Data", "SQL, database normalization, data extraction fundamentals, data accuracy"),
    ("Data & Reporting", "Data visualization, dashboards, analytics, Chart.js"),
    ("Programming", "Python, JavaScript, Embedded C"),
    ("Systems & Cloud", "AWS (Certified), Linux fundamentals, server setup & administration, networking"),
    ("Development Tools", "Git/GitHub, REST APIs, Firebase/Firestore, Docker, CI/CD"),
    ("Professional", "Problem solving, technical documentation, communication, teamwork, presentations")
]

tbl = doc.add_table(rows=len(skills_data), cols=2)
tbl.autofit = False
tbl.columns[0].width = Inches(1.8)
tbl.columns[1].width = Inches(5.6)
for i, (k, v) in enumerate(skills_data):
    row = tbl.rows[i]
    cell_k, cell_v = row.cells[0], row.cells[1]
    cell_k.width = Inches(1.8)
    cell_v.width = Inches(5.6)
    
    pk = cell_k.paragraphs[0]
    pk.paragraph_format.space_before = Pt(0.5)
    pk.paragraph_format.space_after = Pt(0.5)
    pk.paragraph_format.left_indent = Inches(0.1)
    rk = pk.add_run(k)
    rk.bold = True
    rk.font.size = Pt(7.9)
    rk.font.name = 'Arial'

    pv = cell_v.paragraphs[0]
    pv.paragraph_format.space_before = Pt(0.5)
    pv.paragraph_format.space_after = Pt(0.5)
    rv = pv.add_run(v)
    rv.font.size = Pt(7.9)
    rv.font.name = 'Arial'

# 3. WORK HISTORY
add_section_header("WORK HISTORY")
p_job = doc.add_paragraph()
p_job.paragraph_format.space_before = Pt(2.5)
p_job.paragraph_format.space_after = Pt(1.5)
r_job = p_job.add_run("Intern  |  Dtech Group — Bharuch, India  |  02/2024 – 06/2024")
r_job.bold = True
r_job.font.size = Pt(8.8)
r_job.font.name = 'Arial'

add_bullet("Created and configured servers and gained practical exposure to cloud fundamentals, deployment, and infrastructure setup.")
add_bullet("Supported staff with daily technical tasks and helped resolve recurring technical issues.")
add_bullet("Analyzed recurring server problems and worked with cross-functional teams to develop and implement solutions.")
add_bullet("Collaborated with fellow interns on group projects and presentations, strengthening communication, documentation, and teamwork.")

# 4. PROJECTS
add_section_header("PROJECTS")

# MaintAI
p_p1 = doc.add_paragraph()
p_p1.paragraph_format.space_before = Pt(2.5)
p_p1.paragraph_format.space_after = Pt(0.5)
r_p1 = p_p1.add_run("MaintAI — Industrial Maintenance Assistant  |  2026")
r_p1.bold = True
r_p1.font.size = Pt(8.8)
r_p1.font.name = 'Arial'

p_p1_t = doc.add_paragraph()
p_p1_t.paragraph_format.space_before = Pt(0)
p_p1_t.paragraph_format.space_after = Pt(1)
r_p1_t = p_p1_t.add_run("Technologies: Next.js 14, TypeScript, Supabase, PostgreSQL, Gemini 1.5 Flash, Docker, Dexie.js (PWA), Web Speech API, REST APIs")
r_p1_t.font.size = Pt(7.8)
r_p1_t.font.name = 'Arial'

add_bullet("Engineered a full-stack, offline-first PWA using Supabase as the backend, integrating Gemini AI vision and QR scanning for real-time machine identification and automated tool verification.")
add_bullet("Built an interactive AR repair guide with canvas overlays and hands-free voice navigation, translating complex machine SOPs into actionable, step-by-step procedures.")
add_bullet("Worked end-to-end with application data from offline IndexedDB queueing through backend cloud storage, predictive analytics, and user-facing digital compliance certification.")

# Smart Agriculture
p_p2 = doc.add_paragraph()
p_p2.paragraph_format.space_before = Pt(2.5)
p_p2.paragraph_format.space_after = Pt(0.5)
r_p2 = p_p2.add_run("Smart Agriculture — Intelligent Farming Management System  |  2024")
r_p2.bold = True
r_p2.font.size = Pt(8.8)
r_p2.font.name = 'Arial'

p_p2_t = doc.add_paragraph()
p_p2_t.paragraph_format.space_before = Pt(0)
p_p2_t.paragraph_format.space_after = Pt(1)
r_p2_t = p_p2_t.add_run("Technologies: HTML, CSS, JavaScript, Firebase Auth, Firestore, Chart.js, TensorFlow.js, ESP8266, REST API, Groq API")
r_p2_t.font.size = Pt(7.8)
r_p2_t.font.name = 'Arial'

add_bullet("Engineered a full-stack platform using Firestore as the backend, connecting ESP8266 devices to the cloud through REST APIs for real-time data ingestion and monitoring.")
add_bullet("Built a centralized dashboard with live analytics and interactive visualizations using Chart.js, translating raw sensor data into actionable insights.")
add_bullet("Worked end-to-end with application data from ingestion through backend storage, analytics, and user-facing reporting.")

# Object Avoidance Robot
p_p3 = doc.add_paragraph()
p_p3.paragraph_format.space_before = Pt(2.5)
p_p3.paragraph_format.space_after = Pt(0.5)
r_p3 = p_p3.add_run("Object Avoidance and Voice-Controlled Robot  |  2024")
r_p3.bold = True
r_p3.font.size = Pt(8.8)
r_p3.font.name = 'Arial'

p_p3_t = doc.add_paragraph()
p_p3_t.paragraph_format.space_before = Pt(0)
p_p3_t.paragraph_format.space_after = Pt(1)
r_p3_t = p_p3_t.add_run("Technologies: Arduino Uno, ESP8266, Ultrasonic Sensor, Bluetooth (HC-05), Embedded C, Motor Driver (L298N)")
r_p3_t.font.size = Pt(7.8)
r_p3_t.font.name = 'Arial'

add_bullet("Designed an autonomous system combining real-time sensor input with wireless command handling; tuned sensor response and control logic through iterative debugging.")

# 5. EDUCATION
add_section_header("EDUCATION")
p_e1 = doc.add_paragraph()
p_e1.paragraph_format.space_before = Pt(1.5)
p_e1.paragraph_format.space_after = Pt(1)
r_e1 = p_e1.add_run("B.Tech, Computer Engineering — PP Savani University, Surat  |  Expected 05/2027")
r_e1.font.size = Pt(8.3)
r_e1.font.name = 'Arial'

p_e2 = doc.add_paragraph()
p_e2.paragraph_format.space_before = Pt(0)
p_e2.paragraph_format.space_after = Pt(2)
r_e2 = p_e2.add_run("Diploma, Computer Engineering — PP Savani University, Surat  |  05/2024")
r_e2.font.size = Pt(8.3)
r_e2.font.name = 'Arial'

# 6. CERTIFICATIONS
add_section_header("CERTIFICATIONS")
add_bullet("AWS Certification — 03/2026")
add_bullet("Deloitte – Data Analytics Job Simulation — 06/2026")
add_bullet("TATA – GenAI Powered Data Analytics Job Simulation — 06/2026")
add_bullet("TATA – Data Visualisation: Empowering Business with Effective Insights — 07/2026")
add_bullet("NPTEL – Software Project Management — 10/2025")
add_bullet("Coursera – Android Development — 05/2025")

doc_path_pro = r"c:\dev\pro\Het_Joshi_Resume_MaintAI.docx"
doc_path_dl = r"C:\Users\hetjo\Downloads\Het_Joshi_Resume_MaintAI.docx"
doc.save(doc_path_pro)
doc.save(doc_path_dl)
print("Saved DOCX to both project and Downloads folders successfully!")
