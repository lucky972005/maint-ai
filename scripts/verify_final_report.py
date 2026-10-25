import fitz

doc = fitz.open(r"C:\dev\pro\MaintAI_Final_Hard_Bound_Project_Report_Het_Joshi.pdf")
print(f"Final PDF Total Pages: {len(doc)}")

# Verify chapters start at top of pages
ch_found = {}
for idx, page in enumerate(doc):
    p_num = idx + 1
    if p_num < 12:
        continue
    txt = page.get_text()
    for ch in range(1, 16):
        tag = f"CHAPTER {ch}"
        if tag in txt and f"Chapter {ch}" not in ch_found:
            first_line = txt.strip().split("\n")[0]
            ch_found[f"Chapter {ch}"] = (p_num, first_line)
    for app in ['A', 'B', 'C']:
        tag = f"CHAPTER {app}"
        if tag in txt and f"Chapter {app}" not in ch_found:
            first_line = txt.strip().split("\n")[0]
            ch_found[f"Chapter {app}"] = (p_num, first_line)

print("\n--- Chapter Verification ---")
for ch, (pg, line) in ch_found.items():
    print(f"  {ch}: Page {pg} (Top line: '{line}')")

# Verify table splits
split_tables = []
for idx, page in enumerate(doc):
    p_num = idx + 1
    if p_num <= 12:
        continue # Preliminary pages (e.g. Page 12 has List of Abbreviations table)
    tabs = page.find_tables()
    txt = page.get_text()
    caps = [l.strip() for l in txt.split("\n") if l.strip().startswith("Table ")]
    if len(tabs.tables) > 0 and len(caps) == 0:
        split_tables.append(p_num)

print("\n--- Split Table Check ---")
if split_tables:
    print(f"Warning: split tables detected on pages: {split_tables}")
else:
    print("SUCCESS: ZERO tables split across pages! Every table is completely contained on a single page!")
