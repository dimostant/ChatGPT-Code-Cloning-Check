import json

def json_data_to_str(json_data):
    return json.dumps(json_data)

def print_json_data(json_data):
    print(json.dumps(json_data))

#get data from json file and return it in usable format, always include
def get_json_data(file_path):
    with open(file_path) as file:
        return json.load(file)

def get_user_conversation(json_data, user, conversation):
    user_conversations = json_data["Sources"][user]["ChatgptSharing"][0]["Conversations"][conversation]
    return user_conversations  

def get_conversation_question(user_conversation):
    question = user_conversation["Prompt"]
    return question

def get_conversation_answer(user_conversation):
    answer = user_conversation["Answer"]
    return answer

def get_conversation_code(user_conversation):
    code = user_conversation["ListOfCode"]
    return code