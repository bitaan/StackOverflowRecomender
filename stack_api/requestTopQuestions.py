#!/usr/bin/env python
# -*- coding: utf-8 -*-

#users/{id}/top-answer-tags Get the top tags (by score) a single user has posted answers in.


import requests
import json
import sys
import time

user_request_payload = {'key':'Fk2OzBSIscRuxnV2hWNMYg((', 'order': 'desc', 'sort': 'reputation', 'site': 'stackoverflow', 'pagesize': 100}
#get top 100 users by reputation
user_request = requests.get('https://api.stackexchange.com/2.2/users', params=user_request_payload)

users = user_request.json()["items"]

with open("users.json",'w') as users_file:
  for user in users:
      print(json.dumps(user), file=users_file)
    
user_ids = [str(user["user_id"]) for user in users]

has_more = True
answer_request_payload = user_request_payload
answer_request_payload["sort"] = "activity"
answer_request_payload["pagesize"] = 5
quota_remaining = 1


with open("top-answer-tags.json",'w') as answers_file:
  for user_id in user_ids:
    if(quota_remaining == 0):
      print("QUOTA EXCEEDED! CATASTROPHIC FAILURE!!!")
      break
    answer_request = requests.get('https://api.stackexchange.com/2.2/users/'+user_id+'/top-answer-tags', params=answer_request_payload)
    response = answer_request.json()
    if("quota_remaining" not in response):
      print("REQUEST ERROR, WAITING...", file=sys.stderr)
      time.sleep(2)
      continue

    #print(response, file=sys.stderr);
    quota_remaining = response["quota_remaining"]
    
    for tag in response["items"]:
      print(json.dumps(tag), file=answers_file)
      
    print("SAVED",len(response["items"]),"TAGS TO DISK")
      
    if "backoff" in response:
      print("BACKING OFF FOR",response["backoff"],"SECONDS")
      time.sleep(response["backoff"])
    else:
      time.sleep(1.0/29.0)
