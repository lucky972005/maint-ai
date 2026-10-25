import os
import subprocess
import fitz

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @page {
    size: letter portrait;
    margin: 0.5in 0.55in 0.45in 0.55in;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  body {
    font-family: Arial, Helvetica, sans-serif;
    color: #111111;
    background: #ffffff;
    font-size: 8.4pt;
    line-height: 1.25;
    -webkit-print-color-adjust: exact;
  }
  .header {
    text-align: center;
    margin-bottom: 6pt;
  }
  .header h1 {
    font-size: 19.5pt;
    font-weight: bold;
    letter-spacing: 0.5pt;
    margin-bottom: 2pt;
    color: #000000;
  }
  .contact-line {
    font-size: 8.4pt;
    color: #222222;
    line-height: 1.35;
  }
  .contact-line a {
    color: #222222;
    text-decoration: none;
  }
  .section-title {
    font-size: 10.2pt;
    font-weight: bold;
    color: #000000;
    letter-spacing: 0.3pt;
    margin-top: 5.5pt;
    margin-bottom: 1.5pt;
    border-bottom: 0.75pt solid #000000;
    padding-bottom: 1pt;
    text-transform: uppercase;
  }
  .summary-text {
    font-size: 8.3pt;
    line-height: 1.25;
    text-align: justify;
    margin-top: 2.5pt;
    margin-bottom: 3.5pt;
    color: #1a1a1a;
  }
  .skills-table {
    width: 100%;
    margin-top: 2pt;
    margin-bottom: 3pt;
    border-collapse: collapse;
  }
  .skills-table td {
    padding: 1.1pt 0;
    font-size: 7.9pt;
    vertical-align: top;
  }
  .skills-label {
    width: 135pt;
    font-weight: bold;
    color: #000000;
    padding-left: 8pt;
  }
  .skills-value {
    color: #1a1a1a;
  }
  .job-header {
    font-size: 8.8pt;
    font-weight: bold;
    color: #000000;
    margin-top: 2.5pt;
    margin-bottom: 1.5pt;
  }
  .project-item {
    margin-top: 3pt;
    margin-bottom: 2.5pt;
  }
  .project-title {
    font-size: 8.8pt;
    font-weight: bold;
    color: #000000;
    margin-bottom: 1pt;
  }
  .project-tech {
    font-size: 7.8pt;
    color: #2a2a2a;
    margin-bottom: 1.5pt;
  }
  .bullet-list {
    list-style: none;
    padding-left: 0;
  }
  .bullet-list li {
    position: relative;
    padding-left: 11pt;
    font-size: 8.2pt;
    line-height: 1.22;
    margin-bottom: 1.2pt;
    color: #1a1a1a;
    text-align: justify;
  }
  .bullet-list li::before {
    content: "•";
    position: absolute;
    left: 2pt;
    top: 0;
    font-size: 8pt;
    color: #000000;
  }
  .edu-row {
    font-size: 8.3pt;
    margin-top: 2pt;
    margin-bottom: 1.5pt;
    color: #1a1a1a;
  }
  .cert-list {
    list-style: none;
    padding-left: 0;
    margin-top: 2pt;
  }
  .cert-list li {
    position: relative;
    padding-left: 11pt;
    font-size: 8.2pt;
    line-height: 1.25;
    margin-bottom: 1pt;
    color: #1a1a1a;
  }
  .cert-list li::before {
    content: "•";
    position: absolute;
    left: 2pt;
    top: 0;
    font-size: 8pt;
    color: #000000;
  }
</style>
</head>
<body>

<div class="header">
  <h1>HET JOSHI</h1>
  <div class="contact-line">Bharuch, India &nbsp;|&nbsp; +91 9409476665 &nbsp;|&nbsp; <a href="mailto:hetjoshi535@gmail.com">hetjoshi535@gmail.com</a></div>
  <div class="contact-line"><a href="https://linkedin.com/in/het-joshi-6b4649256">linkedin.com/in/het-joshi-6b4649256</a> &nbsp;|&nbsp; <a href="https://github.com/lucky972005">github.com/lucky972005</a></div>
</div>

<div class="section-title">PROFESSIONAL SUMMARY</div>
<div class="summary-text">
  Final-year Computer Engineering student with practical experience in SQL, database fundamentals, Python, data visualization, and application data handling, supported by internship and academic project experience. Comfortable working with structured data, building dashboards, troubleshooting technical issues, and learning new technologies quickly. Strong communicator with a methodical approach to data accuracy, problem solving, and team collaboration.
</div>

<div class="section-title">TECHNICAL SKILLS</div>
<table class="skills-table">
  <tr>
    <td class="skills-label">Database & Data</td>
    <td class="skills-value">SQL, database normalization, data extraction fundamentals, data accuracy</td>
  </tr>
  <tr>
    <td class="skills-label">Data & Reporting</td>
    <td class="skills-value">Data visualization, dashboards, analytics, Chart.js</td>
  </tr>
  <tr>
    <td class="skills-label">Programming</td>
    <td class="skills-value">Python, JavaScript, Embedded C</td>
  </tr>
  <tr>
    <td class="skills-label">Systems & Cloud</td>
    <td class="skills-value">AWS (Certified), Linux fundamentals, server setup & administration, networking</td>
  </tr>
  <tr>
    <td class="skills-label">Development Tools</td>
    <td class="skills-value">Git/GitHub, REST APIs, Firebase/Firestore, Docker, CI/CD</td>
  </tr>
  <tr>
    <td class="skills-label">Professional</td>
    <td class="skills-value">Problem solving, technical documentation, communication, teamwork, presentations</td>
  </tr>
</table>

<div class="section-title">WORK HISTORY</div>
<div class="job-header">Intern &nbsp;|&nbsp; Dtech Group — Bharuch, India &nbsp;|&nbsp; 02/2024 – 06/2024</div>
<ul class="bullet-list">
  <li>Created and configured servers and gained practical exposure to cloud fundamentals, deployment, and infrastructure setup.</li>
  <li>Supported staff with daily technical tasks and helped resolve recurring technical issues.</li>
  <li>Analyzed recurring server problems and worked with cross-functional teams to develop and implement solutions.</li>
  <li>Collaborated with fellow interns on group projects and presentations, strengthening communication, documentation, and teamwork.</li>
</ul>

<div class="section-title">PROJECTS</div>

<div class="project-item">
  <div class="project-title">MaintAI — Industrial Maintenance Assistant &nbsp;|&nbsp; 2026</div>
  <div class="project-tech">Technologies: Next.js 14, TypeScript, Supabase, PostgreSQL, Gemini 1.5 Flash, Docker, Dexie.js (PWA), Web Speech API, REST APIs</div>
  <ul class="bullet-list">
    <li>Engineered a full-stack, offline-first PWA using Supabase as the backend, integrating Gemini AI vision and QR scanning for real-time machine identification and automated tool verification.</li>
    <li>Built an interactive AR repair guide with canvas overlays and hands-free voice navigation, translating complex machine SOPs into actionable, step-by-step procedures.</li>
    <li>Worked end-to-end with application data from offline IndexedDB queueing through backend cloud storage, predictive analytics, and user-facing digital compliance certification.</li>
  </ul>
</div>

<div class="project-item">
  <div class="project-title">Smart Agriculture — Intelligent Farming Management System &nbsp;|&nbsp; 2024</div>
  <div class="project-tech">Technologies: HTML, CSS, JavaScript, Firebase Auth, Firestore, Chart.js, TensorFlow.js, ESP8266, REST API, Groq API</div>
  <ul class="bullet-list">
    <li>Engineered a full-stack platform using Firestore as the backend, connecting ESP8266 devices to the cloud through REST APIs for real-time data ingestion and monitoring.</li>
    <li>Built a centralized dashboard with live analytics and interactive visualizations using Chart.js, translating raw sensor data into actionable insights.</li>
    <li>Worked end-to-end with application data from ingestion through backend storage, analytics, and user-facing reporting.</li>
  </ul>
</div>

<div class="project-item">
  <div class="project-title">Object Avoidance and Voice-Controlled Robot &nbsp;|&nbsp; 2024</div>
  <div class="project-tech">Technologies: Arduino Uno, ESP8266, Ultrasonic Sensor, Bluetooth (HC-05), Embedded C, Motor Driver (L298N)</div>
  <ul class="bullet-list">
    <li>Designed an autonomous system combining real-time sensor input with wireless command handling; tuned sensor response and control logic through iterative debugging.</li>
  </ul>
</div>

<div class="section-title">EDUCATION</div>
<div class="edu-row">B.Tech, Computer Engineering — PP Savani University, Surat &nbsp;|&nbsp; Expected 05/2027</div>
<div class="edu-row">Diploma, Computer Engineering — PP Savani University, Surat &nbsp;|&nbsp; 05/2024</div>

<div class="section-title">CERTIFICATIONS</div>
<ul class="cert-list">
  <li>AWS Certification — 03/2026</li>
  <li>Deloitte – Data Analytics Job Simulation — 06/2026</li>
  <li>TATA – GenAI Powered Data Analytics Job Simulation — 06/2026</li>
  <li>TATA – Data Visualisation: Empowering Business with Effective Insights — 07/2026</li>
  <li>NPTEL – Software Project Management — 10/2025</li>
  <li>Coursera – Android Development — 05/2025</li>
</ul>

</body>
</html>
"""

html_path = os.path.abspath(r"c:\dev\pro\Het_Joshi_Resume_MaintAI.html")
pdf_path = os.path.abspath(r"c:\dev\pro\Het_Joshi_Resume_MaintAI.pdf")
downloads_pdf_path = os.path.abspath(r"C:\Users\hetjo\Downloads\Het_Joshi_Resume_MaintAI.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={pdf_path}",
    "--no-pdf-header-footer",
    html_path
]

print("Rendering HTML to PDF with Edge...")
subprocess.run(cmd, check=True)

# Copy to Downloads as well
import shutil
shutil.copyfile(pdf_path, downloads_pdf_path)

# Verify page count
doc = fitz.open(pdf_path)
print(f"Generated PDF successfully! Page count: {len(doc)}")
for i, p in enumerate(doc):
    print(f"Page {i+1} rect: {p.rect}")
