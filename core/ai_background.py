"""Vibrant AI-themed desktop background for NovaOS — generates wallpaper image with Pillow."""

import random
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

WALLPAPER_PATH = Path(__file__).resolve().parent.parent / "data" / "ai_wallpaper.png"


def generate_ai_wallpaper(width=1920, height=1080):
    """Generate a vibrant AI-themed gradient wallpaper with glowing orbs and grid."""

    # Deep dark blue base
    img = Image.new("RGB", (width, height), (5, 8, 20))
    draw = ImageDraw.Draw(img)

    # ---- Horizontal gradient: dark center -> brighter purple/cyan edges ----
    for y in range(height):
        ratio_y = y / height
        for x in range(0, width, 2):
            ratio_x = x / width
            # Dark in center, brighter toward edges
            edge = max(abs(ratio_x - 0.5), abs(ratio_y - 0.5)) * 2
            r = int(8 + 30 * edge)
            g = int(5 + 15 * edge)
            b = int(20 + 60 * edge)
            draw.rectangle([x, y, x + 1, y + 1], fill=(r, g, b))

    # ---- Bright grid lines ----
    grid_color = (12, 25, 45)
    spacing = 50
    for x in range(0, width, spacing):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, spacing):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # ---- Large glowing orbs — MUCH brighter ----
    orb_colors = [
        (0, 229, 255),    # bright cyan
        (100, 80, 255),   # purple
        (255, 0, 200),    # magenta
        (0, 255, 120),    # green
        (60, 130, 255),   # blue
    ]

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    orb_draw = ImageDraw.Draw(overlay)

    for _ in range(12):
        color = random.choice(orb_colors)
        ox = random.randint(50, width - 50)
        oy = random.randint(50, height - 50)
        radius = random.randint(120, 300)

        # Large soft glow rings — much higher alpha
        for ring in range(10, 0, -1):
            r = int(radius * ring * 0.25)
            alpha = max(8, int(120 / ring))
            orb_draw.ellipse(
                [ox - r, oy - r, ox + r, oy + r],
                fill=(color[0], color[1], color[2], alpha)
            )

        # Bright solid core
        core_r = int(radius * 0.12)
        orb_draw.ellipse(
            [ox - core_r, oy - core_r, ox + core_r, oy + core_r],
            fill=(color[0], color[1], color[2], 200)
        )

    # Blur for soft glow
    overlay_blurred = overlay.filter(ImageFilter.GaussianBlur(radius=50))

    # Composite
    img_rgba = img.convert("RGBA")
    composite = Image.alpha_composite(img_rgba, overlay_blurred)
    img = composite.convert("RGB")
    draw = ImageDraw.Draw(img)

    # ---- Bright floating particles ----
    particle_colors = [(0, 229, 255), (100, 80, 255), (255, 0, 200), (60, 130, 255), (0, 255, 120)]
    particles = []
    for _ in range(150):
        px = random.randint(0, width)
        py = random.randint(0, height)
        size = random.randint(1, 5)
        color = random.choice(particle_colors)
        draw.ellipse([px, py, px + size, py + size], fill=color)
        particles.append((px, py))

    # ---- Connection lines between nearby particles ----
    for i, p1 in enumerate(particles):
        for p2 in particles[i + 1 : i + 6]:
            dist = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
            if dist < 120:
                a = int(80 * (1 - dist / 120))
                draw.line([p1, p2], fill=(a, a + 30, a + 60), width=1)

    # ---- Subtle horizontal scan lines ----
    for y in range(0, height, 3):
        if y % 6 == 0:
            draw.line([(0, y), (width, y)], fill=(0, 0, 0), width=1)

    # Save
    WALLPAPER_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(WALLPAPER_PATH), "PNG")
    return str(WALLPAPER_PATH)


def ensure_wallpaper():
    """Generate wallpaper if it doesn't exist or is too small, return path."""
    if not WALLPAPER_PATH.exists() or WALLPAPER_PATH.stat().st_size < 100_000:
        generate_ai_wallpaper()
    return str(WALLPAPER_PATH)
