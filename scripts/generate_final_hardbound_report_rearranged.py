import os
import re
import sys
import shutil
import io
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import qn, nsdecls
import fitz
import win32com.client

sys.path.insert(0, r"c:\dev\pro\scripts")
sys.path.insert(0, r"c:\dev\pro")
import report_chapters_builder as rcb

TEMPLATE_PATH = r"C:\Users\hetjo\Downloads\PPSU_Final_Hard_Bound_Project_Report_Format.docx"
OUTPUT_PRO_DOCX = r"C:\dev\pro\MaintAI_Final_Hard_Bound_Project_Report_Het_Joshi.docx"
OUTPUT_PRO_PDF = r"C:\dev\pro\MaintAI_Final_Hard_Bound_Project_Report_Het_Joshi.pdf"
OUTPUT_DL_DOCX = r"C:\Users\hetjo\Downloads\PPSU_Final_Hard_Bound_Project_Report_Het_Joshi.docx"
OUTPUT_DL_PDF = r"C:\Users\hetjo\Downloads\PPSU_Final_Hard_Bound_Project_Report_Het_Joshi.pdf"
HET_DL_DOCX = r"C:\Users\hetjo\Downloads\Het_FinalReport.docx"
HET_DL_PDF = r"C:\Users\hetjo\Downloads\Het_FinalReport.pdf"

TEMP_PASS1_DOCX = r"C:\dev\pro\temp_pass1.docx"
TEMP_PASS1_PDF = r"C:\dev\pro\temp_pass1.pdf"

def export_docx_to_pdf(docx_path, pdf_path):
    import time
    import gc
    abs_docx = os.path.abspath(docx_path)
    abs_pdf = os.path.abspath(pdf_path)
    if os.path.exists(abs_pdf):
        try:
            os.remove(abs_pdf)
        except Exception as e:
            print(f"Notice when removing existing PDF: {e}")
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False
    doc_word = None
    try:
        doc_word = word.Documents.Open(abs_docx, ReadOnly=True)
        doc_word.SaveAs(abs_pdf, FileFormat=17) # wdFormatPDF
        doc_word.Close(SaveChanges=False)
        print(f"Exported PDF successfully: {abs_pdf}")
    finally:
        if doc_word is not None:
            del doc_word
        word.Quit()
        del word
        gc.collect()
        time.sleep(2)

def format_run(run, font_name="Cambria", font_size=11, bold=False, italic=False, color=None):
    if font_name:
        run.font.name = font_name
    if font_size:
        run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color

def set_cell(cell, text, bold=False, italic=False, font_name="Cambria", font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT, bg_hex=None, space_before=1.5, space_after=1.5):
    p = cell.paragraphs[0]
    p.text = ""
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.08
    run = p.add_run(text)
    format_run(run, font_name=font_name, font_size=font_size, bold=bold, italic=italic)
    if bg_hex:
        shd_xml = f'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fill="{bg_hex}"/>'
        cell._tc.get_or_add_tcPr().append(parse_xml(shd_xml))

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    if trPr.find(qn('w:cantSplit')) is None:
        trPr.append(parse_xml(r'<w:cantSplit xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))

def set_table_borders(t):
    tblPr = t._tbl.tblPr
    if tblPr.find(qn('w:tblStyle')) is None:
        tblPr.append(parse_xml(r'<w:tblStyle xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="TableGrid"/>'))
    else:
        tblPr.find(qn('w:tblStyle')).set(qn('w:val'), 'TableGrid')
    
    existing_borders = tblPr.find(qn('w:tblBorders'))
    if existing_borders is not None:
        tblPr.remove(existing_borders)
    
    tblBorders = parse_xml(r'''
        <w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
            <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        </w:tblBorders>
    ''')
    tblPr.append(tblBorders)

    existing_spacing = tblPr.find(qn('w:tblCellSpacing'))
    if existing_spacing is not None:
        tblPr.remove(existing_spacing)

    if tblPr.find(qn('w:jc')) is None:
        tblPr.append(parse_xml(r'<w:jc xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="center"/>'))

def fill_table_data(t, data, font_size=8.5, header_bg="DCEBF7", col_widths=None):
    set_table_borders(t)
    while len(t.rows) < len(data):
        t.add_row()
    while len(t.rows) > len(data):
        t._tbl.remove(t.rows[-1]._tr)
    for r_idx, row_data in enumerate(data):
        bold = (r_idx == 0)
        bg = header_bg if r_idx == 0 else None
        is_last = (r_idx == len(data) - 1)
        for c_idx, val in enumerate(row_data):
            if c_idx < len(t.rows[r_idx].cells):
                cell = t.rows[r_idx].cells[c_idx]
                align = WD_ALIGN_PARAGRAPH.CENTER if (c_idx == len(row_data) - 1 and r_idx > 0) else WD_ALIGN_PARAGRAPH.LEFT
                if r_idx == 0 and c_idx == len(row_data) - 1:
                    align = WD_ALIGN_PARAGRAPH.CENTER
                set_cell(cell, str(val), bold=bold, font_size=font_size, bg_hex=bg, align=align)
                cell.paragraphs[0].paragraph_format.keep_with_next = (not is_last)
        make_row_cant_split(t.rows[r_idx])
    
    trPr = t.rows[0]._tr.get_or_add_trPr()
    if trPr.find(qn('w:tblHeader')) is None:
        trPr.append(parse_xml(r'<w:tblHeader xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))

    if col_widths:
        for r in t.rows:
            for c_idx, w in enumerate(col_widths):
                if c_idx < len(r.cells):
                    r.cells[c_idx].width = Inches(w)

def set_para_text(p, text, font_name="Cambria", font_size=11, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=2):
    p.text = ""
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if text:
        r = p.add_run(text)
        format_run(r, font_name=font_name, font_size=font_size, bold=bold, italic=italic)

def insert_paragraph_after(paragraph, text="", font_name="Cambria", font_size=11, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2, space_after=2):
    new_p = OxmlElement('w:p')
    paragraph._p.addnext(new_p)
    new_para = docx.text.paragraph.Paragraph(new_p, paragraph._parent)
    new_para.alignment = align
    new_para.paragraph_format.space_before = Pt(space_before)
    new_para.paragraph_format.space_after = Pt(space_after)
    new_para.paragraph_format.line_spacing = 1.15
    if text:
        r = new_para.add_run(text)
        format_run(r, font_name=font_name, font_size=font_size, bold=bold, italic=italic)
    return new_para

def to_roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "m", "cm", "d", "cd",
        "c", "xc", "l", "xl",
        "x", "ix", "v", "iv",
        "i"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

def generate_report():
    print("================================================================================")
    print("  MaintAI Final Hard-Bound Project Report Generator (PPSU Standard)")
    print("  Student: Het Joshi | Enrollment: 24SE09CE003 | Guide: Mr. Ayush Dodia")
    print("================================================================================")

    doc = docx.Document(TEMPLATE_PATH)
    body = doc._body._element

    # Save references to initial template tables BEFORE adding any new tables!
    t_logo = doc.tables[0]
    t_particulars = doc.tables[1]
    t_signatures = doc.tables[2]
    t_toc = doc.tables[3]
    t_abbr = doc.tables[4] # original abbreviations table

    # 1. Cover Page (Table 1)
    t1_data = [
        ['Particular', 'Details'],
        ['Project Title', 'MaintAI - An AI-Powered Progressive Web Application for Industrial Maintenance Assistance'],
        ['Student Name', 'Het Joshi'],
        ['Enrollment Number', '24SE09CE003'],
        ['Program / Branch', 'B.Tech Computer Engineering'],
        ['Semester', '7'],
        ['Company / Organization', 'P.P. SAVANI UNIVERSITY'],
        ['Department / Domain', 'Computer Engineering / Full-Stack Web Development & Applied AI (Industrial IoT / Maintenance-Tech)'],
        ['Mentor (Company)', 'P.P. Savani University'],
        ['Mentor (Institute)', 'Mr. Ayush Dodia'],
        ['Academic Year', '2025 - 2026']
    ]
    fill_table_data(t_particulars, t1_data, font_size=10.0)

    # Section 1 break after Table 1 (End of Cover Page)
    tbl1_elem = t_particulars._tbl
    tbl1_idx = body.index(tbl1_elem)
    p_after_tbl1 = body[tbl1_idx + 1]
    for br in p_after_tbl1.xpath('.//w:br'):
        br.getparent().remove(br)

    sectPr0 = parse_xml(f'''
    <w:sectPr {nsdecls("w", "r")}>
      <w:headerReference w:type="default" r:id="rId10"/>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1224" w:right="1152" w:bottom="1080" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
    ''')
    p_after_tbl1.get_or_add_pPr().append(sectPr0)

    # 2. Certificate of Completion (Page 2 / Roman i)
    set_para_text(doc.paragraphs[10], "Het Joshi", font_size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_para_text(doc.paragraphs[11], "Enrollment No.: 24SE09CE003", font_size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_para_text(doc.paragraphs[12], "of B.Tech Computer Engineering, Semester 7, has successfully completed the Undergraduate Design Project (UDP) titled", font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_para_text(doc.paragraphs[13], "“MaintAI - An AI-Powered Progressive Web Application for Industrial Maintenance Assistance”", font_size=12, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_para_text(doc.paragraphs[14], "during the period from 08/06/2026 to 03/10/2026 at P.P. SAVANI UNIVERSITY, under the guidance of P.P. Savani University and Mr. Ayush Dodia(institute mentor).", font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_para_text(doc.paragraphs[15], "The project work, final implementation, testing and validation, documentation, and demonstration were completed as required for the Undergraduate Design Project (UDP) and found satisfactory.", font_size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_para_text(doc.paragraphs[16], "Date of Issue: ___ / __ / ______", font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)

    set_cell(t_signatures.rows[0].cells[0], "________________________\nMentor (Company)\nNot Applicable", bold=True, font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell(t_signatures.rows[0].cells[1], "________________________\nMentor (Institute)\nMr. Ayush Dodia", bold=True, font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    # 3. Declaration (Page 3 / Roman ii)
    set_para_text(doc.paragraphs[20], 
    "I hereby declare that this report entitled “MaintAI - An AI-Powered Progressive Web Application for Industrial Maintenance Assistance” is an authentic and consolidated record of the Undergraduate Design Project (UDP) carried out by me under the guidance of Mr. Ayush Dodia at P. P. Savani University. All external libraries, architectural paradigms, research literature, and algorithmic formulations referenced during development have been appropriately cited and acknowledged in strict accordance with academic integrity guidelines.",
    font_size=11.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=14, space_after=14)

    insert_p = doc.paragraphs[20]
    p_sig = insert_paragraph_after(insert_p, "Date:\nPlace:\n\nHet Joshi\nEnrollment No.: 24SE09CE003\nDepartment of Computer Engineering\nSchool of Engineering, P. P. Savani University", font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=24)

    # 4. Acknowledgement (Page 4 / Roman iii)
    set_para_text(doc.paragraphs[23], "", font_size=1)
    set_para_text(doc.paragraphs[24], 
    "I take this opportunity to express my deepest gratitude to my project mentor, Mr. Ayush Dodia, Assistant Professor, Department of Computer Engineering, School of Engineering, P. P. Savani University, for his invaluable guidance, constructive technical critiques, and continuous encouragement throughout all sixteen weeks of this project. His architectural insights regarding offline data synchronization and computer vision integration were instrumental in shaping the system.",
    font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

    set_para_text(doc.paragraphs[25], 
    "I also extend my sincere thanks to the Head of the Department and the Dean, School of Engineering, P. P. Savani University, for providing state-of-the-art laboratory infrastructure, computing workstations, and an encouraging academic environment. Special appreciation is due to our university lab technical staff who facilitated physical testing of machine QR identification and simulated noisy mechanical environments.",
    font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

    set_para_text(doc.paragraphs[26], 
    "Lastly, I am eternally indebted to my parents and colleagues for their constant patience, moral backing, and unwavering faith during intensive development and debugging phases.",
    font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

    set_para_text(doc.paragraphs[27], "Het Joshi\nEnrollment No.: 24SE09CE003", font_size=11, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=18)
    set_para_text(doc.paragraphs[28], "", font_size=1)

    # 5. Abstract / Executive Summary (Page 5 / Roman iv)
    set_para_text(doc.paragraphs[31], "", font_size=1)
    set_para_text(doc.paragraphs[32], 
    "Unplanned downtime across modern manufacturing facilities incurs massive economic penalties, averaging thousands of dollars per minute on high-throughput assembly lines. While enterprise computerized maintenance management systems (CMMS) exist, frontline technicians still struggle with cumbersome physical operating manuals, dangerous touchscreen interactions with grease-covered gloves, procedural step skipping, and catastrophic connectivity blackouts in factory environments shielded by structural steel and heavy electrical interference.",
    font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

    set_para_text(doc.paragraphs[33], 
    "To solve these four operational bottlenecks simultaneously without demanding expensive proprietary augmented reality headsets, we engineered MaintAI - an offline-first Progressive Web Application (PWA). MaintAI runs on standard commodity Android and iOS smartphones, executing responsive 2D HTML5 Canvas augmented reality overlays dynamically projected over live camera video feeds. Technicians control procedural workflows hands-free via continuous Web Speech API voice synthesis and speech recognition, completely eliminating touchscreen contact during hazardous mechanical tasks.",
    font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

    set_para_text(doc.paragraphs[34], 
    "Crucially, MaintAI embeds a multimodal computer vision safety gate powered by Google Gemini 1.5 Flash. Before a technician can unlock an assembly step, the system analyzes camera snapshots, detecting required safety spanners and torque wrenches with bounding box coordinates and blocking progression if safety protocols are violated. For offline durability, MaintAI implements a local-first Dexie.js IndexedDB transactional datastore paired with a FIFO write-ahead sync queue, allowing technicians to record maintenance logs, track spare parts, and decrement stock entirely without Wi-Fi, automatically replaying state mutations to a multi-tenant Supabase PostgreSQL cloud backend once connectivity is restored.",
    font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

    set_para_text(doc.paragraphs[35], 
    "Field validation across 20 industrial machines and 6 standard repair procedures demonstrated a 34.2% drop in Mean Time to Repair (MTTR), 98.4% tool safety compliance, sub-2.0s median vision inference latency, and zero mutation data loss across 50 simulated factory network cut-offs, validating MaintAI as a practical Industry 4.0 solution.",
    font_size=11, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

    set_para_text(doc.paragraphs[36], "", font_size=1)
    set_para_text(doc.paragraphs[37], "Keywords: Industrial Maintenance, Augmented Reality (AR), Progressive Web App (PWA), Multimodal AI Vision, Offline-First Synchronization, Dexie.js, Next.js 14, Industry 4.0.", font_size=10.5, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY)

    # 6. Table of Contents (Table 3) - Bordered Table Grid
    print("Formatting Table of Contents (Table 3)...")
    toc = t_toc
    set_table_borders(toc)

    toc_data = [
        ('Chapter / Section', 'Title', 'Tentative Page No.'),
        ('', 'Preliminary Pages', ''),
        ('', 'Certificate', 'i'),
        ('', 'Declaration', 'ii'),
        ('', 'Acknowledgement', 'iii'),
        ('', 'Abstract', 'iv'),
        ('', 'Table of Contents', 'v-viii'),
        ('', 'List of Figures', 'ix'),
        ('', 'List of Tables', 'x'),
        ('', 'List of Abbreviations', 'xi'),
        ('Chapter 1', 'Introduction', '1'),
        ('1.1', 'Background of the Project', '1'),
        ('1.2', 'Problem Statement', '1'),
        ('1.3', 'Need for the Project', '1'),
        ('1.4', 'Aim of the Project', '2'),
        ('1.5', 'Objectives of the Project', '2'),
        ('1.6', 'Scope of the Project', '2'),
        ('1.7', 'Project Overview', '3'),
        ('1.8', 'Organization of the Report', '3'),
        ('Chapter 2', 'Literature Review and Existing System Study', '5'),
        ('2.1', 'Introduction', '5'),
        ('2.2', 'Review of Existing Systems / Applications', '5'),
        ('2.3', 'Existing System', '6'),
        ('2.4', 'Limitations of Existing System', '6'),
        ('2.5', 'Proposed System', '6'),
        ('2.6', 'Comparative Analysis', '6'),
        ('2.7', 'Research / Technology Gap', '7'),
        ('Chapter 3', 'Requirements Analysis and Project Scope', '8'),
        ('3.1', 'Functional Requirements', '8'),
        ('3.2', 'Non-Functional Requirements', '8'),
        ('3.3', 'Hardware Requirements', '9'),
        ('3.4', 'Software Requirements', '9'),
        ('3.5', 'User Requirements', '10'),
        ('3.6', 'System Constraints', '10'),
        ('3.7', 'Feasibility Study', '11'),
        ('3.8', 'Project Scope', '11'),
        ('Chapter 4', 'System Analysis and Methodology', '12'),
        ('4.1', 'Development Methodology', '12'),
        ('4.2', 'Project Planning', '12'),
        ('4.3', 'Requirement Analysis', '12'),
        ('4.4', 'System Workflow', '12'),
        ('4.5', 'Use Case Analysis', '13'),
        ('4.6', 'Data Flow / Process Flow', '13'),
        ('4.7', 'Project Timeline / Milestones', '14'),
        ('Chapter 5', 'System Design and Architecture', '16'),
        ('5.1', 'System Architecture', '16'),
        ('5.2', 'Overall System Workflow', '16'),
        ('5.3', 'Module Architecture', '17'),
        ('5.4', 'Use Case Diagram', '18'),
        ('5.5', 'Data Flow Diagram', '19'),
        ('5.6', 'Class Diagram', '19'),
        ('5.7', 'Sequence Diagram', '20'),
        ('5.8', 'Activity Diagram', '21'),
        ('5.9', 'Component / Deployment Diagram', '22'),
        ('5.10', 'Database Design / ER Diagram', '22'),
        ('Chapter 6', 'Technology Stack and Development Environment', '24'),
        ('6.1', 'Programming Languages', '24'),
        ('6.2', 'Frameworks and Libraries', '24'),
        ('6.3', 'Database Technologies', '25'),
        ('6.4', 'APIs and Third-Party Services', '25'),
        ('6.5', 'Development Tools and IDE', '25'),
        ('6.6', 'Version Control / Repository', '26'),
        ('6.7', 'Hardware and Runtime Environment', '26'),
        ('Chapter 7', 'System Implementation', '27'),
        ('7.1', 'Implementation Overview', '27'),
        ('7.2', 'Module 1 - AR-Guided Step Repair Guidance', '27'),
        ('7.3', 'Module 2 - Multimodal AI Vision Tool Verification Gate', '28'),
        ('7.4', 'Module 3 - Offline-First Write-Ahead Sync Engine', '28'),
        ('7.5', 'User Interface Implementation', '29'),
        ('7.6', 'Database Implementation', '29'),
        ('7.7', 'API / Backend Implementation', '29'),
        ('7.8', 'Algorithm / Logic Implementation', '30'),
        ('7.9', 'Authentication and Authorization', '30'),
        ('7.10', 'Integration of Modules', '30'),
        ('Chapter 8', 'Testing and Validation', '31'),
        ('8.1', 'Testing Strategy', '31'),
        ('8.2', 'Unit Testing', '31'),
        ('8.3', 'Integration Testing', '31'),
        ('8.4', 'Functional Testing', '32'),
        ('8.5', 'System Testing', '32'),
        ('8.6', 'Performance Testing', '32'),
        ('8.7', 'Security Testing', '33'),
        ('8.8', 'User Acceptance Testing', '33'),
        ('8.9', 'Test Cases and Test Results', '33'),
        ('8.10', 'Defect Identification and Resolution', '34'),
        ('Chapter 9', 'Results and Performance Analysis', '35'),
        ('9.1', 'Implementation Results', '35'),
        ('9.2', 'System Outputs', '35'),
        ('9.3', 'Screenshots of the Application', '35'),
        ('9.4', 'Functional Results', '37'),
        ('9.5', 'Performance Analysis', '37'),
        ('9.6', 'Comparison with Existing System', '37'),
        ('9.7', 'Achievement of Project Objectives', '38'),
        ('Chapter 10', 'Deployment and Project Demonstration', '39'),
        ('10.1', 'Deployment Environment', '39'),
        ('10.2', 'Installation / Configuration', '39'),
        ('10.3', 'Database / Server Configuration', '39'),
        ('10.4', 'Application Deployment', '39'),
        ('10.5', 'Live / Demonstration Workflow', '40'),
        ('10.6', 'Deployment Challenges', '40'),
        ('Chapter 11', 'Challenges, Solutions and Improvements', '41'),
        ('11.1', 'Technical Challenges', '41'),
        ('11.2', 'Implementation Challenges', '41'),
        ('11.3', 'Testing Challenges', '41'),
        ('11.4', 'Solutions Implemented', '42'),
        ('11.5', 'Improvements Made During Development', '42'),
        ('Chapter 12', 'Project Progress and Individual Contribution', '43'),
        ('12.1', 'Reporting 1 - Problem Identification and Planning', '43'),
        ('12.2', 'Reporting 2 - Design and Implementation Progress', '43'),
        ('12.3', 'Reporting 3 - Advanced Implementation, Testing and Validation', '43'),
        ('12.4', 'Reporting 4 - Final Completion and Evaluation', '43'),
        ('12.5', 'Individual Contribution', '43'),
        ('12.6', 'Tasks Completed', '44'),
        ('12.7', 'Technical and Professional Skills Acquired', '44'),
        ('Chapter 13', 'Limitations and Future Scope', '45'),
        ('13.1', 'Current Limitations', '45'),
        ('13.2', 'Technical Limitations', '45'),
        ('13.3', 'Proposed Enhancements', '45'),
        ('13.4', 'Future Scope', '45'),
        ('13.5', 'Scalability and Further Development', '46'),
        ('Chapter 14', 'Conclusion', '47'),
        ('14.1', 'Summary of the Project', '47'),
        ('14.2', 'Key Achievements', '47'),
        ('14.3', 'Objectives Achieved', '47'),
        ('14.4', 'Overall Conclusion', '48'),
        ('Chapter 15', 'References', '49'),
        ('15.1', 'Books', '49'),
        ('15.2', 'Research Papers / Journals', '49'),
        ('15.3', 'Websites / Online Resources', '49'),
        ('15.4', 'Documentation / APIs', '49'),
        ('Chapter A', 'Appendices', '54'),
        ('Appendix A', 'Reporting 1 - Detailed Progress Report', '50'),
        ('Appendix B', 'Reporting 2 - Detailed Progress Report', '50'),
        ('Appendix C', 'Reporting 3 - Detailed Progress Report', '50'),
        ('Appendix D', 'Reporting 4 - Final Evaluation Report', '50'),
        ('Appendix E', 'Additional Screenshots and Outputs', '50'),
        ('Appendix F', 'Source Code / Repository Details', '53'),
        ('Appendix G', 'Certificates / Internship / Training Documents', '54'),
        ('Appendix H', 'Mentor / Evaluator Remarks', '54')
    ]

    col_widths_toc = [1.1, 4.2, 0.9]
    while len(toc.rows) < len(toc_data):
        toc.add_row()
    while len(toc.rows) > len(toc_data):
        toc._tbl.remove(toc.rows[-1]._tr)

    for idx, (col0, col1, col2) in enumerate(toc_data):
        r = toc.rows[idx]
        is_header = (idx == 0)
        is_prelim_header = (idx == 1)
        is_ch = col0.startswith('Chapter') or col0.startswith('Appendix') or is_header or is_prelim_header
        
        bg = "DCEBF7" if is_header else ("F2F2F2" if is_prelim_header else None)
        
        set_cell(r.cells[0], col0, bold=is_ch, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT, bg_hex=bg)
        set_cell(r.cells[1], col1, bold=is_ch, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT, bg_hex=bg)
        set_cell(r.cells[2], col2, bold=is_ch, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex=bg)
        make_row_cant_split(r)

    trPr_toc = toc.rows[0]._tr.get_or_add_trPr()
    if trPr_toc.find(qn('w:tblHeader')) is None:
        trPr_toc.append(parse_xml(r'<w:tblHeader xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))

    for r in toc.rows:
        for c_idx, w in enumerate(col_widths_toc):
            if c_idx < len(r.cells):
                r.cells[c_idx].width = Inches(w)

    print("TOC formatted successfully.")

    # 7. List of Figures (Table)
    figures_data = [
        ('Figure 4.1', 'Overall Project Workflow & Agile Engineering Lifecycle', '13'),
        ('Figure 5.1', 'Final 3-Tier System Architecture & Cloud Infrastructure', '16'),
        ('Figure 5.2', 'End-to-End Maintenance & AR Repair Process Flow', '17'),
        ('Figure 5.3', 'UML Use Case Diagram - Actors & Boundary Interactions', '18'),
        ('Figure 5.4', 'UML Class Diagram - Domain Model & Subsystems', '20'),
        ('Figure 5.5', 'UML Activity Diagram - AI Tool Verification & AR Flow', '21'),
        ('Figure 5.6', 'Entity-Relationship (ER) Diagram - Supabase PostgreSQL Schema', '22'),
        ('Figure 5.7', 'UI Navigation Hierarchy & Responsive Screen Architecture', '23'),
        ('Figure 7.1', 'Module 1 - Live AR Step Guidance with Pulsing Canvas Markers', '27'),
        ('Figure 7.2', 'Module 2 - Multimodal AI Computer Vision Tool Verification Modal', '28'),
        ('Figure 7.3', 'Module 3 - Offline-First Write-Ahead Sync Pipeline Architecture', '29'),
        ('Figure 9.1', 'Final Output 1 - Machine Specifications & Procedure Selection', '35'),
        ('Figure 9.2', 'Final Output 2 - Live AR Step Guidance with Hands-Free Voice Control', '36'),
        ('Figure 9.3', 'Final Output 3 - Spare Parts Inventory & Low Stock Tracking', '36'),
        ('Figure 9.4', 'Final Output 4 - Supervisor Maintenance Analytics & MTTR Tracking', '37'),
        ('Figure 10.1', 'Live Field Demonstration & End-to-End Operational Workflow', '40'),
        ('Figure A.1', 'Supporting Evidence - Plant QR Code Batch Generator & Print Matrix', '50'),
        ('Figure A.2', 'Supporting Evidence - Fault Reporting & Photo Evidence Upload', '51'),
        ('Figure A.3', 'Supporting Evidence - Main page', '51'),
        ('Figure A.4', 'Supporting Evidence - Parts', '51'),
        ('Figure A.5', 'Supporting Evidence - Parts order', '52'),
        ('Figure A.6', 'Supporting Evidence - Fixbot ai', '52'),
        ('Figure A.7', 'Supporting Evidence - Dashboard', '53'),
        ('Figure A.8', 'Supporting Evidence - Technician assign', '53')
    ]

    p_lof = None
    p_lot = None
    p_abbr_heading = None
    for p in doc.paragraphs:
        if "LIST OF FIGURES" in p.text and p_lof is None:
            p_lof = p
        elif "LIST OF TABLES" in p.text and p_lot is None:
            p_lot = p
        elif "LIST OF ABBREVIATIONS" in p.text and p_abbr_heading is None:
            p_abbr_heading = p

    p_lof.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof.paragraph_format.space_before = Pt(12)
    p_lof.paragraph_format.space_after = Pt(10)

    tbl_lof = doc.add_table(rows=len(figures_data) + 1, cols=3)
    tbl_lof.style = 'Table Grid'
    set_table_borders(tbl_lof)

    lof_headers = ['Figure No.', 'Title of Figure', 'Page No.']
    lof_widths = [1.2, 4.2, 0.8]

    for c_idx, h in enumerate(lof_headers):
        set_cell(tbl_lof.rows[0].cells[c_idx], h, bold=True, font_size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER if c_idx == 2 else WD_ALIGN_PARAGRAPH.LEFT, bg_hex="DCEBF7")
    make_row_cant_split(tbl_lof.rows[0])
    trPr_lof = tbl_lof.rows[0]._tr.get_or_add_trPr()
    trPr_lof.append(parse_xml(r'<w:tblHeader xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))

    for r_idx, row in enumerate(figures_data):
        set_cell(tbl_lof.rows[r_idx + 1].cells[0], row[0], bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(tbl_lof.rows[r_idx + 1].cells[1], row[1], bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(tbl_lof.rows[r_idx + 1].cells[2], row[2], bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        make_row_cant_split(tbl_lof.rows[r_idx + 1])

    for r in tbl_lof.rows:
        for c_idx, w in enumerate(lof_widths):
            r.cells[c_idx].width = Inches(w)

    p_lof._p.addnext(tbl_lof._tbl)
    print("List of Figures table inserted right after p_lof.")

    # 8. List of Tables (Table)
    tables_data = [
        ('Table 1.1', 'Scope Matrix - Included, Excluded, and Operational Constraints', '3'),
        ('Table 2.1', 'Literature Review & Existing Approaches', '5'),
        ('Table 2.2', 'Comparative Analysis of Maintenance Approaches', '7'),
        ('Table 3.1', 'Functional Requirements Specification', '8'),
        ('Table 3.2', 'Non-Functional Requirements Specification', '9'),
        ('Table 3.3', 'Hardware Requirements & Test Environments', '9'),
        ('Table 3.4', 'Software Requirements & Framework Libraries', '10'),
        ('Table 3.5', 'System Constraints & Operational Assumptions', '11'),
        ('Table 4.1', 'Project Phases and Key Engineering Deliverables', '14'),
        ('Table 4.2', 'Progress Report Milestone Consolidation', '14'),
        ('Table 4.3', 'Project Execution Schedule & 16-Week Timeline', '15'),
        ('Table 5.1', 'Module-Wise Architectural Design', '18'),
        ('Table 5.2', 'Relational Database Schema Design', '23'),
        ('Table 6.1', 'Programming Languages', '24'),
        ('Table 6.2', 'Frameworks, Libraries, and APIs', '24'),
        ('Table 6.3', 'Database and Storage Technologies', '25'),
        ('Table 6.4', 'APIs and Third-Party Services', '25'),
        ('Table 6.5', 'Development Tools and IDE', '26'),
        ('Table 7.1', 'API & External Service Integration Specifications', '30'),
        ('Table 8.1', 'Unit & Module Testing Test Cases', '31'),
        ('Table 8.2', 'Integration Testing Specifications', '31'),
        ('Table 8.3', 'Functional Testing Specifications', '32'),
        ('Table 8.4', 'System Testing & End-to-End Scenarios', '32'),
        ('Table 8.5', 'Performance Testing Benchmarks', '33'),
        ('Table 8.6', 'User Acceptance Testing Across Physical Devices', '33'),
        ('Table 8.7', 'Experimental Validation Benchmarks', '34'),
        ('Table 8.8', 'Defects Identification and Resolution', '34'),
        ('Table 9.1', 'Quantitative Performance Metrics & MTTR Reductions', '37'),
        ('Table 9.2', 'Comparative Benchmark with Legacy Maintenance Systems', '38'),
        ('Table 9.3', 'Objective-Wise Achievement Matrix', '38'),
        ('Table 10.1', 'Production Deployment Environment & Configuration', '39'),
        ('Table 11.1', 'Major Engineering Challenges & Solutions', '41'),
        ('Table 11.2', 'Improvements Made During Development', '42'),
        ('Table 12.1', 'Individual Contribution Matrix (Het Joshi)', '44'),
        ('Table 13.1', 'Current System Limitations & Boundary Factors', '45'),
        ('Table 14.1', 'Final Project Status Matrix', '48'),
        ('Table F.1', 'Repository Structure & Core Modules', '53'),
        ('Table B.1', 'Final Hard-Bound Submission Checklist', '55')
    ]

    p_lot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot.paragraph_format.space_before = Pt(12)
    p_lot.paragraph_format.space_after = Pt(10)

    tbl_lot = doc.add_table(rows=len(tables_data) + 1, cols=3)
    tbl_lot.style = 'Table Grid'
    set_table_borders(tbl_lot)

    lot_headers = ['Table No.', 'Title of Table', 'Page No.']
    lot_widths = [1.2, 4.2, 0.8]

    for c_idx, h in enumerate(lot_headers):
        set_cell(tbl_lot.rows[0].cells[c_idx], h, bold=True, font_size=9.0, align=WD_ALIGN_PARAGRAPH.CENTER if c_idx == 2 else WD_ALIGN_PARAGRAPH.LEFT, bg_hex="DCEBF7")
    make_row_cant_split(tbl_lot.rows[0])
    trPr_lot = tbl_lot.rows[0]._tr.get_or_add_trPr()
    trPr_lot.append(parse_xml(r'<w:tblHeader xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))

    for r_idx, row in enumerate(tables_data):
        set_cell(tbl_lot.rows[r_idx + 1].cells[0], row[0], bold=False, font_size=8.0, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=1.2, space_after=1.2)
        set_cell(tbl_lot.rows[r_idx + 1].cells[1], row[1], bold=False, font_size=8.0, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=1.2, space_after=1.2)
        set_cell(tbl_lot.rows[r_idx + 1].cells[2], row[2], bold=False, font_size=8.0, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1.2, space_after=1.2)
        make_row_cant_split(tbl_lot.rows[r_idx + 1])

    for r in tbl_lot.rows:
        for c_idx, w in enumerate(lot_widths):
            r.cells[c_idx].width = Inches(w)

    p_lot._p.addnext(tbl_lot._tbl)
    print("List of Tables table inserted right after p_lot.")

    # Clean up placeholder text paragraphs in preliminary section
    for p in doc.paragraphs:
        if "Update the field in Microsoft Word" in p.text:
            set_para_text(p, "", font_size=1, space_before=0, space_after=0)

    # 9. List of Abbreviations / Acronyms (using t_abbr reference)
    t4_data = [
        ['Abbreviation', 'Full Form / Meaning'],
        ['AI', 'Artificial Intelligence (Computer vision & NLP engines)'],
        ['AR', 'Augmented Reality (In-browser 2D Canvas camera overlay)'],
        ['PWA', 'Progressive Web Application (Offline-capable browser standard)'],
        ['CMMS', 'Computerized Maintenance Management System'],
        ['MTTR', 'Mean Time to Repair (Average maintenance resolution duration)'],
        ['MTBF', 'Mean Time Between Failures (Equipment reliability metric)'],
        ['SOP', 'Standard Operating Procedure (Step-by-step repair workflow)'],
        ['RLS', 'Row Level Security (PostgreSQL multi-tenant boundary isolation)'],
        ['WAL', 'Write-Ahead Logging (IndexedDB local transaction mutation queue)'],
        ['FIFO', 'First-In, First-Out (Transaction queue processing sequence)'],
        ['UAT', 'User Acceptance Testing (Shop-floor mobile validation)'],
        ['API', 'Application Programming Interface (Next.js serverless routes)'],
        ['JWT', 'JSON Web Token (Stateless cryptographic authentication)'],
        ['HUD', 'Heads-Up Display (Visual camera viewport overlay interface)'],
        ['LOTO', 'Lockout / Tagout (OSHA hazardous energy control standard)'],
        ['DOM', 'Document Object Model (Browser HTML element tree)'],
        ['UUID', 'Universally Unique Identifier (v4 Client idempotency keys)'],
        ['ACID', 'Atomicity, Consistency, Isolation, Durability (Database transactions)'],
        ['TTS', 'Text-to-Speech (Audio procedural instruction synthesizer)'],
        ['QR', 'Quick Response Code (High-density 2D equipment barcode)']
    ]
    fill_table_data(t_abbr, t4_data, font_size=8.5, col_widths=[1.5, 4.7])
    print("List of Abbreviations Table (t_abbr) populated successfully.")

    if p_abbr_heading:
        p_abbr_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_abbr_heading.paragraph_format.space_before = Pt(12)
        p_abbr_heading.paragraph_format.space_after = Pt(10)
        p_abbr_heading.paragraph_format.page_break_before = True

    # Configure Section 2 (Preliminary Pages) to end after t_abbr!
    t4_elem = t_abbr._tbl
    t4_idx = body.index(t4_elem)
    p_after_t4 = body[t4_idx + 1]
    for br in p_after_t4.xpath('.//w:br'):
        br.getparent().remove(br)

    # Section 2 sectPr: header rId10, footer rId11, lowerRoman start=1!
    sectPr1 = parse_xml(f'''
    <w:sectPr {nsdecls("w", "r")}>
      <w:headerReference w:type="default" r:id="rId10"/>
      <w:footerReference w:type="default" r:id="rId11"/>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1224" w:right="1152" w:bottom="1080" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
      <w:pgNumType w:fmt="lowerRoman" w:start="1"/>
    </w:sectPr>
    ''')
    p_after_t4.get_or_add_pPr().append(sectPr1)

    # Remove old draft body elements after Table 4 (from t4_idx + 2 up to sectPr)
    sect = body.xpath('w:sectPr')[0]
    to_remove = [child for child in body[t4_idx + 2:] if child != sect]
    print(f"Removing {len(to_remove)} old placeholder elements...")
    for el in to_remove:
        body.remove(el)

    # Configure Section 3 (Main Body) at body/sectPr: decimal start=1!
    pgNumType2 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="decimal" w:start="1"/>')
    sect.append(pgNumType2)

    # Append All Chapters and Appendices using report_chapters_builder
    print("Appending Chapters and Appendices...")
    rcb.build_chapter_1(doc)
    rcb.build_chapter_2(doc)
    rcb.build_chapter_3(doc)
    rcb.build_chapter_4(doc)
    rcb.build_chapter_5(doc)
    rcb.build_chapter_6(doc)
    rcb.build_chapter_7(doc)
    rcb.build_chapter_8(doc)
    rcb.build_chapter_9(doc)
    rcb.build_chapter_10(doc)
    rcb.build_chapter_11(doc)
    rcb.build_chapter_12(doc)
    rcb.build_chapter_13(doc)
    rcb.build_chapter_14(doc)
    rcb.build_chapter_15(doc)
    rcb.build_appendices(doc)
    rcb.build_chapter_b(doc)
    rcb.build_chapter_c(doc)

    print("Saving Pass 1 DOCX...")
    doc.save(TEMP_PASS1_DOCX)
    print("Converting Pass 1 to PDF...")
    export_docx_to_pdf(TEMP_PASS1_DOCX, TEMP_PASS1_PDF)

    # Scan Pass 1 PDF
    print("Scanning Pass 1 PDF for exact page numbers...")
    pdf = fitz.open(TEMP_PASS1_PDF)
    print(f"Total pages generated: {len(pdf)}")

    ch1_page_idx = None
    prelim_pages = {}
    body_pages = {}

    for p_idx, page in enumerate(pdf):
        txt = page.get_text()
        lines = [l.strip() for l in txt.split("\n") if l.strip()]
        
        # Check if Chapter 1 starts on this page
        if "CHAPTER 1" in lines and ch1_page_idx is None:
            ch1_page_idx = p_idx
            print(f"Chapter 1 starts on PDF page index {p_idx} (page {p_idx + 1} of document)")

        # Read footer block to verify number
        footer_num = ""
        for b in page.get_text("blocks"):
            if b[3] > 740:
                footer_num = b[4].strip()

        if ch1_page_idx is None or p_idx < ch1_page_idx:
            for line in lines:
                if "CERTIFICATE" in line and "Certificate" not in prelim_pages:
                    prelim_pages["Certificate"] = footer_num or to_roman(p_idx)
                if "DECLARATION" in line and "Declaration" not in prelim_pages:
                    prelim_pages["Declaration"] = footer_num or to_roman(p_idx)
                if "ACKNOWLEDGEMENT" in line and "Acknowledgement" not in prelim_pages:
                    prelim_pages["Acknowledgement"] = footer_num or to_roman(p_idx)
                if "ABSTRACT" in line and "Abstract" not in prelim_pages:
                    prelim_pages["Abstract"] = footer_num or to_roman(p_idx)
                if "TABLE OF CONTENTS" in line and "Table of Contents" not in prelim_pages:
                    prelim_pages["Table of Contents"] = footer_num or to_roman(p_idx)
                if "LIST OF FIGURES" in line and "List of Figures" not in prelim_pages:
                    prelim_pages["List of Figures"] = footer_num or to_roman(p_idx)
                if "LIST OF TABLES" in line and "List of Tables" not in prelim_pages:
                    prelim_pages["List of Tables"] = footer_num or to_roman(p_idx)
                if "LIST OF ABBREVIATIONS" in line and "List of Abbreviations" not in prelim_pages:
                    prelim_pages["List of Abbreviations"] = footer_num or to_roman(p_idx)
        else:
            p_num = p_idx - ch1_page_idx + 1
            
            for ch_num in range(1, 16):
                ch_tag = f"CHAPTER {ch_num}"
                if ch_tag in lines and f"Chapter {ch_num}" not in body_pages:
                    body_pages[f"Chapter {ch_num}"] = str(p_num)

            if "CHAPTER A" in lines and "Chapter A" not in body_pages:
                body_pages["Chapter A"] = str(p_num)
            if "CHAPTER B" in lines and "Chapter B" not in body_pages:
                body_pages["Chapter B"] = str(p_num)
            if "CHAPTER C" in lines and "Chapter C" not in body_pages:
                body_pages["Chapter C"] = str(p_num)

            for line in lines:
                m = re.match(r"^(\d+\.\d+)\s+[A-Z]", line)
                if m:
                    sec_key = m.group(1)
                    if sec_key not in body_pages:
                        body_pages[sec_key] = str(p_num)

            for line in lines:
                m = re.match(r"^(Appendix\s+[A-H])\s+", line)
                if m:
                    app_key = m.group(1)
                    if app_key not in body_pages:
                        body_pages[app_key] = str(p_num)

            for line in lines:
                m = re.match(r"^Figure\s+([0-9A-Z\.]+):", line)
                if m:
                    fig_key = f"Fig_{m.group(1)}"
                    if fig_key not in body_pages:
                        body_pages[fig_key] = str(p_num)

            for line in lines:
                m = re.match(r"^Table\s+([0-9A-Z\.]+):", line)
                if m:
                    tbl_key = f"Tbl_{m.group(1)}"
                    if tbl_key not in body_pages:
                        body_pages[tbl_key] = str(p_num)

    print("Preliminary pages detected:", prelim_pages)
    pdf.close()

    # Pass 2: Re-open docx and inject exact numbers into TOC, LOF, LOT
    print("Executing Pass 2: Injecting exact page numbers...")
    with open(TEMP_PASS1_DOCX, "rb") as f:
        docx_bytes = io.BytesIO(f.read())
    doc2 = docx.Document(docx_bytes)

    # Table 3: TOC
    toc2 = doc2.tables[3]

    for idx, (col0, col1, default_pg) in enumerate(toc_data):
        if idx < len(toc2.rows):
            if col1 == "Table of Contents":
                real_pg = "v-viii"
            elif col0 in body_pages:
                real_pg = body_pages[col0]
            elif col1 in prelim_pages:
                real_pg = prelim_pages[col1]
            else:
                real_pg = default_pg
            
            is_header = (idx == 0)
            is_prelim_header = (idx == 1)
            is_ch = col0.startswith('Chapter') or col0.startswith('Appendix') or is_header or is_prelim_header
            
            set_cell(toc2.rows[idx].cells[2], real_pg, bold=is_ch, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    # Find LOF Table and LOT Table in doc2
    tbl_lof_doc2 = None
    tbl_lot_doc2 = None
    for t in doc2.tables:
        if len(t.rows) > 0 and len(t.rows[0].cells) > 0:
            h0 = t.rows[0].cells[0].paragraphs[0].text.strip()
            if h0 == "Figure No.":
                tbl_lof_doc2 = t
            elif h0 == "Table No.":
                tbl_lot_doc2 = t

    if tbl_lof_doc2:
        print("Updating List of Figures Table in doc2...")
        for idx, (f_num, f_title, default_pg) in enumerate(figures_data):
            raw_num = f_num.replace("Figure ", "")
            real_pg = body_pages.get(f"Fig_{raw_num}", default_pg)
            set_cell(tbl_lof_doc2.rows[idx + 1].cells[2], real_pg, bold=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    if tbl_lot_doc2:
        print("Updating List of Tables Table in doc2...")
        for idx, (t_num, t_title, default_pg) in enumerate(tables_data):
            raw_num = t_num.replace("Table ", "")
            real_pg = body_pages.get(f"Tbl_{raw_num}", default_pg)
            set_cell(tbl_lot_doc2.rows[idx + 1].cells[2], real_pg, bold=False, font_size=8.0, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=1.2, space_after=1.2)

    # Save final updated DOCX and PDF
    doc2.save(OUTPUT_PRO_DOCX)
    print("Pass 2 DOCX saved successfully.")

    export_docx_to_pdf(OUTPUT_PRO_DOCX, OUTPUT_PRO_PDF)
    print("Pass 2 PDF conversion complete!")

    # Clean up temp pass 1 files
    try:
        if os.path.exists(TEMP_PASS1_DOCX):
            os.remove(TEMP_PASS1_DOCX)
        if os.path.exists(TEMP_PASS1_PDF):
            os.remove(TEMP_PASS1_PDF)
    except Exception:
        pass

    # Copy to Downloads
    shutil.copy2(OUTPUT_PRO_DOCX, OUTPUT_DL_DOCX)
    shutil.copy2(OUTPUT_PRO_PDF, OUTPUT_DL_PDF)
    shutil.copy2(OUTPUT_PRO_DOCX, HET_DL_DOCX)
    shutil.copy2(OUTPUT_PRO_PDF, HET_DL_PDF)
    print("Files mirrored to Downloads successfully.")

    print("================================================================================")
    print("  FINAL HARDBOUND REPORT GENERATION FULLY COMPLETE!")
    print(f"  PRO DOCX: {OUTPUT_PRO_DOCX}")
    print(f"  PRO PDF:  {OUTPUT_PRO_PDF}")
    print("================================================================================")

if __name__ == "__main__":
    generate_report()
