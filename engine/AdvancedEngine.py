from tensorflow import keras

from engine.NeuralNetwork import NeuralNetwork


class AdvancedEngine:

    def __init__(self, neural_network=None, saved_model=''):
        if neural_network:
            self.neural_network = neural_network
        else:
            model = keras.models.load_model(saved_model)
            self.neural_network = NeuralNetwork(model)

    def choose_move(self, game):
        return self.neural_network.decide(game)
