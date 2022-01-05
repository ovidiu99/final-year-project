import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL
import threading
import time

import constants


class FifthPage(tk.Frame):
    def initialize_grid(self):
        rows = 3
        columns = 3
        for row in range(rows):
            self.grid_rowconfigure(row, weight=1)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def generate_middle_frame(self):
        middle_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)
        self.label = tk.Label(
            middle_frame,
            text="Fifth page",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.label.pack()

        return middle_frame

    def analyze_values(self):
        while True:
            print("FIFTH PAGE")

    def analyze_values_thread(self):
        self.analyze_thread = threading.Thread(target=self.analyze_values, args=())
        self.analyze_thread.start()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.user = self.controller.user
        self.initialize_grid()

        self.middle_frame = self.generate_middle_frame()
        self.middle_frame.grid(row=1, column=0, columnspan=3)

    def start_threads(self):
        print("FIFTH PAGE")
        # self.analyze_values_thread()
