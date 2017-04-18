#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
