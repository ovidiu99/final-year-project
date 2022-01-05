from headband_input import HeadbandInputCalculation


class User:
    _eeg_calm_state_values = []
    _eeg_clenching_state_values = []

    _average_difference_af7_calm_state = None
    _average_difference_af8_calm_state = None

    _average_difference_af7_clenching_state = None
    _average_difference_af8_clenching_state = None

    _input_listening_values = []
    _sequence = []

    def save_egg_calm_state_values(self, eeg_list):
        self._eeg_calm_state_values.append(eeg_list)

    def get_egg_calm_state_values(self):
        return self._eeg_calm_state_values

    def save_egg_clenching_state_values(self, eeg_list):
        self._eeg_clenching_state_values.append(eeg_list)

    def get_egg_clenching_state_values(self):
        return self._eeg_clenching_state_values

    def save_input_listening_values(self, eeg_list):
        self._input_listening_values.append(eeg_list)

    def clear_input_listening_values(self):
        self._input_listening_values = []

    def get_input_listening_values(self):
        return self._input_listening_values

    def get_clenching_threshold_values(self):
        threshold_af7 = (
            self._average_difference_af7_calm_state
            + self._average_difference_af7_clenching_state
        ) / 2
        threshold_af8 = (
            self._average_difference_af8_calm_state
            + self._average_difference_af8_clenching_state
        ) / 2
        return threshold_af7, threshold_af8

    def add_to_sequence(self):
        self._sequence.append(1)

    def get_sequence(self):
        return self._sequence

    def clear_sequence(self):
        self._sequence = []

    def update_average_difference(self, average_difference, counter, high, low):
        return (average_difference * (counter - 1) + (high - low)) / counter

    def calculate_average_calm_state_difference(self):
        (
            self._average_difference_af7_calm_state,
            self._average_difference_af8_calm_state,
        ) = HeadbandInputCalculation.calculate_average_difference(
            self._eeg_calm_state_values
        )

    def calculate_average_clenching_state_difference(self):
        (
            self._average_difference_af7_clenching_state,
            self._average_difference_af8_clenching_state,
        ) = HeadbandInputCalculation.calculate_average_difference(
            self._eeg_clenching_state_values
        )
