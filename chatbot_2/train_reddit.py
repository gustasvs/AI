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

# Load and preprocess data

questions = []
answers = []
with open('reddit_data/train.from', 'r') as f:
  lines = f.readlines()
  for line in lines:
    questions.append(line)
with open('reddit_data/train.to', 'r') as f:
  lines = f.readlines()
  for line in lines:
    answers.append(line)


# Tokenize
tokenizer = tfds.features.text.SubwordTextEncoder.build_from_corpus(questions + answers, target_vocab_size=TARGET_VOCAB_SIZE)

START_TOKEN = [tokenizer.vocab_size]
END_TOKEN   = [tokenizer.vocab_size + 1]
VOCAB_SIZE  = tokenizer.vocab_size + 2

questions, answers = tokenize_and_filter(questions, answers, START_TOKEN, END_TOKEN, tokenizer)

print('Vocab size: {}'.format(VOCAB_SIZE))
print('Number of samples: {}'.format(len(questions)))


dataset = tf.data.Dataset.from_tensor_slices((
    {
        'inputs': questions,
        'dec_inputs': answers[:, :-1]
    },
    {
        'outputs': answers[:, 1:]
    },
))

dataset = dataset.cache()
dataset = dataset.shuffle(BUFFER_SIZE)
dataset = dataset.batch(BATCH_SIZE)
dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)


# save tokenizer
with open('tokenizer_reddit/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open("tokenizer_reddit/START_TOKEN", "w") as f: 
    f.write(str(START_TOKEN[0])) 
with open("tokenizer_reddit/END_TOKEN", "w") as f: 
    f.write(str(END_TOKEN[0])) 
with open("tokenizer_reddit/VOCAB_SIZE", "w") as f: 
    f.write(str(VOCAB_SIZE)) 



tf.keras.backend.clear_session()

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

model.summary()

checkpoint_path = "model_reddit/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, verbose=1)

model.fit(dataset, epochs=EPOCHS, callbacks=[cp_callback])