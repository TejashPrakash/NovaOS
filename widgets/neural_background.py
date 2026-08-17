import customtkinter as ctk
import random
import math
from core.theme import ThemeManager


class NeuralBackground(ctk.CTkFrame):
    """Animated neural network background with theme integration."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color="#0A0E14",
            **kwargs
        )
        self.theme = ThemeManager()
        self.nodes = []
        self.connections = []
        self._setup_canvas()
        self._create_neural_network()
        self._animate()
    
    def _setup_canvas(self):
        """Setup canvas for neural network animation."""
        self.canvas = ctk.CTkCanvas(
            self,
            width=2000,
            height=2000,
            highlightthickness=0,
            bg=self.theme.get_color("background")
        )
        self.canvas.pack(fill="both", expand=True)
    
    def _create_neural_network(self):
        """Create neural network nodes and connections."""
        # Create nodes
        for _ in range(50):
            x = random.randint(0, 2000)
            y = random.randint(0, 2000)
            size = random.randint(2, 6)
            self.nodes.append({
                "x": x, 
                "y": y, 
                "size": size, 
                "vx": random.uniform(-0.5, 0.5), 
                "vy": random.uniform(-0.5, 0.5)
            })
        
        # Create connections
        for i, node1 in enumerate(self.nodes):
            for node2 in self.nodes[i+1:]:
                distance = math.sqrt((node1["x"] - node2["x"])**2 + (node1["y"] - node2["y"])**2)
                if distance < 200:
                    self.connections.append({
                        "node1": node1, 
                        "node2": node2, 
                        "distance": distance
                    })
    
    def _animate(self):
        """Animate neural network with theme colors."""
        self.canvas.delete("all")
        
        # Update node positions
        for node in self.nodes:
            node["x"] += node["vx"]
            node["y"] += node["vy"]
            
            # Bounce off edges
            if node["x"] < 0 or node["x"] > 2000:
                node["vx"] *= -1
            if node["y"] < 0 or node["y"] > 2000:
                node["vy"] *= -1
        
        # Draw connections with theme colors
        primary_color = self.theme.get_color("primary")
        secondary_color = self.theme.get_color("secondary")
        
        for connection in self.connections:
            node1 = connection["node1"]
            node2 = connection["node2"]
            distance = math.sqrt((node1["x"] - node2["x"])**2 + (node1["y"] - node2["y"])**2)
            
            if distance < 200:
                # Alternate between primary and secondary colors
                color = primary_color if random.random() > 0.5 else secondary_color
                self.canvas.create_line(
                    node1["x"], node1["y"],
                    node2["x"], node2["y"],
                    fill=color,
                    width=1
                )
        
        # Draw nodes with theme colors
        accent_color = self.theme.get_color("accent")
        for node in self.nodes:
            node_color = primary_color if random.random() > 0.3 else accent_color
            self.canvas.create_oval(
                node["x"] - node["size"],
                node["y"] - node["size"],
                node["x"] + node["size"],
                node["y"] + node["size"],
                fill=node_color,
                outline=""
            )
        
        self.after(50, self._animate)