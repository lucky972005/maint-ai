import docx

doc = docx.Document(r"C:\Users\hetjo\Downloads\Internship_UDP_Training_Report_Template for reporting 4.docx")

with open(r"C:\dev\pro\template4_runs_inspection.txt", "w", encoding="utf-8") as out:
    for i, p in enumerate(doc.paragraphs):
        runs_txt = " | ".join([f"r{r_i}:'{r.text}'" for r_i, r in enumerate(p.runs)])
        out.write(f"P[{i}] (text='{p.text}'): {runs_txt}\n")

print("Dumped template4_runs_inspection.txt")
