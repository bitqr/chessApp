from internal import utils
from internal.Board import Board
from internal.Color import Color
from internal.Move import piece_type_to_string
from internal.GameResult import GameResult


class Game:

    def __init__(self, initial_fen_position=''):
        self.move_history = []
        self.captured_pieces = dict()
        self.fifty_move_rule_counter = 0
        self.fullmoves_count = 1
        self.board = Board(8, self, initial_fen_position)
        self.initialize_captured_pieces()
        self.result = GameResult.UNDEFINED
        self.can_be_drawn_by_fifty_move_rule = False
        self.can_be_drawn_by_threefold_repetition = False
        self.past_positions = dict()

    def initialize_captured_pieces(self):
        self.captured_pieces[Color.WHITE] = dict()
        self.captured_pieces[Color.BLACK] = dict()

    def is_over(self):
        return not self.result == GameResult.UNDEFINED

    def add_captured_piece(self, captured_piece, position):
        if captured_piece.type not in self.captured_pieces[captured_piece.color]:
            self.captured_pieces[captured_piece.color][captured_piece.type] = 0
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
                result += '{0} x {1}\n'.format(piece_type_to_string(piece_type), count)
        result += '-----------------------------------\nWhite:\n'
        for piece_type in self.captured_pieces[Color.BLACK]:
            count = self.captured_pieces[Color.BLACK][piece_type]
            if count > 0:
                result += '{0} x {1}\n'.format(piece_type_to_string(piece_type), count)
        result += '-----------------------------------\n'
        if self.is_over():
            result += utils.game_result_to_string[self.result]
        return result

    def end(self):
        for piece_key in self.board.position.legal_moves.keys():
            self.board.position.legal_moves[piece_key] = []

    def can_be_drawn(self):
        return self.can_be_drawn_by_fifty_move_rule or self.can_be_drawn_by_threefold_repetition

    def white_wins(self):
        return self.result in [
            GameResult.WHITE_WINS_BY_RESIGNATION,
            GameResult.WHITE_WINS_BY_CHECKMATE,
            GameResult.WHITE_WINS_ON_TIME
        ]

    def black_wins(self):
        return self.result in [
            GameResult.BLACK_WINS_BY_RESIGNATION,
            GameResult.BLACK_WINS_BY_CHECKMATE,
            GameResult.BLACK_WINS_ON_TIME
        ]

    def is_draw(self):
        return self.result in [
            GameResult.DRAW_BY_MOVE_REPEAT,
            GameResult.DRAW_BY_50_MOVE_RULE,
            GameResult.DRAW_BY_STALEMATE,
            GameResult.DRAW_BY_DEAD_POSITION,
            GameResult.DRAW_BY_MUTUAL_AGREEMENT
        ]

    def get_score(self, color):
        if self.is_draw() or self.result == GameResult.UNDEFINED:
            return 0
        if (self.white_wins() and color == Color.WHITE) or (self.black_wins() and color == Color.BLACK):
            return 1
        return -1
