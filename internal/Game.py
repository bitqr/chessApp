from internal.Board import Board
from internal.Color import Color
from internal.GameResult import GameResult


class Game:

    def __init__(self):
        self.move_history = []
        self.captured_pieces = dict()
        self.captured_pieces[Color.WHITE] = list()
        self.captured_pieces[Color.BLACK] = list()
        self.board = Board(8, self)
        self.result = GameResult.UNDEFINED

    def is_over(self):
        return not self.result == GameResult.UNDEFINED

    def add_captured_piece(self, captured_piece, position):
        self.captured_pieces[captured_piece.color].append(captured_piece)
        position.add_captured_piece(captured_piece)
