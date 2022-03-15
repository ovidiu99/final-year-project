import tkinter as tk
from tkinter import ttk
from tkinter.constants import HORIZONTAL
import threading
import time

import constants
from second_page import SecondPage


class FirstPage(tk.Frame):
    def initialise_grid(self):
        rows = 3
        columns = 3
        for row in range(rows):
            self.grid_rowconfigure(row, weight=1)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def generate_upper_frame(self):
        upper_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)
        self.welcome_label = tk.Label(
            upper_frame,
            text="Welcome to Head Writer",
            font=constants.TITLE_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.welcome_label.pack()
        return upper_frame

    def generate_middle_frame(self):
        middle_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)
        self.connect_label = tk.Label(
            middle_frame,
            text="Connect the headband to proceed",
            font=constants.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.connect_label.pack()
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
        self.progress_bar.pack(pady=(25, 0))
        self.progress_bar.start(20)

        self.blink_label = tk.Label(
            middle_frame,
            text="Blink twice to continue",
            font=constants.LABEL_FONT_BOLD,
            bg=constants.BACKGROUND_COLOUR,
            borderwidth=2,
            relief="solid",
        )

        return middle_frame

    def start_connection_check(self):
        for i in range(1, 4):
            time.sleep(1)
        self.controller.headband_connection.connection_check(
            self.connection_check_successful
        )

    def start_blink_twice_detection_check(self):
        self.progress_bar.pack_forget()
        self.connect_label.config(text="Headband connected")
        self.blink_label.pack(pady=(25, 0), ipadx=(5))
        self.controller.headband_connection.blink_twice_detection(self.blink_detected)

    def connection_check_successful(self):
        self.start_blink_twice_detection_check()

    def connection_check_thread(self):
        self.connection_thread = threading.Thread(
            target=self.start_connection_check, args=()
        )
        self.connection_thread.start()

    def blink_detected(self):
        self.controller.focus_force()
        self.controller.show_frame(SecondPage)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.initialise_grid()

        self.upper_frame = self.generate_upper_frame()
        self.upper_frame.grid(row=0, column=0, columnspan=3)

        self.middle_frame = self.generate_middle_frame()
        self.middle_frame.grid(row=1, column=0, columnspan=3)

    def start_processes(self):
        self.connection_check_thread()
