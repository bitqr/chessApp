import math

from engine.SearchTree import SearchTree
from internal.Color import Color
from internal.Move import Move
from internal.PieceType import PieceType

piece_to_value = {
    PieceType.PAWN: 1,
    PieceType.KNIGHT: 3,
    PieceType.BISHOP: 3,
    PieceType.ROOK: 5,
    PieceType.QUEEN: 10,
    PieceType.KING: 0
}


# Minimax algorithm for chess playing engine
class IntermediateEngine:

    def __init__(self, color):
        self.color = color
        self.search_tree = None
        self.depth = 2

    def evaluation(self, node):
        if node.game.is_over():
            if (node.game.white_wins() and self.color == Color.WHITE) \
                    or (node.game.black_wins() and self.color == Color.BLACK):
                return 1000
            if (node.game.white_wins() and self.color == Color.BLACK) \
                    or (node.game.black_wins() and self.color == Color.WHITE):
                return -1000
        result = 0
        for piece in node.game.board.position.pieces_positions:
            if piece.color == self.color:
                result += piece_to_value[piece.type]
            else:
                result -= piece_to_value[piece.type]
        return result

    def develop_node(self, node, depth):
        if depth == 0:
            node.value = self.evaluation(node)
        else:
            self.search_tree.expand(node)
            for child in node.children:
                self.develop_node(node.children[child], depth - 1)

    def update_evaluations(self, node):
        if node.is_leaf():
            node.value = self.evaluation(node)
            return node.value
        else:
            for child in node.children.values():
                if node.game.board.position.color_to_move == self.color:
                    node.value = max(node.value, self.update_evaluations(child))
                else:
                    node.value = min(node.value, self.update_evaluations(child))
            return node.value

    def choose_move(self, game):
        self.search_tree = SearchTree(game.board.fen_position)
        # Develop nodes until given depth
        self.develop_node(self.search_tree.root, self.depth)
        # Evaluate and return the choice with best evaluation
        self.update_evaluations(self.search_tree.root)
        current_value = - math.inf
        chosen_move = None
        for move in self.search_tree.root.children:
            if self.search_tree.root.children[move].value > current_value:
                chosen_move = move
                current_value = self.search_tree.root.children[move].value
        return Move(game.board.squares[(chosen_move.origin_square.rank, chosen_move.origin_square.file)],
                    game.board.squares[(chosen_move.destination_square.rank, chosen_move.destination_square.file)],
                    game.board.squares)
