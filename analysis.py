#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 19:09:04 2016

@author: anant
"""

eval_op  = open("eval_op.txt", 'r')

correct = []
incorrect = []
for line in eval_op:
    if( line.startswith("Correct ") ):
        line_split = line.split()
        correct += [ line_split[1] ]
    if( line.startswith("Incorrect ") ):
        line_split = line.split()
        incorrect += [ line_split[1] ]


ques_file = open("question.txt", 'r')

q_dict = {}

for line in ques_file:
    line = line.strip()
    if(not line):
        continue
    
    line_split = line.split( )
    if(line_split[0] == "<num>"):
        questid =line_split[2]

    if((line_split[0] != "<num>")and (line_split[0] !="<desc>") and
       (line_split[0] !="<top>") and (line_split[0]!="</top>")):
        qtype=line_split[0]
        if qtype.startswith('Where'):
            qtype = 'Where'
        if qtype.startswith('Who'):
            qtype = 'Who'
        if qtype.startswith('When'):
            qtype = 'When'
        q_dict[questid] = qtype

q_classification = {"Where": { "correct": [], "incorrect":[] }, "Who": { "correct": [], "incorrect":[] } , "When": { "correct": [], "incorrect":[] }}

for q in correct:
    q_classification[ q_dict[q]]["correct"] += [q]
for q_id in incorrect:
    if( q_id == "1241"):
        q_id = '124'
    if( q_id == "1471"):
        q_id = '147'    
    q_classification[ q_dict[q_id]]["incorrect"] += [q_id]

