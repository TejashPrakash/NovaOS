from sdk.app import NovaApp

import customtkinter as ctk


class NotesApp(NovaApp):

    APP_NAME = "Notes"

    APP_ICON = "📝"

    def build(self):

        self.build_placeholder(self.APP_NAME)