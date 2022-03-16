import pytest


from headband_input import HeadbandInput


@pytest.fixture
def headband_input():
    """Returns a Headband input instance"""
    return HeadbandInput()


def _add_eeg_calm_state_values(headband_input):
    headband_input.reinitialise_eeg_calm_state_values()
    headband_input.save_eeg_calm_state_values([801.2, 801.5])
    headband_input.save_eeg_calm_state_values([798.7, 798.4])
    headband_input.save_eeg_calm_state_values([802.6, 802.2])
    headband_input.save_eeg_calm_state_values([799.2, 799.7])
    headband_input.save_eeg_calm_state_values([800.1, 800.4])
    headband_input.save_eeg_calm_state_values([797.9, 797.1])
    headband_input.save_eeg_calm_state_values([803.1, 802.7])


def _add_eeg_clenching_state_values(headband_input):
    headband_input.reinitialise_eeg_clenching_state_values()
    headband_input.save_eeg_clenching_state_values([828.2, 828.6])
    headband_input.save_eeg_clenching_state_values([781.7, 781.4])
    headband_input.save_eeg_clenching_state_values([831.6, 831.3])
    headband_input.save_eeg_clenching_state_values([778.2, 778.7])
    headband_input.save_eeg_clenching_state_values([825.1, 825.4])
    headband_input.save_eeg_clenching_state_values([781.9, 778.4])
    headband_input.save_eeg_clenching_state_values([826.1, 825.1])


def test_calculate_average_difference(headband_input):
    eeg_values_list = [
        [801.1, 801.3],
        [798.4, 798.7],
        [802.6, 802.1],
        [799.4, 799.2],
        [800.5, 800.3],
    ]
    (
        average_difference_af7,
        average_difference_af8,
    ) = headband_input.calculate_average_difference(eeg_values_list)

    assert "{:.2f}".format(average_difference_af7) == "3.70"
    assert "{:.2f}".format(average_difference_af8) == "3.15"


def test_calculate_average_calm_state_difference(headband_input):
    _add_eeg_calm_state_values(headband_input)
    headband_input.calculate_average_calm_state_difference()
    average_difference_af7 = headband_input._average_difference_af7_calm_state
    average_difference_af8 = headband_input._average_difference_af8_calm_state
    assert "{:.2f}".format(average_difference_af7) == "2.60"
    assert "{:.2f}".format(average_difference_af8) == "2.57"


def test_calculate_average_clenching_state_difference(headband_input):
    _add_eeg_clenching_state_values(headband_input)
    headband_input.calculate_average_clenching_state_difference()
    average_difference_af7 = headband_input._average_difference_af7_clenching_state
    average_difference_af8 = headband_input._average_difference_af8_clenching_state
    assert "{:.2f}".format(average_difference_af7) == "48.35"
    assert "{:.2f}".format(average_difference_af8) == "49.05"


def test_calculate_threshold_values(headband_input):
    _add_eeg_calm_state_values(headband_input)
    _add_eeg_clenching_state_values(headband_input)

    headband_input.calculate_average_calm_state_difference()
    headband_input.calculate_average_clenching_state_difference()
    headband_input.calculate_threshold_values()

    threshold_af7 = headband_input._threshold_af7
    threshold_af8 = headband_input._threshold_af8

    assert "{:.2f}".format(threshold_af7) == "25.47"
    assert "{:.2f}".format(threshold_af8) == "25.81"
