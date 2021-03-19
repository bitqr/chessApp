class Position:

    def __init__(self):
        self.pieces_positions = dict()

    def update_position(self, piece, square):
        self.pieces_positions[piece] = square
