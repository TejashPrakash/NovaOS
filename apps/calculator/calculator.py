from sdk.app import NovaApp
import customtkinter as ctk


class CalculatorApp(NovaApp):
    APP_NAME = "Calculator"
    APP_ICON = "🧮"
    
    def __init__(self, window):
        super().__init__(window)
        self.current_input = ""
        self.result = ""
        
    def build(self):
        # Display
        self._setup_display()
        
        # Buttons
        self._setup_buttons()
        
    def _setup_display(self):
        """Setup calculator display."""
        display_frame = ctk.CTkFrame(
            self.content,
            height=80,
            fg_color="#252B3B",
            corner_radius=12
        )
        display_frame.pack(fill="x", padx=20, pady=20)
        
        self.display = ctk.CTkLabel(
            display_frame,
            text="0",
            font=("Segoe UI", 32, "bold"),
            text_color="#00E5FF"
        )
        self.display.pack(expand=True)
        
    def _setup_buttons(self):
        """Setup calculator buttons."""
        button_frame = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        button_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        buttons = [
            ("C", "#E53935"), ("±", "#FFA500"), ("%", "#FFA500"), ("÷", "#00E5FF"),
            ("7", "#252B3B"), ("8", "#252B3B"), ("9", "#252B3B"), ("×", "#00E5FF"),
            ("4", "#252B3B"), ("5", "#252B3B"), ("6", "#252B3B"), ("-", "#00E5FF"),
            ("1", "#252B3B"), ("2", "#252B3B"), ("3", "#252B3B"), ("+", "#00E5FF"),
            ("0", "#252B3B"), (".", "#252B3B"), ("=", "#00E5FF")
        ]
        
        for i, (text, color) in enumerate(buttons):
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                font=("Segoe UI", 20, "bold"),
                fg_color=color,
                text_color="white" if color != "#00E5FF" else "black",
                corner_radius=12,
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
        """Handle button press."""
        if text == "C":
            self.current_input = ""
            self.result = ""
        elif text == "=":
            try:
                self.result = str(eval(self.current_input.replace("×", "*").replace("÷", "/")))
                self.current_input = self.result
            except:
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
                self.current_input = str(float(self.current_input) / 100)
        else:
            self.current_input += text
            
        self.display.configure(text=self.current_input or self.result or "0")