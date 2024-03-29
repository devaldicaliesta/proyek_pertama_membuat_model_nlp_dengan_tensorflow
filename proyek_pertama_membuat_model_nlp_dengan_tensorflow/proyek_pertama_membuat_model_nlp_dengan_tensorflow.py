# -*- coding: utf-8 -*-
"""Proyek Pertama : Membuat Model NLP dengan TensorFlow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NVd3cXCS5voDLOLqrNAn2qcaA8K-5vzM

Nama : Devaldi Caliesta Octadiani \
Email : devaldicaliesta20@gmail.com \
Alamat Domisili : Kabupaten Bantul, Daerah Istimewa Yogyakarta, 55187
"""

# Menyiapkan Library yang dibutuhkan
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import re
import nltk

from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# melihat dataset
df = pd.read_csv('bbc-news-data.csv', sep="\t") 
df.head()

# melihat info data
df.info()

# melihat missing value
df.isna().sum()

# Drop data yang tidak dibutuhkan
df_new = df.drop(['filename'], axis=1)

df_new.head()

# menghilangkan tanda baca & angka pada coloumn content
def remove_punctuations_numbers(inputs):
    return re.sub(r'[^a-zA-Z]', ' ', inputs)


df_new['content'] = df['content'].apply(remove_punctuations_numbers)

def data_cleaner(review):
   #removing stop words
    review = review.split()
    review = " ".join([word for word in review if not word in stop_words])

    return review

ps = PorterStemmer()
stop_words = stopwords.words('english')

df_new['content'] = df_new['content'].apply(data_cleaner)

# mengecek data yang telah di prepocessing
df_new.head()

# melakukan split data
news = list(df.content)
label = list(df.category)

#bagi data untuk training dan data untuk testing.
news_train, news_test, label_train, label_test = train_test_split(news, label, train_size = 0.8, random_state = 42, shuffle = True)

vocab_size = 10000
embedding_dim = 32
max_length = 256
padding_type='post'

# melakukan tokenize
tokenizer = Tokenizer(num_words = vocab_size, oov_token="<OOV>")
tokenizer.fit_on_texts(news_train)
word_index = tokenizer.word_index

news_train_sqncs = tokenizer.texts_to_sequences(news_train)
news_train_padded = pad_sequences(news_train_sqncs, padding=padding_type, maxlen=max_length)

news_test_sqncs = tokenizer.texts_to_sequences(news_test)
news_test_padded = pad_sequences(news_test_sqncs, padding=padding_type, maxlen=max_length)

category_tokenizer = Tokenizer()
category_tokenizer.fit_on_texts(df.category)
category_index = category_tokenizer.word_index

label_train_label_sqncs = np.array(category_tokenizer.texts_to_sequences(y_train))
label_test_label_sqncs = np.array(category_tokenizer.texts_to_sequences(y_test))

# melakukan arsitektur model kita menggunakan layer Embedding
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(6, activation='softmax')
])
model.compile(loss='sparse_categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
model.summary()

# melatih model kita dengan memanggil fungsi fit() dan menggunakan callback earlystopping

callbacks = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', mode='max', patience=5,
                                                  restore_best_weights=True)

num_epochs = 50
history = model.fit(news_train_padded, label_train_label_sqncs, epochs=num_epochs, 
                    validation_data=(news_test_padded, label_test_label_sqncs), 
                    verbose=2, callbacks=[callbacks], batch_size=32)

#plot accuracy
import matplotlib.pyplot as plt
plt.figure(figsize=(12,6))
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.xlabel("Epochs")
plt.ylabel('Accuracy')
plt.legend(['accuracy', 'val_accuracy'])
plt.title('Train and Validation Loss Graphs')

#plot loss
plt.figure(figsize=(12,6))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.xlabel("Epochs")
plt.ylabel('Loss')
plt.legend(['loss', 'val_loss'])
plt.title('Train and Validation Accuracy Graphs')

