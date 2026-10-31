from keras.models import Model
from keras.layers import Input, Dense, Embedding, GlobalAveragePooling1D

max_features = 15000
embedding_size = 128
max_len = 250

input_text = Input(shape=(None,))
embedding_layer = Embedding(max_features,embedding_size,input_length=max_len)(input_text)
pooling = GlobalAveragePooling1D()(embedding_layer)
output = Dense(1, activation='sigmoid')(pooling)
model = Model(input_text, pooling)
