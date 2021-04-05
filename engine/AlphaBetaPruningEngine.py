import math

from engine import settings
from engine.SearchNode import SearchNode
from engine.SearchTree import SearchTree
from engine.utils import greedy_evaluation
from internal.Game import Game
from internal.Move import Move


# Alpha-Beta pruning algorithm for chess playing engine
# At depth 2
# Beats Stockfish 13 Level 1 (800 Elo)
# Beats Stockfish 13 Level 2 (1100 Elo)
class AlphaBetaPruningEngine:

    def __init__(self, color):
        self.color = color
        self.search_tree = None
        self.depth = settings.ALPHA_BETA_PRUNING_DEPTH

    # In this function, a node is expanded and its evaluation updated
    # We prune the tree if a branch has an evaluation that won't be used
    # by the parent. 2 types of cut (alpha cut and beta cut), depending on
    # min nodes/max nodes
    def develop_alpha_beta_node(self, node, depth, alpha, beta):
        if depth == 0:
            node.value = greedy_evaluation(node, self.color)
            return node.value, 0
        if node.is_terminal():
            # If the node is a checkmate, its value is more important if it comes early in
            # the search tree
            node.value = greedy_evaluation(node, self.color) * (depth + 1)
            return node.value, 0
        # If the node is not terminal, generate the legal moves
        explored_moves = 0
        legal_moves = node.game.board.position.legal_moves_list()
        if node.game.board.position.color_to_move == self.color:
            # Node is a max node
            value = -math.inf
            for move in legal_moves:
                temporary_game = Game(node.game.board.fen_position)
                temporary_game.board.apply_move(move, log=False)
                node.children[move] = SearchNode(temporary_game, node)
                child_value, child_explored_moves = self.develop_alpha_beta_node(
                    node.children[move], depth - 1, alpha, beta
                )
                value = max(value, child_value)
                explored_moves += 1 + child_explored_moves
                if beta <= value:
                    # Beta pruning
                    node.value = value
                    return node.value, explored_moves
                alpha = max(alpha, value)
        else:
            # Node is a min node
            value = math.inf
            for move in legal_moves:
                temporary_game = Game(node.game.board.fen_position)
                temporary_game.board.apply_move(move, log=False)
                node.children[move] = SearchNode(temporary_game, node)
                child_value, child_explored_moves = self.develop_alpha_beta_node(
                    node.children[move], depth - 1, alpha, beta
                )
                explored_moves += 1 + child_explored_moves
                value = min(value, child_value)
                if alpha >= value:
                    # Alpha pruning
                    node.value = value
                    return node.value, explored_moves
                beta = min(beta, value)
        node.value = value
        return node.value, explored_moves

    def choose_move(self, game):
        self.search_tree = SearchTree(game.board.fen_position)
        # Develop nodes until given depth
        value, explored_moves = self.develop_alpha_beta_node(self.search_tree.root, self.depth, -math.inf, math.inf)
        current_value = -math.inf
        chosen_move = None
        for move in self.search_tree.root.children:
            if self.search_tree.root.children[move].value > current_value:
                chosen_move = move
                current_value = self.search_tree.root.children[move].value
        print('Number of explored moves: {0}'.format(explored_moves))
        return Move(game.board.squares[(chosen_move.origin_square.rank, chosen_move.origin_square.file)],
                    game.board.squares[(chosen_move.destination_square.rank, chosen_move.destination_square.file)],
                    game.board.squares)
