import customtkinter as ctk
import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Launch NovaOS: splash -> lock screen -> desktop."""
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.withdraw()

    # Set fullscreen geometry BEFORE showing anything
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    root.geometry(f"{screen_w}x{screen_h}+0+0")
    root.configure(fg_color="#0D1117")

    from core.splash import NovaSplashScreen
    from core.lock_screen import LockScreen
    from core.app import NovaOS

    os_app = None

    def on_lock_screen_unlock():
        """Called when user enters correct password on lock screen."""
        nonlocal os_app
        if os_app is None:
            # Create NovaOS desktop FIRST, then show root
            os_app = NovaOS(root)
            root.deiconify()

    def show_lock_screen():
        """Called when splash finishes — show lock screen, root stays hidden."""
        nonlocal os_app
        # Root stays withdrawn — lock screen is a fullscreen Toplevel
        LockScreen(on_unlock=on_lock_screen_unlock)

    splash = NovaSplashScreen()
    splash.start_boot(show_lock_screen)

    root.mainloop()


if __name__ == "__main__":
    main()