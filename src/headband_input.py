import time
import pyautogui
import pyperclip

from constants import MORSE_CODE


class HeadbandInput:

    # Private variables
    _blink_count = 0
    _last_blink_timer = None

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

    _selected_mode = "Beginner"

    _writing_started = False

    _input_timer = time.time()

    _enter_count = 0

    _show_morse_code = False

    _copy_mode = False

    _screen_width, _screen_height = pyautogui.size()

    # Getter and setter for the blink count
    def get_blink_count(self):
        return self._blink_count

    def set_blink_count(self, value):
        self._blink_count = value

    # Getter and setter for the last blink timer
    def get_last_blink_timer(self):
        return self._last_blink_timer

    def reinitialise_last_blink_timer(self):
        self._last_blink_timer = time.time()

    # Getter and setters for the calm eeg values
    def get_eeg_calm_state_values(self):
        return self._eeg_calm_state_values

    def save_eeg_calm_state_values(self, eeg_list):
        self._eeg_calm_state_values.append(eeg_list)

    def reinitialise_eeg_calm_state_values(self):
        self._eeg_calm_state_values = []

    def get_show_morse_code(self):
        return self._show_morse_code

    def set_show_morse_code(self, value):
        self._show_morse_code = value

    def add_blink_count(self):
        self._blink_count += 1

    def clear_blink_count(self):
        self._blink_count = 0

    def save_eeg_clenching_state_values(self, eeg_list):
        self._eeg_clenching_state_values.append(eeg_list)

    def reinitialise_eeg_clenching_state_values(self):
        self._eeg_clenching_state_values = []

    def get_eeg_clenching_state_values(self):
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

    def change_selected_mode(self):
        if self._selected_mode == "Beginner":
            self._selected_mode = "Advanced"
        else:
            self._selected_mode = "Beginner"

    def get_selected_mode(self):
        return self._selected_mode

    def set_writing_started(self):
        self._writing_started = True

    def get_writing_started(self):
        return self._writing_started

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

    def reinitialise_input_timer(self):
        self._input_timer = time.time()

    def trim_string(self, string, numer_of_chars):
        return string[: len(string) - numer_of_chars]

    def clean_output_sequence(self):
        self._output_sequence = ""

    def get_output_sequence_without_enters(self):
        return self._output_sequence.replace("\n", "")

    def get_number_of_enters(self):
        return self._output_sequence.count("\n")

    def get_text_after_last_enter(self, text):
        text_after_last_enter = text
        if "\n" in text:
            text_length = len(text)
            reversed_text = text[::-1]
            enter_in_reversed_text = reversed_text.index("\n")
            last_enter_index = text_length - 1 - enter_in_reversed_text
            text_after_last_enter = text[-(len(text) - last_enter_index - 1) :]
        return text_after_last_enter

    def max_characters_not_reached(self):
        number_of_enters = self.get_number_of_enters()
        text_after_last_enter = self.get_text_after_last_enter(self._output_sequence)
        return not (
            (
                (self._show_morse_code is True and number_of_enters == 10)
                or (self._show_morse_code is False and number_of_enters == 19)
            )
            and (len(self._output_sequence) > 0 and len(text_after_last_enter) == 62)
        )

    def is_new_row_needed(self):
        number_of_enters = self.get_number_of_enters()
        text_after_last_enter = self.get_text_after_last_enter(self._output_sequence)
        return (
            (self._show_morse_code is True and number_of_enters < 10)
            or (self._show_morse_code is False and number_of_enters < 19)
        ) and (len(self._output_sequence) > 0 and len(text_after_last_enter) == 62)

    def add_to_output_sequence(self, text):
        if self.max_characters_not_reached():
            if self.is_new_row_needed():
                self._output_sequence += "\n"
                self._enter_count += 1
            self._output_sequence += text

    def handle_unit_clenches_seventh_page(self, current_page):
        self._clenching_sequence.append(1)
        if self._copy_mode is False:
            self.add_to_output_sequence("~")
        self._pause_units = 0
        current_page.update_next_action_label(
            len(self._clenching_sequence),
            self._selected_mode,
            self._copy_mode,
            self._show_morse_code,
            self._dots_lines_sequence != "",
        )

    def handle_extra_commands(self, clenching_sequence_length, current_page):
        if (
            clenching_sequence_length >= 5
            and clenching_sequence_length <= 7
            and self._selected_mode == "Beginner"
        ):
            self.add_to_output_sequence(" ")
        if clenching_sequence_length >= 8 and clenching_sequence_length <= 9:
            if self._dots_lines_sequence != "":
                sequence = self._dots_lines_sequence
                self._output_sequence = self.trim_string(
                    self._output_sequence, len(sequence) + self._enter_count
                )
                self._dots_lines_sequence = ""
            else:
                if len(self._output_sequence) >= 1:
                    if self._output_sequence[-1] == "\n":
                        self._output_sequence = self.trim_string(
                            self._output_sequence, 2
                        )
                    else:
                        self._output_sequence = self.trim_string(
                            self._output_sequence, 1
                        )

            current_page.hide_action_label()
        elif clenching_sequence_length >= 10 and clenching_sequence_length <= 11:
            current_page.update_selected_mode()
        elif clenching_sequence_length >= 12 and clenching_sequence_length <= 13:
            current_page.hide_show_morse_code(self._show_morse_code)
        elif clenching_sequence_length >= 14 and clenching_sequence_length <= 15:
            current_page.open_tutorial_page()
        elif clenching_sequence_length >= 16 and clenching_sequence_length <= 20:
            self._copy_mode = True
            clean_text = self.get_output_sequence_without_enters()
            pyperclip.copy(clean_text)
            pyautogui.moveTo(self._screen_width / 2, self._screen_height / 2)
            current_page.start_copy_mode()

    def handle_lines_and_dots(self, clenching_sequence_length):
        if clenching_sequence_length == 1:
            self._dots_lines_sequence += "."
            self.add_to_output_sequence(".")
        elif clenching_sequence_length >= 2 and clenching_sequence_length <= 4:
            self._dots_lines_sequence += "-"
            self.add_to_output_sequence("-")

    def handle_add_symbol(self):
        symbol = None
        sequence = self._dots_lines_sequence
        number_of_enters = 0
        if (
            len(self._output_sequence) > len(sequence)
            and "\n" in self._output_sequence[-(len(sequence)) :]
        ):
            number_of_enters = self._output_sequence[-(len(sequence)) :].count("\n")

        self._output_sequence = self.trim_string(
            self._output_sequence, len(sequence) + number_of_enters
        )
        if sequence in MORSE_CODE.keys():
            symbol = MORSE_CODE[sequence]
            self.add_to_output_sequence(symbol)
        self._dots_lines_sequence = ""

    def handle_unit_pauses_beginner_mode(self, current_page):
        clenching_sequence_length = len(self._clenching_sequence)
        lambdas_sequence_length = self._output_sequence.count("~")
        self._output_sequence = self.trim_string(
            self._output_sequence, lambdas_sequence_length + self._enter_count
        )
        self._pause_units += 1
        if (
            self._pause_units == 1
            and clenching_sequence_length >= 5
            and self._dots_lines_sequence == ""
        ):
            self.handle_extra_commands(clenching_sequence_length, current_page)
        elif self._pause_units < 3 and clenching_sequence_length > 0:
            self.handle_lines_and_dots(clenching_sequence_length)
        elif self._pause_units == 3 and self._dots_lines_sequence != "":
            self.handle_add_symbol()

        self._clenching_sequence = []
        self._enter_count = 0

    def handle_unit_pauses_advanced_mode(self, current_page):
        clenching_sequence_length = len(self._clenching_sequence)
        lambdas_sequence_length = self._output_sequence.count("~")
        self._output_sequence = self.trim_string(
            self._output_sequence, lambdas_sequence_length + self._enter_count
        )
        self._pause_units += 1
        if (
            self._pause_units == 1
            and clenching_sequence_length > 7
            and self._dots_lines_sequence == ""
        ):
            self.handle_extra_commands(clenching_sequence_length, current_page)
        elif self._pause_units < 3 and clenching_sequence_length > 0:
            self.handle_lines_and_dots(clenching_sequence_length)
        elif self._pause_units == 3 and self._dots_lines_sequence != "":
            self.handle_add_symbol()
        elif (
            self._pause_units == 7
            and self._output_sequence != ""
            and self._output_sequence[-1] != " "
        ):
            self.add_to_output_sequence(" ")

        self._clenching_sequence = []
        self._enter_count = 0

    def handle_unit_pauses_copy_mode(self, current_page):
        clench_length = len(self._clenching_sequence)
        if clench_length == 1:
            pyautogui.click()
        elif clench_length >= 2 and clench_length <= 4:
            pyautogui.doubleClick()
        elif clench_length >= 5 and clench_length <= 9:
            pyautogui.hotkey("command", "v")
        elif clench_length >= 10 and clench_length <= 13:
            self._copy_mode = False
            current_page.stop_copy_mode()
            self.clean_output_sequence()

        self._clenching_sequence = []

    def handle_unit_pauses_seventh_page(self, current_page):
        if self._copy_mode is True:
            self.handle_unit_pauses_copy_mode(current_page)
        elif self._selected_mode == "Beginner":
            self.handle_unit_pauses_beginner_mode(current_page)
        elif self._selected_mode == "Advanced":
            self.handle_unit_pauses_advanced_mode(current_page)
        current_page.hide_action_label()

    def handle_input_seventh_page(
        self,
        average_af7_difference,
        average_af8_difference,
        threshold_af7,
        threshold_af8,
        current_page,
    ):
        if (average_af7_difference >= threshold_af7) or (
            average_af8_difference >= threshold_af8
        ):
            self.handle_unit_clenches_seventh_page(current_page)
        else:
            self.handle_unit_pauses_seventh_page(current_page)

        if self._copy_mode is False:
            current_page.update_text_label(self._output_sequence)

    def handle_unit_clenches_fifth_page(self, current_page):
        self._clenching_sequence.append(1)
        self._pause_units = 0
        current_page.update_next_action_label(len(self._clenching_sequence))

    def handle_unit_pauses_fifth_page(self, current_page):
        clench_length = len(self._clenching_sequence)
        if clench_length >= 1 and clench_length < 4:
            current_page.open_tutorial_page()
        elif clench_length >= 4 and clench_length <= 7:
            current_page.update_selected_mode()
        elif clench_length >= 8 and clench_length <= 12:
            current_page.go_to_next_page()

        self._clenching_sequence = []

    def handle_input_fifth_page(
        self,
        average_af7_difference,
        average_af8_difference,
        threshold_af7,
        threshold_af8,
        current_page,
    ):
        if (average_af7_difference >= threshold_af7) or (
            average_af8_difference >= threshold_af8
        ):
            self.handle_unit_clenches_fifth_page(current_page)
        else:
            self.handle_unit_pauses_fifth_page(current_page)

    def handle_input(self, eeg_list, current_page):
        self._input_listening_values.append(eeg_list)
        page_name = current_page.__class__.__name__
        if time.time() - self._input_timer >= 0.25:
            self._input_timer = time.time()
            values = self._input_listening_values
            threshold_af7, threshold_af8 = self.get_clenching_threshold_values()
            (
                average_af7_difference,
                average_af8_difference,
            ) = self.calculate_average_difference(values)

            if page_name == "FifthPage":
                self.handle_input_fifth_page(
                    average_af7_difference,
                    average_af8_difference,
                    threshold_af7,
                    threshold_af8,
                    current_page,
                )
            elif page_name == "SeventhPage":
                self.handle_input_seventh_page(
                    average_af7_difference,
                    average_af8_difference,
                    threshold_af7,
                    threshold_af8,
                    current_page,
                )

            self._input_listening_values = []

    def handle_head_movement(self, eeg_list, current_page):
        y_value = eeg_list[0]
        z_value = eeg_list[1]

        if y_value > 7:
            pyautogui.move(0, -y_value)
        elif y_value < -7:
            pyautogui.move(0, -y_value)

        if z_value > 7:
            pyautogui.move(z_value, 0)
        elif z_value < -7:
            pyautogui.move(z_value, 0)
