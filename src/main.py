import os

import pandas as pd
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

    xl = pd.read_excel(os.path.join('..', 'results.xlsx'))
    column_names = xl.columns.tolist()

    # remove all whitespaces and check for gpt empty code
    if "".join(gpt_answer_clean_code.split()) == '""': #TODO: check?
        xl.loc[len(xl) - 1, [column_names[6]]] = [ # right prefix?
            "Error : Empty gpt_answer_clean_code"
        ]
        xl.to_excel(os.path.join('..', 'results.xlsx'), index=False)

    else :
        for so_api_answer in so_api_id_answers_json:
            so_api_answer_id = so_api_answer["answer_id"]
            so_api_answer_body = so_api_answer.get("body", [])
            if not so_api_answer_body:                                     #TODO: test
                xl.loc[len(xl) - 1, [column_names[5], column_names[6]]] = [
                    so_api_answer_id, 'Error : empty so_api_question_body'  # TODO: check
                ]
                xl.to_excel('results.xlsx', index=False)

            else :
                str_so_api_answer_code = extract_html_code(so_api_answer_body)
                str_so_api_answer_clean_code = remove_non_utf8_chars(str_so_api_answer_code)

                # remove all whitespaces check for so_api empty code
                if "".join(str_so_api_answer_clean_code.split()) == '""':
                    xl.loc[len(xl) - 1, [column_names[5], column_names[8]]] = [  # right prefix?
                        so_api_answer_id, "Error : Empty so_api_answer_clean_code"
                    ]
                    xl.to_excel(os.path.join('..', 'results.xlsx'), index=False)

                else :
                    cloning_percentage = code_cloning_check(gpt_answer_clean_code, str_so_api_answer_clean_code)
                    print(cloning_percentage)

                    xl = pd.read_excel(os.path.join('..', 'results.xlsx'))
                    column_names = xl.columns.tolist()

                    try :
                        xl.loc[len(xl) - 1, [column_names[5], column_names[6]]] = [
                            so_api_answer_id, str_so_api_answer_clean_code
                        ]
                        xl.to_excel(os.path.join('..', 'results.xlsx'), index=False)

                    except :
                        xl.loc[len(xl) - 1, [column_names[5], column_names[6]]] = [
                            so_api_answer_id, "Error :  so_api_answer_clean_code not writable"
                        ]

                        print(
                            f'Error at ->  so_api_answer_id : { so_api_answer_id} |\n'
                            + str_so_api_answer_clean_code
                        )

                    try :
                        xl.loc[len(xl) - 1, [column_names[8], column_names[9]]] = [
                            gpt_answer_clean_code, cloning_percentage
                        ]
                        xl.to_excel(os.path.join('..', 'results.xlsx'), index=False)

                    except :
                        xl.loc[len(xl) - 1, [ column_names[8], column_names[9]]] = [
                            "Error :  gpt clean question not writable", cloning_percentage
                        ]

                        print(
                            f'Error at -> gpt_conversation_num : {xl.iloc[len(xl) - 1, column_names[7]]}'
                            + '|\n' + gpt_answer_clean_code
                        )



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

    so_api_question_num = 0
    break_value = False # remove
    # iterate through every so_api question
    for so_api_question in so_api_questions_json.get("items", []):
        so_api_question_id = so_api_question["question_id"]
        so_api_question_body = so_api_question.get("body", [])

        if not so_api_question_body :
            df = pd.read_excel('results.xlsx')  # are two reads in each if optimal?
            column_names = df.columns.tolist()
            df.loc[len(df), [column_names[0], column_names[1]]] = [
                so_api_question_id, 'Error : empty so_api_question_body' #TODO: check
            ]
            df.to_excel('results.xlsx', index=False)

        else :
            so_api_question_num = so_api_question_num + 1               # remove
            gpt_conversation_num = 0
            str_so_api_question = extract_html_text(so_api_question_body)
            str_so_api_clean_question = remove_non_utf8_chars(str_so_api_question)

            # leaving this block here, compare_answers only takes this as parameter and exp calls are minimum
            if "".join(str_so_api_clean_question.split()) == '""':
                df = pd.read_excel('results.xlsx')  # are two reads in each if optimal?
                column_names = df.columns.tolist()
                df.loc[len(df), [column_names[0], column_names[1]]] = [
                    so_api_question_id, 'Error : empty so_api_question'  # TODO: check
                ]
                df.to_excel('results.xlsx', index=False)
            else:
                so_api_id_answers_json = []
                for so_api_id_answers in so_api_answers_json.get("items", []):
                    if int(list(so_api_id_answers.keys())[0]) == so_api_question_id:
                        so_api_id_answers_json = so_api_id_answers[str(so_api_question_id)]
                        break

                # if so_api_id_answers_json:                                   # TODO: test
                if not so_api_id_answers_json :
                    df = pd.read_excel('results.xlsx')  # are two reads in each if optimal?
                    column_names = df.columns.tolist()
                    df.loc[len(df), [column_names[0], column_names[1]]] = [
                        so_api_question_id, 'Error : question have no answers'  # TODO: check
                    ]
                    df.to_excel('results.xlsx', index=False)
                else :
                    # compare question with every DevGPT question
                    for source in dev_gpt_json.get("Sources", []):
                        for sharing_data in source.get("ChatgptSharing", []):
                            for gpt_conversation in sharing_data.get("Conversations", []):
                                df = pd.read_excel('results.xlsx')
                                column_names = df.columns.tolist()

                                #TODO: log gtp problems by Source/Sharing_data/conversation
                                if not gpt_conversation :
                                    df.loc[len(df), [column_names[0], column_names[1], column_names[2],
                                                     column_names[3]]] = [
                                        so_api_question_id, str_so_api_clean_question, gpt_conversation_num,
                                        "empty gpt conversation"
                                    ]
                                    df.to_excel('results.xlsx', index=False)
                                else :
                                    gpt_conversation_num = gpt_conversation_num + 1

                                    print("id : " + str(gpt_conversation_num))
                                    gpt_question = get_conversation_question(gpt_conversation)
                                    str_gpt_question = json_data_to_str(gpt_question)
                                    str_gpt_clean_question = remove_non_utf8_chars(str_gpt_question)

                                    if "".join(str_gpt_clean_question.split()) == '""':
                                        df.loc[len(df), [column_names[0], column_names[1], column_names[2], column_names[3]]] = [
                                            so_api_question_id, str_so_api_clean_question, gpt_conversation_num, "empty string gpt question"
                                        ]
                                        df.to_excel('results.xlsx', index=False)

                                    else :
                                        questions_similarity = compare_questions(str_so_api_clean_question, str_gpt_clean_question)

                                        # TODO: add excel insert data check
                                        #import unicodedata
                                        # print(repr("".join(str_gpt_clean_question.split()))) #TODO: examine
                                        # cleaned = ''.join(c for c in "".join(str_gpt_clean_question.split()) if unicodedata.category(c)[0] != 'C')
                                        # print(repr(cleaned))  # Check if it's truly empty
                                        # print(cleaned == '""')

                                        try :
                                            df.loc[len(df), [column_names[0], column_names[1]]] = [
                                                so_api_question_id, str_so_api_clean_question
                                            ]

                                            df.to_excel('results.xlsx', index=False)

                                        except :
                                            df.loc[len(df), [column_names[0], column_names[1]]] = [
                                                so_api_question_num, "Error :  so_api_question not writable"
                                            ]
                                            df.to_excel('results.xlsx', index=False)

                                            print(
                                                f'Error at -> so_api_question_num : {so_api_question_num} |\n'
                                                  + str_so_api_clean_question
                                            )

                                        try :
                                            df.loc[len(df) - 1, [column_names[2], column_names[3], column_names[4], column_names[7]]] = [
                                                gpt_conversation_num, str_gpt_clean_question, questions_similarity, gpt_conversation_num
                                            ]
                                            df.to_excel('results.xlsx', index=False)

                                            if 0.7 <= questions_similarity < 1:
                                                gpt_answer_dictionary = get_conversation_code(gpt_conversation)
                                                if gpt_answer_dictionary:                           # TODO: test
                                                    compare_answers(so_api_id_answers_json, gpt_answer_dictionary)

                                        except:

                                            df.loc[len(df) - 1, [column_names[2], column_names[3]]] = [
                                                gpt_conversation_num, "Error :  gpt clean question not writable"
                                            ]
                                            df.to_excel('results.xlsx',  index=False)

                                            print(
                                                f'Error at -> gpt_conversation_num : {gpt_conversation_num}'
                                                  + '|\n' + str_gpt_clean_question
                                            )

                        # inner conv increase the counter e.g. 1 2 3, 3 seen out. 4 5, 5 out. "if" checks out the loop so need >=
                        if gpt_conversation_num >= 17 or break_value is True: #9:        # remove
                            print("Break1")     # remove
                            break               # remove

        if so_api_question_num >= 1:              # remove
            print("break2")             # remove
            break                       # remove
        # break

## UNCOMMENT THIS!!!
# if os.path.basename(os.path.normpath(os.getcwd())) == 'src':
#     os.chdir('..')
os.remove('results.xlsx')
os.popen("copy " + str('resultsC.xlsx') + " " + str('results.xlsx'))
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
#  check for comparison question or answer errors that go unnoticed in excel. eg. cloning percnetage missing


#TODO: future considerations:
#  take only the answer with the most votes
#  compare question context instead of only the title? compare answer context with chat non code response??