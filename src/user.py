class User:
    number_of_iterations_calm_state = 1
    average_eeg_calm_state = [0, 0, 0, 0]
    average_eeg_jaw_clench = [0, 0, 0, 0]

    def update_average_eeg_calm_state(self, eeg_list):
        self.average_eeg_calm_state = [
            self.average_eeg_calm_state[i] + eeg_list[i] for i in range(len(eeg_list))
        ]
