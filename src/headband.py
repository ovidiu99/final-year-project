from pythonosc import dispatcher
from pythonosc import osc_server
import threading

import time

from headband_input import HeadbandInputCalculation


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

    # HANDLERS
    def connection_check_handler(self, address: str, *args):
        sensors_list = [args[1], args[2]]
        if sensors_list == [1.0, 1.0]:
            self.dispatcher.unmap(
                "/muse/elements/horseshoe", self.connection_check_handler
            )
            self.parent_function()

    def record_blink_handler(self, address: str, *args):
        self.dispatcher.unmap("/muse/elements/blink", self.record_blink_handler)
        self.parent_function()

    def record_clench_handler(self, address: str, *args):
        self.dispatcher.unmap("/muse/elements/jaw_clench", self.record_clench_handler)
        self.parent_function()

    def record_normal_state_handler(self, address: str, *args):
        self.user.save_egg_calm_state_values([list(args)[1], list(args)[2]])

    def record_clenching_state_handler(self, address: str, *args):
        self.user.save_egg_clenching_state_values([list(args)[1], list(args)[2]])

    def update_average_difference(self, average_difference, counter, high, low):
        return (average_difference * (counter - 1) + (high - low)) / counter

    def listen_for_input_handler(self, address: str, *args):
        self.user.save_input_listening_values([list(args)[1], list(args)[2]])
        if time.time() - self.timer >= 0.25:
            self.timer = time.time()
            values = self.user.get_input_listening_values()
            threshold_af7, threshold_af8 = self.user.get_clenching_threshold_values()
            (
                average_af7_difference,
                average_af8_difference,
            ) = HeadbandInputCalculation.calculate_average_difference(values)
            if (average_af7_difference >= threshold_af7) or (
                average_af8_difference >= threshold_af8
            ):
                self.user.clear_input_listening_values()
                self.user.add_to_sequence()
            else:
                self.user.clear_input_listening_values()
                sequence = self.user.get_sequence()
                self.user.clear_sequence()

    # UNMAPPINGS
    def unmap_record_normal_state(self):
        self.dispatcher.unmap("/muse/eeg", self.record_normal_state_handler)

    def unmap_record_clenching_state(self):
        self.dispatcher.unmap("/muse/eeg", self.record_clenching_state_handler)

    # ACTIONS
    def connection_check(self, parent_function=None):
        self.parent_function = parent_function
        self.dispatcher.map("/muse/elements/horseshoe", self.connection_check_handler)

    def blink_detection(self, parent_function=None):
        self.parent_function = parent_function
        self.dispatcher.map("/muse/elements/blink", self.record_blink_handler)

    def clench_detection(self, parent_function=None):
        self.parent_function = parent_function
        self.dispatcher.map("/muse/elements/jaw_clench", self.record_clench_handler)

    def record_normal_state(self):
        self.dispatcher.map("/muse/eeg", self.record_normal_state_handler)

    def record_clenching_state(self):
        self.dispatcher.map("/muse/eeg", self.record_clenching_state_handler)

    def listen_for_input(self):
        self.timer = time.time()
        self.dispatcher.map("/muse/eeg", self.listen_for_input_handler)
