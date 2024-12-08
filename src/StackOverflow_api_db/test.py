import json
from collections import Counter

from src.StackOverflow_api_db.manual_db_access.so_api import get_api_answers, get_api_questions_advanced

#Imports array of json answers, under the corresponding question_id as key
def craft_answers(max_pages): # question_ids):
    with open('answers.json', 'r') as a:
        try :
            all_answers = json.load(a)
        except :
            print("file empty") #throws when not empty
            all_answers = {}

    if not "items" in all_answers.keys():
        all_answers = { "items": [] }

    with open('questions.json', 'r') as q: all_questions = json.load(q)
    question_ids = list(set(item["question_id"] for item in all_questions["items"]))

    question_ids = []

    if question_ids:
        for i in range(0, len(question_ids), 100):
            question_ids_chunk = question_ids[i:i + 100]
            new_answers = get_api_answers(question_ids_chunk, max_pages).get('items', [])

            # find unique q_ids in the response answers
            unique_question_ids = list(set(item[key] for item in new_answers for key in item.keys() if key == 'question_id'))

            # iterate through ids, check if exists, add if new
            for q_id in unique_question_ids:
                print(q_id)
                if not any(str(q_id) in item for item in all_answers["items"]):
                    # extra check for incomplete answers amount
                    filtered_id_new_answers = list(item for item in new_answers if item['question_id'] == q_id)
                    filtered_new_answers_json_arr = {q_id: filtered_id_new_answers}  # TODO: order ids getting in?

                    all_answers["items"].append(filtered_new_answers_json_arr)
                    with open('answers.json', 'w') as a: json.dump(all_answers, a, indent=4)
                    #  TODO: leftover ids ( question_ids - unique_question_ids )
                    #  TODO: handle cut-off answers that were cut from last id
                    #  TODO: how to get total answers for a q_id to check
                    #  TODO: could ignore last id and call it next call first
                    #  TODO: case answers more than 100? automatically resolved by StackAPI?

max_pages = 25

has_more = False
# fetch every question
while has_more:
    print("has_more")

    questions = get_api_questions_advanced(max_pages)
    with open('questions.json', 'r') as e: all_questions = json.load(e) #fortesting

    # page limit is 25, fetch next pages until has_more false
    if not all_questions["has_more"]:
        print(all_questions["has_more"])
        has_more = False

    has_more = False  # testing remove

# TODO: sort and duplicate by chunks or alltoghether?

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
        #TODO: this doesnt remove more than one duplicate, must work for all
        question_ids = set(question_ids)

    #sort questions or q_ids

    with open('questions.json', 'w') as f: json.dump(all_questions, f, indent=4)


# fetch answers
craft_answers(25) # question_ids) # implement loop inside


