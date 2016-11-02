#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 16:45:38 2016

@author: anant
"""
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize


def lookup_gen( corpus_per_q ):
    
    max_rank_check = 2

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
    for sentences in corpus_per_q :
        if doc_id == 0:
            doc_id += 1
            continue
        sent_id = 0 
        for sentence in sentences:
            tokenized_sent = word_tokenize( sentence )
            classified_unicode = st.tag( tokenized_sent )
            #convert unicode to string
            classified_sent = [ (str(cu[0]), str(cu[1]).lower()) for cu in classified_unicode ]
            for tup in classified_sent:
                if( not ner_config[tup[1]] == "none"):
                    lookup_list[ ner_config[tup[1]] ] += [(doc_id, sent_id, tup[0])]
            sent_id += 1
        print "NER tagging for: ", doc_id
        doc_id += 1
        if doc_id == max_rank_check:
            break;
    return( lookup_list )


def lookup_gen_test():                          
    corpus_per_q = [
                        [ 
                             "Gandhi is father of India",
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


##### to be relocated later###
#### function to write to answer.txt file:###
def write_to_answer_file( file_handle, answers):
    content = ""
    count = 0;
    for ans in answers:
        content += str(ans[0]) +" "+ str(ans[1]) + " " + ans[2] + "\n"
        count += 1

    while( count < 5 ):
        content += str(answers[0][0]) + "1 nil\n"
    file_handle.write( content )
