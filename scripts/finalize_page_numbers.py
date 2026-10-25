import os
import shutil
import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
import win32com.client

OUTPUT_PRO_DOCX = r"C:\dev\pro\MaintAI_Final_Hard_Bound_Project_Report_Het_Joshi.docx"
OUTPUT_PRO_PDF = r"C:\dev\pro\MaintAI_Final_Hard_Bound_Project_Report_Het_Joshi.pdf"
OUTPUT_DL_DOCX = r"C:\Users\hetjo\Downloads\PPSU_Final_Hard_Bound_Project_Report_Het_Joshi.docx"
OUTPUT_DL_PDF = r"C:\Users\hetjo\Downloads\PPSU_Final_Hard_Bound_Project_Report_Het_Joshi.pdf"

print("Opening docx to inject exact page numbers into TOC, List of Figures, and List of Tables...")
doc = docx.Document(OUTPUT_PRO_DOCX)

def format_run(run, font_name="Cambria", font_size=9.0, bold=False, italic=False):
    if font_name:
        run.font.name = font_name
    if font_size:
        run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic

def set_cell(cell, text, bold=False, italic=False, font_name="Cambria", font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER):
    p = cell.paragraphs[0]
    p.text = ""
    p.alignment = align
    p.paragraph_format.space_before = Pt(2.0)
    p.paragraph_format.space_after = Pt(2.0)
    p.paragraph_format.line_spacing = 1.12
    run = p.add_run(text)
    format_run(run, font_name=font_name, font_size=font_size, bold=bold, italic=italic)

def set_para_text(p, text, font_name="Cambria", font_size=9.5, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=4):
    p.text = ""
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if text:
        r = p.add_run(text)
        format_run(r, font_name=font_name, font_size=font_size, bold=bold, italic=italic)

# Exact Discovered Page Numbers
PAGE_MAP = {
    # Preliminary Pages
    'Certificate': 'i',
    'Declaration': 'ii',
    'Acknowledgement': 'iii',
    'Abstract': 'iv',
    'Table of Contents': 'v',
    'List of Figures': 'vi',
    'List of Tables': 'vii',
    'List of Abbreviations': 'viii',

    # Chapters
    'Chapter 1': '12',
    '1.1': '12', '1.2': '12', '1.3': '13', '1.4': '13', '1.5': '13', '1.6': '13', '1.7': '14', '1.8': '14',

    'Chapter 2': '15',
    '2.1': '15', '2.2': '15', '2.3': '16', '2.4': '16', '2.5': '17', '2.6': '17', '2.7': '18',

    'Chapter 3': '18',
    '3.1': '18', '3.2': '19', '3.3': '19', '3.4': '20', '3.5': '20', '3.6': '21', '3.7': '21', '3.8': '21',

    'Chapter 4': '22',
    '4.1': '22', '4.2': '22', '4.3': '22', '4.4': '22', '4.5': '23', '4.6': '23', '4.7': '24',

    'Chapter 5': '25',
    '5.1': '25', '5.2': '26', '5.3': '27', '5.4': '28', '5.5': '28', '5.6': '28', '5.7': '28', '5.8': '28', '5.9': '29', '5.10': '29',

    'Chapter 6': '31',
    '6.1': '31', '6.2': '31', '6.3': '32', '6.4': '32', '6.5': '33', '6.6': '33', '6.7': '33',

    'Chapter 7': '33',
    '7.1': '33', '7.2': '34', '7.3': '34', '7.4': '35', '7.5': '36', '7.6': '36', '7.7': '36', '7.8': '37', '7.9': '37', '7.10': '37',

    'Chapter 8': '37',
    '8.1': '37', '8.2': '38', '8.3': '38', '8.4': '38', '8.5': '39', '8.6': '39', '8.7': '40', '8.8': '40', '8.9': '40', '8.10': '41',

    'Chapter 9': '41',
    '9.1': '41', '9.2': '41', '9.3': '42', '9.4': '42', '9.5': '43', '9.6': '44', '9.7': '44',

    'Chapter 10': '45',
    '10.1': '45', '10.2': '45', '10.3': '46', '10.4': '46', '10.5': '46', '10.6': '46',

    'Chapter 11': '47',
    '11.1': '47', '11.2': '47', '11.3': '48', '11.4': '48', '11.5': '48',

    'Chapter 12': '48',
    '12.1': '48', '12.2': '49', '12.3': '49', '12.4': '49', '12.5': '49', '12.6': '50', '12.7': '50',

    'Chapter 13': '50',
    '13.1': '50', '13.2': '51', '13.3': '51', '13.4': '51', '13.5': '51',

    'Chapter 14': '51',
    '14.1': '51', '14.2': '51', '14.3': '52', '14.4': '52',

    'Chapter 15': '53',
    '15.1': '53', '15.2': '53', '15.3': '53', '15.4': '53',

    # Appendices
    'Appendices': '54',
    'Appendix A': '54',
    'Appendix B': '54',
    'Appendix C': '54',
    'Appendix D': '54',
    'Appendix E': '54',
    'Appendix F': '55',
    'Appendix G': '55',
    'Appendix H': '56'
}

# Update Table 3 (Table of Contents)
toc = doc.tables[3]
print(f"Updating Table 3 (TOC) with {len(toc.rows)} rows...")

for idx, row in enumerate(toc.rows):
    if idx == 0:
        continue
    col0 = row.cells[0].text.strip()
    col1 = row.cells[1].text.strip()
    
    # Match by col0 (e.g. Chapter 1, 1.1) or col1 (e.g. Certificate)
    page_val = ""
    if col0 in PAGE_MAP:
        page_val = PAGE_MAP[col0]
    elif col1 in PAGE_MAP:
        page_val = PAGE_MAP[col1]

    if page_val:
        is_bold = col0.startswith('Chapter') or col0.startswith('Appendix') or col1 == 'Preliminary Pages' or col1 == 'Appendices'
        set_cell(row.cells[2], page_val, bold=is_bold, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)

# Update List of Figures (Paragraph 45)
print("Updating List of Figures...")
set_para_text(doc.paragraphs[45],
"Figure 4.1: Overall Project Workflow & Agile Engineering Lifecycle ................................. 23\n"
"Figure 5.1: Final 3-Tier System Architecture & Cloud Infrastructure ................................. 26\n"
"Figure 5.2: End-to-End Maintenance & AR Repair Process Flow ......................................... 27\n"
"Figure 5.3: Major UML Class & Relational Database Schema Diagram ............................... 29\n"
"Figure 5.4: Major Interface & UI Wireframe Navigation Hierarchy ...................................... 30\n"
"Figure 7.1: Module 1 — Live AR Step Guidance with Pulsing Canvas Markers .................... 34\n"
"Figure 7.2: Module 2 — Multimodal AI Computer Vision Tool Verification Modal .................. 35\n"
"Figure 7.3: Module 3 — Offline-First Write-Ahead Sync Pipeline Architecture ....................... 36\n"
"Figure 9.1: Final Output 1 — Machine Specifications & Procedure Selection ........................... 42\n"
"Figure 9.2: Final Output 2 — Live AR Step Guidance with Hands-Free Voice Control .................. 42\n"
"Figure 9.3: Final Output 3 — Spare Parts Inventory & Low Stock Tracking ............................. 43\n"
"Figure 9.4: Final Output 4 — Supervisor Maintenance Analytics & MTTR Tracking ................... 43\n"
"Figure 10.1: Live Field Demonstration & End-to-End Operational Workflow ........................... 46\n"
"Figure A.1: Supporting Evidence — Plant QR Code Batch Generator & Print Matrix ................... 54\n"
"Figure A.2: Supporting Evidence — Fault Reporting & Photo Evidence Upload .......................... 55",
font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=4)

# Update List of Tables (Paragraph 49)
print("Updating List of Tables...")
set_para_text(doc.paragraphs[49],
"Table 1.1: Scope Matrix — Included, Excluded, and Operational Constraints ..................... 13\n"
"Table 2.1: Literature Review & Existing Approaches .................................................... 15\n"
"Table 2.2: Comparative Analysis of Maintenance Approaches ................................... 17\n"
"Table 3.1: Functional Requirements Specification .................................................... 18\n"
"Table 3.2: Non-Functional Requirements Specification ............................................. 19\n"
"Table 3.3: Hardware Requirements & Test Environments ........................................... 19\n"
"Table 3.4: Software Requirements & Framework Libraries ......................................... 20\n"
"Table 3.5: System Constraints & Operational Assumptions ........................................... 21\n"
"Table 4.1: Project Phases and Key Engineering Deliverables ......................................... 24\n"
"Table 4.2: Progress Report Milestone Consolidation .................................................... 24\n"
"Table 4.3: Project Execution Schedule & 16-Week Timeline ........................................... 24\n"
"Table 5.1: Module-Wise Architectural Design ............................................................. 27\n"
"Table 5.2: Relational Database Schema Design ............................................................ 30\n"
"Table 6.1: Programming Languages ............................................................................ 31\n"
"Table 6.2: Frameworks, Libraries, and APIs ................................................................ 31\n"
"Table 6.3: Database and Storage Technologies .............................................................. 32\n"
"Table 6.4: APIs and Third-Party Services ..................................................................... 32\n"
"Table 6.5: Development Tools and IDE ...................................................................... 33\n"
"Table 7.1: API & External Service Integration Specifications ...................................... 36\n"
"Table 8.1: Unit & Module Testing Test Cases ............................................................. 38\n"
"Table 8.2: Integration Testing Specifications ............................................................. 38\n"
"Table 8.3: Functional Testing Specifications ............................................................. 38\n"
"Table 8.4: System Testing & End-to-End Scenarios .................................................... 39\n"
"Table 8.5: Performance Testing Benchmarks ................................................................ 39\n"
"Table 8.6: User Acceptance Testing Across Physical Devices ........................................ 40\n"
"Table 8.7: Experimental Validation Benchmarks ........................................................ 40\n"
"Table 8.8: Defects Identification and Resolution .......................................................... 41\n"
"Table 9.1: Quantitative Performance Metrics & MTTR Reductions ............................... 43\n"
"Table 9.2: Comparative Benchmark with Legacy Maintenance Systems ........................ 44\n"
"Table 9.3: Objective-Wise Achievement Matrix ............................................................. 44\n"
"Table 10.1: Production Deployment Environment & Configuration ............................... 45\n"
"Table 11.1: Major Engineering Challenges & Solutions ............................................... 47\n"
"Table 11.2: Improvements Made During Development .................................................... 48\n"
"Table 12.1: Individual Contribution Matrix (Het Joshi) ................................................ 49\n"
"Table 13.1: Current System Limitations & Boundary Factors ........................................... 50\n"
"Table 14.1: Final Project Status Matrix ..................................................................... 52\n"
"Table F.1: Repository Structure & Core Modules .......................................................... 55\n"
"Table B.1: Final Hard-Bound Submission Checklist .................................................... 56",
font_size=9.0, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=4)

print("Saving updated docx...")
doc.save(OUTPUT_PRO_DOCX)
print("DOCX updated successfully!")

# Export to PDF via clean Word COM
print("Exporting finalized PDF via Microsoft Word...")
word = win32com.client.DispatchEx("Word.Application")
word.Visible = False
word.DisplayAlerts = False

try:
    doc_word = word.Documents.Open(os.path.abspath(OUTPUT_PRO_DOCX), ReadOnly=True)
    doc_word.SaveAs(os.path.abspath(OUTPUT_PRO_PDF), FileFormat=17) # 17 = wdFormatPDF
    doc_word.Close(SaveChanges=False)
    print(f"Final PDF exported successfully: {OUTPUT_PRO_PDF}")
finally:
    word.Quit()

# Copy to Downloads
try:
    shutil.copy2(OUTPUT_PRO_DOCX, OUTPUT_DL_DOCX)
    shutil.copy2(OUTPUT_PRO_PDF, OUTPUT_DL_PDF)
    print("Files successfully copied to Downloads folder!")
except Exception as e:
    print(f"Downloads copy notice: {e}")

print("ALL FINAL HARDBOUND DELIVERABLES COMPLETED PERFECTLY!")
