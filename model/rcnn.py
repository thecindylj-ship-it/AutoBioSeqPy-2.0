from keras.models import Model
from keras.layers import Input,Embedding, SpatialDropout1D, SimpleRNN, Lambda, concatenate, Conv1D, GlobalMaxPooling1D, Dense
import tensorflow as tf



max_features = 15000
embedding_size = 128
max_len = 250

input_text = Input(shape=(None,))
embedding_layer = Embedding(max_features,embedding_size,input_length=max_len)(input_text)
text_embed = SpatialDropout1D(0.2)(embedding_layer)
l_embedding = Lambda(lambda x: concatenate([tf.zeros(shape=(tf.shape(x)[0], 1, tf.shape(x)[-1])),x[:, :-1]], axis=1))(text_embed)
r_embedding = Lambda(lambda x: concatenate([tf.zeros(shape=(tf.shape(x)[0], 1, tf.shape(x)[-1])),x[:, 1:]], axis=1))(text_embed)
forward = SimpleRNN(128, return_sequences=True)(l_embedding)
backward = SimpleRNN(128, return_sequences=True, go_backwards=True)(r_embedding)
reverse = Lambda(lambda x: tf.reverse(x, axis=[1]))(backward)
together = concatenate([forward, text_embed, backward], axis=2)
semantic = Conv1D(64, kernel_size=1, activation="tanh")(together)
max_pooling = GlobalMaxPooling1D()(semantic)
output = Dense(1, activation='sigmoid')(max_pooling)
model = Model(input_text, output)
