import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import random
import pickle
from collections import Counter

lemmitizer = WordNetLemmatizer()
hm_lines = 100000
maxpop = 1000
minpop = 50

def create_lexicon(pos, neg):
    lexicon = []
    for fi in [pos, neg]:
        with open(fi,'r') as f:
            contents = f.readlines()
            for line in contents[:hm_lines]:
                all_words = word_tokenize(line.lower())
                lexicon += list(all_words)
    lexicon = [lemmitizer.lemmatize(i) for i in lexicon]
    w_counts = Counter(lexicon)
    #w_counts = {'the':51525, 'and':25242}
    l2 = []
    for w in w_counts:
        if maxpop > w_counts[w] > minpop:
            l2.append(w)
    print(len(l2))
    return l2

def sample_handling(sample, lexicon, classification):
    featureset = []
    with open(sample,'r') as f:
        contents = f.readlines()
        for line in contents[:hm_lines]:
            current_words = word_tokenize(line.lower())
            current_words = [lemmitizer.lemmatize(i) for i in current_words]
            features = np.zeros(len(lexicon))
            for word in current_words:
                if word.lower() in lexicon:
                    index_value = lexicon.index(word.lower())
                    features[index_value] += 1
            features = list(features)
            featureset.append([features, classification])
    return featureset

def create_feature_sets(pos, neg, test_size=0.1):
    lexicon = create_lexicon(pos,neg)
    features = []
    features += sample_handling('pos.txt', lexicon,[1,0])
    features += sample_handling('neg.txt', lexicon,[0,1])
    random.shuffle(features)

    features = np.array(features)
    testing_size = int(test_size*len(features))

    train_x = list(features[:,0][:-testing_size])
    train_y = list(features[:,1][:-testing_size])

    test_x = list(features[:,0][-testing_size:])
    test_y = list(features[:,1][-testing_size:])

    return train_x,train_y,test_x,test_y

if __name__ == '__main__':
    train_x,train_y,test_x,test_y = create_feature_sets('pos.txt', 'neg.txt')
    with open('sentiment_set.pickle','wb') as f:
        pickle.dump([train_x,train_y,test_x,test_y], f)