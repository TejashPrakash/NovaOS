"""Vibrant AI-themed animated desktop background for NovaOS."""

import random
import math
import customtkinter as ctk


class AIBackground(ctk.CTkFrame):
    """Animated AI-themed background with gradient, particles, grid, and glowing orbs."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="#050810", **kwargs)

        self._canvas = None
        self._w = 0
        self._h = 0
        self._particles = []
        self._orbs = []
        self._grid_lines = []
        self._step = 0
        self._build()

    def _build(self):
        self._canvas = ctk.CTkCanvas(
            self, highlightthickness=0, bg="#050810"
        )
        self._canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bind("<Configure>", self._on_resize)
        self.after(100, self._init_scene)

    def _on_resize(self, event):
        self._w = event.width
        self._h = event.height
        self._init_scene()

    def _init_scene(self):
        if self._w < 10 or self._h < 10:
            return

        self._particles = []
        for _ in range(60):
            self._particles.append({
                "x": random.uniform(0, self._w),
                "y": random.uniform(0, self._h),
                "vx": random.uniform(-0.4, 0.4),
                "vy": random.uniform(-0.6, -0.1),
                "size": random.randint(1, 4),
                "brightness": random.randint(30, 150),
                "hue": random.choice(["cyan", "purple", "magenta", "blue"]),
            })

        self._orbs = []
        orb_colors = ["#00E5FF20", "#7B61FF18", "#FF00E515", "#00FF8810"]
        for _ in range(5):
            self._orbs.append({
                "x": random.uniform(100, self._w - 100),
                "y": random.uniform(100, self._h - 100),
                "vx": random.uniform(-0.3, 0.3),
                "vy": random.uniform(-0.3, 0.3),
                "radius": random.randint(80, 200),
                "color": random.choice(orb_colors),
                "pulse_speed": random.uniform(0.02, 0.06),
                "pulse_offset": random.uniform(0, math.pi * 2),
            })

        self._animate()

    def _animate(self):
        if self._w < 10 or self._h < 10:
            self.after(50, self._animate)
            return

        self._canvas.delete("all")
        self._step += 1

        self._draw_gradient_bg()
        self._draw_grid()
        self._draw_orbs()
        self._draw_particles()
        self._draw_connections()

        self.after(40, self._animate)

    def _draw_gradient_bg(self):
        """Draw a subtle radial gradient from center."""
        cx, cy = self._w // 2, self._h // 2
        max_dist = math.sqrt(cx**2 + cy**2)

        steps = 12
        for i in range(steps):
            ratio = i / steps
            r = int(5 + 8 * ratio)
            g = int(8 + 12 * (1 - ratio))
            b = int(16 + 20 * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"

            radius = int(max_dist * (1 - ratio))
            self._canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                fill=color, outline=""
            )

    def _draw_grid(self):
        """Draw subtle animated grid lines."""
        spacing = 80
        grid_color = "#0D1520"

        for x in range(0, self._w, spacing):
            self._canvas.create_line(
                x, 0, x, self._h,
                fill=grid_color, width=1
            )
        for y in range(0, self._h, spacing):
            self._canvas.create_line(
                0, y, self._w, y,
                fill=grid_color, width=1
            )

        # Animated scan line
        scan_y = (self._step * 2) % self._h
        scan_alpha = "#0A1A2A"
        self._canvas.create_line(
            0, scan_y, self._w, scan_y,
            fill=scan_alpha, width=2
        )

    def _draw_orbs(self):
        """Draw floating glowing orbs."""
        for orb in self._orbs:
            orb["x"] += orb["vx"]
            orb["y"] += orb["vy"]

            if orb["x"] < -orb["radius"]:
                orb["x"] = self._w + orb["radius"]
            elif orb["x"] > self._w + orb["radius"]:
                orb["x"] = -orb["radius"]
            if orb["y"] < -orb["radius"]:
                orb["y"] = self._h + orb["radius"]
            elif orb["y"] > self._h + orb["radius"]:
                orb["y"] = -orb["radius"]

            pulse = 0.7 + 0.3 * math.sin(
                self._step * orb["pulse_speed"] + orb["pulse_offset"]
            )
            r = int(orb["radius"] * pulse)

            for ring in range(3, 0, -1):
                ring_r = r * (ring * 0.8)
                alpha = int(20 / ring)
                color_hex = orb["color"][:7]
                r_val = int(color_hex[1:3], 16)
                g_val = int(color_hex[3:5], 16)
                b_val = int(color_hex[5:7], 16)
                r_adj = min(255, r_val + alpha)
                g_adj = min(255, g_val + alpha)
                b_adj = min(255, b_val + alpha)
                ring_color = f"#{r_adj:02x}{g_adj:02x}{b_adj:02x}"

                self._canvas.create_oval(
                    orb["x"] - ring_r, orb["y"] - ring_r,
                    orb["x"] + ring_r, orb["y"] + ring_r,
                    fill="", outline=ring_color, width=1
                )

            # Core
            core_color = orb["color"][:7]
            self._canvas.create_oval(
                orb["x"] - r * 0.3, orb["y"] - r * 0.3,
                orb["x"] + r * 0.3, orb["y"] + r * 0.3,
                fill=core_color, outline=""
            )

    def _draw_particles(self):
        """Draw floating particles with trails."""
        color_map = {
            "cyan": "#00E5FF",
            "purple": "#7B61FF",
            "magenta": "#FF00E5",
            "blue": "#2979FF",
        }

        for p in self._particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]

            if p["y"] < -20:
                p["y"] = self._h + 20
                p["x"] = random.uniform(0, self._w)
            if p["x"] < -20:
                p["x"] = self._w + 20
            elif p["x"] > self._w + 20:
                p["x"] = -20

            color = color_map.get(p["hue"], "#00E5FF")
            brightness = p["brightness"]
            b = min(255, brightness + int(30 * math.sin(self._step * 0.05 + p["x"] * 0.01)))
            glow_color = f"#{min(255, int(color[1:3], 16) + b // 4):02x}{min(255, int(color[3:5], 16) + b // 4):02x}{min(255, int(color[5:7], 16) + b // 4):02x}"

            # Trail
            trail_len = p["size"] * 3
            self._canvas.create_line(
                p["x"], p["y"],
                p["x"] - p["vx"] * trail_len,
                p["y"] - p["vy"] * trail_len,
                fill=glow_color, width=1
            )

            # Particle
            self._canvas.create_oval(
                p["x"] - p["size"], p["y"] - p["size"],
                p["x"] + p["size"], p["y"] + p["size"],
                fill=color, outline=""
            )

    def _draw_connections(self):
        """Draw connections between nearby particles."""
        max_dist = 150
        for i, p1 in enumerate(self._particles):
            for p2 in self._particles[i+1:i+8]:
                dx = p1["x"] - p2["x"]
                dy = p1["y"] - p2["y"]
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < max_dist:
                    alpha = int(40 * (1 - dist / max_dist))
                    self._canvas.create_line(
                        p1["x"], p1["y"], p2["x"], p2["y"],
                        fill=f"#{alpha:02x}{alpha + 20:02x}{alpha + 40:02x}",
                        width=1
                    )
