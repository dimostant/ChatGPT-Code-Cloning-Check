import ChatGBT_db.devgpt_chats as chatgpt_db
from so_api import get_api_question
from so_postgres import get_so_postgres_question

path = 'ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json'

json_data = chatgpt_db.get_json_data(path) # optimize db interface? #just use json.dumps
user_converstations = chatgpt_db.get_user_converstations(json_data, 1)

gpt_question = chatgpt_db.get_user_question(user_converstations, 0)
chatgpt_db.print_json_data(gpt_question)
str_gpt_question = chatgpt_db.json_data_to_str(gpt_question)

# gpt_answer = chatgpt_db.get_user_answer(user_converstations, 0) # gpt_code = chatgpt_db.get_user_code(user_converstations, 0)

so_api_question = get_api_question()
chatgpt_db.print_json_data(so_api_question) #indent=2) # make json handler?

so_postgres_question = get_so_postgres_question()
print(so_postgres_question)

str_so_api_question = chatgpt_db.json_data_to_str(so_api_question)

from compare import compare_questions  

if compare_questions(so_postgres_question , str_gpt_question) >= 0.7:
    print("similar questions")
else:
    print("different questions")

if compare_questions(str_so_api_question, str_so_api_question) >= 0.7:
    print("similar questions")
    #if (answerA code for logokloph answerB)
    #print("logoklophhhhh")
else:
    print("different questions")