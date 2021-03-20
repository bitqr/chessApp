
class Move:

    def __init__(self, piece, square):
        self.piece = piece
        self.square = square

    def is_capture(self):
        return not self.square.is_free()
