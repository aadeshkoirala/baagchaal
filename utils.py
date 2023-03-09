import math


# CALCULATE THE EUCLIDEAN DISTANCE BETWEEN TWO POINTS
def find_distance(p1, p2, round_=False, round_by=2):
    x_distance = p2[0] - p1[0]
    y_distance = p2[1] - p1[1]

    sum_of_squares = (x_distance ** 2) + (y_distance ** 2)
    distance = math.sqrt(sum_of_squares)
    if round_:
        distance = round(distance, round_by)
    return distance


def equal(val_1, val_2, compare_val=(10 ** -3)):
    if abs(val_2 - val_1) <= compare_val:
        return True
    return False


def get_midpoint(p1, p2):
    x = (p1[0] + p2[0]) / 2
    y = (p1[1] + p2[1]) / 2
    return [int(x), int(y)]
