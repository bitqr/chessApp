import logging

from internal import utils
from internal.GameResult import GameResult
from internal.PieceType import PieceType
from internal.Color import Color
from internal.Piece import Piece
from internal.Position import Position
from internal.Square import Square
from internal.utils import compute_castling_rook_move


logging.getLogger().setLevel(logging.INFO)


class Board:

    def __init__(self, size, game):
        self.game = game
        self.squares = dict()
        self.size = size
        self.position = Position()
        for rank in range(size):
            for file in range(size):
                self.squares[(rank, file)] = Square(rank, file)
        self.white_king = Piece(PieceType.KING, Color.WHITE)
        self.black_king = Piece(PieceType.KING, Color.BLACK)
        self.initialize_board()

    def initialize_board(self):
        self.initialize_side(Color.WHITE)
        self.initialize_side(Color.BLACK)
        self.position.update_controlled_squares(self.squares)
        self.position.update_legal_moves(self.squares)
        self.position.color_to_move = Color.WHITE

    def initialize_side(self, piece_color):
        base_rank = 0
        pawn_rank = 1
        if piece_color == Color.WHITE:
            base_rank = self.size - 1
            pawn_rank = self.size - 2
        self.put_piece_on_square(Piece(PieceType.ROOK, piece_color), base_rank, 0)
        self.put_piece_on_square(Piece(PieceType.ROOK, piece_color), base_rank, 7,)
        self.put_piece_on_square(Piece(PieceType.KNIGHT, piece_color), base_rank, 1)
        self.put_piece_on_square(Piece(PieceType.KNIGHT, piece_color), base_rank, 6)
        self.put_piece_on_square(Piece(PieceType.BISHOP, piece_color), base_rank, 2)
        self.put_piece_on_square(Piece(PieceType.BISHOP, piece_color), base_rank, 5)
        self.put_piece_on_square(Piece(PieceType.QUEEN, piece_color), base_rank, 3)
        self.put_piece_on_square(self.white_king if piece_color == Color.WHITE else self.black_king, base_rank, 4)
        for file in range(self.size):
            self.put_piece_on_square(Piece(PieceType.PAWN, piece_color), pawn_rank, file)

    def current_square(self, piece):
        return self.position.pieces_positions[piece]

    def apply_move(self, move):
        target_piece = move.destination_square.content
        self.leave_square(move.piece)
        # If the move is a capture, remove the piece on the destination square
        if move.is_capture:
            self.game.add_captured_piece(target_piece, self.position)
        self.put_piece_on_square(move.piece, move.destination_square.rank, move.destination_square.file)
        if move.is_castle:
            rook_move = compute_castling_rook_move(move, self.squares)
            self.leave_square(rook_move.piece)
            self.put_piece_on_square(
                rook_move.piece,
                rook_move.destination_square.rank,
                rook_move.destination_square.file
            )
            rook_move.piece.never_moved = False
        if move.is_en_passant:
            # In this very specific case, the capture square is NOT the landing square
            captured_pawn_square = self.squares[(move.origin_square.rank, move.destination_square.file)]
            self.game.add_captured_piece(captured_pawn_square.content, self.position)
            captured_pawn_square.empty_content()
        if move.is_promotion:
            move.piece.promote(move.promoted_piece_type)
        move.piece.never_moved = False
        self.position.latest_move = move
        self.game.move_history.append(move)
        self.update_fifty_move_rule_counter(move)
        # Prepare next move
        if move.piece.is_black():
            self.game.fullmoves_count += 1
        self.position.color_to_move = move.piece.opposite_color()
        self.position.update_controlled_squares(self.squares)
        self.position.update_legal_moves(self.squares)
        self.determine_check_situation(move)
        # Look for dead position
        if not move.is_check and not self.game.is_over():
            if self.position.is_dead_position():
                self.game.result = GameResult.DRAW_BY_DEAD_POSITION
                self.game.end()
        logging.info(move.to_string(target_piece))
        # Look for threefold repetition
        self.update_repetition_status()

    def update_repetition_status(self):
        fen_string = self.to_fen_string()
        fen_key = ' '.join(fen_string.split(' ')[:4])
        self.game.past_positions[fen_key] = self.game.past_positions.get(fen_key, 0) + 1
        if self.game.past_positions[fen_key] >= 3:
            self.game.can_be_drawn_by_threefold_repetition = True
        logging.info(fen_string)

    def determine_check_situation(self, move):
        remaining_moves = self.position.legal_moves_count()
        # print(remaining_moves)
        if move.piece.is_white():
            if self.position.is_in_check(self.black_king):
                move.is_check = True
                if remaining_moves == 0:
                    self.game.result = GameResult.WHITE_WINS_BY_CHECKMATE
        else:
            if self.position.is_in_check(self.white_king):
                move.is_check = True
                if remaining_moves == 0:
                    self.game.result = GameResult.BLACK_WINS_BY_CHECKMATE
        if remaining_moves == 0 and not move.is_check:
            self.game.result = GameResult.DRAW_BY_STALEMATE

    def leave_square(self, piece):
        current_square = self.position.pieces_positions[piece]
        current_square.empty_content()

    def put_piece_on_square(self, piece, rank, file):
        self.squares[(rank, file)].content = piece
        self.position.update_position(piece, self.squares[(rank, file)])

    def update_fifty_move_rule_counter(self, move):
        if move.is_pawn_move() or move.is_capture or move.is_en_passant:
            self.game.fifty_move_rule_counter = 0
        else:
            self.game.fifty_move_rule_counter += 1
        if self.game.fifty_move_rule_counter >= 100:
            self.game.can_be_drawn_by_fifty_move_rule = True

    def to_fen_string(self):
        result = ''
        for rank in range(8):
            empty_count = 0
            for file in range(8):
                if self.squares[(rank, file)].is_free():
                    empty_count += 1
                else:
                    if empty_count > 0:
                        result += str(empty_count)
                        empty_count = 0
                    piece = self.squares[(rank, file)].content
                    result += piece.to_fen_letter()
            if empty_count > 0:
                result += str(empty_count)
            if rank < 7:
                result += '/'
        result += ' {0} '.format(utils.color_to_fen(self.position.color_to_move))
        # Castling rights
        castling_rights_field = ''
        if self.white_king.never_moved:
            if self.squares[(7, 7)].content.is_rook() and self.squares[(7, 7)].content.never_moved:
                castling_rights_field += 'K'
            if self.squares[(7, 0)].content.is_rook() and self.squares[(7, 0)].content.never_moved:
                castling_rights_field += 'Q'
        if self.black_king.never_moved:
            if self.squares[(0, 7)].content.is_rook() and self.squares[(0, 7)].content.never_moved:
                castling_rights_field += 'k'
            if self.squares[(0, 0)].content.is_rook() and self.squares[(0, 0)].content.never_moved:
                castling_rights_field += 'q'
        if castling_rights_field == '':
            castling_rights_field = '-'
        result += '{0} '.format(castling_rights_field)
        # En passant square (if any)
        latest_move = self.position.latest_move
        if latest_move and latest_move.is_double_pawn_move:
            en_passant_square_rank = (latest_move.origin_square.rank + latest_move.destination_square.rank) / 2
            result += self.squares[(en_passant_square_rank, latest_move.origin_square.file)].to_string()
        else:
            result += '-'
        result += ' {0} {1}'.format(self.game.fifty_move_rule_counter, self.game.fullmoves_count)
        return result
