from headband_connection import HeadbandConnection

import tkinter as tk
import constants
import socket

from first_page import FirstPage
from headband_input import HeadbandInput
from second_page import SecondPage
from seventh_page import SeventhPage
from third_page import ThirdPage
from fourth_page import FourthPage
from fifth_page import FifthPage
from sixth_page import SixthPage


class Main(tk.Tk):
    frame_width = 800
    frame_height = 600

    def handle_battery_value(self, value):
        self.battery_label.config(text=f" {int(value/100)}% ")

    def listen_for_battery(self):
        self.headband_connection.listen_for_battery(self.handle_battery_value)

    def handle_connection_values(self, values):
        connection_value = sum(values)
        connection_text = ""
        if connection_value >= 2.0 and connection_value < 4.0:
            connection_text = f" Connection: Good "
        elif connection_value >= 4.0 and connection_value < 8.0:
            connection_text = f" Connection: Medium "
        elif connection_value >= 8.0:
            connection_text = f" Connection: Bad "

        self.connection_label.config(text=connection_text)

    def listen_for_connection(self):
        self.headband_connection.listen_for_connection(self.handle_connection_values)

    def __init__(self, ip, port, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.headband_input = HeadbandInput()
        self.headband_connection = HeadbandConnection(self, ip, port)

        # region Set of the window's title and size
        self.title("Head Writer")
        self.geometry(f"{self.frame_width}x{self.frame_height}")
        # endregion

        # region Initialise main frame
        main_frame = tk.Frame(self)
        main_frame.pack(side="top", fill="both", expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        # endregion

        # region Battery and connection labels
        self.battery_label = tk.Label(
            self,
            text=" - % ",
            font=constants.LABEL_FONT_VERY_SMALL_BOLD,
            bg=constants.BACKGROUND_COLOUR,
            borderwidth=1,
            relief="solid",
        )

        self.connection_label = tk.Label(
            self,
            text="",
            font=constants.LABEL_FONT_VERY_SMALL_BOLD,
            bg=constants.BACKGROUND_COLOUR,
        )
        # endregion

        # region Initialise all the other pages
        self.frames = {}
        for frame in (
            FirstPage,
            SecondPage,
            ThirdPage,
            FourthPage,
            FifthPage,
            SixthPage,
            SeventhPage,
        ):
            page_frame = frame(main_frame, self)
            self.frames[frame] = page_frame

            page_frame.grid(row=0, column=0, sticky="nsew")
        # endregion

        # Show the first page
        self.show_frame(FirstPage)

    def show_frame(self, page):
        """Show a frame for the given page name"""
        frame = self.frames[page]
        frame.tkraise()
        frame.start_processes()

        if page == SecondPage:
            self.battery_label.place(relx=0.01, rely=0.98, anchor="sw")
            self.connection_label.place(relx=0.99, rely=0.98, anchor="se")
            self.listen_for_battery()
            self.listen_for_connection()


def get_ip_address():
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect(("8.8.8.8", 80))
    return ip.getsockname()[0]


if __name__ == "__main__":
    main = Main(get_ip_address(), 5000)
    main.lift()
    main.attributes("-topmost", True)
    main.mainloop()
