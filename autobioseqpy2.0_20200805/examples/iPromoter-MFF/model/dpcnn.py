from keras.models import Model
from keras.layers import Input, Embedding, SpatialDropout1D, Conv1D,Dense, Activation, Add, MaxPooling1D, GlobalMaxPooling1D


max_features = 15000
embedding_size = 128
max_len = 250

input_text = Input(shape=(None,))
embedding_layer = Embedding(max_features,embedding_size,input_length=max_len)(input_text)
text_embed = SpatialDropout1D(0.2)(embedding_layer)
repeat = 3
size = max_len
region_x = Conv1D(filters=250, kernel_size=3, padding='same', strides=1)(text_embed)
x = Activation(activation='relu')(region_x)
x = Conv1D(filters=250, kernel_size=3, padding='same', strides=1)(x)
x = Activation(activation='relu')(x)
x = Conv1D(filters=250, kernel_size=3, padding='same', strides=1)(x)
x = Add()([x, region_x])

for _ in range(repeat):
    px = MaxPooling1D(pool_size=3, strides=2, padding='same')(x)
    size = int((size + 1) / 2)
    x = Activation(activation='relu')(px)
    x = Conv1D(filters=250, kernel_size=3, padding='same', strides=1)(x)
    x = Activation(activation='relu')(x)
    x = Conv1D(filters=250, kernel_size=3, padding='same', strides=1)(x)
    x = Add()([x, px])

x = MaxPooling1D(pool_size=size)(x)
sentence_embed = GlobalMaxPooling1D()(x)
dense_layer = Dense(256, activation='relu')(sentence_embed)
output = Dense(1, activation='sigmoid')(dense_layer)
model = Model(input_text, output)
