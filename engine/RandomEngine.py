import random


class RandomEngine:

    def __init__(self):
        self.decision = None

    def simulate(self, game):
        while not game.is_over():
            move = self.choose_move(game.board.position, game.can_be_drawn())
            if move == 'DRAW':
                game.apply_draw()
            else:
                game.board.apply_move(move, log=False)

    def choose_move(self, position, can_be_drawn=False):
        # If the game can be drawn, it is automatically drawn, to ensure random games don't take too much time
        if can_be_drawn:
            return 'DRAW'
        possible_moves = position.legal_moves_list()
        self.decision = random.choice(possible_moves)
        return self.decision
