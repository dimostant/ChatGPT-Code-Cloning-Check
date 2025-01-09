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
    # TODO: check amd fix if set gives unsorted answer

    question_ids = [] # remove
    #TODO: sort answers
    if question_ids:
        for i in range(0, len(question_ids), 100):
            question_ids_chunk = question_ids[i:i + 100]
            new_answers = get_api_answers(question_ids_chunk, max_pages).get('items', [])

            # find unique q_ids in the response answers
            unique_question_ids = list(set(item[key] for item in new_answers for key in item.keys() if key == 'question_id'))

            # iterate through ids, check if exists, add if new
            for q_id in unique_question_ids:
                print(q_id)
                # check if answers_id already exist in questions json ids else add them and rewrite the file
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

                    # TODO: print page

def craft_questions(max_pages):
    has_more = True
    page = 1
    # fetch every question
    while has_more:
        with open('questions.json', 'r') as e:
            try :
                all_questions = json.load(e)
            except :
                #empty non json content #throws when not empty
                print("file empty")
                all_questions = [] #TODO: this to { "items": [] } and test

        new_questions = get_api_questions_advanced(max_pages, page)
        #TODO: handle quota ending and possible errors
        all_questions += new_questions["items"]

        with open('questions.json', 'w') as f:
            json.dump(all_questions, f, indent=4) #for testing

        print(
            "has_more : ", new_questions["has_more"], "|",
            "quota : ", new_questions["quota_remaining"], "|",
            "last_page : ", new_questions["page"],
        )
        if not new_questions["has_more"]:
            break

        page += max_pages
    # TODO: confirm how to keep results if interrupt
    # TODO: are there duplicates using the above way? sort and duplicate by chunks or alltoghether?
    # if 'all_questions' in vars():
    #     # remove duplicates
    #     question_ids = list(item["question_id"] for item in all_questions["items"])
    #     if len(set(question_ids)) < len(question_ids):
    #         print("dups")
    #         counts = Counter(question_ids)
    #         dupids = [id for id in counts if counts[id] > 1]
    #         for dupid in dupids:
    #             for question in all_questions["items"]:
    #                  if question["question_id"] == dupid:
    #                      all_questions["items"].remove(question)
    #                      break
    #         #TODO: this doesnt remove more than one duplicate, must work for all
    #         question_ids = set(question_ids)

# TODO: need a way to access total pages?
max_pages = 50

# # fetch questions
craft_questions(max_pages)
# # fetch answers
# craft_answers(max_pages) # question_ids)