import json
from collections import Counter
from src.StackOverflow_api_db.manual_db_access.so_api import get_api_answers, get_api_questions

#Imports array of json answers, under the corresponding question_id as key
def craft_answers(questions_max_pages): # question_ids):
    with open('crafted_answers_arrays.json', 'r') as e:
        try :
            all_answers = json.load(e)
        except :
            print("file empty")
            all_answers = {}

    if not "items" in all_answers.keys():
        all_answers = { "items": [] }

    with open('questions_api_response.json', 'r') as e: all_questions = json.load(e)
    question_ids = list(set(item["question_id"] for item in all_questions["items"]))
    #sort q_ids #implement while
    question_ids = question_ids[:100]

    if question_ids:
        new_answers = get_api_answers(question_ids, questions_max_pages).get('items', []) # all question id's answers in a json

        # with open('test.json', 'w') as f: json.dump(new_answers, f, indent=4) # for testing, remove
        # with open('test.json', 'r') as e: new_answers = json.load(e)  # for testing, remove

        # find unique q_ids in the response answers
        unique_question_ids = list(set(item[key] for item in new_answers for key in item.keys() if key == 'question_id'))


        # iterate through ids, check if exists, add if new
        for q_id in unique_question_ids:
            if not any(str(q_id) in item for item in all_answers["items"]):
                # extra check for incomplete answers amount
                filtered_id_new_answers = list(item for item in new_answers if item['question_id'] == q_id)
                filtered_new_answers_json_arr = {q_id: filtered_id_new_answers}  # order ids getting in?

                all_answers["items"].append(filtered_new_answers_json_arr)
                with open('crafted_answers_arrays.json', 'w') as f: json.dump(all_answers, f, indent=4)
                #  leftover ids ( question_ids - unique_question_ids )
                #  handle cut-off answers that were cut from last id
                #  how to get total answers for a q_id to check
                #  could ignore last id and call it next call first


# current_page = 1
# while var["has_more"] is True:
#     print(current_page)
#
#     # do the stackapi call and see results, do I need and how to handle backoff
#
#     current_page += 1
#     if current_page % 15 == 0:
#         time.sleep(30)
#         print("stop")
#
#     if var["quota_remaining"] < 50 :
#         print(current_page)
#         break
#
#     #backoff? is it automatic?

# fetch every question
has_more = False
while has_more:
    print("has_more")

    # questions = get_api_questions_advanced() # TODO: set the next page
    with open('questions_api_response.json', 'r') as e: all_questions = json.load(e) #fortesting

    # page limit is 25, fetch next pages until has_more false
    if not all_questions["has_more"]:
        print(all_questions["has_more"])
        has_more = False

    has_more = False  # remove

if 'all_questions' in vars():
    # remove duplicates
    question_ids = list(item["question_id"] for item in all_questions["items"])
    if len(set(question_ids)) < len(question_ids):
        print("dups")
        counts = Counter(question_ids)
        dupids = [id for id in counts if counts[id] > 1]
        for dupid in dupids:
            for question in all_questions["items"]:
                 if question["question_id"] == dupid:
                     all_questions["items"].remove(question)
                     break
        question_ids = set(question_ids)

    with open('questions_api_response.json', 'w') as f: json.dump(all_questions, f, indent=4)


#fetch answers
craft_answers(25) # question_ids) # implement loop inside
