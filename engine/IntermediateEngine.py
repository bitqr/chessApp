import math

from engine import settings
from engine.SearchTree import SearchTree
from engine.utils import greedy_evaluation
from internal.Color import Color
from internal.Move import Move


# Minimax algorithm for chess playing engine
# At depth 2
# Beats Stockfish 13 Level 1 (800 Elo)
# Beats Stockfish 13 Level 2 (1100 Elo)
# But cannot defeat Stockfish Level 3 (1400 Elo)
class IntermediateEngine:

    def __init__(self, color=Color.WHITE):
        self.color = color
        self.search_tree = None
        self.depth = settings.MINIMAX_SEARCH_DEPTH

    def develop_node(self, node, depth):
        if depth > 0 and not node.is_terminal():
            self.search_tree.expand_minimax(node)
            for child in node.children:
                self.develop_node(node.children[child], depth - 1)

    def update_evaluations(self, node):
        if node.is_leaf():
            node.value = greedy_evaluation(node, self.color)
            return node.value
        else:
            node.value = -math.inf if node.game.board.position.color_to_move == self.color else math.inf
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
        current_value = -math.inf
        chosen_move = None
        for move in self.search_tree.root.children:
            if self.search_tree.root.children[move].value > current_value:
                chosen_move = move
                current_value = self.search_tree.root.children[move].value
        print('Number of explored moves: {0}'.format(len(self.search_tree.states)))
        return Move(game.board.squares[(chosen_move.origin_square.rank, chosen_move.origin_square.file)],
                    game.board.squares[(chosen_move.destination_square.rank, chosen_move.destination_square.file)],
                    game.board.squares)
