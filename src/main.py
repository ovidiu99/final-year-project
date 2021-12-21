from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio

from headband import Headband

import tkinter as tk
from tkinter import font


from first_page import FirstPage
from second_page import SecondPage


class Main(tk.Tk):
    frame_width = 800
    frame_height = 500

    def __init__(self, ip, port, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.headband = Headband(self, ip, port)

        self.TITLE_FONT = font.Font(family="Helvetica", size=30, weight="bold")
        self.LABEL_FONT = font.Font(family="Helvetica", size=24)

        self.geometry(f"{self.frame_width}x{self.frame_height}")

        main_frame = tk.Frame(self)
        main_frame.pack(side="top", fill="both", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for frame in (FirstPage, SecondPage):
            page_frame = frame(main_frame, self)
            self.frames[frame] = page_frame

            page_frame.grid(row=0, column=0, sticky="nsew")

        # Show the first page
        self.show_frame(FirstPage)

    def show_frame(self, page):
        """Show a frame for the given page name"""
        frame = self.frames[page]
        frame.tkraise()


if __name__ == "__main__":
    main = Main("192.168.100.96", 5000)
    main.mainloop()
