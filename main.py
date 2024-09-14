import ChatGBT_db.devgpt_chats as chatgpt_db
from so_api import get_api_question, get_api_answer #change to importing the entire file?
from so_postgres import get_so_postgres_question

#inputs
question_id = 4 #can also be an array of ids
user = 1
path = 'ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json'

#figure out in what sequence to get DevGPT questions and StackOverflow api questions
#check date of stackoverflow data to be before the release of ChatGPT
#filter for what programming the question is about, maybe use the tags from stackoverflow and the answer too for both

json_data = chatgpt_db.get_json_data(path) # optimize db interface? #just use json.dumps
user_converstations = chatgpt_db.get_user_converstations(json_data, user)

#get data from DevGPT
gpt_question = chatgpt_db.get_user_question(user_converstations, 0)
chatgpt_db.print_json_data(gpt_question)
str_gpt_question = chatgpt_db.json_data_to_str(gpt_question)

# gpt_answer = chatgpt_db.get_user_answer(user_converstations, 0) # gpt_code = chatgpt_db.get_user_code(user_converstations, 0)

#get data from StackOverflow API
so_api_question = get_api_question(question_id)
chatgpt_db.print_json_data(so_api_question) #indent=2) # make json handler?
str_so_api_question = chatgpt_db.json_data_to_str(so_api_question)

# #get data from StackOverflow Postgres Db
# so_postgres_question = get_so_postgres_question()
# print(so_postgres_question)


from compare import compare_questions  

#compare different questions test case

if compare_questions(str_so_api_question , str_gpt_question) >= 0.7:
    print("similar questions")
else:
    print("different questions")

#compare similar or same questions

if compare_questions(str_so_api_question, str_so_api_question) == 1:
    print("identical questions")
    #ignore

elif compare_questions(str_so_api_question, str_so_api_question) >= 0.7 and compare_questions(str_so_api_question, str_so_api_question) < 1:
    print("similar questions")

    #compare answers codes code

    #ramp of how much the code matches, 1 to 0.7/ 0.69 to 0.3/ 0.29 to 0 and categorize, where will this be stored?

    #if (answerA code for logokloph answerB)
    #print("logoklophhhhh")
else:
    print("different questions")

#ansers codes code
so_api_answer = get_api_answer(question_id)
chatgpt_db.print_json_data(so_api_answer)

print("\n devgpt code \n")

gpt_code = chatgpt_db.get_user_code(user_converstations, 0)
chatgpt_db.print_json_data(gpt_code)



# while gpt_question != None: 
# get them 100 by 100 to optimize the process, maybe 50? do optimal call of the api  
# while so_api_question ???: