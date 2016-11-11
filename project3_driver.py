#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 20:44:31 2016

"""
import build_corpus
import question_process
import project_config

#
# Folder path entered below should contain doc_dev.7z and question.txt files
# doc_dev.7z should be unzipped and copied to the folder doc_dev in the same path
#

input_path_is_correct = 0;

while (not input_path_is_correct) :
    #
    # Enter the path where doc_dev is present.
    #
    path = input("\nInput path to the parent folder of doc_dev: ")
    document_path = path+"doc_dev/"
    print "\nWill start reading at:", document_path, "\n";
    confirm = input("If that's right enter yes else no: ");
    if (confirm.lower() =="yes") :
        input_path_is_correct = 1

#
# Unzipped content is stored in documents folder
#

#preprocessed_data = build_corpus.build_corpus(document_path)
while True:
    input_value = input("\nEnter the doc score : ")
    project_config.doc_score_weight = float(input_value)

    input_value = input("\nEnter the max rank check folder count : ")
    project_config.max_rank_check = int(input_value)

    input_value = input("\n Lower case mode on? (1/0) : ")
    project_config.lowercase_mode_on = int(input_value)

    input_value = input("\nEnter context span value (1-n): ")
    project_config.context_span = int(input_value)

    question_process.question_processing(path, preprocessed_data)

    print "max_rank_check: ", project_config.max_rank_check
    print "doc score weight: ", project_config.doc_score_weight
    print "lower case mode: ", project_config.lowercase_mode_on
    print "context span: ", project_config.context_span
    print "stemming: 1"
