"""Vibrant AI-themed desktop background for NovaOS — generates wallpaper image with Pillow."""

import random
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

WALLPAPER_PATH = Path(__file__).resolve().parent.parent / "data" / "ai_wallpaper.png"


def generate_ai_wallpaper(width=1920, height=1080):
    """Generate a vibrant AI-themed gradient wallpaper with glowing orbs and grid."""

    # Start with deep blue-purple base
    img = Image.new("RGB", (width, height), (8, 10, 25))
    draw = ImageDraw.Draw(img)

    # ---- Radial gradient with vibrant colors ----
    cx, cy = width // 2, height // 2
    max_dist = math.sqrt(cx**2 + cy**2)

    for y in range(0, height, 2):
        for x in range(0, width, 2):
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            ratio = min(dist / max_dist, 1.0)

            # Dark center, brighter edges with purple/cyan tint
            r = int(15 + 25 * ratio)
            g = int(10 + 20 * ratio * (1 - ratio) * 3)
            b = int(35 + 50 * ratio)

            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            draw.rectangle([x, y, x + 1, y + 1], fill=(r, g, b))

    # ---- Bright grid lines ----
    grid_color = (15, 30, 50)
    spacing = 60
    for x in range(0, width, spacing):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, spacing):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # ---- Large glowing orbs with RGBA overlay ----
    orb_colors = [
        (0, 229, 255),    # bright cyan
        (123, 97, 255),   # purple
        (255, 0, 229),    # magenta
        (0, 255, 136),    # green
        (41, 121, 255),   # blue
    ]

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    orb_draw = ImageDraw.Draw(overlay)

    for _ in range(10):
        color = random.choice(orb_colors)
        ox = random.randint(100, width - 100)
        oy = random.randint(100, height - 100)
        radius = random.randint(100, 250)

        # Multiple rings for glow effect
        for ring in range(8, 0, -1):
            r = int(radius * ring * 0.3)
            alpha = int(40 / ring)
            orb_draw.ellipse(
                [ox - r, oy - r, ox + r, oy + r],
                fill=(color[0], color[1], color[2], alpha)
            )

        # Bright core
        core_r = int(radius * 0.15)
        orb_draw.ellipse(
            [ox - core_r, oy - core_r, ox + core_r, oy + core_r],
            fill=(color[0], color[1], color[2], 120)
        )

    # Blur for soft glow
    overlay_blurred = overlay.filter(ImageFilter.GaussianBlur(radius=40))

    # Composite
    img_rgba = img.convert("RGBA")
    composite = Image.alpha_composite(img_rgba, overlay_blurred)
    img = composite.convert("RGB")
    draw = ImageDraw.Draw(img)

    # ---- Bright floating particles ----
    particle_colors = [(0, 229, 255), (123, 97, 255), (255, 0, 229), (41, 121, 255)]
    particles = []
    for _ in range(100):
        px = random.randint(0, width)
        py = random.randint(0, height)
        size = random.randint(1, 4)
        color = random.choice(particle_colors)
        draw.ellipse([px, py, px + size, py + size], fill=color)
        particles.append((px, py))

    # ---- Connection lines ----
    for i, p1 in enumerate(particles):
        for p2 in particles[i + 1:i + 5]:
            dist = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
            if dist < 150:
                a = int(60 * (1 - dist / 150))
                draw.line(
                    [p1, p2],
                    fill=(a, a + 20, a + 50),
                    width=1
                )

    # ---- Subtle horizontal scan lines ----
    for y in range(0, height, 4):
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, 15) if y % 8 == 0 else (0, 0, 0, 0), width=1)

    # Save
    WALLPAPER_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(WALLPAPER_PATH), "PNG")
    return str(WALLPAPER_PATH)


def ensure_wallpaper():
    """Generate wallpaper if it doesn't exist, return path."""
    if not WALLPAPER_PATH.exists():
        generate_ai_wallpaper()
    return str(WALLPAPER_PATH)
