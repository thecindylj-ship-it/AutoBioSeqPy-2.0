from keras.models import Model
from keras.layers import Input, Embedding, SpatialDropout1D, Conv1D, GRU, concatenate, Dense, Bidirectional, GlobalAveragePooling1D, GlobalMaxPooling1D

max_features = 15000
embedding_size = 128


input_text = Input(shape=(None,))
embedding_layer = Embedding(max_features,embedding_size,input_length=250)(input_text)
text_embed = SpatialDropout1D(0.2)(embedding_layer)
gru_layer = Bidirectional(GRU(128, return_sequences=True))(text_embed)
conv_layer = Conv1D(64, kernel_size=2, padding="valid", kernel_initializer="he_uniform")(gru_layer)
avg_pool = GlobalAveragePooling1D()(conv_layer)
max_pool = GlobalMaxPooling1D()(conv_layer)
sentence_embed = concatenate([avg_pool, max_pool])
dense_layer = Dense(256, activation='relu')(sentence_embed)
output = Dense(1, activation='sigmoid')(dense_layer)
model = Model(input_text, output)
