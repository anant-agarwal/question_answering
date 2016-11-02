#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 16:45:38 2016

"""
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize


def lookup_gen( corpus_per_q ):

    max_rank_check = 7

    stanford_path = "./stanford-ner-2015-12-09/"
    stanford_model_path = stanford_path + '/classifiers/english.muc.7class.distsim.crf.ser.gz'
    stanford_jar_path = stanford_path + 'stanford-ner.jar'
    st = StanfordNERTagger( stanford_model_path, stanford_jar_path)


    ner_config = {    "location": "where",
                      "person" : "who",
                      "organization": "where",
                      "date": "when",
                      "time": "when",
                      "money": "none",
                      "percent": "none",
                      'o': "none",
                  }

    lookup_list = { "who": [] , "where": [], "when":[] }

    doc_id = 0
    for doc in corpus_per_q :
        if doc_id == 0:      # This condition is to skip the empty doc in the begining
            doc_id += 1
            continue
        sent_id = 0 
        sent_len_list = []
        doc_content = []
        #get cumulative lengths of sentences in a list and club all the sentences of doc together.
        for sentence in doc:
            tokenized_sent = word_tokenize( sentence )
            try:
                previous_len = sent_len_list[-1]
            except:
                previous_len = 0
            sent_len_list += [ previous_len + len(tokenized_sent) ]
            doc_content += tokenized_sent

        #NER the whole doc at once
        doc_arr = st.tag(doc_content)

        loop_var = 0 #iterator over sent len list
        start_index = 0 #keeps track of sentence starting point
        for sentence in doc:
            last_index = sent_len_list[ loop_var ]
            classified_unicode = doc_arr[ start_index:last_index ]

            #convert unicode to string
            classified_sent = []
            for cu in classified_unicode:
                try:
                    classified_sent += [ (str(cu[0]), str(cu[1]).lower()) ]
                except:
                    print( cu[0], cu[1], "conversion to raw string failed")

            for tup in classified_sent:
                if( not ner_config[tup[1]] == "none"):
                    lookup_list[ ner_config[tup[1]] ] += [(doc_id, sent_id, tup[0])]
            sent_id += 1
            loop_var += 1
            start_index = last_index

        doc_id += 1

        if doc_id > max_rank_check:
            break;
    return( lookup_list )

''' sample run for the function in this file ''
def lookup_gen_test():                          
    corpus_per_q = [
                        [ 
                             "Gandhi is father of India.",
                             "Newton made laws of motion",
                        ],
                        [
                             "Apple makes Iphone",
                             "Hololens was made by Microsoft",
                             "Facebook has caputerd VR space"
                        ],
                        [
                             "New Macbooks are not upto the mark",
                             "Surface desktops are the new thing to look at"
                        ]
                    ]
    print( lookup_gen( corpus_per_q ) )

##sample call below
#lookup_gen_test()
'''