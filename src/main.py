import os
from distutils.dir_util import remove_tree

import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from ChatGBT_db.devgpt_chats import get_json_data, get_conversation_code, get_conversation_question, json_data_to_str
from code_handling import extract_html_code, extract_html_text, extract_dictionary_code, remove_non_utf8_chars, code_cloning_check

def compare_questions(api_question, gpt_question):                                                         #TODO: test
    #remove the \n and replacing with " " for ease
    #print("\n comparing questions :\n", api_question.replace("\n", " "), "\nand :\n", gpt_question.replace("\n", " "))

    x_list = word_tokenize(api_question)
    y_list = word_tokenize(gpt_question)

    sw = stopwords.words('english')
    l1 = []
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
    # print("similarity: ", cosine)

    return cosine

def compare_answers(so_api_id_answers_json, gpt_answer_dictionary): #might change to answers
    # TODO: complete and test if "remove" function provides code safe to be compared
    gpt_answer_code = extract_dictionary_code(gpt_answer_dictionary)
    gpt_answer_clean_code = remove_non_utf8_chars(gpt_answer_code)

    # remove all whitespaces and check for gpt empty code
    if "".join(gpt_answer_clean_code.split()) != "":
        for so_api_answer in so_api_id_answers_json:
            so_api_answer_body = so_api_answer.get("body", [])
            if so_api_answer_body:                                     #TODO: test
                so_api_answer_id = so_api_answer["answer_id"]
                so_api_answer_code = extract_html_code(so_api_answer_body)
                so_api_answer_clean_code = remove_non_utf8_chars(so_api_answer_code)

                # remove all whitespaces check for so_api empty code
                if "".join(so_api_answer_clean_code.split()) != "":
                    cloning_percentage = code_cloning_check(gpt_answer_clean_code, so_api_answer_clean_code)
                    print(cloning_percentage)

                    xl = pd.read_excel(os.path.join('..', 'results.xlsx'))
                    column_names = xl.columns.tolist()
                    try :
                        xl.loc[len(xl) - 1 if len(xl) > 0 else len(xl), [column_names[5], column_names[6], column_names[8], column_names[9]]] = [
                            so_api_answer_id, so_api_answer_clean_code, gpt_answer_clean_code, cloning_percentage
                        ]
                        xl.to_excel(os.path.join('..', 'results.xlsx'), index=False)
                        return True
                    except :
                        print("Error Answers")
                        return False


def compare_process ():
    # read all DevGPT conversations
    dev_gpt_json = get_json_data(
        'ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json'
    )

    # read all questions from db file
    so_api_questions_json = get_json_data(
        os.path.join('StackOverflow_api_db', 'db', 'questions.json')
    )

    # read all answers from db file
    so_api_answers_json = get_json_data(
        os.path.join('StackOverflow_api_db', 'db', 'answers.json')
    )

    so_api_question_num = 0                        # remove
    # iterate through every so_api question
    for so_api_question in so_api_questions_json.get("items", []):
        so_api_question_body = so_api_question.get("body", [])
        if so_api_question_body :
            so_api_question_num += 1               # remove
            gtp_conversation_num = 0
            so_api_question_id = so_api_question["question_id"]
            str_so_api_question = extract_html_text(so_api_question_body)
            str_so_api_clean_question = remove_non_utf8_chars(str_so_api_question)

            # leaving this here compare_answers only takes this as parameter and exp calls are minimum
            if "".join(str_so_api_clean_question.split()) != "":
                so_api_id_answers_json = []
                for so_api_id_answers in so_api_answers_json.get("items", []):
                    if int(list(so_api_id_answers.keys())[0]) == so_api_question_id:
                        so_api_id_answers_json = so_api_id_answers[str(so_api_question_id)]
                        break

                if so_api_id_answers_json:                                   # TODO: test
                    # compare question with every DevGPT question
                    for source in dev_gpt_json.get("Sources", []):
                        for sharing_data in source.get("ChatgptSharing", []):
                            for gpt_conversation in sharing_data.get("Conversations", []):
                                if gpt_conversation :
                                    gtp_conversation_num += gtp_conversation_num
                                    print(gtp_conversation_num)        # remove
                                    gpt_question = get_conversation_question(gpt_conversation)
                                    str_gpt_question = json_data_to_str(gpt_question)
                                    str_gpt_clean_question = remove_non_utf8_chars(str_gpt_question)

                                    if "".join(str_gpt_clean_question.split()) != "":
                                        questions_similarity = compare_questions(str_so_api_clean_question, str_gpt_clean_question)

                                        df = pd.read_excel(os.path.join('..', 'results.xlsx'))
                                        try:
                                            df.loc[len(df)] = [
                                                so_api_question_id, str_so_api_clean_question, gtp_conversation_num, str_gpt_clean_question, questions_similarity, np.nan, np.nan, gtp_conversation_num, np.nan, np.nan
                                            ]

                                            df.to_excel(os.path.join('..', 'results.xlsx'), index=False)

                                            if 0.7 <= questions_similarity < 1:
                                                gpt_answer_dictionary = get_conversation_code(gpt_conversation)
                                                if gpt_answer_dictionary:                           # TODO: test
                                                    compare_answers(so_api_id_answers_json, gpt_answer_dictionary)
                                                    # answer_comparison = compare_answers(so_api_id_answers_json, gpt_answer_dictionary)
                                                    # if not answer_comparison :
                                                        # xl.loc[len(xl) - 1 if len(xl) > 0 else len(xl), [column_names[5], column_names[6], column_names[8], column_names[9]]] = [
                                                        #     str(so_api_question_num) + " " + str(gtp_conversation_num) + "Error"
                                                        # ]
                                                        #
                                                        # xl.to_excel(os.path.join('..', 'results.xlsx'), index=False)

                                        except:
                                            df.loc[len(df), 0] = [
                                                str(so_api_question_num) + " " + str(gtp_conversation_num) + "Error"
                                            ]
                                            print("Error")

                                            df.to_excel(os.path.join('..', 'results.xlsx'),  index=False)

                        # inner conv increase the counter e.g. 1 2 3, 3 seen out. 4 5, 5 out. "if" checks out the loop so need >=
                        # if gpt_conversation_num >= 1:        # remove
                        #     print("Break1")     # remove
                        #     break               # remove

                if so_api_question_num >= 10:              # remove
                    print("break2")             # remove
                    break                       # remove

## UNCOMMENT THIS!!!
# if os.path.basename(os.path.normpath(os.getcwd())) == 'src':
#     os.chdir('..')
compare_process()

# TODO: check for empty question and others empty things like this ( i think {}) EVERYWHERE
#  refactor json functions
#  check for chinese characters e.t.c and skip question #is the solution above proper?
#  does all_answers file need checking before used above?
#  should all answers be returned in items after db_builder : yes?
#  why are answers unordered? fix
#  only compare with python code from DevGPT, extra code that confirms its python code? where? ( at answer code extraction function? at data retrieval? after data retrieval? )
#  should answer comparison of < 0.7 be ignored?
#  should question line in excel appear with the answers



#TODO: future considerations:
#  take only the answer with the most votes
#  compare question context instead of only the title? compare answer context with chat non code response??