from PySide6 import QtWidgets, QtGui, QtCore
import gui.util


class BoardGUI(QtWidgets.QWidget):

    def __init__(self, board, square_size):
        super().__init__()
        self.piece_to_sprite = gui.util.piece_to_sprite()
        self.square_size = square_size
        self.layout = QtWidgets.QGridLayout(self)
        self.board_width = board.size * square_size
        self.board_height = board.size * square_size
        self.initialize_board(board)

    def initialize_board(self, board):
        for rank in range(board.size):
            for file in range(board.size):
                square = board.squares[rank][file]
                square_label = self.create_square(square)
                self.layout.addWidget(square_label, rank, file)
                if not square.is_free():
                    piece_label = self.create_piece(square)
                    self.layout.addWidget(piece_label, rank, file)
        self.resize(self.board_width, self.board_height)

    def create_square(self, square):
        square_label = QtWidgets.QLabel()
        sheet_white_square = QtGui.QPixmap('sprites/whiteSquare.png').scaled(
            QtCore.QSize(self.square_size, self.square_size)
        )
        sheet_black_square = QtGui.QPixmap('sprites/blackSquare.png').scaled(
            QtCore.QSize(self.square_size, self.square_size)
        )
        square_label.setPixmap(sheet_white_square if (square.rank + square.file) % 2 == 0 else sheet_black_square)
        square_label.setScaledContents(True)
        return square_label

    def create_piece(self, square):
        sheet_piece = QtGui.QPixmap(
            f'sprites/{self.piece_to_sprite[(square.content.type, square.content.color)]}.png'
        ).scaled(QtCore.QSize(self.square_size, self.square_size))
        piece_label = QtWidgets.QLabel()
        piece_label.setPixmap(sheet_piece)
        piece_label.move(square.rank * self.square_size, square.file * self.square_size)
        piece_label.setScaledContents(True)
        return piece_label
