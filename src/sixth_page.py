import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL, LEFT, TOP

import threading
import time

import constants


class SixthPage(tk.Frame):
    def initialize_grid(self):
        rows = 3
        columns = 3
        for row in range(rows):
            self.grid_rowconfigure(row, weight=1)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def generate_upper_frame(self):
        upper_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)
        self.text_label_upper = tk.Label(
            upper_frame,
            text="Help page",
            font=constants.LABEL_FONT_BOLD,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.text_label_upper.pack()

        return upper_frame

    def generate_middle_frame(self):
        middle_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)
        self.middle_label_1 = tk.Label(
            middle_frame,
            text="The application classifies the input from the headband using units, where a unit is"
            + "\n0.25 seconds.",
            font=constants.LABEL_FONT_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            justify=LEFT,
        )
        self.middle_label_2 = tk.Label(
            middle_frame,
            text="The application has two modes:",
            font=constants.LABEL_FONT_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            justify=LEFT,
        )
        self.middle_label_3 = tk.Label(
            middle_frame,
            text="1) Beginner mode:"
            + "\n    - Clench for 1 unit to for a dot"
            + "\n    - Clench between 2 and 4 units for a line"
            + "\n    - The application will automatically try to turn the current dots and lines sequence"
            + "\n      into a symbol after every 0.75 seconds pause"
            + "\n    - To add a space and go to the next word, clench your jaw between 5 and 7 units",
            font=constants.LABEL_FONT_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            justify=LEFT,
        )
        self.middle_label_4 = tk.Label(
            middle_frame,
            text="2) Advanced mode:"
            + "\n    - Same as the beginner mode, except the spacing between words will be"
            + "\n      automatically added by the application after 1.75 seconds",
            font=constants.LABEL_FONT_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            justify=LEFT,
        )
        self.middle_label_5 = tk.Label(
            middle_frame,
            text="Other commands:"
            + "\n    - To delete the previous symbol, clench your jaw for 8-9 units"
            + "\n    - To change the mode, clench your jaw for 10-11 units"
            + "\n    - To hide/show the morse code alphabet, clench your jaw for 12-13 units"
            + "\n    - To copy the text to another window, clench your jaw for 16-20 units",
            font=constants.LABEL_FONT_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            justify=LEFT,
        )

        self.middle_label_1.pack(side=TOP, anchor="w")
        self.middle_label_2.pack(pady=(20, 0), side=TOP, anchor="w")
        self.middle_label_3.pack(pady=(5, 0), side=TOP, anchor="w")
        self.middle_label_4.pack(pady=(5, 0), side=TOP, anchor="w")
        self.middle_label_5.pack(pady=(20, 0), side=TOP, anchor="w")

        return middle_frame

    def generate_bottom_frame(self):
        bottom_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)
        self.text_label_lower = tk.Label(
            bottom_frame,
            text="Clench to go back",
            font=constants.LABEL_FONT_BOLD,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.text_label_lower.pack(side=TOP, anchor="w")
        return bottom_frame

    def start_clench_detection_check(self):
        time.sleep(0.5)
        self.headband_connection.clench_detection(self.clench_detected)

    def clench_detection_thread(self):
        self.clench_thread = threading.Thread(
            target=self.start_clench_detection_check,
            args=(),
        )
        self.clench_thread.start()

    def clench_detected(self):
        from fifth_page import FifthPage
        from seventh_page import SeventhPage

        writing_started = self.headband_input.get_writing_started()

        if not writing_started:
            self.controller.show_frame(FifthPage)
        else:
            self.controller.show_frame(SeventhPage)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.headband_connection = self.controller.headband_connection
        self.headband_input = self.controller.headband_input
        self.initialize_grid()

        self.upper_frame = self.generate_upper_frame()
        self.middle_frame = self.generate_middle_frame()
        self.bottom_frame = self.generate_bottom_frame()

        self.upper_frame.grid(row=0, column=0, columnspan=3)
        self.middle_frame.grid(row=1, column=0, columnspan=3)
        self.bottom_frame.grid(row=2, column=0, columnspan=3)

    def start_threads(self):
        self.clench_detection_thread()
