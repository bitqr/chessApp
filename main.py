import sys
from gui.BoardGUI import BoardGUI
from internal.Board import Board
from PySide6 import QtWidgets


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setApplicationName("Chess App")
    board = Board(8)
    chessBoard = BoardGUI(board, 100)
    chessBoard.setLayout(chessBoard.layout)
    chessBoard.show()
    sys.exit(app.exec_())
