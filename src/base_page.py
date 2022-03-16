import tkinter as tk
from tkinter import ttk
from tkinter.constants import HORIZONTAL
import threading
import time

import constants
from second_page import SecondPage


class BasePage(tk.Frame):
    def initialise_grid(self):
        print("INITIALISING IN", self)
        rows = 3
        columns = 3
        for row in range(rows):
            self.grid_rowconfigure(row, weight=1)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)
