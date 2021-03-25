import random


class RandomEngine:

    def __init__(self):
        self.decision = None

    def choose_move(self, position):
        possible_moves = position.legal_moves_list()
        self.decision = random.choice(possible_moves)
        return self.decision
