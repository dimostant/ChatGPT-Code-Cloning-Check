from compare import compare_questions
from code_handling import extract_html_code, extract_dictionary_code
import ChatGBT_db.devgpt_chats as chatgpt_db
from so_api import get_api_question, get_api_answer  #change to importing the entire file?

#invent a function that can detect the kind of question, and get the appropriate answers e.t.c accordingly
def compare_process (so_question_id, gpt_conversation):
    so_api_question = get_api_question(so_question_id)  # make json handler?
    str_so_api_question = chatgpt_db.json_data_to_str(so_api_question)
    print("StackOverflow question :", str_so_api_question)

    gpt_question = chatgpt_db.get_conversation_question(gpt_conversation)
    str_gpt_question = chatgpt_db.json_data_to_str(gpt_question)
    print("DevGPT        question :", str_gpt_question)

    # #get data from StackOverflow Postgres Db
    # so_postgres_question = get_so_postgres_question()
    # print(so_postgres_question)

    #should the contexts of the questions even be checked before comparing code??
    similarity = compare_questions(str_so_api_question, str_gpt_question)

    if similarity == 1:
        print("identical questions\n")
        #ignore

    elif 0.7 <= similarity < 1:
        print("similar questions, checking...\n")

        #ramp of how much the code matches, 1 to 0.7/ 0.69 to 0.3/ 0.29 to 0 and categorize, where will this be stored?
        #if (answerA code for cloning answerB) print("cloning")

        #compare answers codes code

        print("\n so api code \n")

        #answer MUST contain code, or ignored
        so_api_answer_body = get_api_answer(so_question_id)
        # chatgpt_db.print_json_data(so_api_answer_body)
        so_api_answer_code = extract_html_code(so_api_answer_body)
        print(so_api_answer_code)

        # needs a function that cleans the string of irrelevant to the code text that is left over
        # insert code to abstract syntax tree (python code only!)
        # tree1 = ast.parse(extracted_so_api_code)

        print("\n DevGPT code \n")

        gpt_answer_dictionary = chatgpt_db.get_conversation_code(gpt_conversation)
        # chatgpt_db.print_json_data(gpt_answer_code_dictionary)

        # extract blocks of code to a string with \n and cleanup irrelevant information to the code
        gpt_answer_code = extract_dictionary_code(gpt_answer_dictionary)
        print(gpt_answer_code)

        # needs a function that cleans the string of irrelevant to the code text that is left over

        # insert code to abstract syntax tree (python code only!)
        # tree2 = ast.parse(extracted_gpt_answer_code )

        #cloning Code comparison and result extraction, then saved somewhere

    else:
        print("different questions\n")