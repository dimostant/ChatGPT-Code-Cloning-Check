#https://api.stackexchange.com/docs/

from stackapi import StackAPI

SITE = StackAPI('stackoverflow')

def get_api_question(list_of_ids):
    api_question = SITE.fetch('questions/{ids}', ids = list_of_ids)

    return api_question["items"][0]["title"]

def get_api_answer(list_of_ids, order = 'desc', sort = 'activity'):
    api_questions = SITE.fetch('questions/{ids}/answers', ids = list_of_ids, filter = '!nNPvSNdWme') 
    api_question = api_questions["items"][0]["body"]

    return api_question