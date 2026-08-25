from sdk.app import NovaApp
import customtkinter as ctk
from core.theme import ThemeManager


class CalculatorApp(NovaApp):
    APP_NAME = "Calculator"
    APP_ICON = "🧮"
    DEFAULT_WIDTH = 400
    DEFAULT_HEIGHT = 500
    
    def __init__(self, window):
        super().__init__(window)
        self.current_input = ""
        self.result = ""
        self.theme = ThemeManager()
        
    def build(self):
        # Display
        self._setup_display()
        
        # Buttons
        self._setup_buttons()
        
    def _setup_display(self):
        """Setup calculator display with theme colors."""
        display_frame = ctk.CTkFrame(
            self.content,
            height=80,
            fg_color=self.theme.get_color("surface_light"),
            corner_radius=12,
            border_width=1,
            border_color=self.theme.get_color("primary_dim")
        )
        display_frame.pack(fill="x", padx=20, pady=20)
        
        self.display = ctk.CTkLabel(
            display_frame,
            text="0",
            font=("Segoe UI", 32, "bold"),
            text_color=self.theme.get_color("primary")
        )
        self.display.pack(expand=True)
        
    def _setup_buttons(self):
        """Setup calculator buttons with theme colors."""
        button_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        button_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        buttons = [
            ("C", self.theme.get_color("error")),
            ("±", "#FFA500"),
            ("%", "#FFA500"),
            ("÷", self.theme.get_color("primary")),
            ("7", self.theme.get_color("surface_light")),
            ("8", self.theme.get_color("surface_light")),
            ("9", self.theme.get_color("surface_light")),
            ("×", self.theme.get_color("primary")),
            ("4", self.theme.get_color("surface_light")),
            ("5", self.theme.get_color("surface_light")),
            ("6", self.theme.get_color("surface_light")),
            ("-", self.theme.get_color("primary")),
            ("1", self.theme.get_color("surface_light")),
            ("2", self.theme.get_color("surface_light")),
            ("3", self.theme.get_color("surface_light")),
            ("+", self.theme.get_color("primary")),
            ("0", self.theme.get_color("surface_light")),
            (".", self.theme.get_color("surface_light")),
            ("=", self.theme.get_color("primary"))
        ]
        
        for i, (text, color) in enumerate(buttons):
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                font=("Segoe UI", 20, "bold"),
                fg_color=color,
                text_color="white" if color != self.theme.get_color("primary") else "black",
                corner_radius=12,
                hover_color=self.theme.get_color("primary_hover") if color == self.theme.get_color("primary") else color,
                command=lambda t=text: self._button_press(t)
            )
            
            row = i // 4
            col = i % 4
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
        # Configure grid weights
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
            
    def _button_press(self, text):
        """Handle button press with safer calculations."""
        if text == "C":
            self.current_input = ""
            self.result = ""
        elif text == "=":
            try:
                expression = self.current_input.replace("×", "*").replace("÷", "/")
                allowed_chars = set("0123456789+-*/.()")
                if all(c in allowed_chars for c in expression):
                    self.result = str(eval(expression))
                    self.current_input = self.result
                else:
                    self.result = "Invalid input"
                    self.current_input = ""
            except Exception:
                self.result = "Error"
                self.current_input = ""
        elif text == "±":
            if self.current_input:
                if self.current_input.startswith("-"):
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = "-" + self.current_input
        elif text == "%":
            if self.current_input:
                try:
                    self.current_input = str(float(self.current_input) / 100)
                except Exception:
                    self.current_input = ""
        else:
            self.current_input += text
            
        self.display.configure(text=self.current_input or self.result or "0")