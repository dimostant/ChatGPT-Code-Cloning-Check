from datetime import datetime
from stackapi import StackAPI
from src.constants import SO_KEY


# https://api.stackexchange.com/docs/
key = SO_KEY
SITE = StackAPI('stackoverflow', key = SO_KEY)
default_max_pages = SITE.max_pages

def get_api_questions(list_of_ids, max_pages):
    SITE.max_pages = max_pages
    api_questions = SITE.fetch('questions/{ids}', ids = list_of_ids)
    print("quota remaining: ", api_questions["quota_remaining"])

    return api_questions

def get_api_questions_advanced(page, max_pages):
    SITE.max_pages = max_pages
    questions = SITE.fetch('search/advanced', page=page, todate=datetime(2021,9,1),
                       order='asc', sort='creation', accepted=True, closed=True, tagged='python', filter='!*1PUVE3Qq3HSQhXM1rAf4Bn*qUK)kYEiMeqfYwRhD')
    print("quota remaining: ", questions["quota_remaining"])

    return questions

def get_api_answers(list_of_ids, max_pages):
    SITE.max_pages = max_pages
    api_answers = SITE.fetch('questions/{ids}/answers', ids = list_of_ids, filter = '!nNPvSNdWme')
    print("quota remaining: ", api_answers["quota_remaining"])

    return api_answers