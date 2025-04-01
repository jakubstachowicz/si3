import math


def heuristic(connect4):
    threes_difference = 0
    for three in connect4.iter_Ns(3):
        if three == ['o', 'o', 'o']:
            threes_difference += 1
        elif three == ['x', 'x', 'x']:
            threes_difference -= 1
    smoothing_factor = 3.0
    return 2 / (1 + math.exp(-threes_difference / smoothing_factor)) - 1
