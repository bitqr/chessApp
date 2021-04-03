import math

from engine import settings
from engine.SearchNode import SearchNode
from engine.SearchTree import SearchTree


class Engine:

    def __init__(self, neural_net):
        self.neural_network = neural_net

    def run_mcts(self, game):
        search_tree = SearchTree(game.board.fen_position, settings.EXPLORATION_PARAMETER, self.neural_network)
        fen_position = game.board.fen_position
        if fen_position not in search_tree.states:
            search_tree.states[fen_position] = SearchNode(game)
        starting_node = search_tree.states[fen_position]
        search_tree.run_simulations(starting_node, settings.MONTE_CARLO_SIMULATIONS_COUNT)
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
        # Create the pair (input, output) to update the model
        mcts_adapted_policy_vector = search_tree.root.create_output_probability_vector()
        return chosen_move, mcts_adapted_policy_vector
