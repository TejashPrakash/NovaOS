import customtkinter as ctk
from core.splash import NovaSplashScreen


def main():
    """Launch NovaOS with an animated boot splash."""
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.withdraw()

    def boot_desktop():
        root.deiconify()
        from core.app import NovaOS
        os_app = NovaOS(root)
        os_app.run()

    splash = NovaSplashScreen()
    splash.start_boot(boot_desktop)

    root.mainloop()


if __name__ == "__main__":
    main()