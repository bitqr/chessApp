import tensorflow
from tensorflow import keras
from tensorflow.keras import layers, Input

from engine import utils

fen_position = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
input_vector = utils.from_fen_to_input_vector(fen_position)
input_vector = tensorflow.convert_to_tensor([input_vector], dtype=tensorflow.float32)
print(input_vector)


model = keras.Sequential(name="my_neural_network")
first_layer = layers.Dense(2, activation="relu", name="layer1")

# As decided, the input vectors, representing chessboard positions, will be of size 784
model.add(Input(shape=784,))
model.add(first_layer)

print(first_layer.weights)
print(first_layer.bias)

y = model(input_vector)
print('Number of weights after calling the model:', len(model.weights))
model.summary()
