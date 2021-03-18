from internal.PieceType import PieceType
from internal.PieceColor import PieceColor
from internal.Piece import Piece
from internal.Square import Square


class Board:

    def __init__(self, size):
        self.squares = [size]
        self.size = size
        for rank in range(size):
            self.squares = [[Square(rank, file) for rank in range(size)] for file in range(size)]
        self.initialize_board()

    def initialize_board(self):
        self.initialize_side(PieceColor.WHITE)
        self.initialize_side(PieceColor.BLACK)

    def initialize_side(self, piece_color):
        base_row = 0
        pawn_row = 1
        if piece_color == PieceColor.WHITE:
            base_row = self.size - 1
            pawn_row = self.size - 2
        self.squares[base_row][0].set_content(Piece(PieceType.ROOK, piece_color))
        self.squares[base_row][7].set_content(Piece(PieceType.ROOK, piece_color))
        self.squares[base_row][1].set_content(Piece(PieceType.KNIGHT, piece_color))
        self.squares[base_row][6].set_content(Piece(PieceType.KNIGHT, piece_color))
        self.squares[base_row][2].set_content(Piece(PieceType.BISHOP, piece_color))
        self.squares[base_row][5].set_content(Piece(PieceType.BISHOP, piece_color))
        self.squares[base_row][3].set_content(Piece(PieceType.QUEEN, piece_color))
        self.squares[base_row][4].set_content(Piece(PieceType.KING, piece_color))
        for file in range(self.size):
            self.squares[pawn_row][file].set_content(Piece(PieceType.PAWN, piece_color))
