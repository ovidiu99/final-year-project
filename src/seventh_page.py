import tkinter as tk
from tkinter import BOTTOM, CENTER, LEFT, RIGHT, ttk
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL, TOP
import threading
import time
from turtle import width

import constants
from sixth_page import SixthPage


class SeventhPage(tk.Frame):
    def initialize_grid(self):
        rows = 3
        columns = 3
        for row in range(rows):
            if row == 2 or row == 0:
                self.grid_rowconfigure(row, weight=0)
            else:
                self.grid_rowconfigure(row, weight=1)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def generate_upper_frame(self):
        upper_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)

        self.help_page_label = tk.Label(
            upper_frame,
            text="Help page - 14x clench units",
            font=constants.LABEL_FONT_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            borderwidth=2,
            relief="solid",
        )

        self.action_label = tk.Label(
            upper_frame,
            text="Action: None",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
            fg=constants.BACKGROUND_COLOUR,
            borderwidth=2,
            relief="flat",
        )

        self.help_page_label.pack(
            side=LEFT, anchor="n", padx=(10, 0), pady=(20, 0), ipadx=(10), ipady=(5)
        )

        self.action_label.pack(
            side=RIGHT, anchor="n", padx=(0, 10), pady=(20, 0), ipadx=(10), ipady=(5)
        )
        return upper_frame

    def generate_current_position_indicator_frame(self, middle_frame):
        current_position_frame = tk.Frame(middle_frame, bg=constants.BACKGROUND_COLOUR)
        current_position_frame.grid_rowconfigure(0, weight=1)
        current_position_frame.grid_columnconfigure(0, weight=1)
        current_position_frame.grid_columnconfigure(1, weight=1)

        self.current_possition_label_up = tk.Label(
            current_position_frame,
            text="",
            font=constants.LABEL_FONT_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            fg=constants.BACKGROUND_COLOUR,
        )

        current_possition_pointer = tk.Label(
            current_position_frame,
            text="↑",
            font=constants.LABEL_FONT_SMALL,
            bg=constants.BACKGROUND_COLOUR,
        )
        current_possition_pointer.grid(row=0, column=1, sticky="w")

        return current_position_frame

    def generate_middle_frame(self):
        middle_frame = tk.Frame(
            self,
            bg=constants.BACKGROUND_COLOUR,
            highlightbackground="black",
            highlightthickness=1,
        )
        self.text_label = tk.Label(
            middle_frame,
            text="",
            font=constants.LABEL_FONT_SMALL,
            bg=constants.BACKGROUND_COLOUR,
            anchor="w",
            justify=LEFT,
        )

        self.current_position_indicator_grame = (
            self.generate_current_position_indicator_frame(middle_frame)
        )

        self.text_label.pack(side=TOP, anchor="w", pady=(0, 0), fill="both")
        self.current_position_indicator_grame.pack(side=TOP, anchor="w")

        return middle_frame

    def generate_morse_code_alphabet_frame(self, bottom_frame):
        morse_code_alphabet_frame = tk.Frame(
            bottom_frame, bg=constants.BACKGROUND_COLOUR
        )
        row = 0
        column = 0
        for index, key in enumerate(constants.MORSE_CODE):
            morse_code_alphabet_frame.grid_rowconfigure(row, weight=1)
            morse_code_alphabet_frame.grid_columnconfigure(column, weight=1)
            symbol = constants.MORSE_CODE[key]
            symbol_label = tk.Label(
                morse_code_alphabet_frame,
                text=f"{symbol}  {key}",
                font=constants.LABEL_FONT_SMALL,
                bg=constants.BACKGROUND_COLOUR,
            )
            symbol_label.grid(row=row, column=column, padx=(16, 16), pady=(0, 5))
            if (index + 1) % 8 == 0:
                row += 1
                column = 0
            else:
                column += 1

        return morse_code_alphabet_frame

    def generate_selected_mode_frame(self, middle_frame):
        selected_mode_frame = tk.Frame(middle_frame, bg=constants.BACKGROUND_COLOUR)
        selected_mode_frame.grid_rowconfigure(0, weight=1)
        selected_mode_frame.grid_columnconfigure(0, weight=1)
        selected_mode_frame.grid_columnconfigure(1, weight=1)

        label = tk.Label(
            selected_mode_frame,
            text="Selected mode:",
            font=constants.LABEL_FONT_SMALL,
            bg=constants.BACKGROUND_COLOUR,
        )
        label.grid(row=0, column=0)

        selected_mode = self.headband_input.get_selected_mode()
        self.selected_mode_label = tk.Label(
            selected_mode_frame,
            text=selected_mode,
            font=constants.LABEL_FONT_SMALL_BOLD,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.selected_mode_label.grid(row=0, column=1)

        return selected_mode_frame

    def generate_bottom_frame(self):
        bottom_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)

        self.morse_code_alphabet_frame = self.generate_morse_code_alphabet_frame(
            bottom_frame
        )

        self.selected_mode_frame = self.generate_selected_mode_frame(bottom_frame)

        self.selected_mode_frame.pack(side=BOTTOM, pady=(10, 0))

        return bottom_frame

    def hide_action_label(self):
        self.action_label.config(
            text="Action: None", fg=constants.BACKGROUND_COLOUR, relief="flat"
        )

    def show_action_label(self, text):
        self.action_label.config(text=text, fg="black", relief="solid")

    def update_next_action_label(
        self, clench_length, selected_mode, copy_mode, show_morse_code
    ):
        if copy_mode is True:
            if clench_length == 1:
                self.show_action_label("Action: Click")
            elif clench_length >= 2 and clench_length <= 4:
                self.show_action_label("Action: Double click")
            elif clench_length >= 5 and clench_length <= 9:
                self.show_action_label("Action: Paste")
            elif clench_length >= 10 and clench_length <= 13:
                self.show_action_label("Action: Close copy mode")
            elif clench_length >= 14:
                self.hide_action_label()
        else:
            if clench_length == 1:
                self.show_action_label("Action: Dot")
            elif clench_length >= 2 and clench_length <= 4:
                self.show_action_label("Action: Line")
            elif clench_length >= 5 and clench_length <= 7:
                if selected_mode == "Beginner":
                    self.show_action_label("Action: Space")
                elif selected_mode == "Advanced":
                    self.hide_action_label()
            elif clench_length >= 8 and clench_length <= 9:
                self.show_action_label("Action: Delete last character")
            elif clench_length >= 10 and clench_length <= 11:
                self.show_action_label("Action: Change mode")
            elif clench_length >= 12 and clench_length <= 13:
                text = "Action: Show morse code"
                if show_morse_code is True:
                    text = "Action: Hide morse code"
                self.show_action_label(text)
            elif clench_length >= 14 and clench_length <= 15:
                self.show_action_label("Action: Open tutorial page")
            elif clench_length >= 16 and clench_length <= 20:
                self.show_action_label("Action: Open copy mode")
            elif clench_length > 20:
                self.hide_action_label()

    def update_selected_mode(self):
        self.headband_input.change_selected_mode()
        selected_mode = self.headband_input.get_selected_mode()
        self.selected_mode_label.config(text=selected_mode)

    def hide_show_morse_code(self, show_morse_code):
        if show_morse_code is True:
            self.morse_code_alphabet_frame.pack_forget()
        else:
            self.morse_code_alphabet_frame.pack(side=BOTTOM)
        self.headband_input.set_show_morse_code(not show_morse_code)

    def open_tutorial_page(self):
        self.headband_connection.unmap_listen_for_input()
        self.controller.show_frame(SixthPage)

    def update_text_label(self, text):
        self.text_label.config(text=text)
        if len(text) == 0:
            self.current_possition_label_up.grid_forget()
        else:
            text_after_last_enter = text
            if "\n" in text:
                text_after_last_enter = self.headband_input.get_text_after_last_enter(
                    text
                )
            self.current_possition_label_up.config(
                text=text[: len(text_after_last_enter) - 1]
            )
            self.current_possition_label_up.grid(row=0, column=0, sticky="w")

    def handle_input(self, input_list):
        self.headband_input.handle_input(input_list, self)

    def listen_for_input(self):
        self.headband_connection.listen_for_input(self.handle_input)

    def listen_for_input_thread(self):
        self.input_thread = threading.Thread(target=self.listen_for_input, args=())
        self.input_thread.start()

    def handle_head_movement(self, input_list):
        self.headband_input.handle_head_movement(input_list, self)

    def listen_for_head_movement(self):
        self.headband_connection.listen_for_head_movement(self.handle_head_movement)

    def listen_for_head_movement_thread(self):
        self.head_movement_thread = threading.Thread(
            target=self.listen_for_head_movement, args=()
        )
        self.head_movement_thread.start()

    def start_copy_mode(self):
        self.listen_for_head_movement_thread()

    def stop_copy_mode(self):
        self.controller.focus_force()
        self.headband_connection.unmap_listen_for_head_movement()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.headband_connection = self.controller.headband_connection
        self.headband_input = self.controller.headband_input
        self.initialize_grid()

        self.upper_frame = self.generate_upper_frame()
        self.middle_frame = self.generate_middle_frame()
        self.bottom_frame = self.generate_bottom_frame()

        self.upper_frame.grid(
            row=0, column=0, columnspan=3, sticky="nswe", pady=(0, 20)
        )
        self.middle_frame.grid(
            row=1, column=0, columnspan=3, sticky="nswe", padx=(10, 10)
        )
        self.bottom_frame.grid(
            row=2, column=0, columnspan=3, sticky="ns", pady=(10, 10)
        )

    def start_threads(self):
        selected_mode = self.headband_input.get_selected_mode()
        self.selected_mode_label.config(text=selected_mode)
        if selected_mode == "Beginner":
            self.headband_input.set_show_morse_code(True)
            self.morse_code_alphabet_frame.pack(side=BOTTOM)
        self.listen_for_input_thread()
