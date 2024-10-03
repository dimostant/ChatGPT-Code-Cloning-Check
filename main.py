import ChatGBT_db.devgpt_chats as chatgpt_db
#from so_api import get_api_questions, get_api_answers  #change to importing the entire file?

from cloning import code_cloning_check
from code_handling import extract_html_code, extract_html_text, extract_dictionary_code, remove_non_utf8_chars

import ast
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def compare_questions(api_question, gpt_question):
    # must also test
    # print removing the \n and replacing with " " for ease
    print("\ncomparing questions :\n", api_question.replace("\n", " "), "\nand :\n", gpt_question.replace("\n", " "))

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
    # TODO: improve so the code that filters the data doesnt happen unnecessarily
    gpt_answer_dictionary = chatgpt_db.get_conversation_code(gpt_conversation)
    gpt_answer_code = extract_dictionary_code(gpt_answer_dictionary)
    gpt_answer_clean_code = remove_non_utf8_chars(gpt_answer_code)
    # print("DevGPT code : \n", gpt_answer_clean_code)

    if "".join(gpt_answer_clean_code.split()) != "": #removes all whitespaces
        # TODO: ADD SLEEP SO YOU DONT HIT THE THROTTLE AGAIN

        # only for testing
        answers_path = 'so_api_answers.json'
        so_api_answers_json = chatgpt_db.get_json_data(answers_path)

        # so_api_answers_json = get_api_answers(so_question_id) #put this out of the function?
        # TODO: take only the one with the most votes

        for item in so_api_answers_json.get('items', []) or []:
           if item.get("body"):
                so_api_answer_body = item["body"]
                so_api_answer_code = extract_html_code(so_api_answer_body)
                so_api_answer_clean_code = remove_non_utf8_chars(so_api_answer_code)
                # print("api code: ", so_api_answer_clean_code)

                code_cloning_check(gpt_answer_clean_code, so_api_answer_clean_code)
                # compare answer context?
                # TODO: needs a function that cleans the string of irrelevant to the code text that is left over
                # TODO: if (answerA code for cloning answerB) print("cloning")
                # TODO: ramp of how much the code matches, 1 to 0.7/ 0.69 to 0.3/ 0.29 to 0 and categorize, where will this be stored?
                # TODO: cloning Code comparison and result extraction, then store the results in CSV or JSON and in what structure


# invent a function that can detect the kind of question, and get the appropriate answers e.t.c accordingly
def compare_process (so_question_id, dev_gpt_data):
    # only for testing
    questions_path = 'so_api_questions.json'
    so_api_questions_json = chatgpt_db.get_json_data(questions_path)

    # so_api_questions_json = get_api_questions(so_question_id)
    #TODO: ADD SLEEP SO YOU DONT HIT THE THROTTLE AGAIN

    for item in so_api_questions_json.get("items", []) or []:
        # TODO: consider title, should the contexts of the questions even be checked before comparing code??
        if item.get("body") :
            so_api_question_body = item["body"] #improve? # for title?
            str_so_api_question = extract_html_text(so_api_question_body) #test if this is right
            str_so_api_clean_question = remove_non_utf8_chars(str_so_api_question)
            # print("StackOverflow question :", str_so_api_clean_question)

            counter = 0 #delete after testing

            #TODO: check for empty boxes everywhere
            for source in dev_gpt_data.get("Sources", []) or []: #will not iterate if empty
                for sharing_data in source.get("ChatgptSharing", []) or []:
                    for gpt_conversation in sharing_data.get("Conversations", []) or []:
                        if gpt_conversation :
                            gpt_question = chatgpt_db.get_conversation_question(gpt_conversation)
                            # TODO: check for empty question and others emtys like this
                            str_gpt_question = chatgpt_db.json_data_to_str(gpt_question)
                            # TODO:check for chinese characters e.t.c and skip question #filter for python
                            # print("DevGPT        question :", str_gpt_question)

                            counter = counter + 1
                            print(counter)

                            similarity = compare_questions(str_so_api_clean_question, str_gpt_question)

                            similarity = 0.8
                            if similarity == 1:
                                print("identical questions\n")
                                # is that right?

                            elif 0.7 <= similarity < 1:
                                # print("similar questions, checking...\n")
                                compare_answers(so_question_id, gpt_conversation)

                            else:
                                print("different questions\n")

                #  inner conv increase the counter e.g. 1 2 3, 3 seen out. 4 5, 5 out.
                # "if" checks out the loop so need <=
                if counter >= 4: break




#inputs #must be arr #[79018992]
question_id = [59325633]

#get data from DevGPT
dev_gpt_json = chatgpt_db.get_json_data('ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json') # optimize db interface? #just use json.dumps

compare_process(question_id, dev_gpt_json)

# TODO: traverse through all stackoverflow questions before [chatGPT releaseDate] by finding the last question id of that date or the date, any implications?
# TODO: get them e.g. 100 by 100 to optimize the process, maybe 50? do optimal call of the api
# TODO: filter the question from the coding language tags, must be e.g. Python
# TODO: extra code that confirms its python

# TODO: identical case [questionId],[gpt_conversation]
# TODO: different case [questionId],[gpt_conversation]
# TODO: match     case [questionId],[gpt_conversation]

# TODO: HOW TO DO THE TESTING??