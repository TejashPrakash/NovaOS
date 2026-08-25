import customtkinter as ctk

from ai.skills import find
from core.theme import ThemeManager
from widgets.glass import GlassFrame


class Launcher:

    def __init__(self, root, kernel):

        self.root = root
        self.kernel = kernel

        self.window_manager = kernel.window_manager
        self.process_manager = kernel.process_manager

        self.visible = False
        self.animation_step = 0
        self.is_animating = False
        self.ai_enabled = True
        self.theme = ThemeManager()

        # -----------------------------
        # Launcher Window
        # -----------------------------

        self.frame = GlassFrame(
            self.root,
            width=500,
            height=500,
            blur_amount=20,
            opacity=0.95,
            fg_color=self.theme.get_color("surface"),
            corner_radius=20,
            border_width=2,
            border_color=self.theme.get_color("primary")
        )

        # -----------------------------
        # Search Box
        # -----------------------------

        self.search = ctk.CTkEntry(
            self.frame,
            placeholder_text="Search applications...",
            height=45,
            fg_color=self.theme.get_color("surface_light"),
            text_color=self.theme.get_color("text_primary"),
            placeholder_text_color=self.theme.get_color("text_muted"),
            corner_radius=10,
            border_width=1,
            border_color=self.theme.get_color("primary_dim")
        )

        self.search.pack(
            padx=20,
            pady=(20, 15),
            fill="x"
        )

        self.search.bind(
            "<KeyRelease>",
            self.filter_apps
        )

        # -----------------------------
        # Escape closes launcher
        # -----------------------------

        self.frame.bind("<Escape>", lambda e: self.hide())
        self.search.bind("<Escape>", lambda e: self.hide())
        self.search.bind("<Return>", lambda e: self._launch_first_app())
        self.search.bind("<Up>", lambda e: self._navigate_apps(-1))
        self.search.bind("<Down>", lambda e: self._navigate_apps(1))

        # -----------------------------
        # Apps Container
        # -----------------------------

        self.apps_frame = ctk.CTkScrollableFrame(
            self.frame,
            fg_color="transparent"
        )

        self.apps_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # -----------------------------
        # AI Response Display
        # -----------------------------

        self.ai_response_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        self.ai_response_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        self.ai_response_label = ctk.CTkLabel(
            self.ai_response_frame,
            text="",
            font=("Segoe UI", 11),
            text_color=self.theme.get_color("accent"),
            wraplength=460
        )
        self.ai_response_label.pack(fill="x")

        # -----------------------------
        # Available Apps
        # -----------------------------

        self.apps = [
            ("🌐", "Browser"),
            ("📝", "Notes"),
            ("🧮", "Calculator"),
            ("📁", "Files"),
            (">_", "Terminal"),
            ("🌤", "Weather"),
            ("📅", "Calendar"),
            ("📊", "System Monitor"),
            ("⚙", "Settings")
        ]

        self.buttons = []

        self.build_apps()

    # ========================================

    def build_apps(self):

        for button in self.buttons:
            button.destroy()

        self.buttons.clear()

        for icon, app in self.apps:

            btn = ctk.CTkButton(
                self.apps_frame,
                text=f"{icon} {app}",
                height=45,
                anchor="w",
                fg_color=self.theme.get_color("surface_light"),
                text_color=self.theme.get_color("text_primary"),
                hover_color=self.theme.get_color("primary"),
                corner_radius=8,
                border_width=1,
                border_color=self.theme.get_color("primary_dim"),
                command=lambda a=app: self.launch(a)
            )

            btn.pack(
                fill="x",
                pady=5
            )

            self.buttons.append(btn)

    # ========================================

    def filter_apps(self, event=None):
        """Filter apps and show AI responses."""
        query = self.search.get().lower()

        results = self.process_search(query)

        if results.get('ai_response'):
            self.ai_response_label.configure(
                text=f"🤖 {results['ai_response']}"
            )
            self.ai_response_frame.pack(fill="x", padx=20, pady=(0, 10))
        else:
            self.ai_response_frame.pack_forget()

        for button in self.buttons:

            text = button.cget("text").lower()

            if query in text:

                button.pack(fill="x", pady=5)

            else:

                button.pack_forget()
                
    # ========================================

    def process_search(self, query: str) -> dict:
        """Process search query with AI enhancement."""
        results = {
            'apps': [],
            'ai_response': None,
            'web_results': []
        }

        # First check if AI skills can handle this
        if self.ai_enabled:
            query_lower = query.lower()
            
            # Check for time queries
            if any(word in query_lower for word in ['time', 'date', 'weather', 'calculate']):
                # Try to find matching skill
                for skill_name in ['get_current_time', 'get_current_date', 'get_datetime_info', 'get_weather', 'calculate']:
                    skill = find(skill_name)
                    if skill:
                        try:
                            if skill_name == 'calculate':
                                result = skill.run(self.kernel, expression=query)
                            elif 'weather' in skill_name:
                                result = skill.run(self.kernel, location=query.replace('weather in', '').replace('weather', '').strip())
                            elif 'time' in skill_name and 'date' not in skill_name:
                                result = skill.run(self.kernel, timezone='UTC')
                            else:
                                result = skill.run(self.kernel)
                            
                            results['ai_response'] = result
                            return results
                        except Exception as e:
                            print(f"[Launcher] AI skill error: {e}")

        # Fall back to app search
        results['apps'] = self._search_apps(query)
        return results

    def _search_apps(self, query: str) -> list:
        """Search installed applications."""
        query_lower = query.lower()
        matching_apps = []

        from apps.registry import APP_REGISTRY
        for app_name, app_class in APP_REGISTRY.items():
            if query_lower in app_name.lower():
                matching_apps.append({
                    'name': app_name,
                    'class': app_class
                })

        return matching_apps
                
    # ========================================

    def launch(self, app):

        self.kernel.process_manager.start_process(app)

        self.hide()

    # ========================================

    def show(self):
        """Show launcher with smooth animation."""
        if self.visible or self.is_animating:
            return

        self.is_animating = True
        self.visible = True
        self.animation_step = 0

        self.frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self._animate_show()

    def _animate_show(self):
        """Animate launcher appearance."""
        if self.animation_step < 10:
            self.animation_step += 1
            alpha = self.animation_step / 10
            if alpha >= 1:
                self.frame.configure(border_width=2)
            else:
                self.frame.configure(border_width=int(2 * alpha))

            self.root.after(20, self._animate_show)
        else:
            self.is_animating = False
            self.search.focus()

    # ========================================

    def hide(self):
        """Hide launcher with smooth animation."""
        if not self.visible or self.is_animating:
            return

        self.is_animating = True
        self.animation_step = 10
        self._animate_hide()

    def _animate_hide(self):
        """Animate launcher disappearance."""
        if self.animation_step > 0:
            self.animation_step -= 1
            alpha = self.animation_step / 10
            if alpha <= 0:
                self.frame.configure(border_width=0)
            else:
                self.frame.configure(border_width=int(2 * alpha))

            self.root.after(20, self._animate_hide)
        else:
            self.is_animating = False
            self.visible = False
            self.frame.place_forget()
            self.search.delete(0, "end")
            self.ai_response_label.configure(text="")
            self.ai_response_frame.pack_forget()
            self.filter_apps()

    # ========================================

    def toggle(self):

        if self.visible:

            self.hide()

        else:

            self.show()

    def _launch_first_app(self):
        """Launch the first visible app from search results."""
        visible_buttons = [btn for btn in self.buttons if btn.winfo_ismapped()]
        if visible_buttons:
            text = visible_buttons[0].cget("text")
            app_name = text.split(" ", 1)[1] if " " in text else text
            self.launch(app_name)

    def _navigate_apps(self, direction):
        """Navigate through app results with arrow keys."""
        visible_buttons = [btn for btn in self.buttons if btn.winfo_ismapped()]
        if not visible_buttons:
            return

        current_focus = self.focus_get()

        if current_focus in visible_buttons:
            current_index = visible_buttons.index(current_focus)
            new_index = (current_index + direction) % len(visible_buttons)
            visible_buttons[new_index].focus()
        else:
            if direction > 0:
                visible_buttons[0].focus()
            else:
                visible_buttons[-1].focus()