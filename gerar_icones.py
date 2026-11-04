#!/usr/bin/env python3
"""Gera todos os ícones do PWA. Requer Pillow: pip install Pillow"""
from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('icons', exist_ok=True)

BG_TOP = (15, 23, 42)       # #0f172a
BG_BOTTOM = (30, 41, 59)    # #1e293b
ACCENT = (56, 189, 248)     # #38bdf8
ACCENT2 = (124, 58, 237)    # #7c3aed
YELLOW = (250, 204, 21)     # #facc15

def draw_icon(size, maskable=False):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fundo com gradiente vertical
    for y in range(size):
        t = y / size
        r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Se maskable, mantém padding de 20% (safe zone)
    pad = size * 0.2 if maskable else size * 0.1
    inner = size - 2 * pad

    # Círculo de destaque (gradiente simulado)
    cx, cy = size // 2, size // 2
    radius = inner // 2
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=ACCENT2 + (255,))
    r2 = int(radius * 0.75)
    draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=ACCENT + (255,))

    # Triângulo "play" no centro (branco)
    tri = radius * 0.55
    points = [
        (cx - tri * 0.5, cy - tri),
        (cx - tri * 0.5, cy + tri),
        (cx + tri * 0.9, cy),
    ]
    draw.polygon(points, fill=(255, 255, 255, 255))

    # Borda amarela (D-Pad focus)
    border = max(2, size // 40)
    draw.rectangle([border, border, size - border, size - border], outline=YELLOW + (255,), width=border)

    return img

# Icon 192
draw_icon(192).save('icons/icon-192.png')

# Icon 512
draw_icon(512).save('icons/icon-512.png')

# Icon 512 maskable (safe zone maior)
draw_icon(512, maskable=True).save('icons/icon-512-maskable.png')

# Favicon 64
draw_icon(64).save('icons/favicon.png')

print('✅ Ícones gerados em ./icons/')