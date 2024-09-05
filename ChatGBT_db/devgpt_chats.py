import json

def json_data_to_str(json_data):
    return json.dumps(json_data)

def print_json_data(json_data):
    print(json.dumps(json_data))

#get data from json file and return it in usable format, always include
def get_json_data(file_path):
    with open(file_path) as file:
        return json.load(file)

def get_user_converstations(json_data, user):
    user_conversations = json_data["Sources"][user]["ChatgptSharing"][0]["Conversations"]
    return user_conversations  

def get_user_question(user_conversations, conversation):   
    question = user_conversations[conversation]["Prompt"] 
    return question

def get_user_answer(user_conversations, conversation):
    answer = user_conversations[conversation]["Answer"] 
    return answer

def get_user_code(user_conversations, conversation):
    code = user_conversations[conversation]["ListOfCode"]
    return code