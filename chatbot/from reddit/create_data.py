import sqlite3
import pandas as pd
from datetime import datetime
import re

TIMEFRAMES = ['2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06',
              '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12']

total_total_rows = 0

def preprocess_sentence(w):
    w = w.lower().strip()
    # w = w.replace('’', '\'')
    w = re.sub(r"[^a-zA-Z0-9.?]+", " ", w)

    # consequitivedots = re.compile(r'\.{4,}')
    # w = consequitivedots.sub('', w)

    # # pirms punktiem utt ielikt atstarpi
    w = re.sub(r"([?.'])", r" \1 ", w)
    # nonemt atkartojosas atstaarpes # w = re.sub(' +', ' ', w)
    w = re.sub(r'[" "]+', " ", w)
    w = w.replace('amp x200b', '')
    
    w = w.strip()

    if w == "":
        w = "xd"
    return w

def writeinfile(file_name, file_meaning):
    with open(file_name, "a", encoding='utf8') as f:
        for content in df[file_meaning].values:
            content = preprocess_sentence(content)
            f.write(content + '\n')


for timeframe in TIMEFRAMES:
    print(f"timeframe - {timeframe} ...")
    connection = sqlite3.connect(f"{timeframe}.db")
    c = connection.cursor()
    limit = 50
    last_unix = 0
    cur_lenght = limit
    counter = 0
    test_done = False
    while cur_lenght == limit:
        df = pd.read_sql(f"SELECT * FROM parent_reply WHERE unix > {last_unix} and parent NOT NULL and score > 100 ORDER BY unix ASC LIMIT {limit}", connection)
        last_unix = df.tail(1)['unix'].values[0]
        cur_lenght = len(df)
        if not test_done:
            writeinfile("test.from", 'parent')
            writeinfile("test.to", 'comment')
            test_done = True
            print(f"test done - {counter * limit}, time - {datetime.now()}")
            limit = 10000
            cur_lenght = limit
        else:
            writeinfile("train.from", 'parent')
            writeinfile("train.to", 'comment')
        counter += 1
        # if counter % 10 == 0:
            # print(f"total rows - {counter * limit}, time - {datetime.now()}")

    print(f"total rows - {counter * limit}, time - {datetime.now()}")
    total_total_rows += counter * limit

print(f"total rows --> {total_total_rows}")


