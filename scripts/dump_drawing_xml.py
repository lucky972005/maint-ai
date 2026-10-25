import docx

doc = docx.Document(r"C:\Users\hetjo\Downloads\Internship_UDP_Training_Report_Template for reporting 4.docx")
p = doc.paragraphs[1] # '1. Student Information'
for r in p.runs:
    if "drawing" in r._r.xml:
        with open(r"C:\dev\pro\run_drawing.xml", "w", encoding="utf-8") as f:
            f.write(r._r.xml)
        print("Wrote run_drawing.xml successfully")
        break
