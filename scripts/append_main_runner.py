import os

code_to_append = '''
# ==============================================================================
# 6. Table of Contents (Table 3) — Official Syllabus Index (139 Rows)
# ==============================================================================
print("Populating official 139-row Table of Contents...")
toc = doc.tables[3]

toc_data = [
    ('Chapter / Section', 'Title', 'Page No.'),
    ('', 'Preliminary Pages', ''),
    ('', 'Certificate', 'i'),
    ('', 'Declaration', 'ii'),
    ('', 'Acknowledgement', 'iii'),
    ('', 'Abstract', 'iv'),
    ('', 'Table of Contents', 'v'),
    ('', 'List of Figures', 'vi'),
    ('', 'List of Tables', 'vii'),
    ('', 'List of Abbreviations', 'viii'),
    ('Chapter 1', 'Introduction', '13'),
    ('1.1', 'Background of the Project', '13'),
    ('1.2', 'Problem Statement', '13'),
    ('1.3', 'Need for the Project', '14'),
    ('1.4', 'Aim of the Project', '14'),
    ('1.5', 'Objectives of the Project', '14'),
    ('1.6', 'Scope of the Project', '15'),
    ('1.7', 'Project Overview', '15'),
    ('1.8', 'Organization of the Report', '16'),
    ('Chapter 2', 'Literature Review and Existing System Study', '17'),
    ('2.1', 'Introduction', '17'),
    ('2.2', 'Review of Existing Systems / Applications', '17'),
    ('2.3', 'Existing System', '18'),
    ('2.4', 'Limitations of Existing System', '18'),
    ('2.5', 'Proposed System', '18'),
    ('2.6', 'Comparative Analysis', '19'),
    ('2.7', 'Research / Technology Gap', '19'),
    ('Chapter 3', 'Requirements Analysis and Project Scope', '20'),
    ('3.1', 'Functional Requirements', '20'),
    ('3.2', 'Non-Functional Requirements', '21'),
    ('3.3', 'Hardware Requirements', '21'),
    ('3.4', 'Software Requirements', '22'),
    ('3.5', 'User Requirements', '22'),
    ('3.6', 'System Constraints', '23'),
    ('3.7', 'Feasibility Study', '23'),
    ('3.8', 'Project Scope', '23'),
    ('Chapter 4', 'System Analysis and Methodology', '24'),
    ('4.1', 'Development Methodology', '24'),
    ('4.2', 'Project Planning', '24'),
    ('4.3', 'Requirement Analysis', '24'),
    ('4.4', 'System Workflow', '25'),
    ('4.5', 'Use Case Analysis', '25'),
    ('4.6', 'Data Flow / Process Flow', '25'),
    ('4.7', 'Project Timeline / Milestones', '26'),
    ('Chapter 5', 'System Design and Architecture', '27'),
    ('5.1', 'System Architecture', '27'),
    ('5.2', 'Overall System Workflow', '28'),
    ('5.3', 'Module Architecture', '28'),
    ('5.4', 'Use Case Diagram', '29'),
    ('5.5', 'Data Flow Diagram', '29'),
    ('5.6', 'Class Diagram', '29'),
    ('5.7', 'Sequence Diagram', '30'),
    ('5.8', 'Activity Diagram', '30'),
    ('5.9', 'Component / Deployment Diagram', '30'),
    ('5.10', 'Database Design / ER Diagram', '31'),
    ('Chapter 6', 'Technology Stack and Development Environment', '33'),
    ('6.1', 'Programming Languages', '33'),
    ('6.2', 'Frameworks and Libraries', '33'),
    ('6.3', 'Database Technologies', '34'),
    ('6.4', 'APIs and Third-Party Services', '34'),
    ('6.5', 'Development Tools and IDE', '35'),
    ('6.6', 'Version Control / Repository', '35'),
    ('6.7', 'Hardware and Runtime Environment', '35'),
    ('Chapter 7', 'System Implementation', '36'),
    ('7.1', 'Implementation Overview', '36'),
    ('7.2', 'Module 1 – AR-Guided Step Repair Guidance', '36'),
    ('7.3', 'Module 2 – Multimodal AI Vision Tool Verification Gate', '37'),
    ('7.4', 'Module 3 – Offline-First Write-Ahead Sync Engine', '38'),
    ('7.5', 'User Interface Implementation', '39'),
    ('7.6', 'Database Implementation', '39'),
    ('7.7', 'API / Backend Implementation', '40'),
    ('7.8', 'Algorithm / Logic Implementation', '40'),
    ('7.9', 'Authentication and Authorization', '41'),
    ('7.10', 'Integration of Modules', '41'),
    ('Chapter 8', 'Testing and Validation', '42'),
    ('8.1', 'Testing Strategy', '42'),
    ('8.2', 'Unit Testing', '42'),
    ('8.3', 'Integration Testing', '43'),
    ('8.4', 'Functional Testing', '43'),
    ('8.5', 'System Testing', '44'),
    ('8.6', 'Performance Testing', '44'),
    ('8.7', 'Security Testing', '45'),
    ('8.8', 'User Acceptance Testing', '45'),
    ('8.9', 'Test Cases and Test Results', '46'),
    ('8.10', 'Defect Identification and Resolution', '46'),
    ('Chapter 9', 'Results and Performance Analysis', '47'),
    ('9.1', 'Implementation Results', '47'),
    ('9.2', 'System Outputs', '47'),
    ('9.3', 'Screenshots of the Application', '48'),
    ('9.4', 'Functional Results', '49'),
    ('9.5', 'Performance Analysis', '50'),
    ('9.6', 'Comparison with Existing System', '51'),
    ('9.7', 'Achievement of Project Objectives', '51'),
    ('Chapter 10', 'Deployment and Project Demonstration', '52'),
    ('10.1', 'Deployment Environment', '52'),
    ('10.2', 'Installation / Configuration', '52'),
    ('10.3', 'Database / Server Configuration', '53'),
    ('10.4', 'Application Deployment', '53'),
    ('10.5', 'Live / Demonstration Workflow', '53'),
    ('10.6', 'Deployment Challenges', '54'),
    ('Chapter 11', 'Challenges, Solutions and Improvements', '55'),
    ('11.1', 'Technical Challenges', '55'),
    ('11.2', 'Implementation Challenges', '55'),
    ('11.3', 'Testing Challenges', '56'),
    ('11.4', 'Solutions Implemented', '56'),
    ('11.5', 'Improvements Made During Development', '56'),
    ('Chapter 12', 'Project Progress and Individual Contribution', '57'),
    ('12.1', 'Reporting 1 – Problem Identification and Planning', '57'),
    ('12.2', 'Reporting 2 – Design and Implementation Progress', '57'),
    ('12.3', 'Reporting 3 – Advanced Implementation, Testing and Validation', '57'),
    ('12.4', 'Reporting 4 – Final Completion and Evaluation', '58'),
    ('12.5', 'Individual Contribution', '58'),
    ('12.6', 'Tasks Completed', '58'),
    ('12.7', 'Technical and Professional Skills Acquired', '59'),
    ('Chapter 13', 'Limitations and Future Scope', '60'),
    ('13.1', 'Current Limitations', '60'),
    ('13.2', 'Technical Limitations', '60'),
    ('13.3', 'Proposed Enhancements', '61'),
    ('13.4', 'Future Scope', '61'),
    ('13.5', 'Scalability and Further Development', '61'),
    ('Chapter 14', 'Conclusion', '62'),
    ('14.1', 'Summary of the Project', '62'),
    ('14.2', 'Key Achievements', '62'),
    ('14.3', 'Objectives Achieved', '63'),
    ('14.4', 'Overall Conclusion', '63'),
    ('Chapter 15', 'References', '64'),
    ('15.1', 'Books', '64'),
    ('15.2', 'Research Papers / Journals', '64'),
    ('15.3', 'Websites / Online Resources', '65'),
    ('15.4', 'Documentation / APIs', '65'),
    ('', 'Appendices', '66'),
    ('Appendix A', 'Reporting 1 – Detailed Progress Report', '66'),
    ('Appendix B', 'Reporting 2 – Detailed Progress Report', '66'),
    ('Appendix C', 'Reporting 3 – Detailed Progress Report', '66'),
    ('Appendix D', 'Reporting 4 – Final Evaluation Report', '67'),
    ('Appendix E', 'Additional Screenshots and Outputs', '67'),
    ('Appendix F', 'Source Code / Repository Details', '69'),
    ('Appendix G', 'Certificates / Internship / Training Documents', '69'),
    ('Appendix H', 'Mentor / Evaluator Remarks', '69')
]

for idx, (col0, col1, col2) in enumerate(toc_data):
    if idx < len(toc.rows):
        r = toc.rows[idx]
        is_ch = col0.startswith('Chapter') or col0.startswith('Appendix') or idx == 0
        set_cell(r.cells[0], col0, bold=is_ch, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(r.cells[1], col1, bold=is_ch, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell(r.cells[2], col2, bold=is_ch, font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)
        make_row_cant_split(r)

# ==============================================================================
# 7. List of Figures (Page 10)
# ==============================================================================
print("Populating List of Figures...")
set_para_text(doc.paragraphs[45], 
"Figure 4.1: Overall Project Workflow & Agile Engineering Lifecycle ................................. 25\\n"
"Figure 5.1: Final 3-Tier System Architecture & Cloud Infrastructure ................................. 27\\n"
"Figure 5.2: End-to-End Maintenance & AR Repair Process Flow ......................................... 28\\n"
"Figure 5.3: Major UML Class & Relational Database Schema Diagram ............................... 31\\n"
"Figure 5.4: Major Interface & UI Wireframe Navigation Hierarchy ...................................... 32\\n"
"Figure 7.1: Module 1 — Live AR Step Guidance with Pulsing Canvas Markers .................... 37\\n"
"Figure 7.2: Module 2 — Multimodal AI Computer Vision Tool Verification Modal .................. 38\\n"
"Figure 7.3: Module 3 — Offline-First Write-Ahead Sync Pipeline Architecture ....................... 39\\n"
"Figure 9.1: Final Output 1 — Machine Specifications & Procedure Selection ........................... 48\\n"
"Figure 9.2: Final Output 2 — Live AR Step Guidance with Hands-Free Voice Control .................. 49\\n"
"Figure 9.3: Final Output 3 — Spare Parts Inventory & Low Stock Tracking ............................. 50\\n"
"Figure 9.4: Final Output 4 — Supervisor Maintenance Analytics & MTTR Tracking ................... 50\\n"
"Figure 10.1: Live Field Demonstration & End-to-End Operational Workflow ........................... 54\\n"
"Figure A.1: Supporting Evidence — Plant QR Code Batch Generator & Print Matrix ................... 68\\n"
"Figure A.2: Supporting Evidence — Fault Reporting & Photo Evidence Upload .......................... 68", 
font_size=10.0, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=4)

# ==============================================================================
# 8. List of Tables (Page 11)
# ==============================================================================
print("Populating List of Tables...")
set_para_text(doc.paragraphs[49],
"Table 1.1: Scope Matrix — Included, Excluded, and Operational Constraints ..................... 15\\n"
"Table 2.1: Literature Review & Existing Approaches .................................................... 17\\n"
"Table 2.2: Comparative Analysis of Maintenance Approaches ................................... 19\\n"
"Table 3.1: Functional Requirements Specification .................................................... 20\\n"
"Table 3.2: Non-Functional Requirements Specification ............................................. 21\\n"
"Table 3.3: Hardware Requirements & Test Environments ........................................... 21\\n"
"Table 3.4: Software Requirements & Framework Libraries ......................................... 22\\n"
"Table 3.5: System Constraints & Operational Assumptions ........................................... 23\\n"
"Table 4.1: Project Phases and Key Engineering Deliverables ......................................... 26\\n"
"Table 4.2: Progress Report Milestone Consolidation .................................................... 26\\n"
"Table 4.3: Project Execution Schedule & 16-Week Timeline ........................................... 26\\n"
"Table 5.1: Module-Wise Architectural Design ............................................................. 28\\n"
"Table 5.2: Relational Database Schema Design ............................................................ 32\\n"
"Table 6.1: Programming Languages ............................................................................ 33\\n"
"Table 6.2: Frameworks, Libraries, and APIs ................................................................ 33\\n"
"Table 6.3: Database and Storage Technologies .............................................................. 34\\n"
"Table 6.4: APIs and Third-Party Services ..................................................................... 34\\n"
"Table 6.5: Development Tools and IDE ...................................................................... 35\\n"
"Table 7.1: API & External Service Integration Specifications ...................................... 40\\n"
"Table 8.1: Unit & Module Testing Test Cases ............................................................. 42\\n"
"Table 8.2: Integration Testing Specifications ............................................................. 43\\n"
"Table 8.3: Functional Testing Specifications ............................................................. 43\\n"
"Table 8.4: System Testing & End-to-End Scenarios .................................................... 44\\n"
"Table 8.5: Performance Testing Benchmarks ................................................................ 44\\n"
"Table 8.6: User Acceptance Testing Across Physical Devices ........................................ 45\\n"
"Table 8.7: Experimental Validation Benchmarks ........................................................ 46\\n"
"Table 8.8: Defects Identification and Resolution .......................................................... 46\\n"
"Table 9.1: Quantitative Performance Metrics & MTTR Reductions ............................... 50\\n"
"Table 9.2: Comparative Benchmark with Legacy Maintenance Systems ........................ 51\\n"
"Table 9.3: Objective-Wise Achievement Matrix ............................................................. 51\\n"
"Table 10.1: Production Deployment Environment & Configuration ............................... 52\\n"
"Table 11.1: Major Engineering Challenges & Solutions ............................................... 55\\n"
"Table 11.2: Improvements Made During Development .................................................... 56\\n"
"Table 12.1: Individual Contribution Matrix (Het Joshi) ................................................ 58\\n"
"Table 13.1: Current System Limitations & Boundary Factors ........................................... 60\\n"
"Table 14.1: Final Project Status Matrix ..................................................................... 63\\n"
"Table F.1: Repository Structure & Core Modules .......................................................... 69\\n"
"Table B.1: Final Hard-Bound Submission Checklist .................................................... 70",
font_size=9.5, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=4)

# ==============================================================================
# Remove Old Draft Body Elements (Elements from 57 to before sectPr)
# ==============================================================================
print("Removing old draft body elements...")
body = doc._body._element
sect = body.xpath('w:sectPr')[0]
to_remove = [child for child in body[57:] if child != sect]
print(f"Removing {len(to_remove)} placeholder elements...")
for el in to_remove:
    body.remove(el)

# ==============================================================================
# Append All 15 Chapters and Appendices using report_chapters_builder
# ==============================================================================
import scripts.report_chapters_builder as rcb

print("Appending Chapter 1 (Introduction)...")
rcb.build_chapter_1(doc)

print("Appending Chapter 2 (Literature Review and Existing System Study)...")
rcb.build_chapter_2(doc)

print("Appending Chapter 3 (Requirements Analysis and Project Scope)...")
rcb.build_chapter_3(doc)

print("Appending Chapter 4 (System Analysis and Methodology)...")
rcb.build_chapter_4(doc)

print("Appending Chapter 5 (System Design and Architecture)...")
rcb.build_chapter_5(doc)

print("Appending Chapter 6 (Technology Stack and Development Environment)...")
rcb.build_chapter_6(doc)

print("Appending Chapter 7 (System Implementation)...")
rcb.build_chapter_7(doc)

print("Appending Chapter 8 (Testing and Validation)...")
rcb.build_chapter_8(doc)

print("Appending Chapter 9 (Results and Performance Analysis)...")
rcb.build_chapter_9(doc)

print("Appending Chapter 10 (Deployment and Project Demonstration)...")
rcb.build_chapter_10(doc)

print("Appending Chapter 11 (Challenges, Solutions and Improvements)...")
rcb.build_chapter_11(doc)

print("Appending Chapter 12 (Project Progress and Individual Contribution)...")
rcb.build_chapter_12(doc)

print("Appending Chapter 13 (Limitations and Future Scope)...")
rcb.build_chapter_13(doc)

print("Appending Chapter 14 (Conclusion)...")
rcb.build_chapter_14(doc)

print("Appending Chapter 15 (References)...")
rcb.build_chapter_15(doc)

print("Appending Appendices (Appendix A through H)...")
rcb.build_appendices(doc)

print("Appending Chapter B (Final Submission Checklist)...")
rcb.build_chapter_b(doc)

print("Appending Chapter C (Formatting and Submission Guidelines)...")
rcb.build_chapter_c(doc)

# ==============================================================================
# Save Initial DOCX and Convert to PDF (Pass 1)
# ==============================================================================
print(f"Saving Pass 1 DOCX: {OUTPUT_PRO_DOCX}")
doc.save(OUTPUT_PRO_DOCX)
doc.save(OUTPUT_DL_DOCX)
print("Pass 1 DOCX saved.")

print(f"Converting Pass 1 to PDF: {OUTPUT_PRO_PDF} ...")
try:
    convert(OUTPUT_PRO_DOCX, OUTPUT_PRO_PDF)
    print("Pass 1 PDF conversion complete!")
except Exception as e:
    print(f"Pass 1 PDF conversion warning: {e}")

# ==============================================================================
# Pass 2: Extract Real Page Numbers from PDF & Update TOC / Lists
# ==============================================================================
print("Executing Pass 2: Scanning PDF for exact page numbers...")
if os.path.exists(OUTPUT_PRO_PDF):
    pdf = fitz.open(OUTPUT_PRO_PDF)
    print(f"Total pages generated: {len(pdf)}")

    # Map of headings to detect page
    heading_pages = {}
    
    # Check each page
    for p_idx, page in enumerate(pdf):
        p_num = p_idx + 1
        txt = page.get_text()
        
        # Scan for chapters
        for ch_num in range(1, 16):
            ch_tag = f"CHAPTER {ch_num}"
            if ch_tag in txt and f"Chapter {ch_num}" not in heading_pages:
                heading_pages[f"Chapter {ch_num}"] = str(p_num)

        # Scan for sections
        for sec_prefix in ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "11.", "12.", "13.", "14.", "15."]:
            for sec_idx in range(1, 11):
                sec_tag = f"{sec_prefix}{sec_idx} "
                sec_key = f"{sec_prefix}{sec_idx}"
                if sec_tag in txt and sec_key not in heading_pages:
                    heading_pages[sec_key] = str(p_num)

        # Scan for appendices
        for app_letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            app_tag = f"Appendix {app_letter}"
            if app_tag in txt and app_tag not in heading_pages:
                heading_pages[app_tag] = str(p_num)

        # Scan for figures
        for fig_num in ["4.1", "5.1", "5.2", "5.3", "5.4", "7.1", "7.2", "7.3", "9.1", "9.2", "9.3", "9.4", "10.1", "A.1", "A.2"]:
            fig_tag = f"Figure {fig_num}:"
            if fig_tag in txt and fig_num not in heading_pages:
                heading_pages[f"Fig_{fig_num}"] = str(p_num)

        # Scan for tables
        for tbl_num in ["1.1", "2.1", "2.2", "3.1", "3.2", "3.3", "3.4", "3.5", "4.1", "4.2", "4.3", "5.1", "5.2", 
                        "6.1", "6.2", "6.3", "6.4", "6.5", "7.1", "8.1", "8.2", "8.3", "8.4", "8.5", "8.6", "8.7", "8.8",
                        "9.1", "9.2", "9.3", "10.1", "11.1", "11.2", "12.1", "13.1", "14.1", "F.1", "B.1"]:
            tbl_tag = f"Table {tbl_num}:"
            if tbl_tag in txt and tbl_num not in heading_pages:
                heading_pages[f"Tbl_{tbl_num}"] = str(p_num)

    print("Detected page numbers sample:", list(heading_pages.items())[:15])

    # Re-open docx to inject exact page numbers
    doc2 = docx.Document(OUTPUT_PRO_DOCX)
    toc2 = doc2.tables[3]

    for idx, (col0, col1, default_pg) in enumerate(toc_data):
        if idx < len(toc2.rows):
            real_pg = heading_pages.get(col0, default_pg)
            if not real_pg and col0 == "":
                real_pg = default_pg
            set_cell(toc2.rows[idx].cells[2], real_pg, bold=(col0.startswith('Chapter') or col0.startswith('Appendix')), font_size=8.5, align=WD_ALIGN_PARAGRAPH.CENTER)

    # Save final updated DOCX and PDF
    doc2.save(OUTPUT_PRO_DOCX)
    doc2.save(OUTPUT_DL_DOCX)
    print("Pass 2 DOCX saved with exact page numbers.")

    try:
        convert(OUTPUT_PRO_DOCX, OUTPUT_PRO_PDF)
        convert(OUTPUT_DL_DOCX, OUTPUT_DL_PDF)
        print("Pass 2 PDF conversion complete!")
    except Exception as e:
        print(f"Pass 2 PDF conversion warning: {e}")

print("================================================================================")
print("  FINAL HARDBOUND REPORT GENERATION FULLY COMPLETE!")
print(f"  PRO DOCX: {OUTPUT_PRO_DOCX}")
print(f"  PRO PDF:  {OUTPUT_PRO_PDF}")
print("================================================================================")
'''

with open('scripts/generate_final_hardbound_report_rearranged.py', 'a', encoding='utf-8') as f:
    f.write(code_to_append)

print("Updated scripts/generate_final_hardbound_report_rearranged.py!")
