from second_page import SecondPage
from user import User
from pythonosc import dispatcher
from pythonosc import osc_server
import asyncio
import threading
import sys


class Headband:
    def __init__(self, controller, ip, port=5000):
        self.ip = ip
        self.port = port
        self.controller = controller
        self.dispatcher = dispatcher.Dispatcher()
        self.server = osc_server.ThreadingOSCUDPServer(
            (self.ip, self.port), self.dispatcher
        )
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

    def connection_check_handler(self, address: str, *args):
        if args == (1.0, 1.0, 1.0, 1.0):
            self.dispatcher.unmap(
                "/muse/elements/horseshoe", self.connection_check_handler
            )
            self.parent.blink_detection_thread()

    def record_blink_handler(self, address: str, *args):
        self.dispatcher.unmap("/muse/elements/blink", self.record_blink_handler)
        self.parent.go_to_next_page()

    def connection_check(self, parent):
        self.parent = parent
        self.dispatcher.map("/muse/elements/horseshoe", self.connection_check_handler)

    def blink_detection(self, parent):
        self.parent = parent
        self.dispatcher.map("/muse/elements/blink", self.record_blink_handler)
