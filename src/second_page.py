import tkinter as tk
from tkinter import font as tkfont
import constants


class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        label = tk.Label(
            self,
            text="Welcome to Head Writer!2",
            font=controller.TITLE_FONT,
        )
        label.place(relx=0.5, rely=0.20, anchor="center")
