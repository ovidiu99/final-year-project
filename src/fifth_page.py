import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL, TOP
import threading
import time

import constants


class FifthPage(tk.Frame):
    def initialize_grid(self):
        rows = 3
        columns = 3
        for row in range(rows):
            self.grid_rowconfigure(row, weight=1)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def generate_current_position_indicator_frame(self, middle_frame, indicator=""):
        current_position_frame = tk.Frame(middle_frame, bg=constants.BACKGROUND_COLOUR)
        current_position_frame.grid_rowconfigure(0, weight=1)
        current_position_frame.grid_columnconfigure(0, weight=1)
        current_position_frame.grid_columnconfigure(1, weight=1)

        if indicator == "↓":
            self.current_possition_label_down = tk.Label(
                current_position_frame,
                text="",
                font=constants.LABEL_FONT,
                bg=constants.BACKGROUND_COLOUR,
                fg=constants.BACKGROUND_COLOUR,
            )
            self.current_possition_label_down.grid(row=0, column=0)
        elif indicator == "↑":
            self.current_possition_label_up = tk.Label(
                current_position_frame,
                text="",
                font=constants.LABEL_FONT,
                bg=constants.BACKGROUND_COLOUR,
                fg=constants.BACKGROUND_COLOUR,
            )
            self.current_possition_label_up.grid(row=0, column=0)

        current_possition_pointer = tk.Label(
            current_position_frame,
            text=indicator,
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        current_possition_pointer.grid(row=0, column=1)

        return current_position_frame

    def generate_middle_frame(self):
        middle_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)
        self.text_label = tk.Label(
            middle_frame,
            text="",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )

        self.current_position_frame_arrow_down = (
            self.generate_current_position_indicator_frame(middle_frame, "↓")
        )
        self.current_position_frame_arrow_up = (
            self.generate_current_position_indicator_frame(middle_frame, "↑")
        )

        self.current_position_frame_arrow_down.pack()
        self.text_label.pack(side=TOP, anchor="w")
        self.current_position_frame_arrow_up.pack()

        return middle_frame

    def update_text_label(self, text):
        self.current_possition_label_down.config(text=text[: len(text) - 1])
        self.current_possition_label_up.config(text=text[: len(text) - 1])
        self.text_label.config(text=text)

    def handle_input(self, input_list):
        self.headband_input.handle_input(input_list, self)

    def listen_for_input(self):
        self.headband_connection.listen_for_input(self.handle_input)

    def listen_for_input_thread(self):
        self.input_thread = threading.Thread(target=self.listen_for_input, args=())
        self.input_thread.start()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.headband_connection = self.controller.headband_connection
        self.headband_input = self.controller.headband_input
        self.initialize_grid()

        self.middle_frame = self.generate_middle_frame()
        self.middle_frame.grid(row=1, column=0, columnspan=3)

    def start_threads(self):
        self.listen_for_input_thread()
