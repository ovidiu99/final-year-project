class User:
    _eeg_calm_state_values = []
    _eeg_clenching_state_values = []

    _average_difference_af7_calm_state = None
    _average_difference_af8_calm_state = None

    _average_difference_af7_clenching_state = None
    _average_difference_af8_clenching_state = None

    def save_egg_calm_state_values(self, eeg_list):
        self._eeg_calm_state_values.append(eeg_list)

    def save_egg_clenching_state_values(self, eeg_list):
        self._eeg_clenching_state_values.append(eeg_list)

    def update_average_difference(self, average_difference, counter, high, low):
        return (average_difference * (counter - 1) + (high - low)) / counter

    def calculate_average_difference(self, state="calm"):
        last_highest_point_af7 = None
        last_lowest_point_af7 = None
        af7_counter = 1
        last_highest_point_af8 = None
        last_lowest_point_af8 = None
        af8_counter = 1

        average_difference_af7 = 0
        average_difference_af8 = 0

        list = []

        if state == "calm":
            list = self._eeg_calm_state_values
        elif state == "clenching":
            list = self._eeg_clenching_state_values

        for i in range(1, len(list) - 1):
            # AF7 sensor
            if list[i - 1][0] < list[i][0] and list[i][0] > list[i + 1][0]:
                last_highest_point_af7 = list[i][0]
                if last_lowest_point_af7 is not None:
                    average_difference_af7 = self.update_average_difference(
                        average_difference_af7,
                        af7_counter,
                        last_highest_point_af7,
                        last_lowest_point_af7,
                    )
                    af7_counter += 1
            elif list[i - 1][0] > list[i][0] and list[i][0] < list[i + 1][0]:
                last_lowest_point_af7 = list[i][0]
                if last_highest_point_af7 is not None:
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
                if last_lowest_point_af8 is not None:
                    average_difference_af8 = self.update_average_difference(
                        average_difference_af8,
                        af8_counter,
                        last_highest_point_af8,
                        last_lowest_point_af8,
                    )
                    af8_counter += 1
            elif list[i - 1][1] > list[i][1] and list[i][1] < list[i + 1][1]:
                last_lowest_point_af8 = list[i][1]
                if last_highest_point_af8 is not None:
                    average_difference_af8 = self.update_average_difference(
                        average_difference_af8,
                        af8_counter,
                        last_highest_point_af8,
                        last_lowest_point_af8,
                    )
                    af8_counter += 1

        if state == "calm":
            self._average_difference_af7_calm_state = average_difference_af7
            self._average_difference_af8_calm_state = average_difference_af8
        elif state == "clenching":
            self._average_difference_af7_clenching_state = average_difference_af7
            self._average_difference_af8_clenching_state = average_difference_af8
