import threading
import time
import constants
import tkinter as tk

from tkinter import ttk
from tkinter.constants import HORIZONTAL

from base_page import BasePage
from fifth_page import FifthPage


class FourthPage(BasePage):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.headband_input = self.controller.headband_input
        self.initialise_grid()

        self.middle_frame = self.generate_middle_frame()
        self.middle_frame.grid(row=1, column=0, columnspan=3)

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
        self.headband_input.calculate_threshold_values()

        # Wait three seconds before proceeding
        while time.time() - self.timer < 3:
            continue

        self.progress_bar.pack_forget()
        self.controller.show_frame(FifthPage)

    def start_processes(self):
        self.analyse_values()
