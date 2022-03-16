import tkinter as tk


class BasePage(tk.Frame):
    def initialise_grid(self):
        print("INITIALISING IN", self)
        rows = 3
        columns = 3
        for row in range(rows):
            self.grid_rowconfigure(row, weight=1)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)
