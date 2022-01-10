import time

from constants import MORSE_CODE


class HeadbandInput:
    _blink_count = 0

    _eeg_calm_state_values = []
    _eeg_clenching_state_values = []

    _average_difference_af7_calm_state = None
    _average_difference_af8_calm_state = None

    _average_difference_af7_clenching_state = None
    _average_difference_af8_clenching_state = None

    _input_listening_values = []

    _clenching_sequence = []
    _dots_lines_sequence = ""
    _output_sequence = ""

    _pause_units = 0

    _timer = time.time()

    def get_blink_count(self):
        return self._blink_count

    def add_blink_count(self):
        self._blink_count += 1

    def clear_blink_count(self):
        self._blink_count = 0

    def save_egg_calm_state_values(self, eeg_list):
        self._eeg_calm_state_values.append(eeg_list)

    def get_egg_calm_state_values(self):
        return self._eeg_calm_state_values

    def save_egg_clenching_state_values(self, eeg_list):
        self._eeg_clenching_state_values.append(eeg_list)

    def get_egg_clenching_state_values(self):
        return self._eeg_clenching_state_values

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

    def update_average_difference(self, average_difference, counter, high, low):
        return (average_difference * (counter - 1) + (high - low)) / counter

    def calculate_average_difference(self, list=[]):
        last_highest_point_af7 = -1
        last_lowest_point_af7 = -1
        af7_counter = 1
        last_highest_point_af8 = -1
        last_lowest_point_af8 = -1
        af8_counter = 1

        average_difference_af7 = -1
        average_difference_af8 = -1

        for i in range(1, len(list) - 1):
            # AF7 sensor
            if list[i - 1][0] < list[i][0] and list[i][0] > list[i + 1][0]:
                last_highest_point_af7 = list[i][0]
                if last_lowest_point_af7 != -1:
                    average_difference_af7 = self.update_average_difference(
                        average_difference_af7,
                        af7_counter,
                        last_highest_point_af7,
                        last_lowest_point_af7,
                    )
                    af7_counter += 1
            elif list[i - 1][0] > list[i][0] and list[i][0] < list[i + 1][0]:
                last_lowest_point_af7 = list[i][0]
                if last_highest_point_af7 != -1:
                    average_difference_af7 = self.update_average_difference(
                        average_difference_af7,
                        af7_counter,
                        last_highest_point_af7,
                        last_lowest_point_af7,
                    )
                    af7_counter += 1
            # AF8 sensor
            if list[i - 1][1] < list[i][1] and list[i][1] > list[i + 1][1]:
                last_highest_point_af8 = list[i][1]
                if last_lowest_point_af8 != -1:
                    average_difference_af8 = self.update_average_difference(
                        average_difference_af8,
                        af8_counter,
                        last_highest_point_af8,
                        last_lowest_point_af8,
                    )
                    af8_counter += 1
            elif list[i - 1][1] > list[i][1] and list[i][1] < list[i + 1][1]:
                last_lowest_point_af8 = list[i][1]
                if last_highest_point_af8 != -1:
                    average_difference_af8 = self.update_average_difference(
                        average_difference_af8,
                        af8_counter,
                        last_highest_point_af8,
                        last_lowest_point_af8,
                    )
                    af8_counter += 1

        return average_difference_af7, average_difference_af8

    def calculate_average_calm_state_difference(self):
        (
            self._average_difference_af7_calm_state,
            self._average_difference_af8_calm_state,
        ) = self.calculate_average_difference(self._eeg_calm_state_values)

    def calculate_average_clenching_state_difference(self):
        (
            self._average_difference_af7_clenching_state,
            self._average_difference_af8_clenching_state,
        ) = self.calculate_average_difference(self._eeg_clenching_state_values)

    def reinitialize_timer(self):
        self._timer = time.time()

    def trim_string(self, string, numer_of_chars):
        return string[: len(string) - numer_of_chars]

    def handle_unit_clenches(self):
        self._clenching_sequence.append(1)
        self._output_sequence += "~"
        self._pause_units = 0

    def handle_unit_pauses_advanced_mode(self):
        clenching_sequence_lenght = len(self._clenching_sequence)
        self._output_sequence = self.trim_string(
            self._output_sequence, clenching_sequence_lenght
        )
        self._pause_units += 1
        if self._pause_units < 3 and clenching_sequence_lenght > 0:
            if clenching_sequence_lenght == 1:
                self._dots_lines_sequence += "."
                self._output_sequence += "."
            elif clenching_sequence_lenght >= 2 and clenching_sequence_lenght <= 4:
                self._dots_lines_sequence += "-"
                self._output_sequence += "-"
        elif self._pause_units == 3 and self._dots_lines_sequence != "":
            symbol = None
            sequence = self._dots_lines_sequence
            self._output_sequence = self.trim_string(
                self._output_sequence, len(sequence)
            )
            if sequence in MORSE_CODE.keys():
                symbol = MORSE_CODE[sequence]
                self._output_sequence += symbol
            self._dots_lines_sequence = ""
        elif self._pause_units == 7 and self._output_sequence[-1] != " ":
            self._output_sequence += " "

        self._clenching_sequence = []

    def handle_input(self, egg_list, current_page):
        self._input_listening_values.append(egg_list)
        if time.time() - self._timer >= 0.25:
            self._timer = time.time()
            values = self._input_listening_values
            threshold_af7, threshold_af8 = self.get_clenching_threshold_values()
            (
                average_af7_difference,
                average_af8_difference,
            ) = self.calculate_average_difference(values)
            if (average_af7_difference >= threshold_af7) or (
                average_af8_difference >= threshold_af8
            ):
                self.handle_unit_clenches()
            else:
                self.handle_unit_pauses_advanced_mode()

            current_page.update_text_label(self._output_sequence)
            self._input_listening_values = []
