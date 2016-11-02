"""
Get the Question id,Qtype and the Question Description
"""
import matchingAnswer
import lookup_gen

def question_processing(path, preprocessed_data):
    questid =""
    qtype = ""
    line_split =""
    last_processed_question = 88;
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

            if (questid != last_processed_question + 1) :
                print "Fix this"
                assert 0

            answers = matchingAnswer.find_max_matching_answer(questid, qtype,line,
                                                              preprocessed_data["corpus"],
                                                              preprocessed_data["lookup_dict"])
            #print questid
            #print answers
            lookup_gen.write_to_answer_file(questid, write_handle, answers)
            
            last_processed_question = questid
            #
            # for testing, better write a config file soon
            #
            #if questid == 95:
            #    break;
    write_handle.close()

#Sample call
#question_processing("C:/Users/pooja/Desktop/NLP_PROJ3/question.txt")
