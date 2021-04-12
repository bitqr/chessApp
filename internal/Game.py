from internal import utils
from internal.Board import Board
from internal.Color import Color
from internal.Move import piece_type_to_string, Move
from internal.GameResult import GameResult
from internal.PieceType import PieceType
from internal.utils import fen_letter_to_piece, CHESSBOARD_FILE_NAMES, pawn_squares


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

    def read_pgn_move(self, pgn_string):
        color = self.board.position.color_to_move
        if pgn_string == 'O-O':
            origin_square = self.board.squares[(7 if color == Color.WHITE else 0, 4)]
            destination_square = self.board.squares[(7 if color == Color.WHITE else 0, 6)]
            return Move(origin_square, destination_square, self.board.squares)
        if pgn_string == 'O-O-O':
            origin_square = self.board.squares[(7 if color == Color.WHITE else 0, 4)]
            destination_square = self.board.squares[(7 if color == Color.WHITE else 0, 2)]
            return Move(origin_square, destination_square, self.board.squares)
        first_character = pgn_string[0]
        piece_type = PieceType.PAWN
        if first_character in ['K', 'Q', 'B', 'N', 'R']:
            piece_type = fen_letter_to_piece(first_character)[0]
            pgn_string = pgn_string[1:]
        origin_square_file = -1
        origin_square_rank = -1
        if len(pgn_string) > 1 \
                and pgn_string[0] in CHESSBOARD_FILE_NAMES \
                and (pgn_string[1] == 'x' or pgn_string[1] in CHESSBOARD_FILE_NAMES):
            # Case where the file of the origin square is specified
            # Find the origin square
            origin_square_file = CHESSBOARD_FILE_NAMES.index(pgn_string[0])
            pgn_string = pgn_string[1:]
        elif len(pgn_string) > 1 \
                and str.isnumeric(pgn_string[0]) and int(pgn_string[0]) in range(1, 9) \
                and (pgn_string[1] == 'x' or pgn_string[1] in CHESSBOARD_FILE_NAMES):
            # Case where the rank of the origin square is specified
            # Find the origin square
            origin_square_rank = 8 - int(pgn_string[0])
            pgn_string = pgn_string[1:]
        elif len(pgn_string) > 2 \
                and pgn_string[0] in CHESSBOARD_FILE_NAMES \
                and str.isnumeric(pgn_string[1]) and int(pgn_string[1]) in range(1, 9) \
                and (pgn_string[2] == 'x' or pgn_string[1] in CHESSBOARD_FILE_NAMES):
            origin_square_file = CHESSBOARD_FILE_NAMES.index(pgn_string[0])
            origin_square_rank = 8 - int(pgn_string[1])
            pgn_string = pgn_string[2:]
        # Check if capture
        is_capture = False
        if pgn_string[0] == 'x':
            is_capture = True
            pgn_string = pgn_string[1:]
        # Determine destination square
        destination_square = self.board.squares[(8 - int(pgn_string[1]), CHESSBOARD_FILE_NAMES.index(pgn_string[0]))]
        pgn_string = pgn_string[2:]
        if piece_type == PieceType.PAWN and not is_capture:
            origin_square_file = destination_square.file
            if color == Color.WHITE:
                offset = 2 if\
                    self.board.squares[(destination_square.rank + 1, destination_square.file)].is_free() else 1
                origin_square_rank = destination_square.rank + offset
            else:
                offset = 2 if \
                    self.board.squares[(destination_square.rank - 1, destination_square.file)].is_free() else 1
                origin_square_rank = destination_square.rank - offset
        # The origin square must be computed at this point
        if origin_square_rank < 0 or origin_square_file < 0:
            if origin_square_file >= 0:
                # Special case of a pawn capture: (for White it will be rank + 1, for black, rank - 1)
                if is_capture and piece_type == PieceType.PAWN:
                    origin_square_rank = destination_square.rank + 1 \
                        if color == Color.WHITE else destination_square.rank - 1
                else:
                    for rank in range(0, 8):
                        current_piece = self.board.squares[(rank, origin_square_file)].content
                        if current_piece.color == color and current_piece.type == piece_type:
                            origin_square_rank = rank
                            break
            elif origin_square_rank >= 0:
                for file in range(0, 8):
                    current_piece = self.board.squares[(origin_square_rank, file)].content
                    if current_piece.color == color and current_piece.type == piece_type:
                        origin_square_file = file
                        break
            else:
                # We have to find the square by looking at the board
                for piece in self.board.position.pieces_positions:
                    piece_square = self.board.position.pieces_positions[piece]
                    if piece.color == color and piece.type == piece_type and (
                            (piece.is_pawn() and (destination_square.rank, destination_square.file) in pawn_squares(
                                piece, piece_square, self.board.squares, self.board.position.latest_move))
                            or (destination_square.rank, destination_square.file) in
                            self.board.position.controlled_squares[color][piece]):
                        origin_square_rank = piece_square.rank
                        origin_square_file = piece_square.file
                        break
        move = Move(
            self.board.squares[(origin_square_rank, origin_square_file)],
            destination_square,
            self.board.squares
        )
        if len(pgn_string) > 1 and pgn_string[0] == '=':
            # Promotion case, keep the promoted piece type
            move.promoted_piece_type = fen_letter_to_piece(pgn_string[1])[0]
        return move
