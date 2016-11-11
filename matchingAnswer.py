import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import heapq
import project_config

#lookup_list = { '89' : {'when': [], 'who': [], 'where': [(0, 0, 'India'), (1, 1, 'Microsoft')]}   }
# 
#corpus ={ '89': [
#                    [
#                         "Gandhi is father of India",
#                         "Newton made laws of motion",
#                    ],
#                    [
#                         "Apple makes Iphone",
#                         "Hololens was made by Microsoft",
#                         "Facebook has caputerd VR space"
#                    ],
#                    [
#                         "New Macbooks are not upto the mark",
#                         "Surface desktops are the new thing to look at"
#                    ]
#                ]
#       }

# Remove_stop_words should be called after tokenization
#sentence is a list of words ["Hi", "how", "are", "you"]
#returns a new list of words
#move the below two line to the calling code and pass the s_words to the function
s_words = nltk.corpus.stopwords.words('english')
string_stop_words = [ str(x) for x in  s_words]
lowercase_mode_on = True
def remove_stop_words( sentence, stop_words_list ):
    sent = [ w for w in sentence if w.lower() not in stop_words_list ]
    return sent

def calculate_weight(match_count, doc_score) :
    return (doc_score * project_config.doc_score_weight + match_count)

def get_token_set(sentence):
    word_List = word_tokenize(sentence)
    return set(word_List)

def match_question_answer(question_tokens_set, answer_tokens_set):
    common_word_count = len(set.intersection(question_tokens_set, answer_tokens_set))
    return (common_word_count)

def context_based_sentences( corpus, qid, doc_id, sent_id, context_span):
    sentence_list = ""
    current_sentence_number = context_span/2
    context_lower_bound = max(sent_id - current_sentence_number, 0)
    doc_length = len(corpus[qid][doc_id])
    context_upper_bound = min(doc_length - 1,context_lower_bound + context_span -1)
    for sent_num in range(context_lower_bound, context_upper_bound + 1):
        sentence_list = sentence_list + " " + corpus[qid][doc_id][sent_num]
    return sentence_list
    
def find_max_matching_answer(qid, qtype, qtext, corpus, lookup_list, lookup_score):
    h = []
    question_tokens_set = get_token_set(qtext)
    qid = str(qid)
    tuple_list =  lookup_list[str(qid)][qtype.lower()]
    context_span = 4
    top_five_answers = []
    for tup in tuple_list:
        doc_id = tup[0]
        sent_id = tup[1]
        answer = tup[2]
        sentence_list = context_based_sentences(corpus, qid, doc_id, sent_id, context_span)
        answer_tokens_set = get_token_set(sentence_list)
        #Matching tokens in lower case
        if lowercase_mode_on:
            answer_tokens_set = {w.lower() for w in answer_tokens_set}
            question_tokens_set = {w.lower() for w in question_tokens_set}
        common_word_count = match_question_answer(question_tokens_set, answer_tokens_set)
        match_count_weight = calculate_weight(common_word_count,lookup_score[qid][doc_id])
        heapq.heappush(h, (match_count_weight, qid, doc_id, answer))

    top_twenty_tuples = heapq.nlargest(20, h);
    answer_list = []
    for answer_tuple in top_twenty_tuples:
        answer_token = answer_tuple[3]
        if answer_token not in answer_list:
            top_five_answers.append(answer_tuple[1:4])
            answer_list.append(answer_token)
    return top_five_answers[0:5]

''' Sample run for the function in this file''
heap = find_max_matching_answer('89', "where", "where, is Gandhi?", corpus, lookup_list)
print(heap)
#'''
''' sample remove stop words ''
qw = remove_stop_words( ["me", "asd", "qw"], s_words)
print(qw)
'''