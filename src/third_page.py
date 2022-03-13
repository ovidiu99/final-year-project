import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL
import threading
import time

import constants
from fourth_page import FourthPage


class ThirdPage(tk.Frame):
    def initialise_grid(self):
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
            text="The application will now record your head activity\nfor 5 seconds, while clenching your jaw.",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.label.pack()

        self.blink_label = tk.Label(
            middle_frame,
            text="Blink twice to continue",
            font=constants.LABEL_FONT_BOLD,
            bg=constants.BACKGROUND_COLOUR,
            borderwidth=2,
            relief="solid",
        )

        self.clench_label = tk.Label(
            middle_frame,
            text="Clench (and hold) your jaw to start recording",
            font=constants.LABEL_FONT_BOLD,
            bg=constants.BACKGROUND_COLOUR,
            borderwidth=2,
            relief="solid",
        )
        self.clench_label.pack(pady=(25, 0), ipadx=(5))

        self.clench_to_re_record_label = tk.Label(
            middle_frame,
            text="Clench once to re-record",
            font=constants.LABEL_FONT_BOLD,
            bg=constants.BACKGROUND_COLOUR,
            borderwidth=2,
            relief="solid",
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
            mode="determinate",
        )

        return middle_frame

    def start_clench_detection_check(
        self, clench_detected_function_name="start_recording"
    ):
        function = self.clench_detected_functions_mapping[clench_detected_function_name]
        self.headband_connection.clench_detection(function)

    def start_blink_twice_detection_check(self):
        self.headband_connection.blink_twice_detection(self.blink_detected)

    def record_clenching_state(self):
        self.headband_input.reinitialise_eeg_clenching_state_values()
        self.update_progress_bar_thread()
        self.headband_connection.record_clenching_state()

    def clench_to_start_recording_detected(self):
        self.clench_label.pack_forget()
        self.progress_bar.pack(pady=(25, 0))
        self.record_clenching_state()

    def clench_to_re_record_detected(self):
        self.headband_connection.unmap_blink_twice_detection()
        self.clench_to_re_record_label.pack_forget()
        self.label.config(
            text="The application will now record your head activity\nfor 5 seconds, while clenching your jaw."
        )
        self.blink_label.pack_forget()
        self.clench_label.pack(pady=(25, 0), ipadx=(5))
        self.progress_bar["value"] = 0
        self.start_clench_detection_check()

    def blink_detected(self):
        self.headband_connection.unmap_clench_detection()
        self.controller.show_frame(FourthPage)

    def record_clenching_state_finished(self):
        self.headband_connection.unmap_record_clenching_state()
        time.sleep(1)
        self.progress_bar.pack_forget()
        self.label.config(
            text="The head activity, while clenching your jaw, was\nsuccessfully recorded"
        )
        self.blink_label.pack(pady=(25, 0), ipadx=(5))
        self.clench_to_re_record_label.pack(pady=(15, 0), ipadx=(5))
        self.start_blink_twice_detection_check()
        self.start_clench_detection_check("re_record")

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
        self.initialise_grid()

        self.middle_frame = self.generate_middle_frame()
        self.middle_frame.grid(row=1, column=0, columnspan=3)

        self.clench_detected_functions_mapping = {
            "start_recording": self.clench_to_start_recording_detected,
            "re_record": self.clench_to_re_record_detected,
        }

    def start_processes(self):
        self.start_clench_detection_check()
