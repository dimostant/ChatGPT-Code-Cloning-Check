import ujson
from collections import Counter
from src.StackOverflow_api_db.manual_db_access.so_api import get_api_answers, get_api_questions_advanced


#Import array of json answers, under the corresponding question_id as key
def craft_answers(pages):
    with open('answers.json', 'r') as a:
        try:
            all_answers = ujson.load(a)
        except Exception as e:
            print(f'file empty -> {e}') #throws when not empty
            all_answers = {}

    if not "items" in all_answers.keys():
        all_answers = { "items": [] }

    with open('questions.json', 'r') as q:
        all_questions = ujson.load(q)
    question_ids = list(set(item["question_id"] for item in all_questions["items"]))

    if question_ids:
        for i in range(0, len(question_ids), 100):
            question_ids_chunk = question_ids[i:i + 100]
            new_answers = get_api_answers(question_ids_chunk, pages).get('items', [])

            # find unique q_ids in the response answers
            unique_question_ids = list(set(item[key] for item in new_answers for key in item.keys() if key == 'question_id'))

            # iterate through ids, check if exists, add if new
            for question_id in unique_question_ids:
                print(question_id)
                # check if answers_id already exist in questions json ids else add them and rewrite the file
                if not any(str(question_id) in item for item in all_answers["items"]):
                    # extra check for incomplete answers amount
                    filtered_id_new_answers = list(item for item in new_answers if item['question_id'] == question_id)
                    filtered_new_answers_json_arr = {question_id: filtered_id_new_answers}

                    all_answers["items"].append(filtered_new_answers_json_arr)
                    with open('answers.json', 'w') as a:
                        ujson.dump(all_answers, a, indent=4)


def craft_questions(pages):
    has_more = True
    page = 1

    # fetch every question
    while has_more:
        with open('questions.json', 'r') as e:
            try:
                all_questions = ujson.load(e)
            except Exception as e:
                #empty non json content
                print(f'file empty -> {e}')
                all_questions = { "items": [] }

        new_questions = get_api_questions_advanced(page, pages)
        all_questions += new_questions["items"]

        with open('questions.json', 'w') as f:
            ujson.dump(all_questions, f, indent=4) #for testing

        if not new_questions["has_more"]:
            break

        page += pages

    # remove duplicates
    if 'all_questions' in vars():
        question_ids = list(item["question_id"] for item in all_questions["items"])
        if len(set(question_ids)) < len(question_ids):
            counts = Counter(question_ids)
            duplicate_ids = [question_id for question_id in counts if counts[question_id] > 1]
            for duplicate_id in duplicate_ids:
                for question in all_questions["items"]:
                     if question["question_id"] == duplicate_id:
                         all_questions["items"].remove(question)
                         break

            question_ids = set(question_ids)

max_pages = 50

# fetch questions
craft_questions(max_pages)
# fetch answers
craft_answers(max_pages)