#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 20:44:31 2016

"""
import build_corpus
import question_process

#
# User should enter the directory path having 'train' folder.
#
input_path_is_correct = 1;
path = "/Users/Deekshith/Desktop/Cornell/2_NLP/assignment_3/"

#
# folders : 89 to 320
# within each folder : 1 to 100
# 103 for test -- first when question id.
#
document_path = path+"documents/"

while (not input_path_is_correct) :
    path = input("\nInput path to train folder:")
    final_path = path + "train/"
    print("\nWill start reading at:", final_path, "\n");
    confirm = input("If that's right enter yes else no: ");
    if (confirm.lower() =="yes") :
        input_path_is_correct = 1

preprocessed_data = build_corpus.build_corpus(document_path)

question_process.question_processing(path+"question_answering/", preprocessed_data)

#print preprocessed_data["lookup_dict"]
