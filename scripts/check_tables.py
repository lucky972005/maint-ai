import re

with open(r'c:\dev\pro\scripts\report_chapters_builder.py', 'r', encoding='utf-8') as f:
    code = f.read()

tables = re.findall(r'Table [0-9A-Z\.]+: [^\",\n]+', code)
print(f"Total tables found: {len(tables)}")
for t in tables:
    print(" -", t)
