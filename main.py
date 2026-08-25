import customtkinter as ctk


def main():
    """Launch NovaOS: splash -> lock screen -> desktop."""
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.withdraw()

    from core.splash import NovaSplashScreen
    from core.lock_screen import LockScreen
    from core.app import NovaOS

    os_app = None

    def boot_desktop():
        """Called when the splash animation finishes."""
        nonlocal os_app
        root.deiconify()
        os_app = NovaOS(root)

    def show_lock_screen():
        """Called when splash finishes — show lock screen first."""
        nonlocal os_app
        root.deiconify()

        def on_unlock():
            if os_app is None:
                os_app = NovaOS(root)

        LockScreen(on_unlock=on_unlock)

    splash = NovaSplashScreen()
    splash.start_boot(show_lock_screen)

    root.mainloop()


if __name__ == "__main__":
    main()