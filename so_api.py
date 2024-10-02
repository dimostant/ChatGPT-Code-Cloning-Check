from stackapi import StackAPI

#https://api.stackexchange.com/docs/
SITE = StackAPI('stackoverflow')

def get_api_questions(list_of_ids):
    api_questions = SITE.fetch('questions/{ids}', ids = list_of_ids)

    #is that proper?
    return api_questions["items"][0]["title"] if len(api_questions) == 1 else api_questions


def get_api_answers(list_of_ids, order = 'desc', sort = 'activity'):
    api_questions = SITE.fetch('questions/{ids}/answers', ids = list_of_ids, filter = '!nNPvSNdWme')

    return api_questions