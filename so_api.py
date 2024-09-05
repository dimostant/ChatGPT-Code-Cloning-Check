#https://api.stackexchange.com/docs/

from stackapi import StackAPI

SITE = StackAPI('stackoverflow')

def get_api_question(list_of_ids):
    if type(list_of_ids) == int: #ids must be an array, even of one element 
        list_of_ids = [list_of_ids]
    api_question = SITE.fetch('questions/{ids}', ids = list_of_ids) 
    return api_question["items"][0]["title"]

def get_api_answer(list_of_ids):
    if type(list_of_ids) == int:
        list_of_ids = [list_of_ids]
    api_answer = SITE.fetch('answers/{ids}', ids = list_of_ids)
    return api_answer["items"][0]["body"]