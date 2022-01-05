class HeadbandInputCalculation:
    @classmethod
    def update_average_difference(cls, average_difference, counter, high, low):
        return (average_difference * (counter - 1) + (high - low)) / counter

    @classmethod
    def calculate_average_difference(cls, list=[]):
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
                    average_difference_af7 = cls.update_average_difference(
                        average_difference_af7,
                        af7_counter,
                        last_highest_point_af7,
                        last_lowest_point_af7,
                    )
                    af7_counter += 1
            elif list[i - 1][0] > list[i][0] and list[i][0] < list[i + 1][0]:
                last_lowest_point_af7 = list[i][0]
                if last_highest_point_af7 != -1:
                    average_difference_af7 = cls.update_average_difference(
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
                    average_difference_af8 = cls.update_average_difference(
                        average_difference_af8,
                        af8_counter,
                        last_highest_point_af8,
                        last_lowest_point_af8,
                    )
                    af8_counter += 1
            elif list[i - 1][1] > list[i][1] and list[i][1] < list[i + 1][1]:
                last_lowest_point_af8 = list[i][1]
                if last_highest_point_af8 != -1:
                    average_difference_af8 = cls.update_average_difference(
                        average_difference_af8,
                        af8_counter,
                        last_highest_point_af8,
                        last_lowest_point_af8,
                    )
                    af8_counter += 1

        return average_difference_af7, average_difference_af8
