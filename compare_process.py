from compare import compare_questions
from code_handling import extract_html_code, extract_dictionary_code
import ChatGBT_db.devgpt_chats as chatgpt_db


def compare_proccess (so_api_question, gpt_question):
    #should the contexts of the questions even be checked before comparing code??
    similarity = compare_questions(so_api_question, gpt_question)

    if similarity == 1:
        print("identical questions\n")
        #ignore

    elif 0.7 <= similarity < 1:
        print("similar questions, checking...\n")

        # #ramp of how much the code matches, 1 to 0.7/ 0.69 to 0.3/ 0.29 to 0 and categorize, where will this be stored?
        # #if (answerA code for logokloph answerB)
        # #print("logoklophhhhh")
        #
        # #compare answers codes code
        #
        # print("\n so api code \n")
        #
        # # answers codes code
        # so_api_answer_body = get_api_answer(question_id)
        # # chatgpt_db.print_json_data(so_api_answer_body)
        # so_api_answer_code = extract_html_code(so_api_answer_body)
        # print(so_api_answer_code)
        #
        # # needs a function that cleans the string of irrelevant to the code text that is left over
        # # insert code to abstract syntax tree (python code only!)
        # # tree1 = ast.parse(extracted_so_api_code)
        #
        # print("\n devgpt code \n")
        #
        # gpt_answer_dictionary = chatgpt_db.get_user_code(user_conversations, 0)  # is this json or string?
        # # chatgpt_db.print_json_data(gpt_answer_code_dictionary)
        #
        # # extract blocks of code to a string with \n and cleanup irrelavant information to the code
        # gpt_answer_code = extract_dictionary_code(gpt_answer_dictionary)
        # print(gpt_answer_code)
        #
        # # needs a function that cleans the string of irrelevant to the code text that is left over
        #
        # # insert code to abstract syntax tree (python code only!)
        # # tree2 = ast.parse(extracted_gpt_answer_code )
        #
        # # while gpt_question != None:
        # # get them 100 by 100 to optimize the process, maybe 50? do optimal call of the api
        # # while so_api_question ???:

    else:
        print("different questions\n")