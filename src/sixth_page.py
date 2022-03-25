import constants

import tkinter as tk

from tkinter import BOTTOM
from tkinter.constants import LEFT, TOP

from base_page import BasePage


class SixthPage(BasePage):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.headband_connection = self.controller.headband_connection
        self.headband_input = self.controller.headband_input
        self.initialise_grid()

        self.upper_frame = self.generate_upper_frame()
        self.middle_frame = self.generate_middle_frame()
        self.bottom_frame = self.generate_bottom_frame()

        self.upper_frame.grid(row=0, column=0, columnspan=3)
        self.middle_frame.grid(row=1, column=0, columnspan=3)
        self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky="ns", pady=(0, 10))

    def generate_upper_frame(self):
        upper_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)
        self.text_label_upper = tk.Label(
            upper_frame,
            text="Tutorial page",
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
            font=constants.LABEL_FONT_MEDIUM_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            justify=LEFT,
        )
        self.middle_label_2 = tk.Label(
            middle_frame,
            text="The application has two modes of operation:",
            font=constants.LABEL_FONT_MEDIUM_SMALL,
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
            font=constants.LABEL_FONT_MEDIUM_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            justify=LEFT,
        )
        self.middle_label_4 = tk.Label(
            middle_frame,
            text="2) Advanced mode:"
            + "\n    - Same as the beginner mode, except the spacing between words will be"
            + "\n      automatically added by the application after 1.75 seconds",
            font=constants.LABEL_FONT_MEDIUM_SMALL,
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
            font=constants.LABEL_FONT_MEDIUM_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            justify=LEFT,
        )
        self.middle_label_6 = tk.Label(
            middle_frame,
            text="Copy mode:"
            + "\n    - Clench for 1 unit to for a mouse click"
            + "\n    - Clench between 2 and 4 units for a mouse double-click"
            + "\n    - Clench between 5 and 9 units to paste"
            + "\n    - Clench between 10 and 13 units to close the copy mode",
            font=constants.LABEL_FONT_MEDIUM_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            justify=LEFT,
        )

        self.middle_label_1.pack(side=TOP, anchor="w")
        self.middle_label_2.pack(pady=(7, 0), side=TOP, anchor="w")
        self.middle_label_3.pack(pady=(3, 0), side=TOP, anchor="w")
        self.middle_label_4.pack(pady=(3, 0), side=TOP, anchor="w")
        self.middle_label_5.pack(pady=(7, 0), side=TOP, anchor="w")
        self.middle_label_6.pack(pady=(7, 0), side=TOP, anchor="w")

        return middle_frame

    def generate_bottom_frame(self):
        bottom_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)
        self.text_label_lower = tk.Label(
            bottom_frame,
            text="Clench to go back",
            font=constants.LABEL_FONT_SMALL_BOLD,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.text_label_lower.pack(side=BOTTOM)
        return bottom_frame

    def start_clench_detection_check(self):
        self.headband_connection.clench_detection(self.clench_detected)

    def clench_detected(self):
        from fifth_page import FifthPage
        from seventh_page import SeventhPage

        writing_started = self.headband_input.get_writing_started()

        if not writing_started:
            self.controller.show_frame(FifthPage)
        else:
            self.controller.show_frame(SeventhPage)

    def start_processes(self):
        self.start_clench_detection_check()
