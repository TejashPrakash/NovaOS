import customtkinter as ctk

from ai.skills import find


class Launcher:

    def __init__(self, root, kernel):

        self.root = root
        self.kernel = kernel

        self.window_manager = kernel.window_manager
        self.process_manager = kernel.process_manager

        self.visible = False
        self.ai_enabled = True

        # -----------------------------
        # Launcher Window
        # -----------------------------

        self.frame = ctk.CTkFrame(
            self.root,
            width=500,
            height=500,
            fg_color="#1A1F2B",
            corner_radius=20,
            border_width=1,
            border_color="#2F3545"
        )

        # -----------------------------
        # Search Box
        # -----------------------------

        self.search = ctk.CTkEntry(
            self.frame,
            placeholder_text="Search applications...",
            height=45
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
        # Available Apps
        # -----------------------------

        self.apps = [
            ("🌐", "Browser"),
            ("📝", "Notes"),
            ("🧮", "Calculator"),
            ("📁", "Files"),
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
                text=f"{icon}   {app}",
                height=45,
                anchor="w",
                command=lambda a=app: self.launch(a)
            )

            btn.pack(
                fill="x",
                pady=5
            )

            self.buttons.append(btn)

    # ========================================

    def filter_apps(self, event=None):

        query = self.search.get().lower()

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

        if self.visible:
            return

        self.visible = True

        self.frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        self.search.focus()

    # ========================================

    def hide(self):

        self.visible = False

        self.frame.place_forget()

        self.search.delete(0, "end")

        self.filter_apps()

    # ========================================

    def toggle(self):

        if self.visible:

            self.hide()

        else:

            self.show()