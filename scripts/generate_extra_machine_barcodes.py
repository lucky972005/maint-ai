import os
import barcode
from barcode.writer import ImageWriter
import qrcode

out_dir = r"c:\dev\pro\pdf_images"
os.makedirs(out_dir, exist_ok=True)

# 1. QR Codes for machines
machines = [
    ("MACHINE:grundfos-cr-15-001", "qr_grundfos_pump.png"),
    ("MACHINE:cummins-c110d5-001", "qr_cummins_gen.png"),
    ("MACHINE:schuler-ph-400-001", "qr_schuler_press.png"),
    ("MACHINE:haas-vf-2-001", "qr_haas_cnc.png"),
    ("MACHINE:siemens-1le0102-001", "qr_siemens_motor.png"),
    ("MACHINE:atlas-ga-37-001", "qr_atlas_compressor.png"),
]

for text, fn in machines:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0b1120", back_color="#ffffff")
    img.save(os.path.join(out_dir, fn))
    print(f"QR Generated: {fn} -> {text}")

# 2. Code 128 Asset Barcodes
code128 = barcode.get_barcode_class('code128')
barcodes = [
    ("EQ-CR15-2022", "bc_grundfos.png"),
    ("EQ-C110-2019", "bc_cummins.png"),
    ("EQ-PH400-2020", "bc_schuler.png"),
]

for text, fn in barcodes:
    bc = code128(text, writer=ImageWriter())
    p = bc.save(os.path.join(out_dir, fn.replace('.png', '')), options={
        'module_width': 0.35,
        'module_height': 14.0,
        'font_size': 11,
        'text_distance': 4.0,
        'quiet_zone': 3.0,
        'write_text': True,
    })
    print(f"Barcode Generated: {p}")

print("Done generating extra machine assets.")
