import os
import re
import base64
import subprocess
import pymupdf

BASE = r"c:\dev\pro"

# Load real live demo QR code
with open(os.path.join(BASE, "pdf_images", "live_demo_qr.png"), "rb") as f:
    qr_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

# 1. LANDSCAPE
with open(os.path.join(BASE, "test_dense_landscape.html"), "r", encoding="utf-8") as f:
    l_html = f.read()

# Replace font-body with Cambria
l_html = l_html.replace(
    '--font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;',
    '--font-body: "Cambria", Georgia, "Times New Roman", serif;'
)
l_html = l_html.replace("@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');", "")

# Scale Title per guidelines (36 pt)
l_html = l_html.replace("font-size: 27pt;", "font-size: 34pt;")
l_html = l_html.replace("font-size: 15pt;\n      font-weight: 700;\n      color: var(--ppsu-blue);", "font-size: 17pt;\n      font-weight: bold;\n      color: var(--ppsu-blue);")

# Replace QR code in landscape
l_html = re.sub(
    r'<img src="data:image/png;base64,[A-Za-z0-9+/=]+" alt="Demo QR"',
    f'<img src="{qr_b64}" alt="Demo QR"',
    l_html
)

# Remove verified lines from clearance box in landscape
l_html = re.sub(r'<div class="approval-status-badge">\[OFFICIALLY APPROVED FOR B\.TECH CAPSTONE DEFENSE\]</div>\s*', '', l_html)
l_html = l_html.replace('<div><strong>Evaluation:</strong> 100% Practical Verified</div>', '<div><strong>Focus:</strong> Industrial AI & Edge Computing</div>')

# Write to MaintAI_Poster_A2_Landscape.html
with open(os.path.join(BASE, "MaintAI_Poster_A2_Landscape.html"), "w", encoding="utf-8") as f:
    f.write(l_html)
print("[OK] Written MaintAI_Poster_A2_Landscape.html")

# 2. PORTRAIT
with open(os.path.join(BASE, "test_dense_portrait.html"), "r", encoding="utf-8") as f:
    p_html = f.read()

# Replace font-body with Cambria
p_html = p_html.replace(
    '--font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;',
    '--font-body: "Cambria", Georgia, "Times New Roman", serif;'
)
p_html = p_html.replace("@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');", "")

# Scale Title per guidelines (36 pt)
p_html = p_html.replace("font-size: 26pt;", "font-size: 35pt;")
p_html = p_html.replace("font-size: 14pt;\n      font-weight: 700;\n      color: var(--ppsu-blue);", "font-size: 17pt;\n      font-weight: bold;\n      color: var(--ppsu-blue);")

# Replace QR code in portrait
p_html = re.sub(
    r'<img src="data:image/png;base64,[A-Za-z0-9+/=]+" alt="Demo QR"',
    f'<img src="{qr_b64}" alt="Demo QR"',
    p_html
)

# Remove verified line in portrait
p_html = re.sub(r'<span style="color:#b31b1b; font-weight:800;">\[APPROVED FOR B\.TECH DEFENSE - 100% VERIFIED\]</span>\s*', '', p_html)

# Write to MaintAI_Poster_A2_Portrait.html
with open(os.path.join(BASE, "MaintAI_Poster_A2_Portrait.html"), "w", encoding="utf-8") as f:
    f.write(p_html)
print("[OK] Written MaintAI_Poster_A2_Portrait.html")

# 3. COMPILE TO PDF AND RENDER PREVIEWS
chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def compile_pdf(html_file, pdf_file):
    url = "file:///" + os.path.abspath(html_file).replace("\\", "/")
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        url
    ]
    subprocess.run(cmd, check=True)
    doc = pymupdf.open(pdf_file)
    print(f"[COMPILED] {pdf_file}: {len(doc)} page(s), {os.path.getsize(pdf_file)} bytes")
    return len(doc)

def render_png(pdf_file, png_file, dpi=120):
    doc = pymupdf.open(pdf_file)
    pix = doc[0].get_pixmap(dpi=dpi)
    pix.save(png_file)
    print(f"[RENDERED] {png_file}: {pix.width}x{pix.height}")

l_pages = compile_pdf(os.path.join(BASE, "MaintAI_Poster_A2_Landscape.html"), os.path.join(BASE, "MaintAI_Poster_A2_Landscape.pdf"))
render_png(os.path.join(BASE, "MaintAI_Poster_A2_Landscape.pdf"), os.path.join(BASE, "pdf_images", "preview_landscape_ppsu_final.png"))

p_pages = compile_pdf(os.path.join(BASE, "MaintAI_Poster_A2_Portrait.html"), os.path.join(BASE, "MaintAI_Poster_A2_Portrait.pdf"))
render_png(os.path.join(BASE, "MaintAI_Poster_A2_Portrait.pdf"), os.path.join(BASE, "pdf_images", "preview_portrait_ppsu_final.png"))

# Mirror to downloads
import shutil
downloads = r"C:\Users\hetjo\Downloads"
shutil.copy2(os.path.join(BASE, "MaintAI_Poster_A2_Landscape.pdf"), os.path.join(downloads, "MaintAI_Poster_A2_Landscape.pdf"))
shutil.copy2(os.path.join(BASE, "MaintAI_Poster_A2_Portrait.pdf"), os.path.join(downloads, "MaintAI_Poster_A2_Portrait.pdf"))
shutil.copy2(os.path.join(BASE, "MaintAI_Poster_A2_Portrait.pdf"), os.path.join(BASE, "Het_003_poster.pdf"))
print("[MIRRORED] Copied to Downloads and Het_003_poster.pdf")
