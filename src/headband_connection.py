from pythonosc import dispatcher
from pythonosc import osc_server
import threading
import time


class HeadbandConnection:

    _listen_for_input_action = None
    _connection_check_action = None
    _blink_twice_detection_action = None
    _clench_detection_action = None

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
            self._connection_check_action()

    def record_blink_twice_handler(self, address: str, *args):
        blink_count = self.headband_input.get_blink_count()
        last_blink_timer = self.headband_input.get_last_blink_timer()
        if blink_count == 0:
            self.headband_input.add_blink_count()

        # reinitialise the blink count
        blink_count = self.headband_input.get_blink_count()
        if blink_count == 1 and last_blink_timer is None:
            self.headband_input.reinitialise_last_blink_timer()
        elif blink_count == 1 and time.time() - last_blink_timer <= 1:
            self.headband_input.add_blink_count()
        elif blink_count == 1 and time.time() - last_blink_timer > 1:
            self.headband_input.reinitialise_last_blink_timer()

        # reinitialise the blink count
        blink_count = self.headband_input.get_blink_count()
        if blink_count == 2:
            self.headband_input.clear_blink_count()
            self.dispatcher.unmap(
                "/muse/elements/blink", self.record_blink_twice_handler
            )
            self._blink_twice_detection_action()

    def record_clench_handler(self, address: str, *args):
        self.dispatcher.unmap("/muse/elements/jaw_clench", self.record_clench_handler)
        self._clench_detection_action()

    def record_normal_state_handler(self, address: str, *args):
        self.headband_input.save_eeg_calm_state_values([list(args)[1], list(args)[2]])

    def record_clenching_state_handler(self, address: str, *args):
        self.headband_input.save_eeg_clenching_state_values(
            [list(args)[1], list(args)[2]]
        )

    def listen_for_input_handler(self, address: str, *args):
        self._listen_for_input_action([args[1], args[2]])

    def listen_for_head_movement_handler(self, address: str, *args):
        self._listen_for_head_movement_action([args[1], args[2]])

    def listen_for_battery_handler(self, address: str, *args):
        self._listen_for_battery_action(args[0])

    def listen_for_connection_handler(self, address: str, *args):
        self._listen_for_connection_action([args[1], args[2]])

    # UNMAPPINGS
    def unmap_blink_twice_detection(self):
        self.dispatcher.unmap("/muse/elements/blink", self.record_blink_twice_handler)

    def unmap_clench_detection(self):
        self.dispatcher.unmap("/muse/elements/jaw_clench", self.record_clench_handler)

    def unmap_record_normal_state(self):
        self.dispatcher.unmap("/muse/eeg", self.record_normal_state_handler)

    def unmap_record_clenching_state(self):
        self.dispatcher.unmap("/muse/eeg", self.record_clenching_state_handler)

    def unmap_listen_for_input(self):
        self.dispatcher.unmap("/muse/eeg", self.listen_for_input_handler)

    def unmap_listen_for_head_movement(self):
        self.dispatcher.unmap("/muse/gyro", self.listen_for_head_movement_handler)

    def unmap_listen_for_battery(self):
        self.dispatcher.unmap("/muse/batt", self.listen_for_battery_handler)

    def unmap_listen_for_connection(self):
        self.dispatcher.unmap(
            "/muse/elements/horseshoe", self.listen_for_connection_handler
        )

    # ACTIONS
    def connection_check(self, trigger_function=None):
        self._connection_check_action = trigger_function
        self.dispatcher.map("/muse/elements/horseshoe", self.connection_check_handler)

    def blink_twice_detection(self, trigger_function=None):
        self._blink_twice_detection_action = trigger_function
        self.dispatcher.map("/muse/elements/blink", self.record_blink_twice_handler)

    def clench_detection(self, trigger_function=None):
        self._clench_detection_action = trigger_function
        self.dispatcher.map("/muse/elements/jaw_clench", self.record_clench_handler)

    def record_normal_state(self):
        self.dispatcher.map("/muse/eeg", self.record_normal_state_handler)

    def record_clenching_state(self):
        self.dispatcher.map("/muse/eeg", self.record_clenching_state_handler)

    def listen_for_input(self, trigger_function):
        self._listen_for_input_action = trigger_function
        self.headband_input.reinitialise_input_timer()
        self.dispatcher.map("/muse/eeg", self.listen_for_input_handler)

    def listen_for_head_movement(self, trigger_function):
        self._listen_for_head_movement_action = trigger_function
        self.dispatcher.map("/muse/gyro", self.listen_for_head_movement_handler)

    def listen_for_battery(self, trigger_function):
        self._listen_for_battery_action = trigger_function
        self.dispatcher.map("/muse/batt", self.listen_for_battery_handler)

    def listen_for_connection(self, trigger_function):
        self._listen_for_connection_action = trigger_function
        self.dispatcher.map(
            "/muse/elements/horseshoe", self.listen_for_connection_handler
        )
