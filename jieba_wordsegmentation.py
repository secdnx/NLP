# coding: utf-8

import json
import codecs
from hanziconv import HanziConv


# article path
articlepath = 'src_article/pttcontentall_article3452.json'

# segmented article path
cuttedpath = 'cut_test/pttcontentall_article3452_cutted.json'

source = 'ptt'


# load synonyms dictionary
with open('dictionary/dict-same.json', 'r') as f:
    same = json.load(f)
    f.close()

# load stopwords dictionary
with codecs.open('dictionary/formal/stop_words _tfidf2.txt', 'r', encoding='utf-8') as fs:
    stopwords = fs.read().split('\n')
    fs.close()

# punctuation marks that would be replaced
ditto = '[’!"#$%&\'’()*+,-./:;．<=>?@\\^_`\[\]{|}~]+'

# new an empty list to store segmented dict
cutted_list = []

# define a function to do word segmentation(by dict-element)
def cut_words(j_dict):
    try:

        line = j_dict['content'].upper().replace(' ','').replace('\n','').strip()
        line = re.sub(r'<!\[CDATA\[(.*?)\]\]>', '', line)
        line = re.sub(ditto, '', line)

        words = jieba.cut(line, cut_all=False, HMM=True)
        cutted_article = ''
        for x, word in enumerate(words):
            if word in stopwords or word == ' ':
                continue
            if re.match('[0-9]+', word):
                continue
            else:
                if word in same.keys():
                    word = same[word]
                cutted_article += (' ' + word)

        j_dict['city_treated'] = ""
        j_dict['content'] = cutted_article
        j_dict['source'] = source
        j_dict['title'] = re.sub(r'<!\[CDATA\[(.*?)\]\]>', '', j_dict['title'])
        cutted_list.append(j_dict)
    except Exception as e:
        print e
        pass


def worker():
    while not queue.empty():
        a_readytocut = queue.get()
        cut_words(a_readytocut)



import json
import jieba
import re
from datetime import datetime
from threading import Thread
from Queue import Queue

# load JIEBA dictionary
jieba.set_dictionary('dictionary/formal/dict.txt.big')

# load user-define dictionary
jieba.load_userdict("dictionary/formal/userdict.txt")


s1 = datetime.now()


# open article
with open(articlepath, 'rb') as fa:
    a_list = json.load(fa)
    fa.close()

# put every article to Queue
queue = Queue()
for idx, a in enumerate(a_list):
    queue.put(a)
    # print a['title'] + ' put in queue~'





# multithreading
threads = map(lambda i: Thread(target=worker), xrange(2))
map(lambda th: th.start(), threads)
map(lambda th: th.join(), threads)


s2 = datetime.now()

# caculate operating time
print "All  Finish " + str(s2 - s1) + "!!"


# dump list to json file
json = json.dumps(cutted_list, ensure_ascii=False, indent=4, sort_keys=True)
with open(cuttedpath, 'w') as a:
    a.write(json.encode('utf-8'))