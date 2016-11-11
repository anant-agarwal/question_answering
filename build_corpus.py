#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 21:22:42 2016

"""
from nltk import tokenize
import file_reader
import lookup_gen
import project_config

def build_corpus(document_path):
    all_question_list = file_reader.list_all_files(document_path)
    all_question_list.sort()

    corpus = dict()
    lookup_dict = dict()
    lookup_score = dict()

    for question in all_question_list:
        q_id = str(question);
        all_doc_files = file_reader.list_all_files(document_path+q_id+"/")
        all_doc_files.sort()
        document = []
        score = []

        #
        # We do not have a document id 0
        #
        document.append([])
        score.append(0.0)

        for doc_id in all_doc_files :
            doc_id_str = str(doc_id)
            document.append([])

            text_score = file_reader.read_file_text(document_path+q_id+"/"+doc_id_str)

            split_score = text_score[0].split()
            assert(split_score[1] == q_id)
            score.append(float(split_score[5]))

            text = text_score[1].replace('\r\n', '')
            try :
                sentences = tokenize.sent_tokenize(text)
            except :
                #print every_question, doc_id
                text = text.decode("utf-8", "replace")
                sentences = tokenize.sent_tokenize(text)
            total_sentence = len(sentences)
            sentence_index = 0
            while sentence_index < total_sentence :
                document[doc_id].append(sentences[sentence_index])
                sentence_index += 1
        print "processed folder : ", question
        corpus[q_id] = document;
        lookup_score[q_id] = score
        lookup_dict[q_id] = lookup_gen.lookup_gen(corpus[q_id])
        #
        # For testing:
        #
        if (project_config.debug_mode and
            question == project_config.question_boundary) :
            break;

    return {"corpus": corpus, "lookup_dict": lookup_dict, "lookup_score": lookup_score}