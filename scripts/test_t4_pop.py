import docx
from docx.shared import Inches, Pt
from docx.oxml import parse_xml
from docx.oxml.ns import qn

doc = docx.Document(r"C:\Users\hetjo\Downloads\PPSU_Final_Hard_Bound_Project_Report_Format.docx")
body = doc._body._element

ch1_idx = None
for i, el in enumerate(body):
    txt = "".join([t.text for t in el.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if t.text])
    if txt.strip() == "CHAPTER 1":
        ch1_idx = i
        break

print(f"ch1_idx: {ch1_idx}")

# Populate Table 4
t4 = doc.tables[4]
t4_data = [
    ['Abbreviation', 'Full Form / Meaning'],
    ['AI', 'Artificial Intelligence (Computer vision & NLP engines)'],
    ['AR', 'Augmented Reality (In-browser 2D Canvas camera overlay)'],
    ['PWA', 'Progressive Web Application (Offline-capable browser standard)'],
    ['CMMS', 'Computerized Maintenance Management System'],
    ['MTTR', 'Mean Time to Repair (Average maintenance resolution duration)'],
    ['MTBF', 'Mean Time Between Failures (Equipment reliability metric)'],
    ['SOP', 'Standard Operating Procedure (Step-by-step repair workflow)'],
    ['RLS', 'Row Level Security (PostgreSQL multi-tenant boundary isolation)'],
    ['WAL', 'Write-Ahead Logging (IndexedDB local transaction mutation queue)'],
    ['FIFO', 'First-In, First-Out (Transaction queue processing sequence)'],
    ['UAT', 'User Acceptance Testing (Shop-floor mobile validation)'],
    ['API', 'Application Programming Interface (Next.js serverless routes)'],
    ['JWT', 'JSON Web Token (Stateless cryptographic authentication)'],
    ['HUD', 'Heads-Up Display (Visual camera viewport overlay interface)'],
    ['LOTO', 'Lockout / Tagout (OSHA hazardous energy control standard)'],
    ['DOM', 'Document Object Model (Browser HTML element tree)'],
    ['UUID', 'Universally Unique Identifier (v4 Client idempotency keys)'],
    ['ACID', 'Atomicity, Consistency, Isolation, Durability (Database transactions)'],
    ['TTS', 'Text-to-Speech (Audio procedural instruction synthesizer)'],
    ['QR', 'Quick Response Code (High-density 2D equipment barcode)']
]

while len(t4.rows) < len(t4_data):
    t4.add_row()

for r_idx, row in enumerate(t4_data):
    for c_idx, val in enumerate(row):
        cell = t4.rows[r_idx].cells[c_idx]
        cell.text = str(val)

print(f"Populated t4: now has {len(t4.rows)} rows!")
print("Row 0:", [c.text for c in t4.rows[0].cells])
print("Row 20:", [c.text for c in t4.rows[20].cells])
