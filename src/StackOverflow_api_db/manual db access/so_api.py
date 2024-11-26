from stackapi import StackAPI
from datetime import datetime

# https://api.stackexchange.com/docs/
SITE = StackAPI('stackoverflow')
max_pages = SITE.max_pages

def get_api_questions(list_of_ids):
    api_questions = SITE.fetch('questions/{ids}', ids = list_of_ids)
    print("quota remaining : " + api_questions["quota_remaining"])

    return api_questions


def get_api_answers(list_of_ids):
    api_answers = SITE.fetch('questions/{ids}/answers', ids = list_of_ids, filter = '!nNPvSNdWme')
    print("quota remaining : ",  api_answers["quota_remaining"])

    return api_answers


def get_api_questions_advanced():
    SITE.max_pages = 25
    questions = SITE.fetch('search/advanced', todate=datetime(2021,9,1),
                       order='desc', sort='votes', accepted=True, closed=True, tagged='python', filter='!*1PUVE3Qq3HSQhXM1rAf4Bn*qUK)kYEiMeqfYwRhD')
    print("quota remaining : ", questions["quota_remaining"])
    SITE.max_pages = max_pages

    return questions