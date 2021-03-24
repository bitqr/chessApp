from internal import utils
from internal.Board import Board
from internal.Color import Color
from internal.GameResult import GameResult


class Game:

    def __init__(self):
        self.move_history = []
        self.captured_pieces = dict()
        self.fifty_move_rule_counter = 0
        self.fullmoves_count = 1
        self.board = Board(8, self)
        self.initialize_captured_pieces()
        self.result = GameResult.UNDEFINED
        self.can_be_drawn_by_fifty_move_rule = False
        self.can_be_drawn_by_threefold_repetition = False
        self.past_positions = dict()

    def initialize_captured_pieces(self):
        self.captured_pieces[Color.WHITE] = dict()
        self.captured_pieces[Color.BLACK] = dict()
        for piece in self.board.position.pieces_positions:
            self.captured_pieces[piece.color][piece.type] = 0

    def is_over(self):
        return not self.result == GameResult.UNDEFINED

    def add_captured_piece(self, captured_piece, position):
        self.captured_pieces[captured_piece.color][captured_piece.type] += 1
        position.add_captured_piece(captured_piece)

    def apply_resign(self):
        if self.board.position.color_to_move == Color.WHITE:
            self.result = GameResult.BLACK_WINS_BY_RESIGNATION
        else:
            self.result = GameResult.WHITE_WINS_BY_RESIGNATION
        self.end()

    def apply_draw(self):
        if self.can_be_drawn_by_fifty_move_rule:
            self.result = GameResult.DRAW_BY_50_MOVE_RULE
            self.end()
        if self.can_be_drawn_by_threefold_repetition:
            self.result = GameResult.DRAW_BY_MOVE_REPEAT
            self.end()

    def to_string(self):
        result = 'Captured pieces:\nBlack:\n'
        for piece_type in self.captured_pieces[Color.WHITE]:
            count = self.captured_pieces[Color.WHITE][piece_type]
            if count > 0:
                result += '{0} x {1}\n'.format(utils.piece_type_to_string(piece_type), count)
        result += '-----------------------------------\nWhite:\n'
        for piece_type in self.captured_pieces[Color.BLACK]:
            count = self.captured_pieces[Color.BLACK][piece_type]
            if count > 0:
                result += '{0} x {1}\n'.format(utils.piece_type_to_string(piece_type), count)
        result += '-----------------------------------\n'
        if self.is_over():
            result += utils.game_result_to_string[self.result]
        return result

    def end(self):
        for piece_key in self.board.position.legal_moves.keys():
            self.board.position.legal_moves[piece_key] = []

    def can_be_drawn(self):
        return self.can_be_drawn_by_fifty_move_rule or self.can_be_drawn_by_threefold_repetition
