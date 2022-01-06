import time


class HeadbandInput:
    _eeg_calm_state_values = []
    _eeg_clenching_state_values = []

    _average_difference_af7_calm_state = None
    _average_difference_af8_calm_state = None

    _average_difference_af7_clenching_state = None
    _average_difference_af8_clenching_state = None

    _input_listening_values = []
    _sequence = []

    _timer = time.time()

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

    def handle_input(self, egg_list):
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
                print("CLENCHING")
                self._sequence.append(1)
            else:
                self._sequence = []

            self._input_listening_values = []
