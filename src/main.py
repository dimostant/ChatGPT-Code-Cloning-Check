import os
import json

import pandas as pd
import numpy as np
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

import ChatGBT_db.devgpt_chats as chatgpt_db
from cloning import code_cloning_check
from code_handling import extract_html_code, extract_html_text, extract_dictionary_code, remove_non_utf8_chars


def compare_questions(api_question, gpt_question):
    # print removing the \n and replacing with " " for ease
    # print("\ncomparing questions :\n", api_question.replace("\n", " "), "\nand :\n", gpt_question.replace("\n", " "))
    #
    # x_list = word_tokenize(api_question)
    # y_list = word_tokenize(gpt_question)
    #
    # sw = stopwords.words('english')
    # l1 = []
    # l2 = []
    #
    # x_set = {w for w in x_list if not w in sw}
    # y_set = {w for w in y_list if not w in sw}
    #
    # r_vector = x_set.union(y_set)
    #
    # for w in r_vector:
    #     if w in x_set:
    #         l1.append(1)
    #     else:
    #         l1.append(0)
    #     if w in y_set:
    #         l2.append(1)
    #     else:
    #         l2.append(0)
    # c = 0
    #
    # # cosine formula
    # for i in range(len(r_vector)):
    #     c += l1[i] * l2[i]
    #
    # cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    # print("similarity: ", cosine)
    #
    # return cosine
    return 0.8

def compare_answers(so_api_answers_json, gpt_conversation): #might change to answers
    gpt_answer_dictionary = chatgpt_db.get_conversation_code(gpt_conversation)
    gpt_answer_code = extract_dictionary_code(gpt_answer_dictionary)
    gpt_answer_clean_code = remove_non_utf8_chars(gpt_answer_code)
    # TODO: complete and test if "remove" function provides code safe to be compared
    # print("DevGPT code : \n", gpt_answer_clean_code)

    # TODO: check for empty DevGPT answer # test if this is done
    # remove all whitespaces
    if "".join(gpt_answer_clean_code.split()) != "":
        for so_api_answer in so_api_answers_json:
            so_api_answer_id = so_api_answer["answer_id"]
            so_api_answer_body = so_api_answer["body"]
            so_api_answer_code = extract_html_code(so_api_answer_body)
            so_api_answer_clean_code = remove_non_utf8_chars(so_api_answer_code)
            #TODO: the answer must contain code
            # print("api code: ", so_api_answer_clean_code)

            cloning_percentage = code_cloning_check(gpt_answer_clean_code, so_api_answer_clean_code) #TODO: hardcoded, change #TODO: rename?

            xl = pd.read_excel(os.path.join('..', 'results.xlsx'))
            xl.loc[len(xl)] = [
                np.nan, np.nan, np.nan, np.nan, np.nan, so_api_answer_id, so_api_answer_clean_code, ' ', gpt_answer_clean_code, cloning_percentage
            ]
            xl.to_excel(os.path.join('..', 'results.xlsx'), index=False)
           # if item.get("body"):
           #      so_api_answer_id = item["answer_id"]
           #      so_api_answer_body = item["body"]
           #      so_api_answer_code = extract_html_code(so_api_answer_body)
           #      so_api_answer_clean_code = remove_non_utf8_chars(so_api_answer_code)
           #      # print("api code: ", so_api_answer_clean_code)
           #
           #      cloning_percentage = code_cloning_check(gpt_answer_clean_code, so_api_answer_clean_code) #TODO: hardcoded, change #TODO: rename?
           #      print('ans')
           #
           #      xl = pd.read_excel(os.path.join('..', 'results.xlsx'))
           #
           #      xl.loc[len(xl)] = [
           #          np.nan, np.nan, np.nan, np.nan, np.nan, so_api_answer_id, so_api_answer_clean_code, ' ', gpt_answer_clean_code, cloning_percentage
           #      ]
           #      print('ans2')
           #      print('a :', np.nan, np.nan, np.nan, np.nan, np.nan, so_api_answer_id, so_api_answer_clean_code, ' ', gpt_answer_clean_code, cloning_percentage)
           #      row += 1
           #      xl.to_excel(os.path.join('..', 'results.xlsx'), index=False)
           #

            break

def compare_process ():
    # read all DevGPT conversations
    dev_gpt_json = chatgpt_db.get_json_data(
        'ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json'
    )

    # read all questions from db file
    with open(os.path.join('StackOverflow_api_db', 'db', 'questions.json'), 'r') as q:
        so_api_questions_json = json.load(q)

    # read all answers from db file
    with open(os.path.join('StackOverflow_api_db', 'db', 'answers.json'), 'r') as a:
        so_api_answers_json = json.load(a)

    counter1 = 0 # renove
    # iterate through every so_api question
    for so_api_question in so_api_questions_json.get("items", []):
        if so_api_question.get("body") :
            counter1 = counter1 + 1  # remove
            # print(counter1)        # remove
            counter = 0              # remove # used to choose number ( almost ) of gpt chats
            so_api_question_id = so_api_question["question_id"]
            so_api_question_body = so_api_question["body"] #TODO: improve? # for title?
            str_so_api_question = extract_html_text(so_api_question_body)
            str_so_api_clean_question = remove_non_utf8_chars(str_so_api_question)
            # print("StackOverflow question :", str_so_api_clean_question)

            # compare question with every DevGPT question
            for source in dev_gpt_json.get("Sources", []):
                for sharing_data in source.get("ChatgptSharing", []):
                    for gpt_conversation in sharing_data.get("Conversations", []):
                        if gpt_conversation :
                            counter = counter + 1 # remove
                            print(counter)        # remove
                            gpt_question = chatgpt_db.get_conversation_question(gpt_conversation)
                            str_gpt_question = chatgpt_db.json_data_to_str(gpt_question)
                            # TODO: check for empty question and others empty things like this ( i think {}) EVERYWHERE
                            # TODO: check for chinese characters e.t.c and skip question
                            # print("DevGPT        question :", str_gpt_question)

                            # TODO: define chat question index (question number, code number) => [0,1]
                            similarity = compare_questions(str_so_api_clean_question, str_gpt_question) #TODO: hardcoded, change #TODO: rename?

                            df = pd.read_excel(os.path.join('..', 'results.xlsx'))
                            df.loc[len(df)] = [
                                so_api_question_id, str_so_api_clean_question, ' ', str_gpt_question, similarity, np.nan, np.nan, np.nan, np.nan, np.nan
                            ]
                            df.to_excel(os.path.join('..', 'results.xlsx'),  index=False)

                            #TODO: could compare questions anyway and see posible similarities we didnt expect
                            # TODO: way to get rid of try? (1)
                            if 0.7 <= similarity < 1:
                                try:
                                    # TODO: does answer file need checking?
                                    # TODO: what is returned, if the id has no answers
                                    so_api_id_answers_json = []
                                    for so_api_id_answers in so_api_answers_json.get("items", []):
                                        if list(so_api_id_answers.keys())[0] == str(so_api_question_id):
                                            so_api_id_answers_json = so_api_id_answers[str(so_api_question_id)]
                                            break
                                except:
                                    continue
                                # TODO: should this throw error? (2)
                                # TODO:  and gpt_conversations[code (and answer?)]
                                if so_api_id_answers_json:
                                    compare_answers(so_api_id_answers_json, gpt_conversation)

                # inner conv increase the counter e.g. 1 2 3, 3 seen out. 4 5, 5 out. "if" checks out the loop so need >=
                if counter >= 1:        # remove
                    print("Breaaaakkk") # remove
                    break               # remove

        if counter1 >= 1:               # remove
            print("Breaaaakkk break")   # remove
            break                       # remove


# TODO: only compare with python code from DEVGPT, extra code that confirms its python code? where? ( at answer code extraction function? at data retrieval? after data retrieval? )

# TODO: to test compare questions accuracy
# TODO: identical case [questionId],[gpt_conversation]
# TODO: different case [questionId],[gpt_conversation]
# TODO: match     case [questionId],[gpt_conversation]
compare_process()

#TODO: future considerations:
    # TODO: take only the answer with the most votes
    # TODO: compare question context instead of only the title? compare answer context with chat non code response??

