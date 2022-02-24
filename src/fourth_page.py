import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL
import threading
import time

import constants
from fifth_page import FifthPage


class FourthPage(tk.Frame):
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
            text="Analysing the recorded values...",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.label.pack()

        s = ttk.Style()
        s.theme_use("clam")
        s.configure(
            "bar.Horizontal.TProgressbar",
            troughcolor=constants.BACKGROUND_COLOUR,
            bordercolor=constants.PROGRESS_BAR_BORDER_COLOUR,
            background=constants.PROGRESS_BAR_BORDER_COLOUR,
            lightcolor=constants.PROGRESS_BAR_BORDER_COLOUR,
            darkcolor=constants.PROGRESS_BAR_BORDER_COLOUR,
        )
        self.progress_bar = ttk.Progressbar(
            middle_frame,
            style="bar.Horizontal.TProgressbar",
            orient=HORIZONTAL,
            length=150,
            mode="indeterminate",
        )
        self.progress_bar.pack(pady=(25, 0))
        self.progress_bar.start(20)

        return middle_frame

    def analyse_values(self):
        self.timer = time.time()
        self.headband_input.calculate_average_calm_state_difference()
        self.headband_input.calculate_average_clenching_state_difference()
        while time.time() - self.timer < 3:
            continue
        self.progress_bar.pack_forget()
        self.controller.show_frame(FifthPage)

    def analyse_values_thread(self):
        self.analyse_thread = threading.Thread(target=self.analyse_values, args=())
        self.analyse_thread.start()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.headband_input = self.controller.headband_input
        self.initialize_grid()

        self.middle_frame = self.generate_middle_frame()
        self.middle_frame.grid(row=1, column=0, columnspan=3)

    def start_threads(self):
        self.analyse_values_thread()
