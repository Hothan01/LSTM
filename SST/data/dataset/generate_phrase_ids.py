import re
# author: wangjh237@mail2.sysu.edu.cn
# generate phrase ids for sentences in [train, dev, test]
# you can get phrase ids of [train, dev, test] by the 3 generated files.
# and then find corresponding sentences in dictionary.txt

def clean_data(sentence):
    # From yoonkim: https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    sentence = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", sentence)
    sentence = re.sub(r"\s{2,}", " ", sentence)
    return sentence.strip().lower()


split_dict = {'1':[], '2':[], '3':[]}  # 表示三个集合中包含的sentence
i = 0
with open('datasetSplit.txt', 'r', encoding='UTF-8') as f:
    for line in f:
        if i == 0:
            i += 1
            continue
        [sentence_id, split_id] = line.strip().split(',')
        split_dict[split_id].append(sentence_id)
f.close()

sentence_dict = {}  # [id, sentence] pair
i = 0
with open('datasetSentences.txt', 'r') as f:
    for line in f:
        if i == 0:
            i += 1
            continue
        [sentence_id, sentence] = line.strip().split('\t')
        sentence = clean_data(sentence)   # 去除其余字符
        sentence_dict[sentence_id] = sentence
f.close()

phrase_dict = {}  # [phrase, id] pair
with open('dictionary.txt', 'r') as f:
    for line in f:
        [phrase, phrase_id] =line.strip().split('|')
        phrase = phrase.replace('(', '-LRB-').replace(')', '-RRB-')
        phrase = clean_data(phrase)   # 去除其余字符
        phrase_dict[phrase] = phrase_id
        if 'Absorbing charac' in phrase:
            print(phrase)
f.close()

for split_id in split_dict:

    split_phrase_list = []

    for sentence_id in split_dict[split_id]:
        #print(sentence_id, sentence_dict[sentence_id], phrase_dict[sentence_dict[sentence_id]])
        split_phrase_list.append(phrase_dict[sentence_dict[sentence_id]])

    filename = ''
    if split_id == '1':
        filename = 'phrase_ids.train.txt'
    if split_id == '2':
        filename = 'phrase_ids.test.txt'
    if split_id == '3':
        filename = 'phrase_ids.dev.txt'

    f = open('./' + filename, 'w', encoding='UTF-8')
    for phrase_id in split_phrase_list:
        f.write(phrase_id + '\n')
    f.close()
