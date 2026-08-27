import tkinter as tk
import random
import math
from core.theme import ThemeManager


class NeuralBackground(tk.Canvas):
    """Animated neural network background with theme integration.

    Uses tkinter.Canvas directly (not CTkCanvas) to avoid
    the CTkFrame._w int + str crash on Windows.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            highlightthickness=0,
            bg="#0A0E14",
            **kwargs
        )
        self.theme = ThemeManager()
        self.nodes = []
        self.connections = []
        self._create_neural_network()
        self._animate()

    def _create_neural_network(self):
        """Create neural network nodes and connections."""
        for _ in range(50):
            x = random.randint(0, 2000)
            y = random.randint(0, 2000)
            size = random.randint(2, 6)
            self.nodes.append({
                "x": x,
                "y": y,
                "size": size,
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(-0.5, 0.5),
            })

        for i, node1 in enumerate(self.nodes):
            for node2 in self.nodes[i + 1 :]:
                dist = math.sqrt(
                    (node1["x"] - node2["x"]) ** 2
                    + (node1["y"] - node2["y"]) ** 2
                )
                if dist < 200:
                    self.connections.append({
                        "node1": node1,
                        "node2": node2,
                        "distance": dist,
                    })

    def _animate(self):
        """Animate neural network with theme colors."""
        try:
            self.delete("all")

            for node in self.nodes:
                node["x"] += node["vx"]
                node["y"] += node["vy"]
                if node["x"] < 0 or node["x"] > 2000:
                    node["vx"] *= -1
                if node["y"] < 0 or node["y"] > 2000:
                    node["vy"] *= -1

            primary = self.theme.get_color("primary")
            secondary = self.theme.get_color("secondary")
            accent = self.theme.get_color("accent")

            for conn in self.connections:
                n1, n2 = conn["node1"], conn["node2"]
                d = math.sqrt(
                    (n1["x"] - n2["x"]) ** 2 + (n1["y"] - n2["y"]) ** 2
                )
                if d < 200:
                    color = primary if random.random() > 0.5 else secondary
                    self.create_line(
                        n1["x"], n1["y"], n2["x"], n2["y"],
                        fill=color, width=1,
                    )

            for node in self.nodes:
                node_color = primary if random.random() > 0.3 else accent
                s = node["size"]
                self.create_oval(
                    node["x"] - s, node["y"] - s,
                    node["x"] + s, node["y"] + s,
                    fill=node_color, outline="",
                )

            self.after(50, self._animate)
        except Exception:
            pass
