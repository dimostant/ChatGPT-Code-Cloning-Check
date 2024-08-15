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


# ####### latop code #######

# import json

# json_obj = {
#     "Sources": [
#         {
#             "ChatgptSharing": [
#                 {
#                     "Conversations": [
#                         {
#                             "Prompt": "\u4ed6\u4eec\u90fd\u662f\u56fe\u7ed3\u6784\u7684\u5417",
#                             "Answer": "\u662f",
#                             #"Answer": "ChatGPT\u662f\u7684\uff0c\u795e\u7ecf\u7f51\u7edc\u6a21\u578b\u901a\u5e38\u53ef\u4ee5\u8868\u793a\u4e3a\u4e00\u79cd\u79f0\u4e3a\u201c\u8ba1\u7b97\u56fe\u201d\uff08Computational Graph\uff09\u7684\u7ed3\u6784\u3002\u5728\u8fd9\u4e2a\u56fe\u4e2d\uff1a\u8282\u70b9\uff08Nodes\uff09 \u4ee3\u8868\u8fd0\u7b97\uff08\u5982\u52a0\u6cd5\u3001\u4e58\u6cd5\u6216\u66f4\u590d\u6742\u7684\u51fd\u6570\uff0c\u5982\u5377\u79ef\u548c\u6fc0\u6d3b\u51fd\u6570\uff09\u3002\u8fb9\uff08Edges\uff09 \u4ee3\u8868\u6570\u636e\uff08\u901a\u5e38\u662f\u591a\u7ef4\u6570\u7ec4\uff0c\u4e5f\u79f0\u4e3a\u5f20\u91cf\uff09\u4ece\u4e00\u4e2a\u8fd0\u7b97\u6d41\u5411\u53e6\u4e00\u4e2a\u8fd0\u7b97\u3002PyTorch\u5728 PyTorch \u4e2d\uff0c\u9ed8\u8ba4\u60c5\u51b5\u4e0b\u4f7f\u7528\u201c\u52a8\u6001\u8ba1\u7b97\u56fe\u201d\uff08Dynamic Computational Graph\uff09\u3002\u8fd9\u610f\u5473\u7740\u56fe\u662f\u201c\u98de\u884c\u4e2d\u201d\u751f\u6210\u7684\uff0c\u6bcf\u6b21\u8fdb\u884c\u524d\u5411\u4f20\u64ad\u65f6\u90fd\u4f1a\u91cd\u65b0\u6784\u5efa\u3002\u8fd9\u4f7f\u5f97\u6a21\u578b\u66f4\u5bb9\u6613\u8c03\u8bd5\uff0c\u5e76\u4e14\u4e5f\u4f7f\u5f97\u652f\u6301\u53d8\u957f\u8f93\u5165\uff08\u5982\u53ef\u53d8\u5927\u5c0f\u7684\u5e8f\u5217\uff09\u53d8\u5f97\u66f4\u7b80\u5355\u3002TensorFlow\u5728\u65e9\u671f\u7248\u672c\u7684 TensorFlow \u4e2d\uff0c\u4f7f\u7528\u7684\u662f\u201c\u9759\u6001\u8ba1\u7b97\u56fe\u201d\uff08Static Computational Graph\uff09\u3002\u8fd9\u610f\u5473\u7740\u5728\u5f00\u59cb\u4efb\u4f55\u8ba1\u7b97\u4e4b\u524d\uff0c\u60a8\u9700\u8981\u5148\u5b9a\u4e49\u6574\u4e2a\u56fe\uff0c\u7136\u540e\u518d\u6267\u884c\u5b83\u3002\u8fd9\u901a\u5e38\u4f1a\u8ba9\u8c03\u8bd5\u53d8\u5f97\u66f4\u56f0\u96be\uff0c\u4f46\u4e00\u65e6\u56fe\u88ab\u4f18\u5316\uff0c\u63a8\u7406\u901f\u5ea6\u901a\u5e38\u4f1a\u66f4\u5feb\u3002TensorFlow 2.x \u63d0\u4f9b\u4e86 Eager Execution\uff0c\u4f7f\u5f97\u52a8\u6001\u56fe\u6210\u4e3a\u53ef\u80fd\uff0c\u4f46\u4ecd\u7136\u53ef\u4ee5\u901a\u8fc7\u9759\u6001\u56fe\u8fdb\u884c\u4f18\u5316\u3002ONNXONNX \u4e5f\u662f\u7528\u8ba1\u7b97\u56fe\u6765\u8868\u793a\u6a21\u578b\u7684\u3002\u4e0d\u8fc7\uff0c\u4e0e PyTorch \u548c TensorFlow \u4e0d\u540c\uff0cONNX \u4e0d\u7528\u4e8e\u6a21\u578b\u7684\u8bad\u7ec3\uff0c\u53ea\u7528\u4e8e\u8868\u793a\u5df2\u7ecf\u8bad\u7ec3\u597d\u7684\u6a21\u578b\u3002\u8fd9\u6837\u7684\u56fe\u662f\u9759\u6001\u7684\uff0c\u56e0\u4e3a\u5b83\u4e0d\u4f1a\u6539\u53d8\u3002\u5b83\u53ef\u4ee5\u88ab\u4e0d\u540c\u7684\u5de5\u5177\u548c\u5e93\u8bfb\u53d6\uff0c\u7528\u4e8e\u4f18\u5316\u6216\u8fdb\u884c\u6a21\u578b\u63a8\u7406\u3002\u7b80\u8a00\u4e4b\uff0c\u6240\u6709\u4e09\u8005\u90fd\u4f7f\u7528\u56fe\u7ed3\u6784\u6765\u8868\u793a\u795e\u7ecf\u7f51\u7edc\uff0c\u4f46\u5b83\u4eec\u5728\u5982\u4f55\u4f7f\u7528\u548c\u4f18\u5316\u8fd9\u4e9b\u56fe\u65b9\u9762\u6709\u6240\u4e0d\u540c\u3002PyTorch \u4e3b\u8981\u4f7f\u7528\u52a8\u6001\u56fe\uff0cTensorFlow \u53ef\u4ee5\u4f7f\u7528\u9759\u6001\u6216\u52a8\u6001\u56fe\uff0c\u800c ONNX \u4f7f\u7528\u9759\u6001\u56fe\u6765\u8868\u793a\u5df2\u8bad\u7ec3\u597d\u7684\u6a21\u578b\u3002\u5e0c\u671b\u8fd9\u80fd\u89e3\u7b54\u60a8\u7684\u95ee\u9898\uff01\u6709\u5176\u4ed6\u95ee\u9898\uff0c\u8bf7\u968f\u65f6\u63d0\u51fa\u3002",
#                             "ListOfCode": []
#                         }
#                     ]
#                 }
#             ]
#         }
#     ]
# }


# json_obj_string = json.dumps(json_obj["Sources"])
# #print(json_obj_string)

# # json_obj2 = {
# #     "sources" : "nig"
# # }

# # json_obj2_string = json.dumps(json_obj2["sources"])
# # print(json_obj2_string)

# # Open the file
# with open('snapshot_20231012/20231012_235320_discussion_sharings.json') as file:
#     # Load the JSON data
#     json_data = json.load(file)

# # Convert the JSON data to a string and print it
# json_string = json.dumps(json_data["Sources"][1]["ChatgptSharing"][0]["Conversations"][0]["ListOfCode"])
# #print(json_string)

# def get_conversation_question():
#     print()

# def get_user_converstations(user):
#     conversations = json_data["Sources"][1]["ChatgptSharing"][0]["Conversations"]
#     #user_chats = json.dumps(json_data["Sources"][1]["ChatgptSharing"][0]["Conversations"])
#     #print(user_chats)
#     print(json.dumps(conversations))
#     question = conversations[0]["Prompt"]
#     print(json.dumps(question))
#     #add answer and find how to combine code answers with the answer

# get_user_converstations(1)

# ####### laptop code #######