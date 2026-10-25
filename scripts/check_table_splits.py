import fitz

doc = fitz.open(r"C:\dev\pro\MaintAI_Final_Hard_Bound_Project_Report_Het_Joshi.pdf")

# In PyMuPDF, find tables on each page using page.find_tables()
for p_idx, page in enumerate(doc):
    p_num = p_idx + 1
    tabs = page.find_tables()
    txt = page.get_text()
    if p_num <= 11:
        continue # skip preliminary
    table_captions = [line.strip() for line in txt.split("\n") if line.strip().startswith("Table ")]
    print(f"Page {p_num}: {len(tabs.tables)} table(s) detected. Captions: {table_captions}")
