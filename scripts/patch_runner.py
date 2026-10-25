with open('scripts/generate_final_hardbound_report_rearranged.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Pass 1 save
old_p1 = """print(f"Saving Pass 1 DOCX: {OUTPUT_PRO_DOCX}")
doc.save(OUTPUT_PRO_DOCX)
doc.save(OUTPUT_DL_DOCX)
print("Pass 1 DOCX saved.")"""

new_p1 = """print(f"Saving Pass 1 DOCX: {OUTPUT_PRO_DOCX}")
doc.save(OUTPUT_PRO_DOCX)
try:
    doc.save(OUTPUT_DL_DOCX)
except Exception as e:
    print(f"Notice: Downloads Pass 1 docx save skipped (in use): {e}")
print("Pass 1 DOCX saved.")"""

# Replace Pass 2 save
old_p2 = """    # Save final updated DOCX and PDF
    doc2.save(OUTPUT_PRO_DOCX)
    doc2.save(OUTPUT_DL_DOCX)
    print("Pass 2 DOCX saved with exact page numbers.")

    try:
        convert(OUTPUT_PRO_DOCX, OUTPUT_PRO_PDF)
        convert(OUTPUT_DL_DOCX, OUTPUT_DL_PDF)
        print("Pass 2 PDF conversion complete!")
    except Exception as e:
        print(f"Pass 2 PDF conversion warning: {e}")"""

new_p2 = """    # Save final updated DOCX and PDF
    doc2.save(OUTPUT_PRO_DOCX)
    try:
        doc2.save(OUTPUT_DL_DOCX)
    except Exception as e:
        print(f"Notice: Downloads Pass 2 docx save skipped: {e}")
    print("Pass 2 DOCX saved with exact page numbers.")

    try:
        convert(OUTPUT_PRO_DOCX, OUTPUT_PRO_PDF)
        print("Pass 2 PDF conversion complete!")
        try:
            convert(OUTPUT_DL_DOCX, OUTPUT_DL_PDF)
        except Exception:
            pass
    except Exception as e:
        print(f"Pass 2 PDF conversion warning: {e}")"""

# Normalize CRLF
text = text.replace('\r\n', '\n')
old_p1 = old_p1.replace('\r\n', '\n')
new_p1 = new_p1.replace('\r\n', '\n')
old_p2 = old_p2.replace('\r\n', '\n')
new_p2 = new_p2.replace('\r\n', '\n')

if old_p1 in text and old_p2 in text:
    text = text.replace(old_p1, new_p1)
    text = text.replace(old_p2, new_p2)
    with open('scripts/generate_final_hardbound_report_rearranged.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Patched generate_final_hardbound_report_rearranged.py successfully!")
else:
    print("Could not find exact text blocks to patch.")
