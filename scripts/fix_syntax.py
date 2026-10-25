with open('scripts/report_chapters_builder.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = 0
for i, line in enumerate(lines):
    if skip > 0:
        skip -= 1
        continue
    if 'add_section_heading(doc, "Appendix H", "Mentor / Evaluator Remarks")' in line:
        new_lines.append(line)
        new_lines.append('    add_body_para(doc, "Mentor Remarks: _________________________________________________________________________________\\n\\nEvaluator Remarks: _______________________________________________________________________________\\n\\nFinal Evaluation Grade: [ _________ ]        Mentor Signature: __________________    Date: [ 03 / 10 / 2026 ]")\n')
        # skip until '# ==='
        j = i + 1
        while j < len(lines) and not lines[j].startswith('# ==='):
            j += 1
        skip = j - (i + 1)
    else:
        new_lines.append(line)

with open('scripts/report_chapters_builder.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Syntax fix applied!")
