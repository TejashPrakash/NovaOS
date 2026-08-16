import customtkinter as ctk
from typing import Callable, Optional
import math


class AnimationEngine:
    """Smooth animation engine for premium UI effects."""
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Cubic easing in-out function."""
        return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2
        
    @staticmethod
    def ease_out_back(t: float) -> float:
        """Back easing out function for overshoot effect."""
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)
        
    @staticmethod
    def spring(t: float) -> float:
        """Spring animation function."""
        return 1 - math.cos(t * math.pi * 2) * math.exp(-t * 3)


class AnimatedWidget(ctk.CTkFrame):
    """Widget with smooth animation capabilities."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.animation_engine = AnimationEngine()
        self.current_animation = None
        
    def animate_fade_in(self, duration: int = 300, callback: Optional[Callable] = None):
        """Fade in animation."""
        self._animate_property("alpha", 0, 1, duration, callback)
        
    def animate_fade_out(self, duration: int = 300, callback: Optional[Callable] = None):
        """Fade out animation."""
        self._animate_property("alpha", 1, 0, duration, callback)
        
    def animate_scale(self, scale_from: float, scale_to: float, duration: int = 300, callback: Optional[Callable] = None):
        """Scale animation."""
        self._animate_property("scale", scale_from, scale_to, duration, callback)
        
    def _animate_property(self, property_name: str, from_value: float, to_value: float, duration: int, callback: Optional[Callable]):
        """Animate a property with easing."""
        steps = 20
        step_duration = duration // steps
        
        for i in range(steps + 1):
            progress = i / steps
            eased_progress = self.animation_engine.ease_in_out_cubic(progress)
            current_value = from_value + (to_value - from_value) * eased_progress
            
            self.after(i * step_duration, lambda v=current_value, p=property_name: self._update_property(p, v))
            
        if callback:
            self.after(duration, callback)
            
    def _update_property(self, property_name: str, value: float):
        """Update widget property."""
        if property_name == "alpha":
            # Simulate alpha with color brightness
            brightness = int(255 * value)
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            self.configure(fg_color=color)
        elif property_name == "scale":
            # Simulate scale with widget size
            current_width = self.winfo_width()
            current_height = self.winfo_height()
            new_width = int(current_width * value)
            new_height = int(current_height * value)
            self.configure(width=new_width, height=new_height)