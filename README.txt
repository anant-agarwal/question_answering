

How to run the code :
=====================

— Run assignment3_driver.py [We have used ‘Anaconda’ with ’Spyder’ IDE for the development (python 2.7)]
- Download Stanford NER tagger from http://nlp.stanford.edu/software/stanford-ner-2015-12-09.zip
- Unzip the above and keep it next to the code files, so that ./stanford-ner-2015-12-09/ exits for the code.


Console Output :
================
Input path to the parent folder of doc_dev: "/Users/Deekshith/Desktop/Cornell/2_NLP/assignment_3/question_answering/"

Will start reading at: /Users/Deekshith/Desktop/Cornell/2_NLP/assignment_3/question_answering/doc_dev/

If that's right enter yes else no: "yes"
processed folder :  89
processed folder :  90
processed folder :  91
...
...

Code Organization :
===================

We have created following modules to do required tasks in this project.

1) project3_driver.py
	Driver module for the entire project. Imports other modules to do required tasks.

2) build_corpus.py
	Module which reads all the documents for every question and builds two datastructures.
	1) lookup_gen, a dictionary which stores hints for every question.
	2) corpus : reads all the documents corresponding to each question and store the sentences.

3) lookup_gen.py
        Generates a lookup_gen table for each question, by doing NER tagging on each sentence for all the documents belonging to a question.

4) question_processing.py
	Reads question.txt and for every question, this module will invoke the answer finding module.

5) matchingAnswers.py
	Takes question number, question type and question as a parameter and looks into lookup_gen datastructure for hints. After finding the tuples with hints, loads the
	correspdong sentences from corpus datastructure and finds the best five answers.

6) filereader.py
	APIs for file level operations like read, write.
