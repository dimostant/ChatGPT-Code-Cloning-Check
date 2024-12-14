import json
from collections import Counter

with open('questions.json', 'r') as e:
    all_questions = json.load(e)

question_ids = list(item["question_id"] for item in all_questions)
counts = Counter(question_ids)

print(counts)