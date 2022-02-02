import json
import time

def writeinfile(file_name, content):
    with open(file_name, "a", encoding='utf8') as f:
        f.write(content + '\n')

count = 0
with open('data_from_squad.json') as a:
    data = json.load(a)
    for q in data['data']:
        for qua in q['paragraphs']:
            # print(qua['qas'])
            for qas in qua['qas']:
                quest = qas['question']
                for answer_details in qas['answers']:
                    answ = answer_details['text']
                count += 1
                writeinfile("data.from", quest)
                writeinfile("data.to", answ)
        print(q['title'], count)
                # print(quest)
                # print(answ)
        # time.sleep(1)
                




# writeinfile("test.from", 'parent')
# writeinfile("test.to", 'comment')



