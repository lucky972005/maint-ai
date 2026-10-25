#!/usr/bin/env python3
"""
Generates high-tech telemetry banner matching the uploaded Tailwind Traders reference.
Features:
- Dark navy background (#0D1E36 to #153258 gradient)
- Glowing cyan, electric blue, and subtle red vertical histogram bars
- Overlay binary code digits ('0 1 1 0 1 0 0 1') and telemetry grid lines
- Soft depth blur and particle glow
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH = 2400
HEIGHT = 1000

# Create base image with deep navy gradient
im = Image.new("RGB", (WIDTH, HEIGHT), (13, 30, 54))
draw = ImageDraw.Draw(im)

# Vertical gradient from darker navy to slightly lighter teal-navy
for y in range(HEIGHT):
    factor = y / HEIGHT
    r = int(10 + factor * 12)
    g = int(24 + factor * 28)
    b = int(48 + factor * 45)
    draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

# Create glow overlay
glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_layer)

# Draw subtle grid lines
for x in range(0, WIDTH, 80):
    glow_draw.line([(x, 0), (x, HEIGHT)], fill=(56, 189, 248, 18), width=1)
for y in range(0, HEIGHT, 80):
    glow_draw.line([(0, y), (WIDTH, y)], fill=(56, 189, 248, 18), width=1)

# Draw vertical data histogram bars (cyan, electric blue, coral red)
random.seed(42)
num_bars = 48
bar_width = 24
gap = 46

for i in range(num_bars):
    x = 100 + i * gap
    # Height distribution with dynamic peaks in center
    norm_x = (x - WIDTH / 2) / (WIDTH / 2)
    base_h = int(HEIGHT * (0.35 + 0.5 * math.exp(-norm_x**2 * 2.2)))
    h = int(base_h * (0.6 + 0.8 * random.random()))
    y1 = HEIGHT - int((HEIGHT - h) * 0.45)
    y0 = y1 - h

    # Color choice: mostly cyan and electric blue, with some coral/red bars
    is_red = random.random() < 0.22 and (WIDTH * 0.4 < x < WIDTH * 0.85)
    if is_red:
        color = (244, 63, 94, 200)      # Coral red
        glow_color = (244, 63, 94, 70)
    else:
        # Cyan to electric blue
        color = (56, 189, 248, 220) if random.random() < 0.65 else (34, 110, 253, 210)
        glow_color = (56, 189, 248, 80)

    # Draw glow behind
    glow_draw.rectangle([x - 6, y0 - 6, x + bar_width + 6, y1 + 6], fill=glow_color)
    # Draw core bar
    glow_draw.rectangle([x, y0, x + bar_width, y1], fill=color)
    # Top highlight cap
    glow_draw.rectangle([x, y0, x + bar_width, y0 + 6], fill=(255, 255, 255, 240))

# Blur the glow layer slightly and composite
blurred_glow = glow_layer.filter(ImageFilter.GaussianBlur(radius=8))
im.paste(blurred_glow, (0, 0), blurred_glow)
im.paste(glow_layer, (0, 0), glow_layer)

# Draw crisp binary stream columns like in reference: '1 0 0 1 0 1'
text_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
text_draw = ImageDraw.Draw(text_layer)

binary_cols = [
    (140, "1 0 0 0 1 0 1"),
    (320, "0 0 0 1 0 1"),
    (580, "1 0 0 0 1 0 1"),
    (1420, "10 10 10"),
    (1680, "10 10"),
    (2220, "0 0 1 0 1")
]

for col_x, bin_str in binary_cols:
    chars = bin_str.split()
    start_y = random.randint(120, 250)
    for c_idx, ch in enumerate(chars):
        cy = start_y + c_idx * 56
        # Draw large binary number
        text_draw.text((col_x, cy), ch, fill=(255, 255, 255, 140))

# Draw the big "10" and "0 1" prominently on right like in reference
text_draw.text((1540, 480), "10", fill=(255, 255, 255, 210))
text_draw.text((1720, 520), "10", fill=(255, 255, 255, 190))
text_draw.text((2240, 360), "0", fill=(56, 189, 248, 220))
text_draw.text((2340, 380), "1", fill=(255, 255, 255, 200))

# Composite text layer
im.paste(text_layer, (0, 0), text_layer)

output_path = "public/tailwind_style_banner.png"
im.save(output_path, "PNG")
print(f"[SUCCESS] Generated high-tech telemetry banner: {output_path} ({WIDTH}x{HEIGHT})")
