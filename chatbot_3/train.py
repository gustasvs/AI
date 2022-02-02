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

def preprocess_sentence(w):
    w = w.lower().strip()
    # w = w.replace('’', '\'')
    w = re.sub(r"[^a-zA-Z0-9.?]+", " ", w)

    # consequitivedots = re.compile(r'\.{4,}')
    # w = consequitivedots.sub('', w)

    # # pirms punktiem utt ielikt atstarpi
    w = re.sub(r"([?.])", r" \1 ", w)
    # nonemt atkartojosas atstaarpes # w = re.sub(' +', ' ', w)
    w = re.sub(r'[" "]+', " ", w)
    w = w.replace('amp x200b', '')
    
    w = w.strip()

    if w == "":
        w = "xd"
    return w


questions = []
answers = []
from_ = []
to_ = []
with open('reddit_data/train.from', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = preprocess_sentence(line)
        from_.append(line)
        
with open('reddit_data/train.to', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = preprocess_sentence(line)
        to_.append(line)

for i in range(len(from_)):
    if (len(from_[i].split()) > 1 and len(to_[i].split()) > 1):
        sentence = from_[i] + " " + to_[i]
        # questions.append(sentence.rsplit(' ', 1)[0])
        # answers.append(sentence.split(' ', 1)[1])
        for i in range(1, len(sentence.split())):
            pirma_dala = ''
            otra_dala = ''
            for p in range(0, i):
                pirma_dala += sentence.split()[p] + " "
            for o in range(i, len(sentence.split())):
                otra_dala += sentence.split()[o] + " "
            questions.append(preprocess_sentence(pirma_dala))
            answers.append(preprocess_sentence(otra_dala))

for i in range(10, 20):
    print(questions[i], ' --- ', answers[i])

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
with open('tokenizer/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open("tokenizer/START_TOKEN", "w") as f: 
    f.write(str(START_TOKEN[0])) 
with open("tokenizer/END_TOKEN", "w") as f: 
    f.write(str(END_TOKEN[0])) 
with open("tokenizer/VOCAB_SIZE", "w") as f: 
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

checkpoint_path = "model/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, verbose=1)

model.fit(dataset, epochs=EPOCHS, callbacks=[cp_callback])