import os
import codecs
import random
import time
from collections import defaultdict
import numpy as np

from collections import defaultdict
from nltk.tokenize import word_tokenize
import heapq

# lookUp_List = { '89' : {'when': [], 'who': [], 'where': [(0, 0, 'India'), (1, 1, 'Microsoft')]}   }
# 
# Corpus = [
#                        [
#                             "Gandhi is father of India",
#                             "Newton made laws of motion",
#                        ],
#                        [
#                             "Apple makes Iphone",
#                             "Hololens was made by Microsoft",
#                             "Facebook has caputerd VR space"
#                        ],
#                        [
#                             "New Macbooks are not upto the mark",
#                             "Surface desktops are the new thing to look at"
#                        ]
#                    ]

h = []
def insert_in_heap(common_word_count, QId, Doc_ID, answer):
    heapq.heappush(h, (common_word_count, QId, Doc_ID, answer))

def getTokenSet(sentence):
    word_List = word_tokenize(sentence)
    return set(word_List)

def match_Question_answer(question_Tokens_set, answer_Tokens_set):
    common_word_count = len(set.intersection(question_Tokens_set, answer_Tokens_set))
    return (common_word_count)

def FindMaxMatchingAnswer(QId, QType, QText, Corpus, lookUp_List):
    question_Tokens_set = getTokenSet(QText)
    #tuple_List = lookUp_List.get(QId).get(QType)
    qid = str(QId)
    tuple_List =  lookUp_List[str(qid)][QType.lower()]
    top_five_answers = []
    for tuple in tuple_List:
        #print(tuple)
        Doc_ID = tuple[0]
        Sent_ID = tuple[1]
        answer = tuple[2]
        #try :
        sentence = Corpus[qid][Doc_ID][Sent_ID]
        #except :
            #print qid
        answer_Tokens_set = getTokenSet(sentence)
        common_word_count = match_Question_answer(question_Tokens_set, answer_Tokens_set)
        heapq.heappush(h, (common_word_count, QId, Doc_ID, answer))

    top_five_tuples = heapq.nlargest(5, h);
    for answer_tuple in top_five_tuples:
        top_five_answers.append(answer_tuple[1:4])
    return top_five_answers

# heap = FindMaxMatchingAnswer('89', "where", "where, is Gandhi?", Corpus, lookUp_List)
# print(heap)