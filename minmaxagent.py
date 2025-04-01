import copy
import math

from exceptions import AgentException, GameplayException


# +1 - 'o' is winning, -1 - 'x' is winning
class MinMaxAgent:
    def __init__(self, my_token='o', depth=4):
        self.my_token = my_token
        self.opposite_token = 'x' if my_token == 'o' else 'o'
        self.depth = depth

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        decided = self.minmax(connect4)
        return decided[1]

    def heuristic(self, connect4):
        threes_difference = 0
        for three in connect4.iter_Ns(3):
            if three == ['o', 'o', 'o']:
                threes_difference += 1
            elif three == ['x', 'x', 'x']:
                threes_difference -= 1
        smoothing_factor = 3.0
        return 2 / (1 + math.exp(-threes_difference / smoothing_factor)) - 1

    # [best_score, move]
    def minmax(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')

        if connect4.wins is not None:
            return [1, None] if connect4.wins == 'o' else [-1, None]

        if self.depth == 0:
            return [self.heuristic(connect4), None]

        possible_drops = connect4.possible_drops()

        if not possible_drops:
            return [0, None]

        best_result = float('-inf') if self.my_token == 'o' else float('inf')
        best_move = None

        for drop in possible_drops:
            connect4_copy = copy.deepcopy(connect4)
            opposite_agent = MinMaxAgent(self.opposite_token, self.depth - 1)
            connect4_copy.drop_token(drop)
            try:
                opposite_result = opposite_agent.minmax(connect4_copy)
            except AgentException:
                raise AgentException('not my round')

            if self.my_token == 'o':
                if opposite_result[0] > best_result:
                    best_result = opposite_result[0]
                    best_move = drop
            else:
                if opposite_result[0] < best_result:
                    best_result = opposite_result[0]
                    best_move = drop

        return best_result, best_move
