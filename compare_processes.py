import ast

from code_handling import extract_html_code, extract_dictionary_code, remove_non_utf8_chars
import ChatGBT_db.devgpt_chats as chatgpt_db
from so_api import get_api_question, get_api_answer  #change to importing the entire file?

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def compare_questions(api_question, gpt_question):
    print("\ncomparing :\n" + api_question + "\n" + gpt_question)

    x_list = word_tokenize(api_question)
    y_list = word_tokenize(gpt_question)

    sw = stopwords.words('english')
    l1 = [];
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
    print("so api code \n")
    #answer MUST contain code, or ignored
    # must be Python
    so_api_answers_body = get_api_answer(so_question_id)#put this out of the function?
    for so_api_answer_body in so_api_answers_body:
        so_api_answer_code = extract_html_code(so_api_answer_body)
        so_api_answer_clean_code = remove_non_utf8_chars(so_api_answer_code)
        print(so_api_answer_clean_code)

    # needs a function that cleans the string of irrelevant to the code text that is left over

    # insert code to abstract syntax tree (python code only!)
    # tree1 = ast.parse(extracted_so_api_code)

    print("DevGPT code \n")
    gpt_answer_dictionary = chatgpt_db.get_conversation_code(gpt_conversation)
    # extract blocks of code to a string with \n and cleanup irrelevant information to the code
    gpt_answer_code = extract_dictionary_code(gpt_answer_dictionary)
    gpt_answer_clean_code = remove_non_utf8_chars(gpt_answer_code)
    print(gpt_answer_clean_code)
    # needs a function that cleans the string of irrelevant to the code text that is left over

    # insert code to abstract syntax tree (python code only!)
    #tree2 = ast.parse(gpt_answer_clean_code)

    #if (answerA code for cloning answerB) print("cloning")
    #ramp of how much the code matches, 1 to 0.7/ 0.69 to 0.3/ 0.29 to 0 and categorize, where will this be stored?
    #cloning Code comparison and result extraction, then saved somewhere


#invent a function that can detect the kind of question, and get the appropriate answers e.t.c accordingly
def compare_process (so_question_id, gpt_conversation):
    so_api_question = get_api_question(so_question_id)  # make json handler?
    str_so_api_question = chatgpt_db.json_data_to_str(so_api_question)
    str_so_api_clean_question = remove_non_utf8_chars(str_so_api_question)
    print("StackOverflow question :", str_so_api_clean_question)

    gpt_question = chatgpt_db.get_conversation_question(gpt_conversation)
    str_gpt_question = chatgpt_db.json_data_to_str(gpt_question)
    print("DevGPT        question :", str_gpt_question)

    # #get data from StackOverflow Postgres Db
    # so_postgres_question = get_so_postgres_question()
    # print(so_postgres_question)

    # might need to compare the context of the questions, not only the title
    # should the contexts of the questions even be checked before comparing code??
    similarity = compare_questions(str_so_api_question, str_gpt_question)

    similarity = 0.7

    if similarity == 1:
        print("identical questions\n")
        #ignore

    elif 0.7 <= similarity < 1:
        print("similar questions, checking...\n")
        compare_answers(so_question_id, gpt_conversation)

    else:
        print("different questions\n")