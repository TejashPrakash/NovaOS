import customtkinter as ctk
import random
import math


class NeuralBackground(ctk.CTkFrame):
    """Animated neural network background for premium AI aesthetic."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color="#0A0E14",
            **kwargs
        )
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
            bg="#0A0E14"
        )
        self.canvas.pack(fill="both", expand=True)
        
    def _create_neural_network(self):
        """Create neural network nodes and connections."""
        # Create nodes
        for _ in range(50):
            x = random.randint(0, 2000)
            y = random.randint(0, 2000)
            size = random.randint(2, 6)
            self.nodes.append({"x": x, "y": y, "size": size, "vx": random.uniform(-0.5, 0.5), "vy": random.uniform(-0.5, 0.5)})
            
        # Create connections
        for i, node1 in enumerate(self.nodes):
            for node2 in self.nodes[i+1:]:
                distance = math.sqrt((node1["x"] - node2["x"])**2 + (node1["y"] - node2["y"])**2)
                if distance < 200:
                    self.connections.append({"node1": node1, "node2": node2, "distance": distance})
                    
    def _animate(self):
        """Animate neural network."""
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
                
        # Draw connections
        for connection in self.connections:
            node1 = connection["node1"]
            node2 = connection["node2"]
            distance = math.sqrt((node1["x"] - node2["x"])**2 + (node1["y"] - node2["y"])**2)
            
            if distance < 200:
                alpha = int(255 * (1 - distance / 200))
                self.canvas.create_line(
                    node1["x"], node1["y"],
                    node2["x"], node2["y"],
                    fill="#00E5FF",
                    width=1
                )
                
        # Draw nodes
        for node in self.nodes:
            self.canvas.create_oval(
                node["x"] - node["size"],
                node["y"] - node["size"],
                node["x"] + node["size"],
                node["y"] + node["size"],
                fill="#00E5FF",
                outline=""
            )
            
        self.after(50, self._animate)