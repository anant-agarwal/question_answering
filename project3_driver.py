#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 20:44:31 2016

"""
import build_corpus
import question_process

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

preprocessed_data = build_corpus.build_corpus(document_path)

question_process.question_processing(path, preprocessed_data)
