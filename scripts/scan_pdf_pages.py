import fitz
import re

doc = fitz.open(r"C:\dev\pro\MaintAI_Final_Hard_Bound_Project_Report_Het_Joshi.pdf")
print("Total pages in PDF:", len(doc))

heading_pages = {}

for p_idx, page in enumerate(doc):
    p_num = p_idx + 1
    if p_num < 12:
        continue # skip preliminary pages
    txt = page.get_text()
    lines = [l.strip() for l in txt.split("\n")]

    # Chapters
    for ch in range(1, 16):
        tag = f"CHAPTER {ch}"
        if tag in lines and f"Chapter {ch}" not in heading_pages:
            heading_pages[f"Chapter {ch}"] = str(p_num)
    if "CHAPTER A" in lines and "Chapter A" not in heading_pages:
        heading_pages["Chapter A"] = str(p_num)
    if "CHAPTER B" in lines and "Chapter B" not in heading_pages:
        heading_pages["Chapter B"] = str(p_num)
    if "CHAPTER C" in lines and "Chapter C" not in heading_pages:
        heading_pages["Chapter C"] = str(p_num)

    # Sections: must start at line beginning: "<ch>.<sec> "
    for line in lines:
        m = re.match(r"^(\d+\.\d+)\s+[A-Z]", line)
        if m:
            sec_key = m.group(1)
            if sec_key not in heading_pages:
                heading_pages[sec_key] = str(p_num)

    # Appendices
    for line in lines:
        m = re.match(r"^(Appendix\s+[A-H])\s+", line)
        if m:
            app_key = m.group(1)
            if app_key not in heading_pages:
                heading_pages[app_key] = str(p_num)

    # Figures
    for line in lines:
        m = re.match(r"^Figure\s+([0-9A-Z\.]+):", line)
        if m:
            fig_key = f"Fig_{m.group(1)}"
            if fig_key not in heading_pages:
                heading_pages[fig_key] = str(p_num)

    # Tables
    for line in lines:
        m = re.match(r"^Table\s+([0-9A-Z\.]+):", line)
        if m:
            tbl_key = f"Tbl_{m.group(1)}"
            if tbl_key not in heading_pages:
                heading_pages[tbl_key] = str(p_num)

print("\n--- Refined Scanned Heading Page Map ---")
for k, v in sorted(heading_pages.items()):
    print(f"'{k}': '{v}',")
