import docx

doc = docx.Document(r"C:\Users\hetjo\Downloads\report3.docx")
for i, p in enumerate(doc.paragraphs):
    if "blip" in p._element.xml:
        print(f"P[{i}] text='{p.text[:40]}' HAS IMAGE BLIP")
