import os
from PIL import Image, ImageDraw, ImageFont

W, H = 2000, 650
img = Image.new('RGB', (W, H), '#FFFFFF')
draw = ImageDraw.Draw(img)
font_bold = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 22)
font_reg = ImageFont.truetype(r'C:\Windows\Fonts\segoeui.ttf', 16)
font_title = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', 28)

draw.rectangle([0, 0, W, 70], fill='#0F172A')
draw.text((W // 2, 35), 'Figure 10.1: MaintAI Live Field Demonstration & End-to-End Operational Workflow', fill='#FFFFFF', font=font_title, anchor='mm')

steps = [
    ('Step 1: Machine QR Scan', ['• Scan QR on equipment chassis', '• Instant offline profile fetch', '• Active alarms & SOP loaded'], '#EFF6FF', '#2563EB'),
    ('Step 2: AR Guidance & Voice', ['• Pulsing component markers', '• Lockout safety verification', '• Hands-free voice commands'], '#F0FDF4', '#16A34A'),
    ('Step 3: AI Tool Verification', ['• Camera snapshot of workbench', '• Gemini 1.5 Flash bounding box', '• Safety gate unlocks on match'], '#FEF3C7', '#D97706'),
    ('Step 4: Offline Log & Stock Sync', ['• Write-ahead Dexie.js commit', '• Auto-decrement spare parts', '• Background replay to cloud'], '#FAF5FF', '#7C3AED')
]

for i, (title, lines, bg, bdr) in enumerate(steps):
    x = 60 + i * 480
    draw.rounded_rectangle([x, 130, x + 440, 560], radius=14, fill=bg, outline=bdr, width=3)
    draw.rounded_rectangle([x, 130, x + 440, 195], radius=14, fill=bdr)
    draw.text((x + 220, 162), title, fill='#FFFFFF', font=font_bold, anchor='mm')
    
    y = 230
    for line in lines:
        draw.text((x + 30, y), line, fill='#1E293B', font=font_reg)
        y += 45

    if i < 3:
        draw.line([x + 440, 345, x + 480, 345], fill='#475569', width=4)
        draw.polygon([(x + 480, 345), (x + 465, 335), (x + 465, 355)], fill='#475569')

os.makedirs('pdf_images', exist_ok=True)
img.save('pdf_images/fig_10_1_demo_flow.png', quality=95)
print('Generated pdf_images/fig_10_1_demo_flow.png successfully!')
