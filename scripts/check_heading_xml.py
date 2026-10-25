import docx

doc = docx.Document(r"C:\Users\hetjo\Downloads\Internship_UDP_Training_Report_Template for reporting 4.docx")
for i, p in enumerate(doc.paragraphs):
    pPr_xml = p._p.pPr.xml if p._p.pPr is not None else ""
    if "shd" in pPr_xml:
        print(f"P[{i}]: text='{p.text}'")
