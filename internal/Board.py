from internal.GameResult import GameResult
from internal.PieceType import PieceType
from internal.Color import Color
from internal.Piece import Piece
from internal.Position import Position
from internal.Square import Square
from internal.util import compute_castling_rook_move


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
        origin_square = self.position.pieces_positions[move.piece]
        target_piece = move.square.content
        self.leave_square(move.piece)
        # If the move is a capture, remove the piece on the destination square
        if move.is_capture():
            self.game.add_captured_piece(move.square.content, self.position)
        self.put_piece_on_square(move.piece, move.square.rank, move.square.file)
        if move.is_castle:
            rook_move = compute_castling_rook_move(move, self.squares)
            self.leave_square(rook_move.piece)
            self.put_piece_on_square(rook_move.piece, rook_move.square.rank, rook_move.square.file)
            rook_move.piece.never_moved = False
        move.piece.never_moved = False
        self.game.move_history.append(move)
        self.position.color_to_move = move.piece.opposite_color()
        self.position.update_controlled_squares(self.squares)
        self.position.update_legal_moves(self.squares)
        self.determine_check_situation(move)
        print(move.to_string(origin_square, target_piece))

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
