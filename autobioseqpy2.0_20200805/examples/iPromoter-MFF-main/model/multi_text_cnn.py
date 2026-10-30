from keras.models import Model
from keras.layers import Input, Embedding, SpatialDropout1D, Conv1D, concatenate, Dense, GlobalMaxPooling1D, BatchNormalization


max_features = 15000
embedding_size = 128


input_text = Input(shape=(None,))
embedding_layer = Embedding(max_features,embedding_size,input_length=250)(input_text)
text_embed = SpatialDropout1D(0.2)(embedding_layer)
filter_lengths = [2, 3, 4, 5]
conv_layers = []
for filter_length in filter_lengths:
    conv_layer_1 = Conv1D(filters=300, kernel_size=filter_length, strides=1,padding='valid', activation='relu')(text_embed)
    bn_layer_1 = BatchNormalization()(conv_layer_1)
    conv_layer_2 = Conv1D(filters=300, kernel_size=filter_length, strides=1,padding='valid', activation='relu')(bn_layer_1)
    bn_layer_2 = BatchNormalization()(conv_layer_2)
    maxpooling = GlobalMaxPooling1D()(bn_layer_2)
    conv_layers.append(maxpooling)
sentence_embed = concatenate(inputs=conv_layers)
dense_layer = Dense(256, activation='relu')(sentence_embed)
output = Dense(1, activation='sigmoid')(dense_layer)
model = Model(input_text, output)
