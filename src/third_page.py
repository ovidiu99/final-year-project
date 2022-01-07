import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL
import threading
import time

import constants
from fourth_page import FourthPage


class ThirdPage(tk.Frame):
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
            text="The application will now record your head activity\nfor 5 seconds, while clenching your jaw.\n",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.label.pack()

        self.clench_label = tk.Label(
            middle_frame,
            text="Clench (and hold) your jaw to start recording",
            font=constants.LABEL_FONT_BOLD,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.clench_label.pack(pady=(10, 0))

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
            mode="determinate",
        )

        return middle_frame

    def start_clench_detection_check(self):
        time.sleep(0.5)
        self.headband_connection.clench_detection(self.clench_detected)

    def start_blink_twice_detection_check(self):
        time.sleep(0.5)
        self.headband_connection.blink_twice_detection(self.blink_detected)

    def record_clenching_state(self):
        self.update_progress_bar_thread()
        self.headband_connection.record_clenching_state()

    def clench_detection_thread(self):
        self.clench_thread = threading.Thread(
            target=self.start_clench_detection_check,
            args=(),
        )
        self.clench_thread.start()

    def blink_twice_detection_thread(self):
        self.blink_thread = threading.Thread(
            target=self.start_blink_twice_detection_check, args=()
        )
        self.blink_thread.start()

    def record_clenching_state_thread(self):
        self.record_clenching_thread = threading.Thread(
            target=self.record_clenching_state, args=()
        )
        self.record_clenching_thread.start()

    def clench_detected(self):
        self.clench_label.pack_forget()
        self.progress_bar.pack(pady=(15, 0))
        self.record_clenching_state_thread()

    def blink_detected(self):
        self.controller.show_frame(FourthPage)

    def record_clenching_state_finished(self):
        self.headband_connection.unmap_record_clenching_state()
        time.sleep(1)
        self.progress_bar.pack_forget()
        self.clench_label.config(text="Blink twice to continue")
        self.clench_label.pack(pady=(10, 0))
        self.blink_twice_detection_thread()

    def update_progress_bar(self):
        for i in range(1, 6):
            time.sleep(1)
            self.progress_bar["value"] += 20
            self.update_idletasks()
        self.record_clenching_state_finished()

    def update_progress_bar_thread(self):
        self.progress_bar_thread = threading.Thread(
            target=self.update_progress_bar, args=()
        )
        self.progress_bar_thread.start()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.headband_connection = self.controller.headband_connection
        self.headband_input = self.controller.headband_input
        self.initialize_grid()

        self.middle_frame = self.generate_middle_frame()
        self.middle_frame.grid(row=1, column=0, columnspan=3)

    def start_threads(self):
        self.clench_detection_thread()
