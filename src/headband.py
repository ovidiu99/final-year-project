from pythonosc import dispatcher
from pythonosc import osc_server
import threading

import time


class Headband:
    def __init__(self, controller, ip, port=5000):
        self.ip = ip
        self.port = port
        self.controller = controller
        self.user = self.controller.user
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
            self.parent_function()

    def record_blink_handler(self, address: str, *args):
        self.dispatcher.unmap("/muse/elements/blink", self.record_blink_handler)
        self.parent_function()

    def record_normal_state_handler(self, address: str, *args):
        self.user.update_average_eeg_calm_state(list(args))

    def connection_check(self, parent_function):
        self.parent_function = parent_function
        self.dispatcher.map("/muse/elements/horseshoe", self.connection_check_handler)

    def blink_detection(self, parent_function):
        self.parent_function = parent_function
        self.dispatcher.map("/muse/elements/blink", self.record_blink_handler)

    def record_normal_state(self):
        self.timer = time.time()
        self.dispatcher.map("/muse/eeg", self.record_normal_state_handler)
