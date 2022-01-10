from headband_connection import HeadbandConnection

import tkinter as tk

from first_page import FirstPage
from headband_input import HeadbandInput
from second_page import SecondPage
from third_page import ThirdPage
from fourth_page import FourthPage
from fifth_page import FifthPage


class Main(tk.Tk):
    frame_width = 800
    frame_height = 500

    def __init__(self, ip, port, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.headband_input = HeadbandInput()
        self.headband_connection = HeadbandConnection(self, ip, port)

        self.geometry(f"{self.frame_width}x{self.frame_height}")

        main_frame = tk.Frame(self)
        main_frame.pack(side="top", fill="both", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for frame in (FirstPage, SecondPage, ThirdPage, FourthPage, FifthPage):
            page_frame = frame(main_frame, self)
            self.frames[frame] = page_frame

            page_frame.grid(row=0, column=0, sticky="nsew")

        # Show the first page
        self.show_frame(FirstPage)

    def show_frame(self, page):
        """Show a frame for the given page name"""
        frame = self.frames[page]
        frame.tkraise()
        frame.start_threads()


if __name__ == "__main__":
    main = Main("192.168.100.193", 5000)
    main.mainloop()
