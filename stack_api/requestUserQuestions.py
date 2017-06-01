#!/usr/bin/env python
# -*- coding: utf-8 -*-

#users/{id}/top-answer-tags Get the top tags (by score) a single user has posted answers in.


import requests
import json
import sys
import time

question_request_payload = {'key':'Fk2OzBSIscRuxnV2hWNMYg((', 'order': 'desc', 'sort': 'reputation', 'site': 'stackoverflow', 'pagesize': 100}
#get top 100 users by reputation

answersFile = open("answers.json",'r')

answers = json.load(answersFile)
    
questionIds = [str(answer["question_id"]) for answer in answers]

has_more = True
answer_request_payload = question_request_payload
answer_request_payload["sort"] = "activity"
quota_remaining = 1


with open("user-questions.json",'w') as user_questions:
  #for question_id in questionIds:
	if(quota_remaining == 0):
	  print("QUOTA EXCEEDED! CATASTROPHIC FAILURE!!!")
	question_request = requests.get('https://api.stackexchange.com/2.2/questions/'+(';'.join(questionIds)), params=question_request_payload)
	response = question_request.json()
	if("quota_remaining" not in response):
	  print("REQUEST ERROR, WAITING...", file=sys.stderr)
	  time.sleep(2)

	#print(response, file=sys.stderr);
	quota_remaining = response["quota_remaining"]

	for tag in response["items"]:
	  print(json.dumps(tag), file=user_questions)
	  
	print("SAVED",len(response["items"]),"TAGS TO DISK")
	  
	if "backoff" in response:
	  print("BACKING OFF FOR",response["backoff"],"SECONDS")
	  time.sleep(response["backoff"])
	else:
	  time.sleep(1.0/29.0)