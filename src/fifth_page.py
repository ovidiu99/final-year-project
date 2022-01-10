import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL, TOP
import threading
import time

import constants
from sixth_page import SixthPage


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
        self.text_label = tk.Label(
            middle_frame,
            text="Fifth page",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )

        self.text_label.pack(side=TOP, anchor="w")

        return middle_frame

    def start_blink_twice_detection_check(self):
        time.sleep(0.5)
        self.controller.headband_connection.blink_twice_detection(self.blink_detected)

    def blink_twice_detection_thread(self):
        self.blink_thread = threading.Thread(
            target=self.start_blink_twice_detection_check, args=()
        )
        self.blink_thread.start()

    def blink_detected(self):
        self.controller.show_frame(SixthPage)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.headband_connection = self.controller.headband_connection
        self.headband_input = self.controller.headband_input
        self.initialize_grid()

        self.middle_frame = self.generate_middle_frame()
        self.middle_frame.grid(row=1, column=0, columnspan=3)

    def start_threads(self):
        self.blink_twice_detection_thread()
