import fitz

doc = fitz.open(r"C:\Users\hetjo\.gemini\antigravity-ide\brain\c1fc7eb3-4962-446c-ac62-a9b91c8ebc39\.user_uploaded\media_1790421381263.pdf")
page = doc[0]
d = page.get_text("dict")
for b in d["blocks"]:
    if "lines" in b:
        for l in b["lines"]:
            for s in l["spans"]:
                txt = s["text"].strip()
                if txt:
                    print(f"[{s['bbox'][0]:.1f}, {s['bbox'][1]:.1f}] font={s['font']}, sz={s['size']:.1f}, flags={s['flags']}: {repr(txt[:70])}")
