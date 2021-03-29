import math

from engine import settings
from engine.NeuralNetwork import NeuralNetwork
from engine.SearchTree import SearchTree
from internal.Move import Move


class Engine:

    def __init__(self):
        self.neural_network = NeuralNetwork()
        self.search_tree = None

    def choose_move(self, game):
        # Choose the move here
        # At the beginning of the game, the position may not have a corresponding node in the search tree
        self.search_tree = SearchTree(game.board.fen_position, settings.EXPLORATION_PARAMETER, self.neural_network)
        starting_node = self.search_tree.states[game.board.fen_position]
        self.search_tree.run_simulations(starting_node, settings.MONTE_CARLO_SIMULATIONS_COUNT)
        # After running the simulations from the given node, we can decide the move right away
        chosen_move = None
        current_value = -math.inf
        for move in starting_node.children:
            current_node = starting_node.children[move]
            if current_node.visit_count > current_value:
                current_value = current_node.visit_count
                chosen_move = move
        print('Chosen move = [{0}, {1}]'.format(chosen_move.origin_square.to_string(),
                                                chosen_move.destination_square.to_string()))
        # Create a move with input game objects
        return Move(game.board.squares[(chosen_move.origin_square.rank, chosen_move.origin_square.file)],
                    game.board.squares[(chosen_move.destination_square.rank, chosen_move.destination_square.file)],
                    game.board.squares)
