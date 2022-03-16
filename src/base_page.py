import constants
import tkinter as tk


class BasePage(tk.Frame):
    def initialise_grid(self):
        rows = 3
        columns = 3
        for row in range(rows):
            self.grid_rowconfigure(row, weight=1)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def hide_action_label(self):
        self.action_label.config(
            text="Action: None", fg=constants.BACKGROUND_COLOUR, relief="flat"
        )

    def show_action_label(self, text):
        self.action_label.config(text=text, fg="black")
