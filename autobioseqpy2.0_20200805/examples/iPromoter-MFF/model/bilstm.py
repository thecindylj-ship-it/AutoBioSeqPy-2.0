from keras.models import Model
from keras.layers import Input, Embedding, SpatialDropout1D, Dense, LSTM, Bidirectional, Lambda
import keras.backend as K


max_features = 15000
embedding_size = 128



input_text = Input(shape=(None,))
embedding_layer = Embedding(max_features,embedding_size,input_length=250)(input_text)
text_embed = SpatialDropout1D(0.2)(embedding_layer)
hidden_states = Bidirectional(LSTM(units=128, return_sequences=True))(text_embed)
global_max_pooling = Lambda(lambda x: K.max(x, axis=1))
sentence_embed = global_max_pooling(hidden_states)
dense_layer = Dense(256, activation='relu')(sentence_embed)
output = Dense(1, activation='sigmoid')(dense_layer)
model = Model(input_text, output)


