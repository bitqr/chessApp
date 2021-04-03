import numpy
import tensorflow

from engine import settings, utils
from engine.SearchNode import SearchNode
from engine.utils import from_move_to_output_index
from internal.Game import Game

import math


# This method updates the value for each one of the nodes from the root to the current node
def back_propagate(node, value):
    while node:
        node.value += value
        node = node.parent


class SearchTree:

    # Our search tree starts with an initial position, represented by the root field
    # Generally, a chess game should start with the initial position, but we let it open
    # to start from any initial chess position
    def __init__(self, fen_position, exploration_parameter=settings.EXPLORATION_PARAMETER, neural_network=None):
        game = Game(fen_position)
        self.my_color = game.board.position.color_to_move
        self.root = SearchNode(game)
        self.exploration_parameter = exploration_parameter
        self.neural_network = neural_network
        self.states = dict()
        self.states[game.board.fen_position] = self.root

    def run_simulations(self, node, simulations_count):
        for iteration in range(simulations_count):
            self.search(node)
            if iteration % 50 == 0:
                print("Simulation {0}".format(iteration))

    def search(self, node):
        while not node.is_leaf():
            # While the node has children, select one of them
            node.visit_count += 1
            node = self.select(node)
        # Reached a leaf node
        if not node.is_terminal():
            node.visit_count += 1
            self.expand(node)

    # This method selects good child nodes, starting from given node, based on the evaluation function
    # Generally, the selected node is the one that maximizes the upper confidence bound
    def select(self, node):
        best_evaluation = -math.inf
        chosen_move = None
        for move in node.children:
            confidence_evaluation = node.upper_confidence_bound(move, self.exploration_parameter)
            if confidence_evaluation > best_evaluation:
                best_evaluation = confidence_evaluation
                chosen_move = move
        return node.children[chosen_move]

    # This method generates children, by computing the legal moves of a given position
    # When creating a new child for the expanded node, we get its evaluation from the
    # neural net and pass it to the prior probability (used in the selection argument)
    def expand(self, node):
        legal_moves = node.game.board.position.legal_moves_list()
        if len(legal_moves) == 0:
            return None
        input_vector = utils.from_fen_to_input_vector(node.game.board.fen_position)
        output_vector = self.neural_network.evaluate(input_vector)
        policy = output_vector[0]
        dirichlet_vector = numpy.random.dirichlet(
            numpy.zeros(policy.shape[1]) + settings.DIRICHLET_NOISE_ALPHA_PARAMETER
        )
        for move in legal_moves:
            temporary_game = Game(node.game.board.fen_position)
            temporary_game.board.apply_move(move, log=False)
            if temporary_game.board.fen_position not in self.states:
                output_index = from_move_to_output_index(move)
                prior_probability = tensorflow.gather_nd(policy, [0, output_index])
                # If node is root, add Dirichlet noise to add some variability to node selection
                if node.is_root():
                    prior_probability = (1. - settings.DIRICHLET_NOISE_RATE) * prior_probability +\
                                        settings.DIRICHLET_NOISE_RATE * dirichlet_vector[output_index]
                self.states[temporary_game.board.fen_position] = SearchNode(temporary_game, node, prior_probability)
            node.children[move] = self.states[temporary_game.board.fen_position]
        # Get the value associated to the position
        score = output_vector[1]
        back_propagate(node, score)
