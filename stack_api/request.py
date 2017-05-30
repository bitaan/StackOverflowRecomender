#!/usr/bin/env python
# -*- coding: utf-8 -*-


#questions/unanswered
#questions/unanswered/my-tags
#/api/questions/featured
#/api/users/{ids}/posts  Get all posts (questions and answers) owned by a set of users.

#/api/questions/{ids}/linked  Get the questions that link to the questions identified by a set of ids.
#/api/questions/{ids}/related  Get the questions that are related to the questions identified by a set of ids.

#/api/users/{id}/top-answer-tags  Get the top tags (by score) a single user has posted answers in.
##/api/users/{id}/tags/{tags}/top-answers  Get the top answers a user has posted on questions with a set of tags.

####'client_id':9527, 'scope':'no_expiry', 'key':'Fk2OzBSIscRuxnV2hWNMYg((',

import requests
import json
import sys
import time

user_request_payload = {'order': 'desc', 'sort': 'reputation', 'site': 'stackoverflow', 'pagesize': 100}
user_request = requests.get('https://api.stackexchange.com/2.2/users', params=user_request_payload)

users = user_request.json()["items"]

with open("users.json",'w') as users_file:
  for user in users:
      print(json.dumps(user), file=users_file)
    
user_ids = [str(user["user_id"]) for user in users]

has_more = True
answer_request_payload = user_request_payload
answer_request_payload["sort"] = "activity"
answer_request_payload["page"] = 1
quota_remaining = 1

while(has_more and quota_remaining > 0):
  with open("answers.json",'w') as answers_file:
    answer_request = requests.get('https://api.stackexchange.com/2.2/users/'+(';'.join(user_ids))+'/answers', params=answer_request_payload)
    response = answer_request.json()
    quota_remaining = response["quota_remaining"]
    has_more = response["has_more"]
    print("GOT PAGE",answer_request_payload["page"])
    answer_request_payload["page"] += 1
    
    for answer in response["items"]:
      print(json.dumps(answer), file=answers_file)
      
    print("SAVED",len(response["items"]),"ANSWERS TO DISK")
      
    if "backoff" in response:
      print("BACKING OFF FOR",response["backoff"],"SECONDS")
      time.sleep(response["backoff"])
    else:
      time.sleep(1/29)
