from keras.models import Model
from keras.layers import Input, Embedding, SpatialDropout1D, Conv1D, GlobalMaxPooling1D, concatenate, Dense


max_features = 15000
embedding_size = 128
max_len = 250

input_text = Input(shape=(None,))
embedding_layer = Embedding(max_features,embedding_size,input_length=max_len)(input_text)
text_embed = SpatialDropout1D(0.2)(embedding_layer)
filter_lengths = [2, 3, 4, 5]
conv_layers = []

for filter_length in filter_lengths:
    conv_layer = Conv1D(filters=300, kernel_size=filter_length, padding='valid',strides=1, activation='relu')(text_embed)
    maxpooling = GlobalMaxPooling1D()(conv_layer)
    conv_layers.append(maxpooling)

sentence_embed = concatenate(inputs=conv_layers)
dense_layer = Dense(256, activation='relu')(sentence_embed)
output = Dense(1, activation='sigmoid')(dense_layer)
model = Model(input_text, output)
