"""
Get the Question id,Qtype and the Question Description
"""


def QuestionProcessing(path_to_Q_file):
    questid =""
    qtype = ""
    line_split =""
    #Read the contents from question.txt
    with open(path_to_Q_file) as f:
        file_text = f.readlines()

    for line in file_text:
        line=line.strip()

        if (not line):
            continue
        line_split = line.split( )
        # Question id
        if(line_split[0] == "<num>"):
            questid =int(line_split[2])
        # Question type
        #Questiondescription
        if((line_split[0] != "<num>")and (line_split[0] !="<desc>") and(line_split[0] !="<top>") and (line_split[0]!="</top>")):
            qtype=line_split[0]
            print(questid,qtype,line)
            #FindMatchingAnswers(questid,qtype,line) //Call




#Sample call
QuestionProcessing("C:/Users/pooja/Desktop/NLP_PROJ3/question.txt")
