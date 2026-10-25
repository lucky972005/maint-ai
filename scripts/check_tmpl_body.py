import docx

tmpl = docx.Document(r"C:\Users\hetjo\Downloads\PPSU_Final_Hard_Bound_Project_Report_Format.docx")
body = tmpl._body._element

for i, el in enumerate(body[:75]):
    tag = el.tag.split('}')[-1]
    txt = ""
    if tag == 'p':
        txt = "".join([t.text for t in el.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
    elif tag == 'tbl':
        txt = "TABLE: " + "".join([t.text for t in el.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])[:40]
    print(f"El {i}: <{tag}> {txt[:60]}")
