import math

import tensorflow
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow import Tensor

from engine import utils
from internal.Game import Game


def choose_move(game, policy_vector):
    # In this method we loop over all legal moves in the current position
    # And keep the one that has the best value in the policy vector
    chosen_move = None
    current_value = - math.inf
    for move in game.board.position.legal_moves_list():
        move_evaluation = tensorflow.gather_nd(policy_vector, [0, utils.from_move_to_output_index(move)])
        if move_evaluation > current_value:
            chosen_move = move
            current_value = move_evaluation
    return chosen_move


def initialize_network():
    # Output layer has 4164-components for the policy vector and 1 component for the board evaluation
    model = keras.Sequential()
    model.add(keras.Input(shape=(28, 28, 1)))
    model.add(layers.Conv2D(filters=256, kernel_size=[3, 3], strides=1, input_shape=(28, 28, 1), activation='relu'))
    model.add(layers.MaxPool2D())
    model.add(layers.BatchNormalization())
    model.add(layers.Conv2D(filters=73, kernel_size=[3, 3], strides=1, activation='relu'))
    model.add(layers.MaxPool2D())
    model.add(layers.BatchNormalization())
    model.add(layers.Flatten())
    model.add(layers.Dense(4165, activation='relu', name='output_layer'))
    model.compile(loss=keras.losses.MeanSquaredError())
    return model


class NeuralNetwork:

    def __init__(self, model=None):
        if model:
            self.model = model
        else:
            self.model = initialize_network()

    def evaluate(self, input_vector: Tensor):
        # Receives an input vector and returns
        # - A list of probabilities associated to each action --> policy P(a | s)
        # - A float value giving the expected outcome of the game (last component of the vector)
        # Then, feed this input vector to the model
        # Get the selected move from the output and send it to Monte-Carlo search tree ...
        input_vector = tensorflow.convert_to_tensor([input_vector], dtype=tensorflow.float32)
        input_vector = tensorflow.reshape(input_vector, (-1, 28, 28, 1))
        return self.model(input_vector)

    def simulate(self, board_position, my_color):
        simulation_game = Game(board_position)
        while not simulation_game.is_over():
            move = self.decide(simulation_game)
            simulation_game.board.apply_move(move, log=False)
            if simulation_game.can_be_drawn():
                simulation_game.apply_draw()
        return simulation_game.get_score(my_color)

    def update(self, input_vector, output_vector):
        input_vector = tensorflow.convert_to_tensor(input_vector, dtype=tensorflow.float32)
        input_vector = tensorflow.reshape(input_vector, (-1, 28, 28, 1))
        output_vector = tensorflow.constant(output_vector, dtype=tensorflow.float32)
        self.model.fit(x=input_vector, y=output_vector)

    def decide(self, game):
        # 1st step is to convert the FEN string to an input vector
        input_vector = utils.from_fen_to_input_vector(game.board.fen_position)
        input_vector = tensorflow.convert_to_tensor([input_vector], dtype=tensorflow.float32)
        input_vector = tensorflow.reshape(input_vector, (-1, 28, 28, 1))
        # Get the output policy from the neural net for this position
        policy_vector = tensorflow.constant(self.evaluate(input_vector))
        # Among all possible moves take the one indicated by the policy vector and apply it
        return choose_move(game, policy_vector)

    def save_model(self, file_name):
        self.model.save(file_name)
