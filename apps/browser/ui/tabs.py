import customtkinter as ctk

class BrowserTabs(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=38, fg_color="#202632")
        self.pack_propagate(False)
        self.buttons = {}
        self.callback = None
        self.close_callback = None
        self.plus_callback = None

        self.tabs_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tabs_frame.pack(side="left", fill="x", expand=True)

        self.plus_button = ctk.CTkButton(self, text="+", width=34, command=self.new_tab)
        self.plus_button.pack(side="right", padx=6, pady=4)

    def set_callbacks(self, select_callback, close_callback, new_callback):
        self.callback = select_callback
        self.close_callback = close_callback
        self.plus_callback = new_callback

    def refresh(self, tabs, current_tab):
        for widget in self.tabs_frame.winfo_children():
            widget.destroy()
        self.buttons.clear()

        for tab in tabs:
            frame = ctk.CTkFrame(
                self.tabs_frame,
                fg_color="#2E3646" if tab == current_tab else "#252B38",
                corner_radius=8
            )
            frame.pack(side="left", padx=4, pady=4)

            btn = ctk.CTkButton(
                frame,
                text=tab.title,
                width=130,
                fg_color="transparent",
                hover_color="#3A4255",
                command=lambda t=tab: self.select_tab(t)
            )
            btn.pack(side="left", padx=(6, 2))

            close = ctk.CTkButton(
                frame,
                text="✕",
                width=24,
                fg_color="transparent",
                hover_color="#D32F2F",
                command=lambda t=tab: self.close_tab(t)
            )
            close.pack(side="right", padx=4)

            self.buttons[tab.id] = btn

    def select_tab(self, tab):
        if self.callback:
            self.callback(tab)

    def close_tab(self, tab):
        if self.close_callback:
            self.close_callback(tab)

    def new_tab(self):
        if self.plus_callback:
            self.plus_callback()