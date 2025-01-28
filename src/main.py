import os

import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer

from ChatGBT_db.devgpt_chats import get_json_data, get_conversation_code, get_conversation_question, json_data_to_str
from code_handling import extract_html_code, extract_html_text, extract_dictionary_code, clean_text, code_cloning_check

STOPWORDS = stopwords.words('english')

def preprocess_question(question):
    """Tokenizes and removes stopwords from a question."""
    return [word.lower() for word in word_tokenize(question) if word.lower() not in STOPWORDS]

def compare_questions(api_question, gpt_question):
    """Calculates cosine similarity between two preprocessed questions."""
    # Preprocess questions
    api_tokens = preprocess_question(api_question)
    gpt_tokens = preprocess_question(gpt_question)

    # Use CountVectorizer to compute word frequency vectors
    vectorizer = CountVectorizer(analyzer=lambda x: x)
    vectors = vectorizer.fit_transform([api_tokens, gpt_tokens]).toarray()

    # Calculate cosine similarity
    numerator = np.dot(vectors[0], vectors[1])
    denominator = np.linalg.norm(vectors[0]) * np.linalg.norm(vectors[1])

    # Return cosine similarity, handle zero-vector edge case
    return numerator / denominator if denominator != 0 else 0.0


def compare_answers(so_api_id_answers_json, gpt_answer_dictionary, df, column_names): #might change to answers
    gpt_answer_clean_code = clean_text(extract_dictionary_code(gpt_answer_dictionary))

    # remove all whitespaces and check for gpt empty code
    if "".join(gpt_answer_clean_code.split()) == '""':
        df.loc[len(df) - 1, [column_names[6]]] = ["Error : Empty gpt_answer_clean_code"]            # TODO: check? # right prefix?
        return

    for so_api_answer in so_api_id_answers_json:
        so_api_answer_id = so_api_answer.get("answer_id", [])
        so_api_answer_body = so_api_answer.get("body", [])
        if not so_api_answer_body:                                                              # TODO: test
            df.loc[len(df) - 1, [column_names[5], column_names[6]]] = \
                [so_api_answer_id, 'Error : empty so_api_question_body']                         # TODO: check
            continue

        str_so_api_answer_clean_code = clean_text(extract_html_code(so_api_answer_body))

        # remove all whitespaces check for so_api empty code
        if "".join(str_so_api_answer_clean_code.split()) == '""':
            df.loc[len(df) - 1, [column_names[5], column_names[8]]] = \
                [so_api_answer_id, "Error : Empty so_api_answer_clean_code"] # right prefix?
            continue

        cloning_percentage = code_cloning_check(gpt_answer_clean_code, str_so_api_answer_clean_code)

        df.loc[len(df) - 1, [column_names[5], column_names[6], column_names[8], column_names[9]]] = \
            [so_api_answer_id, str_so_api_answer_clean_code, gpt_answer_clean_code, cloning_percentage]

        # try :
        #     xl.loc[len(xl) - 1, [column_names[5], column_names[6]]] = [so_api_answer_id, str_so_api_answer_clean_code]

        # except Exception as e:
        #     xl.loc[len(xl) - 1, [column_names[5], column_names[6]]] = [so_api_answer_id, "Error :  so_api_answer_clean_code not writable"]
        #
        #     print(
        #         f'Exception : {e} \nError at ->  so_api_answer_id : { so_api_answer_id} |\n'
        #         + str_so_api_answer_clean_code
        #     )

        # try :
        #     xl.loc[len(xl) - 1, [column_names[8], column_names[9]]] = [gpt_answer_clean_code, cloning_percentage]

        # except Exception as e:
        #     xl.loc[len(xl) - 1, [ column_names[8], column_names[9]]] = ["Error :  gpt clean question not writable", cloning_percentage]
        #
        #     print(
        #         f'Exception : {e} \nError at -> gpt_conversation_num : {xl.iloc[len(xl) - 1, column_names[7]]}'
        #         + '|\n' + gpt_answer_clean_code
        #     )



def compare_process ():
    # read all DevGPT conversations
    dev_gpt_json = get_json_data('ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json')
    # read all questions from db file
    so_api_questions_json = get_json_data(os.path.join('StackOverflow_api_db', 'db', 'questions.json'))
    # read all answers from db file
    so_api_answers_json = get_json_data(os.path.join('StackOverflow_api_db', 'db', 'answers.json'))

    df = pd.read_excel('results.xlsx')
    column_names = df.columns.tolist()

    # iterate through every so_api question
    for so_api_question_index, so_api_question in enumerate(so_api_questions_json.get("items", []), start = 1) :
        so_api_question_id = so_api_question.get("question_id", [])
        so_api_question_body = so_api_question.get("body", [])

        if not so_api_question_body :
            df.loc[len(df), [column_names[0], column_names[1]]] = [so_api_question_id, 'Error : empty so_api_question_body']                             #TODO: check
            continue

        str_so_api_clean_question = clean_text( extract_html_text(so_api_question_body))

        # leaving this block here, compare_answers only takes this as parameter and exp calls are minimum
        if "".join(str_so_api_clean_question.split()) == '""':
            df.loc[len(df), [column_names[0], column_names[1]]] = [so_api_question_id, 'Error : empty so_api_question']                             # TODO: check
            continue

        #TODO test #might have a list including an empty list
        so_api_id_answers_json = []
        for so_api_id_answers in so_api_answers_json.get("items", []):
            if int(list(so_api_id_answers.keys())[0]) == so_api_question_id:
                so_api_id_answers_json = so_api_id_answers[str(so_api_question_id)]
                break

        if not so_api_id_answers_json :                                                                                                         # TODO: test
            df.loc[len(df), [column_names[0], column_names[1]]] = \
                [so_api_question_id, 'Error : question has no answers']                       # TODO: check
            continue


        # compare question with every DevGPT question
        for gpt_source_index, source in enumerate(dev_gpt_json.get("Sources", []), start = 1):
            for gpt_sharing_index, sharing_data in enumerate(source.get("ChatgptSharing", []), start = 1):
                for gpt_conversation_index, gpt_conversation in enumerate(sharing_data.get("Conversations", []), start = 1):
                    gpt_num = str(gpt_source_index) + "|" + str(gpt_sharing_index) + "|"+ str(gpt_conversation_index)
                    print(f'question index: { so_api_question_index }, id:  { str(gpt_num) }')

                    if not gpt_conversation :
                        df.loc[len(df), [column_names[0], column_names[1], column_names[2], column_names[3]]] = \
                            [so_api_question_id, str_so_api_clean_question, gpt_num, "empty gpt conversation"]
                        continue

                    gpt_question = get_conversation_question(gpt_conversation)
                    str_gpt_clean_question = clean_text(json_data_to_str(gpt_question))

                    if "".join(str_gpt_clean_question.split()) == '""':
                        df.loc[len(df), [column_names[0], column_names[1], column_names[2], column_names[3]]] = \
                            [so_api_question_id, str_so_api_clean_question, gpt_num, "empty gpt question"]
                        continue

                    questions_similarity = compare_questions(str_so_api_clean_question, str_gpt_clean_question)

                    df.loc[len(df), [column_names[0], column_names[1], column_names[2], column_names[3], column_names[4],column_names[7]]] = \
                        [so_api_question_id, str_so_api_clean_question, gpt_num, str_gpt_clean_question, questions_similarity, gpt_num]

                    if 0.7 <= questions_similarity < 1:
                        gpt_answer_dictionary = get_conversation_code(gpt_conversation)
                        if gpt_answer_dictionary:                                   # TODO: test
                            compare_answers(so_api_id_answers_json, gpt_answer_dictionary, df, column_names)


                                # try :
                                #     df.loc[len(df), [column_names[0], column_names[1]]] = [so_api_question_id, str_so_api_clean_question]
                                #     df.to_excel('results.xlsx', index=False)
                                #
                                # except Exception as e:
                                #     df.loc[len(df), [column_names[0], column_names[1]]] = [so_api_question_index, "Error :  so_api_question not writable"]
                                #
                                #     print(
                                #         f'Exception : {e} \nError at -> so_api_question_index : {so_api_question_index} |\n'
                                #           + str_so_api_clean_question
                                #     )
                                #
                                # try :
                                #     df.loc[len(df) - 1, [column_names[2], column_names[3], column_names[4], column_names[7]]] = [gpt_num, str_gpt_clean_question, questions_similarity, gpt_num]
                                #     df.to_excel('results.xlsx', index=False)
                                #
                                #     if 0.7 <= questions_similarity < 1:
                                #         gpt_answer_dictionary = get_conversation_code(gpt_conversation)
                                #         if gpt_answer_dictionary:                                   # TODO: test
                                #             compare_answers(so_api_id_answers_json, gpt_answer_dictionary, df, column_names)
                                #
                                # except Exception as e:
                                #     df.loc[len(df) - 1, [column_names[2], column_names[3]]] = [gpt_num, "Error :  gpt clean question not writable"]
                                #
                                #     print(
                                #         f'Exception : {e} \nError at -> gpt_conversation_index :' + gpt_num
                                #           + '|\n' + str_gpt_clean_question
                                #     )

        #                 if gpt_source_index >= 18:
        #                     break
        # break

    df.to_excel('results.xlsx', index=False)

# # UNCOMMENT THIS!!!
# if os.path.basename(os.path.normpath(os.getcwd())) == 'src':
#     os.chdir('..')

os.remove('results.xlsx')
os.popen("copy " + str('resultsC.xlsx') + " " + str('results.xlsx'))
compare_process()







# TODO: check for empty question and others empty things like this ( i think {}) EVERYWHERE
#  refactor json functions (what did i mean)
#  check for chinese characters e.t.c and skip question # is the solution above proper?
#  does all_answers file need checking before used above?
#  should all answers be returned in items after db_builder : yes?
#  why are answers unordered? fix
#  only compare with python code from DevGPT, extra code that confirms its python code? where? ( at answer code extraction function? at data retrieval? after data retrieval? )
#  should answer comparison of < 0.7 be ignored?
#  should question line in excel appear with the answers
#  check for comparison question or answer errors that go unnoticed in excel. eg. cloning percentage missing


#TODO: future considerations:
#  take only the answer with the most votes
#  compare question context instead of only the title? compare answer context with chat non code response??