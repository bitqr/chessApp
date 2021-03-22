from internal.Board import Board


class Game:

    def __init__(self):
        self.move_history = []
        self.board = Board(8)
