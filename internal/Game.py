from internal.Board import Board
from internal.GameResult import GameResult


class Game:

    def __init__(self):
        self.move_history = []
        self.captured_pieces = dict()
        self.board = Board(8)
        self.result = GameResult.UNDEFINED
