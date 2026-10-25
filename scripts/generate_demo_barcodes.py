import os
import barcode
from barcode.writer import ImageWriter
import qrcode
from PIL import Image

output_dir = r"c:\dev\pro\pdf_images"
os.makedirs(output_dir, exist_ok=True)

# 1. Generate Parts Barcodes (Code 128)
parts = [
    ("PN-01001", "barcode_pn_01001.png"),
    ("PN-01002", "barcode_pn_01002.png"),
    ("PN-01004", "barcode_pn_01004.png"),
    ("PN-01006", "barcode_pn_01006.png"),
]

code128 = barcode.get_barcode_class('code128')

for code_text, filename in parts:
    filepath = os.path.join(output_dir, filename.replace('.png', ''))
    bc = code128(code_text, writer=ImageWriter())
    # Save barcode
    full_path = bc.save(filepath, options={
        'module_width': 0.35,
        'module_height': 15.0,
        'font_size': 12,
        'text_distance': 4.0,
        'quiet_zone': 4.0,
        'write_text': True,
    })
    print(f"Generated barcode: {full_path}")

# 2. Generate Machine QR Codes
machine_qrs = [
    ("MACHINE:haas-vf-2-001", "qr_haas_cnc.png"),
    ("MACHINE:siemens-1le0102-001", "qr_siemens_motor.png"),
    ("MACHINE:atlas-ga-37-001", "qr_atlas_compressor.png"),
    ("MACHINE:flexco-1900-001", "qr_flexco_conveyor.png"),
    ("https://maint-ai.vercel.app/scan", "qr_app_scan_launcher.png"),
    ("https://maint-ai.vercel.app", "qr_app_home_launcher.png"),
]

for text, filename in machine_qrs:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0f172a", back_color="#ffffff")
    out_path = os.path.join(output_dir, filename)
    img.save(out_path)
    print(f"Generated QR: {out_path} -> {text}")

print("All demo barcode & QR assets successfully generated.")
