import copy

from exceptions import AgentException, GameplayException
from minmax_utils import heuristic


# +1 - 'o' is winning, -1 - 'x' is winning
class AlphaBetaAgent:
    def __init__(self, my_token='o', depth=6):
        self.my_token = my_token
        self.opposite_token = 'x' if my_token == 'o' else 'o'
        self.depth = depth

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        decided = self.alphabeta(connect4, float('-inf'), float('inf'))
        return decided[1]

    # [best_score, move]
    def alphabeta(self, connect4, alpha, beta):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')

        if connect4.wins is not None:
            return [1, None] if connect4.wins == 'o' else [-1, None]

        if self.depth == 0:
            return [heuristic(connect4), None]

        possible_drops = connect4.possible_drops()
        if not possible_drops:
            return [0, None]

        best_result = float('-inf') if self.my_token == 'o' else float('inf')
        best_move = None

        for drop in possible_drops:
            connect4_copy = copy.deepcopy(connect4)
            opposite_agent = AlphaBetaAgent(self.opposite_token, self.depth - 1)
            connect4_copy.drop_token(drop)
            try:
                opposite_result = opposite_agent.alphabeta(connect4_copy, alpha, beta)
            except AgentException:
                raise AgentException('not my round')

            if self.my_token == 'o':
                if opposite_result[0] > best_result:
                    best_result = opposite_result[0]
                    best_move = drop
                alpha = max(alpha, best_result)
            else:
                if opposite_result[0] < best_result:
                    best_result = opposite_result[0]
                    best_move = drop
                beta = min(beta, best_result)

            if beta <= alpha:
                break  # alpha-beta cutoff

        return best_result, best_move
