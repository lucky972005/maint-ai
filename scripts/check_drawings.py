import docx

doc = docx.Document(r"C:\Users\hetjo\Downloads\Internship_UDP_Training_Report_Template for reporting 4.docx")
for i, p in enumerate(doc.paragraphs):
    for j, r in enumerate(p.runs):
        if "drawing" in r._r.xml:
            xml_snippet = r._r.xml[:120].replace("\n", " ")
            print(f"P[{i}] text='{p.text[:30]}' run[{j}] drawing: {xml_snippet}...")
            break
