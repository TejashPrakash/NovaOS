from sdk.app import NovaApp

import customtkinter as ctk


class CalculatorApp(NovaApp):

    APP_NAME = "Calculator"

    APP_ICON = "🧮"

    def build(self):

        self.build_placeholder(self.APP_NAME)