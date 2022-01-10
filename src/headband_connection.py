from pythonosc import dispatcher
from pythonosc import osc_server
import threading


class HeadbandConnection:
    def __init__(self, controller, ip, port=5000):
        self.ip = ip
        self.port = port
        self.controller = controller
        self.headband_input = self.controller.headband_input
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
            self.trigger_function()

    def record_blink_twice_handler(self, address: str, *args):
        self.headband_input.add_blink_count()
        if self.headband_input.get_blink_count() == 2:
            self.headband_input.clear_blink_count()
            self.dispatcher.unmap(
                "/muse/elements/blink", self.record_blink_twice_handler
            )
            self.trigger_function()

    def record_clench_handler(self, address: str, *args):
        self.dispatcher.unmap("/muse/elements/jaw_clench", self.record_clench_handler)
        self.trigger_function()

    def record_normal_state_handler(self, address: str, *args):
        self.headband_input.save_egg_calm_state_values([list(args)[1], list(args)[2]])

    def record_clenching_state_handler(self, address: str, *args):
        self.headband_input.save_egg_clenching_state_values(
            [list(args)[1], list(args)[2]]
        )

    def listen_for_input_handler(self, address: str, *args):
        self.trigger_function([args[1], args[2]])

    # UNMAPPINGS
    def unmap_record_normal_state(self):
        self.dispatcher.unmap("/muse/eeg", self.record_normal_state_handler)

    def unmap_record_clenching_state(self):
        self.dispatcher.unmap("/muse/eeg", self.record_clenching_state_handler)

    # ACTIONS
    def connection_check(self, trigger_function=None):
        self.trigger_function = trigger_function
        self.dispatcher.map("/muse/elements/horseshoe", self.connection_check_handler)

    def blink_twice_detection(self, trigger_function=None):
        self.trigger_function = trigger_function
        self.dispatcher.map("/muse/elements/blink", self.record_blink_twice_handler)

    def clench_detection(self, trigger_function=None):
        self.trigger_function = trigger_function
        self.dispatcher.map("/muse/elements/jaw_clench", self.record_clench_handler)

    def record_normal_state(self):
        self.dispatcher.map("/muse/eeg", self.record_normal_state_handler)

    def record_clenching_state(self):
        self.dispatcher.map("/muse/eeg", self.record_clenching_state_handler)

    def listen_for_input(self, trigger_function):
        self.trigger_function = trigger_function
        self.headband_input.reinitialize_timer()
        self.dispatcher.map("/muse/eeg", self.listen_for_input_handler)
