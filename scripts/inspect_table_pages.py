import fitz # PyMuPDF
import re

doc = fitz.open(r"C:\dev\pro\MaintAI_Final_Hard_Bound_Project_Report_Het_Joshi.pdf")
print("Total pages in PDF:", len(doc))

# Find each Table occurrence across pages
table_pattern = re.compile(r"Table\s+([0-9A-Z\.]+):")
found_tables = {}

for p_idx, page in enumerate(doc):
    text = page.get_text()
    for match in table_pattern.finditer(text):
        t_num = match.group(1)
        found_tables.setdefault(t_num, []).append(p_idx + 1)

print("\n--- Tables and their starting pages in PDF ---")
for t_num, pages in found_tables.items():
    print(f"Table {t_num}: found on pages {pages}")
