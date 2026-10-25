import docx

doc = docx.Document(r"C:\dev\pro\MaintAI_Final_Hard_Bound_Project_Report_Het_Joshi.docx")
body = doc._body._element

start_idx = None
end_idx = None
for i, el in enumerate(body):
    txt = "".join([t.text for t in el.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
    if 'LIST OF ABBREVIATIONS' in txt:
        start_idx = i
    if 'CHAPTER 1' in txt:
        end_idx = i
        break

print(f"start_idx (LIST OF ABBREVIATIONS): {start_idx}")
print(f"end_idx (CHAPTER 1): {end_idx}")

for i in range(max(0, start_idx - 3), min(len(body), end_idx + 3)):
    tag = body[i].tag.split('}')[-1]
    txt = "".join([t.text for t in body[i].findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
    print(f"  El {i}: <{tag}> '{txt[:60]}'")
