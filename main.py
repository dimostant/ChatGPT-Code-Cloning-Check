import ChatGBT_db.devgpt_chats as chatgpt_db
from so_api import get_api_question, get_api_answer #change to importing the entire file?
from so_postgres import get_so_postgres_question
from compare import compare_questions
import ast
from bs4 import BeautifulSoup

#inputs
question_id = 4 #can also be an array of ids
user = 1
path = 'ChatGBT_db/DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json'


#figure out in what sequence to get DevGPT questions and StackOverflow api questions
#check date of stackoverflow data to be before the release of ChatGPT
#filter for what programming the question is about, maybe use the tags from stackoverflow and the answer too for both

#get data from DevGPT
json_data = chatgpt_db.get_json_data(path) # optimize db interface? #just use json.dumps
user_conversations = chatgpt_db.get_user_converstations(json_data, user)

gpt_question = chatgpt_db.get_user_question(user_conversations, 0)
chatgpt_db.print_json_data(gpt_question)
str_gpt_question = chatgpt_db.json_data_to_str(gpt_question)

# gpt_answer = chatgpt_db.get_user_answer(user_conversations, 0) # gpt_code = chatgpt_db.get_user_code(user_conversations, 0)

#get data from StackOverflow API
so_api_question = get_api_question(question_id)
chatgpt_db.print_json_data(so_api_question) #indent=2) # make json handler?
str_so_api_question = chatgpt_db.json_data_to_str(so_api_question)

# #get data from StackOverflow Postgres Db
# so_postgres_question = get_so_postgres_question()
# print(so_postgres_question)

#compare different questions test case

if compare_questions(str_so_api_question , str_gpt_question) >= 0.7:
    print("similar questions")
else:
    print("different questions")

#compare similar or same questions

if compare_questions(str_so_api_question, str_so_api_question) == 1:
    print("identical questions")
    #ignore

elif 0.7 <= compare_questions(str_so_api_question, str_so_api_question) < 1:
    print("similar questions")

    #compare answers codes code

    #ramp of how much the code matches, 1 to 0.7/ 0.69 to 0.3/ 0.29 to 0 and categorize, where will this be stored?

    #if (answerA code for logokloph answerB)
    #print("logoklophhhhh")
else:
    print("different questions")

#answers codes code
so_api_answer_body = get_api_answer(question_id)
print(so_api_answer_body)
chatgpt_db.print_json_data(so_api_answer_body)

# Parse the HTML content
soup = BeautifulSoup(chatgpt_db.json_data_to_str(so_api_answer_body), 'html.parser')

# Find all code snippets inside <pre><code> tags
code_snippets = [pre.get_text() for pre in soup.find_all('pre')]

# Find all inline code snippets inside <code> tags not within <pre>
inline_code_snippets = [code.get_text() for code in soup.find_all('code') if code.parent.name != 'pre'] #needs testing, e.g <pre><code>1<code>2</code>3</pre></code>, is it in order?

# Combine all extracted code snippets
extracted_so_api_code = "\n".join(code_snippets + inline_code_snippets)

tree1 = ast.parse(extracted_so_api_code)

print("\n devgpt code \n")

gpt_code = chatgpt_db.get_user_code(user_conversations, 0)
chatgpt_db.print_json_data(gpt_code)





# while gpt_question != None: 
# get them 100 by 100 to optimize the process, maybe 50? do optimal call of the api  
# while so_api_question ???: