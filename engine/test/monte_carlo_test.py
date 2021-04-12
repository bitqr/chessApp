from tensorflow import keras

from engine.Engine import Engine
from engine.NeuralNetwork import NeuralNetwork
from engine.train_model_self_play import mcts_self_play
from internal.Game import Game


# Load the neural network that MCTS will use to run its simulations
model = keras.models.load_model('../../resources/model_parameters/trained_model')
neural_net = NeuralNetwork(model)
test_game = Game()
test_engine = Engine(neural_net)

ins, policy_output, score_output = mcts_self_play(test_game, test_engine)

neural_net.update(ins, policy_output, score_output)
neural_net.save_model('../../resources/model_parameters/trained_model')
