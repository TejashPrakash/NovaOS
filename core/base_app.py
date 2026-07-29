from abc import ABC, abstractmethod

import customtkinter as ctk


class BaseApp(ABC):

    APP_NAME = "Application"
    APP_ICON = "📦"

    MIN_WIDTH = 520
    MIN_HEIGHT = 360

    def __init__(self, window):

        self.window = window
        self.content = window.content

    @property
    def manager(self):
        return self.window.manager

    def focus(self):
        self.window.focus_window()

    def close(self):
        self.window.close()

    @abstractmethod
    def build(self):
        pass