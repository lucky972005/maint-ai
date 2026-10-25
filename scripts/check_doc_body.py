import docx

doc = docx.Document(r"C:\dev\pro\MaintAI_Final_Hard_Bound_Project_Report_Het_Joshi.docx")
body = doc._body._element

for i, el in enumerate(body[:65]):
    tag = el.tag.split('}')[-1]
    txt = ""
    if tag == 'p':
        txt = "".join([t.text for t in el.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
    elif tag == 'tbl':
        txt = "TABLE: " + "".join([t.text for t in el.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])[:40]
    print(f"Doc El {i}: <{tag}> {txt[:60]}")
