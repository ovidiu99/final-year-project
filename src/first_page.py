import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter.constants import HORIZONTAL
import threading
import time

import constants
from second_page import SecondPage


class FirstPage(tk.Frame):
    def initialize_grid(self):
        rows = 3
        columns = 3
        for row in range(rows):
            self.grid_rowconfigure(row, weight=1)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def generate_middle_frame(self):
        self.middle_frame = tk.Frame(self, bg=constants.BACKGROUND_COLOUR)
        self.connect_label = tk.Label(
            self.middle_frame,
            text="Connect the headband to proceed",
            font=self.controller.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.connect_label.pack()
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("red.Horizontal.TProgressbar", foreground="red", background="red")
        self.progress_bar = ttk.Progressbar(
            self.middle_frame,
            style="red.Horizontal.TProgressbar",
            orient=HORIZONTAL,
            length=50,
            mode="indeterminate",
        )
        self.progress_bar.pack()
        self.progress_bar.start(50)

        return self.middle_frame

    def start_connection_check(self):
        for i in range(1, 4):
            time.sleep(1)
        self.controller.headband.connection_check(self)

    def start_blink_detection_check(self):
        time.sleep(1)
        self.progress_bar.pack_forget()
        self.connect_label.config(text="Headband connected!")
        self.blink_label.grid(row=2, column=0, columnspan=3)
        self.controller.headband.blink_detection(self)

    def connection_check_thread(self):
        self.connection_thread = threading.Thread(
            target=self.start_connection_check, args=()
        )
        self.connection_thread.start()

    def blink_detection_thread(self):
        self.blink_thread = threading.Thread(
            target=self.start_blink_detection_check, args=()
        )
        self.blink_thread.start()

    def go_to_next_page(self):
        self.controller.show_frame(SecondPage)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=constants.BACKGROUND_COLOUR)
        self.controller = controller
        self.initialize_grid()

        self.welcome_label = tk.Label(
            self,
            text="Welcome to Head Writer!",
            font=controller.TITLE_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )
        self.welcome_label.grid(row=0, column=0, columnspan=3)

        middle_frame = self.generate_middle_frame()
        middle_frame.grid(row=1, column=0, columnspan=3)

        self.blink_label = tk.Label(
            self,
            text="Everything ready! Blink to continue.",
            font=controller.LABEL_FONT,
            bg=constants.BACKGROUND_COLOUR,
        )

        self.connection_check_thread()
