import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('punkt')

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
#string_stop_words = [ str(x) for x in  s_words]

def remove_stop_words( sentence, stop_words_list ):
    sent = [ w for w in sentence if w.lower() not in stop_words_list ]
    return set(sent)

def calculate_weight(match_count, doc_score) :
    return (doc_score * project_config.doc_score_weight + match_count)

def stem_sentence(sentence):
    stemmed_wordlist=[]
    ps=PorterStemmer()
    words=word_tokenize(sentence)
    words = set(words)
    for w in words:
        try:
            #stemmed_wordlist.append(ps.stem(w))
            stemmed_wordlist.append(str(ps.stem(w)))
        except:
            print(w)
    return set(stemmed_wordlist)

def get_token_set(sentence):
    word_List = word_tokenize(sentence)
    return set(word_List)

def match_question_answer(question_tokens_set, answer_tokens_set):
    common_word_count = len(set.intersection(question_tokens_set, answer_tokens_set))
    return (common_word_count)

def preprocess_sentence_before_match(sentence):
    stemmed_sentence = stem_sentence(sentence)
    return remove_stop_words(stemmed_sentence,s_words)

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
    h2 = []
    #question_tokens_set = get_token_set(qtext)
    #qtext_stemmed = stem_sentence(qtext)
    #question_tokens_set = remove_stop_words(qtext_stemmed, s_words)
    question_tokens_set = preprocess_sentence_before_match(qtext)

    qid = str(qid)
    tuple_list =  lookup_list[str(qid)][qtype.lower()]
    context_span = project_config.context_span
    top_five_answers = []
    for tup in tuple_list:
        doc_id = tup[0]
        sent_id = tup[1]
        answer = tup[2]
        #
        # Skip documents based on project_config.max_rank_check!
        #
        if doc_id > project_config.max_rank_check :
            break;

        sentence = corpus[qid][doc_id][sent_id]
        sentence_list = context_based_sentences(corpus, qid, doc_id, sent_id, context_span)

        #sentence = stem_sentence(sentence)
        #answer_tokens_set = remove_stop_words(sentence, s_words)
        #answer_tokens_set = get_token_set(sentence)
        answer_tokens_set = preprocess_sentence_before_match(sentence_list)

        #Matching tokens in lower case
        if project_config.lowercase_mode_on:
            answer_tokens_set = {w.lower() for w in answer_tokens_set}
            question_tokens_set = {w.lower() for w in question_tokens_set}

        common_word_count = match_question_answer(question_tokens_set, answer_tokens_set)
        match_count_weight = calculate_weight(common_word_count,lookup_score[qid][doc_id])
        heapq.heappush(h, (match_count_weight, qid, doc_id, answer))
        heapq.heappush(h2, (common_word_count, qid, doc_id, answer))

    top_twenty_tuples = heapq.nlargest(20, h);
    top_twenty_tuples_unw = heapq.nlargest(20,h2)
    top_five_answers_unw = []

    answer_list = []

    for answer_tuple in top_twenty_tuples:
        answer_token = answer_tuple[3]
        if answer_token not in answer_list:
            top_five_answers.append(answer_tuple[1:4])
            answer_list.append(answer_token)

    for answer_tuple in top_twenty_tuples_unw:
        answer_token = answer_tuple[3]
        if answer_token not in answer_list:
            top_five_answers_unw.append(answer_tuple[1:4])
            answer_list.append(answer_token)

    return top_five_answers[0:2] + top_five_answers_unw[0:3]

''' Sample run for the function in this file''
heap = find_max_matching_answer('89', "where", "where, is Gandhi?", corpus, lookup_list)
print(heap)
#'''
''' sample remove stop words : tokenized sentnece as input'''
qw = remove_stop_words( ["me", "asd", "qw"], s_words)
print(qw)
#'''
