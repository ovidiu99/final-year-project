class User:
    def __init__(self):
        self.eeg_calm_state_values = []
        self.eeg_clenching_state_values = []

        self.number_of_iterations_calm_state = 1
        self.number_of_iterations_clenching_state = 1

        self.average_eeg_calm_state = [0, 0, 0, 0]
        self.average_eeg_jaw_clench = [0, 0, 0, 0]

    def save_egg_calm_state_values(self, eeg_list):
        self.eeg_calm_state_values.append(eeg_list)

    def save_egg_clenching_state_values(self, eeg_list):
        self.eeg_clenching_state_values.append(eeg_list)

    def update_average_eeg_calm_state(self, eeg_list):
        self.average_eeg_calm_state = [
            (i * (self.number_of_iterations_calm_state - 1) + j)
            / self.number_of_iterations_calm_state
            for i, j in zip(self.average_eeg_calm_state, eeg_list)
        ]
        self.number_of_iterations_calm_state += 1

    def update_average_eeg_clenching_state(self, eeg_list):
        self.average_eeg_jaw_clench = [
            (i * (self.number_of_iterations_clenching_state - 1) + j)
            / self.number_of_iterations_clenching_state
            for i, j in zip(self.average_eeg_jaw_clench, eeg_list)
        ]
        self.number_of_iterations_clenching_state += 1
