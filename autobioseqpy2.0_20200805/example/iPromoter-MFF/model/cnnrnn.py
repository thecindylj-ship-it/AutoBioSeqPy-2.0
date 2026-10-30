from keras.models import Model
from keras.layers import Input, Embedding, SpatialDropout1D, Conv1D, GRU, concatenate, Dense, Bidirectional, MaxPooling1D, GlobalMaxPooling1D




max_features = 15000
embedding_size = 128


input_text = Input(shape=(None,))
embedding_layer = Embedding(max_features,embedding_size,input_length=250)(input_text)
text_embed = SpatialDropout1D(0.2)(embedding_layer)
conv_layer = Conv1D(300, kernel_size=3, padding="valid", activation='relu')(text_embed)
conv_max_pool = MaxPooling1D(pool_size=2)(conv_layer)
gru_layer = Bidirectional(GRU(128, return_sequences=True))(conv_max_pool)
sentence_embed = GlobalMaxPooling1D()(gru_layer)
dense_layer = Dense(256, activation='relu')(sentence_embed)
output = Dense(1, activation='sigmoid')(dense_layer)
model = Model(input_text, output)
