import customtkinter as ctk

from core.desktop import Desktop

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main():
    app = Desktop()
    app.mainloop()


if __name__ == "__main__":
    main()