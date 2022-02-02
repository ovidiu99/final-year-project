import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL
import threading
import time

import constants
from third_page import ThirdPage


class SecondPage(tk.Frame):
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
            text="The application will now record your head activity\nfor 5 seconds, while in a calm state.\n\nPlease do not blink your eyes or clench your jaw.",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.label.pack()

        self.blink_label = tk.Label(
            middle_frame,
            text="Blink twice to start recording",
            font=constants.LABEL_FONT_BOLD,
            bg=constants.BACKGROUND_COLOUR,
            borderwidth=2,
            relief="solid",
        )
        self.blink_label.pack(pady=(25, 0), ipadx=(5))

        self.clench_label = tk.Label(
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

    def start_blink_twice_detection_check(self, blink_detected_function_name):
        function = self.blink_detected_functions_mapping[blink_detected_function_name]
        time.sleep(0.5)
        self.controller.headband_connection.blink_twice_detection(function)

    def blink_twice_detection_thread(
        self, blink_detected_function_name="start_recording"
    ):
        self.blink_thread = threading.Thread(
            target=self.start_blink_twice_detection_check,
            args=(blink_detected_function_name,),
        )
        self.blink_thread.start()

    def blink_to_start_recording_detected(self):
        self.blink_label.pack_forget()
        self.progress_bar.pack(pady=(25, 0))
        self.record_normal_state_thread()

    def blink_to_go_to_next_page_detected(self):
        self.headband_connection.unmap_clench_detection()
        self.controller.show_frame(ThirdPage)

    def record_normal_state(self):
        self.headband_input.reinitialize_eeg_calm_state_values()
        self.update_progress_bar_thread()
        self.headband_connection.record_normal_state()

    def record_normal_state_thread(self):
        self.record_normal_thread = threading.Thread(
            target=self.record_normal_state, args=()
        )
        self.record_normal_thread.start()

    def record_normal_state_finished(self):
        self.headband_connection.unmap_record_normal_state()
        time.sleep(1)
        self.progress_bar.pack_forget()
        self.blink_label.config(text="Blink twice to continue")
        self.blink_label.pack(pady=(25, 0), ipadx=(5))
        self.clench_label.pack(pady=(15, 0), ipadx=(5))
        self.blink_twice_detection_thread("next_page")
        self.clench_detection_thread()

    def update_progress_bar(self):
        for i in range(1, 6):
            time.sleep(1)
            self.progress_bar["value"] += 20
            self.update_idletasks()
        self.record_normal_state_finished()

    def update_progress_bar_thread(self):
        self.progress_bar_thread = threading.Thread(
            target=self.update_progress_bar, args=()
        )
        self.progress_bar_thread.start()

    def clench_detected(self):
        self.headband_connection.unmap_blink_twice_detection()
        self.clench_label.pack_forget()
        self.blink_label.config(text="Blink twice to start recording")
        self.progress_bar["value"] = 0
        self.blink_twice_detection_thread()

    def start_clench_detection_check(self):
        time.sleep(0.5)
        self.headband_connection.clench_detection(self.clench_detected)

    def clench_detection_thread(self):
        self.clench_thread = threading.Thread(
            target=self.start_clench_detection_check,
            args=(),
        )
        self.clench_thread.start()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.headband_connection = self.controller.headband_connection
        self.headband_input = self.controller.headband_input
        self.initialize_grid()

        self.middle_frame = self.generate_middle_frame()
        self.middle_frame.grid(row=1, column=0, columnspan=3)

        self.blink_detected_functions_mapping = {
            "start_recording": self.blink_to_start_recording_detected,
            "next_page": self.blink_to_go_to_next_page_detected,
        }

    def start_threads(self):
        self.blink_twice_detection_thread()
