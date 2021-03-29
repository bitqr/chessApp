from engine import settings
from engine.RandomEngine import RandomEngine
from engine.SearchNode import SearchNode
from internal.Game import Game

import random
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
        self.random_engine = RandomEngine()

    def run_simulations(self, node, simulations_count):
        for iteration in range(simulations_count):
            self.search(node)
            if iteration % 1 == 0:
                print("Simulation {0}".format(iteration))

    def search(self, node):
        while not node.is_leaf():
            # While the node has children, select one of them
            node.visit_count += 1
            node = self.select(node)
        if not node.is_terminal():
            node.visit_count += 1
            node = self.expand(node)
        self.simulate(node)

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
    def expand(self, node):
        legal_moves = node.game.board.position.legal_moves_list()
        if len(legal_moves) == 0:
            return None
        for move in legal_moves:
            temporary_game = Game(node.game.board.fen_position)
            temporary_game.board.apply_move(move, log=False)
            if temporary_game.board.fen_position not in self.states:
                self.states[temporary_game.board.fen_position] = SearchNode(temporary_game, move, node)
            node.children[move] = self.states[temporary_game.board.fen_position]
        # Choose a random child of the node and start a play-out from it
        return random.choice(list(node.children.values()))

    # This method runs a simulation starting from the given node, until a terminal/leaf node is reached.
    # When the simulation is over, the nodes in the path up to the root can receive an average reward/value
    def simulate(self, node):
        # Consider distinctly the terminal case
        if node.is_terminal():
            node.value = node.game.get_score(self.my_color)
        else:
            # If the game continues, run the game until an end is reached
            temporary_game = Game(node.game.board.fen_position)
            self.random_engine.simulate(temporary_game)
            back_propagate(node, temporary_game.get_score(self.my_color))
