from nltk.tokenize import word_tokenize
import heapq

# lookup_list = { '89' : {'when': [], 'who': [], 'where': [(0, 0, 'India'), (1, 1, 'Microsoft')]}   }
# 
# corpus ={ '89': [
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
#           }

def get_token_set(sentence):
    word_List = word_tokenize(sentence)
    return set(word_List)

def match_question_answer(question_tokens_set, answer_tokens_set):
    common_word_count = len(set.intersection(question_tokens_set, answer_tokens_set))
    return (common_word_count)

def find_max_matching_answer(qid, qtype, qtext, corpus, lookup_list):
    h = []
    question_tokens_set = get_token_set(qtext)
    qid = str(qid)
    tuple_list =  lookup_list[str(qid)][qtype.lower()]
    top_five_answers = []
    for tup in tuple_list:
        doc_id = tup[0]
        sent_id = tup[1]
        answer = tup[2]
        sentence = corpus[qid][doc_id][sent_id]
        answer_tokens_set = get_token_set(sentence)
        common_word_count = match_question_answer(question_tokens_set, answer_tokens_set)
        heapq.heappush(h, (common_word_count, qid, doc_id, answer))

    top_five_tuples = heapq.nlargest(5, h);
    for answer_tuple in top_five_tuples:
        top_five_answers.append(answer_tuple[1:4])
    return top_five_answers

''' Sample run for the function in this file''
 heap = find_max_matching_answer('89', "where", "where, is Gandhi?", corpus, lookup_list)
 print(heap)
'''