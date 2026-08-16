import customtkinter as ctk
import random
import math


class AmbientLighting(ctk.CTkFrame):
    """Ambient lighting effects for premium atmosphere."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color="transparent",
            **kwargs
        )
        self.light_orbs = []
        self.animation_time = 0
        self._setup_lighting()
        self._animate_lights()
        
    def _setup_lighting(self):
        """Setup ambient light orbs."""
        colors = ["#00E5FF", "#7B61FF", "#FF00E5"]
        
        for i in range(6):
            orb = ctk.CTkFrame(
                self,
                width=random.randint(80, 150),
                height=random.randint(80, 150),
                fg_color=random.choice(colors),
                corner_radius=40
            )
            
            x = random.randint(100, 1500)
            y = random.randint(100, 800)
            orb.place(x=x, y=y)
            
            self.light_orbs.append({
                "orb": orb,
                "x": x,
                "y": y,
                "vx": random.uniform(-0.2, 0.2),
                "vy": random.uniform(-0.2, 0.2),
                "base_alpha": random.uniform(0.1, 0.25)
            })
            
    def _animate_lights(self):
        """Animate ambient lighting."""
        self.animation_time += 0.05
        
        for light in self.light_orbs:
            light["x"] += light["vx"]
            light["y"] += light["vy"]
            
            # Bounce off edges
            if light["x"] < 50 or light["x"] > 1550:
                light["vx"] *= -1
            if light["y"] < 50 or light["y"] > 850:
                light["vy"] *= -1
                
            # Pulsate alpha
            pulsating_alpha = light["base_alpha"] + 0.1 * math.sin(self.animation_time + light["x"] * 0.01)
            pulsating_alpha = max(0.05, min(0.35, pulsating_alpha))
            
            # Update position
            light["orb"].place(x=light["x"], y=light["y"])
            
        self.after(50, self._animate_lights)