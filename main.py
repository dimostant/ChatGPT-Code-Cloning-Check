import ChatGBT_db.devgpt_chats as chatgpt_db
from compare_process import compare_process

#inputs
question_id = 79018992 #can also be an array of ids
user = 1
path = 'ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json'

#get data from DevGPT
json_data = chatgpt_db.get_json_data(path) # optimize db interface? #just use json.dumps

#investigate if it is needed to include Extra DevGPT db data
gpt_conversation = chatgpt_db.get_user_conversation(json_data, user, 0)

#figure out in what sequence to get DevGPT questions and StackOverflow api questions
#check date of stackoverflow data to be before the release of ChatGPT
#filter for what programming the question is about, maybe use the tags from stackoverflow and the answer too for both
#is there a use for the text of the answers?
#include question and answers comments


# while so_api_question ???:
#traverse through all stackoverflow questions before [chatGPT releaseDate] by finding the last question id of that date or the date, any implications?
#get them e.g. 100 by 100 to optimize the process, maybe 50? do optimal call of the api
#question not empty
#filter the question from the coding language tags, must be e.g. Python
#extra code that confirms its python

#somehow traverse through all DevGPT conversations
#must be Python

#compare so_api_questions argument, gpt_question
compare_process(question_id, gpt_conversation)

#identical case [questionId],[gpt_conversation]
#different case [questionId],[gpt_conversation]
#match     case [questionId],[gpt_conversation]