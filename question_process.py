"""
Get the Question id,Qtype and the Question Description
"""
import matchingAnswer
import lookup_gen

def QuestionProcessing(path, preprocessed_data):
    questid =""
    qtype = ""
    line_split =""
    #Read the contents from question.txt
    path_to_Q_file = path+"question.txt"
    answer_file = path+"answer.txt"

    write_handle = open(answer_file, "w")
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
        if((line_split[0] != "<num>")and (line_split[0] !="<desc>") and
           (line_split[0] !="<top>") and (line_split[0]!="</top>")):
            qtype=line_split[0]
            print(questid,qtype,line)
            print "finding answers for questid: ", questid
            if qtype.startswith('Where'):
                qtype = 'Where'
            if qtype.startswith('Who'):
                qtype = 'Who'
            if qtype.startswith('When'):
                qtype = 'When'

            answers = matchingAnswer.FindMaxMatchingAnswer(questid, qtype,line,
                                                           preprocessed_data["corpus"],
                                                           preprocessed_data["lookup_dict"])
            #print questid
            #print answers
            lookup_gen.write_to_answer_file(write_handle, answers)
    write_handle.close()

#Sample call
#QuestionProcessing("C:/Users/pooja/Desktop/NLP_PROJ3/question.txt")
