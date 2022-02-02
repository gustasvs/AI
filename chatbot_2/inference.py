# https://github.com/tensorflow/examples/blob/master/community/en/transformer_chatbot.ipynb

import tensorflow as tf
# assert tf.__version__.startswith('2')
tf.random.set_seed(1234)

import tensorflow_datasets as tfds
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import pickle

from functions import *
from hparams import *


with open('tokenizer/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open("tokenizer/START_TOKEN", "r") as f: 
    START_TOKEN = [int(f.read())] 
with open("tokenizer/END_TOKEN", "r") as f: 
    END_TOKEN = [int(f.read())]
with open("tokenizer/VOCAB_SIZE", "r") as f: 
    VOCAB_SIZE = int(f.read())


def evaluate(sentence):
  sentence = preprocess_sentence(sentence)

  sentence = tf.expand_dims(
      START_TOKEN + tokenizer.encode(sentence) + END_TOKEN, axis=0)

  output = tf.expand_dims(START_TOKEN, 0)

  for i in range(MAX_LENGTH):
    predictions = model(inputs=[sentence, output], training=False)

    # select the last word from the seq_len dimension
    predictions = predictions[:, -1:, :]
    predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

    # return the result if the predicted_id is equal to the end token
    if tf.equal(predicted_id, END_TOKEN[0]):
      break

    # concatenated the predicted_id to the output which is given to the decoder
    # as its input.
    output = tf.concat([output, predicted_id], axis=-1)

  return tf.squeeze(output, axis=0)


def predict(sentence):
  prediction = evaluate(sentence)

  predicted_sentence = tokenizer.decode(
      [i for i in prediction if i < tokenizer.vocab_size])

  return predicted_sentence


def create_model():
   
    model = transformer(
    vocab_size=VOCAB_SIZE,
    num_layers=NUM_LAYERS,
    units=UNITS,
    d_model=D_MODEL,
    num_heads=NUM_HEADS,
    dropout=DROPOUT)

    learning_rate = CustomSchedule(D_MODEL)

    optimizer = tf.keras.optimizers.Adam(learning_rate, beta_1=0.9, beta_2=0.98, epsilon=1e-9)

    model.compile(optimizer=optimizer, loss=loss_function, metrics=[accuracy])

    return model

model = create_model()


checkpoint_path = "model/cp.ckpt"

model.load_weights(checkpoint_path)


while True:
    question = input("\n--> ")
    if question == "" or question == None:
        continue
    output = predict(question)
    print(output)

