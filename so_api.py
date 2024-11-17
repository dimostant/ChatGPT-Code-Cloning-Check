from stackapi import StackAPI

# https://api.stackexchange.com/docs/
SITE = StackAPI('stackoverflow')

def get_api_questions(list_of_ids):
    api_questions = SITE.fetch('questions/{ids}', ids = list_of_ids)
    print("quota remaining : " + api_questions["quota_remaining"])

    return api_questions


def get_api_answers(list_of_ids, order = 'desc', sort = 'activity'):
    api_questions = SITE.fetch('questions/{ids}/answers', ids = list_of_ids, filter = '!nNPvSNdWme')
    print("quota remaining : ", api_questions["quota_remaining"])

    return api_questions