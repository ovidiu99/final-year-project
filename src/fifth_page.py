import tkinter as tk
from tkinter import IntVar, ttk
from tkinter import font as tkfont
from tkinter.constants import DISABLED, HORIZONTAL, LEFT, SE, TOP

import threading
import time

import constants
from seventh_page import SeventhPage
from sixth_page import SixthPage


class FifthPage(tk.Frame):

    _selected_mode = "Beginner"

    def initialize_grid(self):
        rows = 3
        columns = 3
        for row in range(rows):
            self.grid_rowconfigure(row, weight=1)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def generate_upper_frame(self):
        upper_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)
        self.upper_label_1 = tk.Label(
            upper_frame,
            text="The recorded data has been analysed!",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.upper_label_1.pack()
        return upper_frame

    def generate_selected_mode_frame(self, middle_frame):
        selected_mode_frame = tk.Frame(middle_frame, bg=constants.BACKGROUND_COLOUR)
        selected_mode_frame.grid_rowconfigure(0, weight=1)
        selected_mode_frame.grid_columnconfigure(0, weight=1)
        selected_mode_frame.grid_columnconfigure(1, weight=1)

        label = tk.Label(
            selected_mode_frame,
            text="Selected mode:",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        label.grid(row=0, column=0)

        self.selected_mode_label = tk.Label(
            selected_mode_frame,
            text=self._selected_mode,
            font=constants.LABEL_FONT_BOLD,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.selected_mode_label.grid(row=0, column=1)

        return selected_mode_frame

    def generate_middle_frame(self):
        middle_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)

        self.middle_label_1 = tk.Label(
            middle_frame,
            text="Clench your jaw once to see the tutorial",
            font=constants.LABEL_FONT_SMALL_BOLD,
            bg=constants.BACKGROUND_COLOUR,
            borderwidth=2,
            relief="solid",
        )
        self.middle_label_2 = tk.Label(
            middle_frame,
            text="Clench your jaw for 1 second to change the mode",
            font=constants.LABEL_FONT_SMALL_BOLD,
            bg=constants.BACKGROUND_COLOUR,
            borderwidth=2,
            relief="solid",
        )
        self.middle_label_3 = tk.Label(
            middle_frame,
            text="Clench your jaw for 2 seconds to continue",
            font=constants.LABEL_FONT_SMALL_BOLD,
            bg=constants.BACKGROUND_COLOUR,
            borderwidth=2,
            relief="solid",
        )

        self.middle_label_1.pack(ipadx=15, ipady=10)
        self.middle_label_2.pack(pady=(15, 0), ipadx=15, ipady=10)
        self.middle_label_3.pack(pady=(15, 0), ipadx=15, ipady=10)
        return middle_frame

    def generate_lower_frame(self):
        lower_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)

        self.action_label = tk.Label(
            lower_frame,
            text="Action: None",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
            fg=constants.BACKGROUND_COLOUR,
        )

        self.selected_mode_frame = self.generate_selected_mode_frame(lower_frame)

        self.selected_mode_frame.pack()

        self.action_label.pack(pady=(20, 0))
        return lower_frame

    def update_next_action_label(self, clench_length):
        if clench_length >= 1 and clench_length < 4:
            self.action_label.config(text="Action: Open tutorial page", fg="black")
        elif clench_length >= 4 and clench_length < 8:
            self.action_label.config(text="Action: Change mode", fg="black")
        elif clench_length >= 8:
            self.action_label.config(text="Action: Go to next page", fg="black")

    def open_tutorial_page(self):
        self.headband_connection.unmap_listen_for_input()
        self.controller.show_frame(SixthPage)
        self.action_label.config(text="Action: None", fg=constants.BACKGROUND_COLOUR)

    def update_selected_mode(self):
        if self._selected_mode == "Beginner":
            self._selected_mode = "Advanced"
        else:
            self._selected_mode = "Beginner"
        self.selected_mode_label.config(text=self._selected_mode)
        self.action_label.config(text="Action: None", fg=constants.BACKGROUND_COLOUR)

    def go_to_next_page(self):
        self.headband_connection.unmap_listen_for_input()
        self.controller.show_frame(SeventhPage)
        self.action_label.config(text="Action: None", fg=constants.BACKGROUND_COLOUR)

    def clench_handler(self, input_list):
        self.headband_input.handle_input(input_list, self)

    def clench_input(self):
        self.headband_connection.listen_for_input(self.clench_handler)

    def listen_for_clenching_thread(self):
        self.clenching_thread = threading.Thread(target=self.clench_input, args=())
        self.clenching_thread.start()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.headband_connection = self.controller.headband_connection
        self.headband_input = self.controller.headband_input
        self.initialize_grid()

        self.upper_frame = self.generate_upper_frame()
        self.middle_frame = self.generate_middle_frame()
        self.lower_frame = self.generate_lower_frame()

        self.upper_frame.grid(row=0, column=0, columnspan=3)
        self.middle_frame.grid(row=1, column=0, columnspan=3)
        self.lower_frame.grid(row=2, column=0, columnspan=3)

    def start_threads(self):
        self.listen_for_clenching_thread()
