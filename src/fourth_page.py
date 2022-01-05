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
            text="Analyzing the recorded values...",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.label.pack()

        self.blink_label = tk.Label(
            middle_frame,
            text="Blink to continue",
            font=constants.LABEL_FONT_BOLD,
            bg=constants.BACKGROUND_COLOUR,
        )

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
        self.progress_bar.pack(pady=(10, 0))
        self.progress_bar.start(20)

        return middle_frame

    def analyze_values(self):
        self.timer = time.time()
        self.user.calculate_average_difference(state="calm")
        self.user.calculate_average_difference(state="clenching")
        while time.time() - self.timer < 5:
            continue
        self.progress_bar.pack_forget()
        self.blink_label.pack(pady=(10, 0))
        self.blink_detection_thread()

    def start_blink_detection_check(self):
        time.sleep(0.5)
        self.controller.headband.blink_detection(self.blink_detected)

    def analyze_values_thread(self):
        self.analyze_thread = threading.Thread(target=self.analyze_values, args=())
        self.analyze_thread.start()

    def blink_detection_thread(self):
        self.blink_thread = threading.Thread(
            target=self.start_blink_detection_check, args=()
        )
        self.blink_thread.start()

    def blink_detected(self):
        self.controller.show_frame(FifthPage)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.user = self.controller.user
        self.initialize_grid()

        self.middle_frame = self.generate_middle_frame()
        self.middle_frame.grid(row=1, column=0, columnspan=3)

    def start_threads(self):
        self.analyze_values_thread()
