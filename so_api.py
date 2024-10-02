from stackapi import StackAPI

#https://api.stackexchange.com/docs/
SITE = StackAPI('stackoverflow')

def get_api_question(list_of_ids):
    api_question = SITE.fetch('questions/{ids}', ids = list_of_ids)

    return api_question["items"][0]["title"]

def get_api_answers(list_of_ids, order = 'desc', sort = 'activity'):
    api_questions = SITE.fetch('questions/{ids}/answers', ids = list_of_ids, filter = '!nNPvSNdWme')

    return api_questions