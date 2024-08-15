from stackapi import StackAPI

SITE = StackAPI('stackoverflow')
api_questions = SITE.fetch('questions/{ids}', ids=[4])

def get_api_question():
    return api_questions["items"][0]["title"]