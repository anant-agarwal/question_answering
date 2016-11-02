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
    for doc in corpus_per_q :
        if doc_id == 0:
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
            classified_sent = [ (str(cu[0]), str(cu[1]).lower()) for cu in classified_unicode ]
            for tup in classified_sent:
                if( not ner_config[tup[1]] == "none"):
                    lookup_list[ ner_config[tup[1]] ] += [(doc_id, sent_id, tup[0])]
            sent_id += 1
            loop_var += 1
            start_index = last_index

        #print "NER tagging for: ", doc_id
        doc_id += 1

        if doc_id > max_rank_check:
            break;
        #print("done")
    return( lookup_list )


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
    #test_set = "Bratislava--By 2 May 1994, the Slovak Government will submit to the International Court of Justice in The Hague the `Memorandum of the Slovak Republic on the Gabcikovo-Nagymaros Hydroelectric Power Project.' We expect the document to consist of 2,000-2,500 pages, Jan Lisuch, state secretary at the Ministry of Foreign Affairs, told yesterday's meeting of the National Council of the Slovak Republic [NRSR] Commission for Issues of the Danube Hydroelectric Projects. The state secretary also briefed the NRSR commission on findings acquired thus far about the impact of the Gabcikovo hydroelectric project on the level of underground water in Zitny Ostrov [Rye Island, area along the Danube in southern Slovakia], on water supply in the system of Danube branches, and on improving navigation on the Danube. [passage omitted]  At their meeting yesterday, members of the NRSR commission also discussed a reply to a letter from Andras Pap, chairman of the Hungarian Parliament's committee dealing with the hydroelectric project. The reply states that the solution to the problem of a sufficient amount of water in the Danube branches [on Hungarian territory] lies in the mutually agreed construction of a dam at Dunakiliti. This would make it possible to supply the network of branches in the Szigetkoz area with up to 140 cubic meters of water per second. Academician Juraj Hrasko, chairman of the NRSR commission, stressed that the flow in the old river bed [of the Danube] could be increased after the completion of an automatic water diversion system at a newly built small hydroelectric power plant [at Dunakiliti]. This pledge [to increase flow in the old riverbed] would mean a reduction in the production of electricity in Gabcikovo by about 28 million kilowatt-hours annually, which would extend the period necessary for the investment costs to be recouped. On no account will the Slovak side consider this temporary solution to be a retreat from positions during the discussion of the Slovak-Hungarian dispute before the International Court of Justice in The Hague. The failure to implement solutions, the blueprints of which are ready and agreement on which had already been reached, runs counter to our common interest in the creation of optimal conditions for the ecological system of Danube wetland forests, the reply from the NRSR commission to Andras Pap's letter states."
    #test_set = test_set.split(".")
    #corpus_per_q += [test_set]
    #st_tags = st.tag(test_set)

    #print( lookup_gen( corpus_per_q ) )

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
        count += 1
    file_handle.write( content )
