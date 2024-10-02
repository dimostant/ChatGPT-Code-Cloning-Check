import ChatGBT_db.devgpt_chats as chatgpt_db
from compare_processes import compare_process

#inputs
question_id = [59325633] #[79018992] #must be arr
user = 1
#user_conversation??
path = 'ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json'

#get data from DevGPT
DevGPT_data = chatgpt_db.get_json_data(path) # optimize db interface? #just use json.dumps

#whatever handles SO data needs to remove html artifacts
#figure out in what sequence to get DevGPT questions and StackOverflow api questions
#check date of stackoverflow data to be before the release of ChatGPT
#filter for what programming the question is about, maybe use the tags from stackoverflow and the answer too for both
#is there a use for the text of the answers?
#include question and answers comments
# method getAllquestions and filter bydate etc
# method while so_api_question date < chatGPT release date ???:
# method for i = 0 ; i <= id_lastpostbefore chatGPT release
#traverse through all stackoverflow questions before [chatGPT releaseDate] by finding the last question id of that date or the date, any implications?
#get them e.g. 100 by 100 to optimize the process, maybe 50? do optimal call of the api
#question not empty
#filter the question from the coding language tags, must be e.g. Python
#extra code that confirms its python
#remove non utf8 from json

# gpt_conversation = ""

for source in DevGPT_data.get("Sources", []):
    chatgpt_sharing = source.get("ChatgptSharing", [])
    for sharing_data in chatgpt_sharing: #this index will always be 0 should i remove? # this is for safety
        conversations = sharing_data.get("Conversations", [])
        for conversation in conversations: #is this safe if no conversation exists?
            gpt_conversation = conversation
            #chatgpt_db.print_json_data(conversation)
            #filter for python



#compare so_api_questions argument, gpt_question
gpt_conversation = chatgpt_db.get_user_conversation(DevGPT_data, user, 0)
compare_process(question_id, gpt_conversation)

#identical case [questionId],[gpt_conversation]
#different case [questionId],[gpt_conversation]
#match     case [questionId],[gpt_conversation]

#store the results in CSV or JSON and in what structure
#HOW TO DO THE TESTIONG??