import sqlite3
import json
from datetime import datetime

timeframe = '2019-12'
sql_transaction = []

connection = sqlite3.connect(f'{timeframe}.db')
c = connection.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS parent_reply
    (parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT, 
    comment TEXT, subreddit TEXT, unix INT, score INT)""")

def format_data(data):
    data = data.replace("\n", " ").replace("\r", " ").replace('"', "'")
    return data

def acceptable(data):
    if len(data.split(' ')) > 10 or len(data) < 1:
         return False
    elif len(data) > 100:
        return False
    elif data == '[deleted]' or data == '[removed]':
        return False
    elif 'http' in data:
        return False
    elif 'www' in data:
        return False
    elif '/' in data:
        return False
    else:
        return True

def find_parent(parent_id):
    try:
        sql = f"SELECT comment FROM parent_reply WHERE comment_id = '{parent_id}' LIMIT 1"
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        print("find_parent", e)
        return False

def find_existing_score(parent_id):
    try:
        sql = f"SELECT score FROM parent_reply WHERE parent_id = '{parent_id}' LIMIT 1"
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        print("find_existing_score", e)
        return False

def transaction_builder(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []

def sql_insert_replace_comment(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id =?;""".format(parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
        transaction_builder(sql)
    except Exception as e:
        print('replace comment',str(e))

def sql_insert_has_parent(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(parentid, commentid, parent, comment, subreddit, int(time), score)
        transaction_builder(sql)
    except Exception as e:
        print('s0 insertion',str(e))

def sql_insert_no_parent(commentid,parentid,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}",{},{});""".format(parentid, commentid, comment, subreddit, int(time), score)
        transaction_builder(sql)
    except Exception as e:
        print('replace_comment_noparent',str(e))


if __name__ == "__main__":
    create_table()
    row_counter = 0
    paired_rows = 0
    replaced_rows = 0

    with open("C:/Python123/AI/chatbot/reddit_data/{}/RC_{}".format(timeframe.split('-')[0], timeframe), buffering=1000) as f:
        for row in f:
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            try:
                comment_id = row['name']
            except:
                comment_id = 't1_' + row['id']
            parent_data = find_parent(parent_id)
            if score > 100:
                if acceptable(body):
                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score:
                        if score > existing_comment_score:
                            sql_insert_replace_comment(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
                            replaced_rows += 1
                    else:
                        if parent_data:
                            sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
                            paired_rows += 1
                        else:
                            sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score)
            if row_counter % 1000000 == 0:
                print(f"total rows - {row_counter}, paired rows - {paired_rows}, replaced rows - {replaced_rows}, time - {datetime.now()}")
        print(f"total rows - {row_counter}, paired rows - {paired_rows}, replaced rows - {replaced_rows}, time - {datetime.now()}")


