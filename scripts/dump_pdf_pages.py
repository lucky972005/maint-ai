import fitz

doc = fitz.open(r"C:\dev\pro\MaintAI_Reporting_4_Het_Joshi.pdf")

with open(r"C:\dev\pro\generated_pdf_pages.txt", "w", encoding="utf-8") as f:
    for i, p in enumerate(doc):
        f.write(f"\n==================== PAGE {i+1} ====================\n")
        f.write(p.get_text("text"))

print("Dumped generated_pdf_pages.txt")
