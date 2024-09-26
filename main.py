import ChatGBT_db.devgpt_chats as chatgpt_db
from so_api import get_api_question #change to importing the entire file?
from so_postgres import get_so_postgres_question
from compare_process import compare_proccess

#inputs
question_id = 79018992 #can also be an array of ids
user = 1
path = 'ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json'

#figure out in what sequence to get DevGPT questions and StackOverflow api questions
#check date of stackoverflow data to be before the release of ChatGPT
#filter for what programming the question is about, maybe use the tags from stackoverflow and the answer too for both
#is there a use for the text of the answers?
#include question and answerscomments

#get data from DevGPT
json_data = chatgpt_db.get_json_data(path) # optimize db interface? #just use json.dumps
gpt_conversation = chatgpt_db.get_user_conversation(json_data, user, 0)

gpt_question = chatgpt_db.get_conversation_question(gpt_conversation)
str_gpt_question = chatgpt_db.json_data_to_str(gpt_question)
print("DevGPT        question :", str_gpt_question)


#get data from StackOverflow API
so_api_question = get_api_question(question_id) # make json handler?
str_so_api_question = chatgpt_db.json_data_to_str(so_api_question)
print("StackOverflow question :", str_so_api_question)

# #get data from StackOverflow Postgres Db
# so_postgres_question = get_so_postgres_question()
# print(so_postgres_question)

#compare so_api_questiona argument, gpt_question

compare_proccess(str_so_api_question, question_id, str_so_api_question)
#THIS ONLY WORKS BECAUSE THE STRING IS IDENTICAL
#identical case

compare_proccess(str_so_api_question ,question_id, str_gpt_question)
#different case

#match case