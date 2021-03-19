from internal.PieceType import PieceType
from internal.Color import Color
from internal.Piece import Piece
from internal.Position import Position
from internal.Square import Square


class Board:

    def __init__(self, size):
        self.squares = dict()
        self.size = size
        self.position = Position()
        for rank in range(size):
            for file in range(size):
                self.squares[(rank, file)] = Square(rank, file)
        self.initialize_board()

    def initialize_board(self):
        self.initialize_side(Color.WHITE)
        self.initialize_side(Color.BLACK)

    def initialize_side(self, piece_color):
        base_rank = 0
        pawn_rank = 1
        if piece_color == Color.WHITE:
            base_rank = self.size - 1
            pawn_rank = self.size - 2
        self.put_piece_on_square(base_rank, 0, Piece(PieceType.ROOK, piece_color))
        self.put_piece_on_square(base_rank, 7, Piece(PieceType.ROOK, piece_color))
        self.put_piece_on_square(base_rank, 1, Piece(PieceType.KNIGHT, piece_color))
        self.put_piece_on_square(base_rank, 6, Piece(PieceType.KNIGHT, piece_color))
        self.put_piece_on_square(base_rank, 2, Piece(PieceType.BISHOP, piece_color))
        self.put_piece_on_square(base_rank, 5, Piece(PieceType.BISHOP, piece_color))
        self.put_piece_on_square(base_rank, 3, Piece(PieceType.QUEEN, piece_color))
        self.put_piece_on_square(base_rank, 4, Piece(PieceType.KING, piece_color))
        for file in range(self.size):
            self.put_piece_on_square(pawn_rank, file, Piece(PieceType.PAWN, piece_color))

    def put_piece_on_square(self, rank, file, piece):
        self.squares[(rank, file)].set_content(piece)
        self.position.update_position(piece, self.squares[(rank, file)])
