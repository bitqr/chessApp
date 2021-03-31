import tensorflow
from tensorflow import keras

from engine import utils
from engine.NeuralNetwork import NeuralNetwork

fen_position = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
input_vector = utils.from_fen_to_input_vector(fen_position)
input_vector = tensorflow.convert_to_tensor([input_vector], dtype=tensorflow.float32)
print(input_vector)

# Neural network starting from scratch
neural_network = NeuralNetwork()

# Train the model on random data
neural_network.model.compile()

y = neural_network.evaluate(input_vector)
neural_network.model.summary()

print(y)

neural_network.save_model('../../resources/model_parameters/example_model')

# Load the model in a new NN
copied_model = keras.models.load_model('../../resources/model_parameters/example_model')
other_neural_network = NeuralNetwork(copied_model)

y2 = other_neural_network.evaluate(input_vector)

# Check that both neural networks provide the same evaluation
print(y2)

other_neural_network.model.summary()
