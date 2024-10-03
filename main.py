from cloning import code_cloning_check
from code_handling import extract_html_code, extract_html_text, extract_dictionary_code, remove_non_utf8_chars
import ChatGBT_db.devgpt_chats as chatgpt_db
#from so_api import get_api_questions, get_api_answers  #change to importing the entire file?
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import ast

def compare_questions(api_question, gpt_question):
    #print removing the \n and replacing with " " for ease
    #print("\ncomparing questions :\n", api_question.replace("\n", " "), "\nand :\n", gpt_question.replace("\n", " "))

    x_list = word_tokenize(api_question)
    y_list = word_tokenize(gpt_question)

    sw = stopwords.words('english')
    l1 = []#;
    l2 = []

    x_set = {w for w in x_list if not w in sw}
    y_set = {w for w in y_list if not w in sw}

    r_vector = x_set.union(y_set)

    for w in r_vector:
        if w in x_set:
            l1.append(1)
        else:
            l1.append(0)
        if w in y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(r_vector)):
        c += l1[i] * l2[i]

    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    print("similarity: ", cosine)

    return cosine

def compare_answers(so_question_id, gpt_conversation): #might change to answers
    gpt_answer_dictionary = chatgpt_db.get_conversation_code(gpt_conversation)
    gpt_answer_code = extract_dictionary_code(gpt_answer_dictionary)
    gpt_answer_clean_code = remove_non_utf8_chars(gpt_answer_code)
    #print("DevGPT code : \n", get_answer_clean_code)
    #print(gpt_answer_clean_code)
    # needs a function that cleans the string of irrelevant to the code text that is left over

    # insert code to abstract syntax tree (python code only!)
    #tree2 = ast.parse(gpt_answer_clean_code)

    #print("so api code \n")
    #answer MUST contain code, or ignored
    # must be Python
    # TODO: ADD SLEEP SO YOU DONT HIT THE THROTTLE AGAIN

    #only for testing
    answers_path = 'so_api_answers.json'
    so_api_answers_json = chatgpt_db.get_json_data(answers_path)

    #travers through api received answers of a question, TODO: take only the one with the most votes
    # so_api_answers_json = get_api_answers(so_question_id) #put this out of the function?

    for item in so_api_answers_json.get('items', []):
        so_api_answer_body = item["body"]
        if so_api_answer_body is not None:
            so_api_answer_code = extract_html_code(so_api_answer_body)
            so_api_answer_clean_code = remove_non_utf8_chars(so_api_answer_code)
            #print("api code: ", so_api_answer_clean_code)

            code_cloning_check(gpt_answer_clean_code, so_api_answer_clean_code)

    # compare answer context?
    # needs a function that cleans the string of irrelevant to the code text that is left over
    # insert code to abstract syntax tree (python code only!)
    # tree1 = ast.parse(extracted_so_api_code)



    #if (answerA code for cloning answerB) print("cloning")
    #ramp of how much the code matches, 1 to 0.7/ 0.69 to 0.3/ 0.29 to 0 and categorize, where will this be stored?
    #cloning Code comparison and result extraction, then saved somewhere

#invent a function that can detect the kind of question, and get the appropriate answers e.t.c accordingly
def compare_process (so_question_id, dev_gpt_data):
    #only for testing
    questions_path = 'so_api_questions.json'
    so_api_questions_json = chatgpt_db.get_json_data(questions_path)

    # so_api_questions_json = get_api_questions(so_question_id)  # make json handler?
    #TODO: ADD SLEEP SO YOU DONT HIT THE THROTTLE AGAIN

    for item in so_api_questions_json.get("items", []):
        #print(item)
        #consider title, should the contexts of the questions even be checked before comparing code??
        so_api_question_body = item["body"] #improve?
        # for title?
        str_so_api_question = extract_html_text(so_api_question_body) #test if this is right
        str_so_api_clean_question = remove_non_utf8_chars(str_so_api_question)
        #print("StackOverflow question :", str_so_api_clean_question)

        counter = 0 #delete after testing

        #TODO: check for empty boxes everywhere
        for source in dev_gpt_data.get("Sources", []):
            for sharing_data in source.get("ChatgptSharing", []):
                for gpt_conversation in sharing_data.get("Conversations", []): #is this safe if no conversation exists? #this index will always be 0 should I remove? # this is for safety
                    gpt_question = chatgpt_db.get_conversation_question(gpt_conversation)
                    str_gpt_question = chatgpt_db.json_data_to_str(gpt_question)
                    #check for chinese characters and skip question
                    #print("DevGPT        question :", str_gpt_question)

                    counter = counter + 1
                    #print(counter)
                    #filter for python

                    similarity = compare_questions(str_so_api_clean_question, str_gpt_question)

                    similarity = 0.8
                    if similarity == 1:
                        print("identical questions\n")
                        #ignore #is that right?

                    elif 0.7 <= similarity < 1:
                        #print("similar questions, checking...\n")
                        compare_answers(so_question_id, gpt_conversation)

                    else:
                        print("different questions\n")
            #  inner conv increase the counter e.g. 1 2 3, 3 seen out. 4 5, 5 out.
            # "if" checks out the loop so need <=
            if counter >= 3: break


#inputs
question_id = [59325633] #[79018992] #must be arr
user = 1

#get data from DevGPT
path = 'ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json'
dev_gpt_data = chatgpt_db.get_json_data(path) # optimize db interface? #just use json.dumps

compare_process(question_id, dev_gpt_data)

#whatever handles SO data needs to remove html artifacts
#figure out in what sequence to get DevGPT questions and StackOverflow api questions
#check date of stackoverflow data to be before the release of ChatGPT
#filter for what programming the question is about, maybe use the tags from stackoverflow and the answer too for both
#is there a use for the text of the answers?
#include question and answers comments
# method get All questions and filter by date e.t.c.
# method while so_api_question date < chatGPT release date ???:
# method for i = 0 ; i <= id_last post before chatGPT release
#traverse through all stackoverflow questions before [chatGPT releaseDate] by finding the last question id of that date or the date, any implications?
#get them e.g. 100 by 100 to optimize the process, maybe 50? do optimal call of the api
#question not empty
#filter the question from the coding language tags, must be e.g. Python
#extra code that confirms its python
#remove non utf8 from json

# gpt_conversation = ""

# for source in DevGPT_data.get("Sources", []):
#     chatgpt_sharing = source.get("ChatgptSharing", [])
#     for sharing_data in chatgpt_sharing: #this index will always be 0 should I remove? # this is for safety
#         conversations = sharing_data.get("Conversations", [])
#         for conversation in conversations: #is this safe if no conversation exists?
#             gpt_conversation = conversation
#             chatgpt_db.print_json_data(conversation)
#             #filter for python


#compare so_api_questions argument, gpt_question


#identical case [questionId],[gpt_conversation]
#different case [questionId],[gpt_conversation]
#match     case [questionId],[gpt_conversation]

#store the results in CSV or JSON and in what structure
#HOW TO DO THE TESTING??