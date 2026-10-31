import keras_nlp
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


MAX_SEQUENCE_LENGTH = 81
VOCAB_SIZE = 15000
EMBED_DIM = 128
INTERMEDIATE_DIM = 512

input_ids = keras.Input(shape=(None,), dtype="int64", name="input_ids")
x = keras_nlp.layers.TokenAndPositionEmbedding(
    vocabulary_size=VOCAB_SIZE,
    sequence_length=MAX_SEQUENCE_LENGTH,
    embedding_dim=EMBED_DIM,
    mask_zero=True,
)(input_ids)
x = keras_nlp.layers.FNetEncoder(intermediate_dim=INTERMEDIATE_DIM)(inputs=x)
x = keras_nlp.layers.FNetEncoder(intermediate_dim=INTERMEDIATE_DIM)(inputs=x)
x = keras_nlp.layers.FNetEncoder(intermediate_dim=INTERMEDIATE_DIM)(inputs=x)
x = keras.layers.GlobalAveragePooling1D()(x)
model = keras.Model(inputs=input_ids, outputs=x)

