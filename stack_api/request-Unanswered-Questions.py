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

## /2.2/questions/no-answers?pagesize=100&order=desc&sort=activity&site=stackoverflowRun

question_request_payload = {'key':'Fk2OzBSIscRuxnV2hWNMYg((', 'order': 'desc', 'sort': 'activity', 'site': 'stackoverflow', 'pagesize': 100}
question_request = requests.get('https://api.stackexchange.com//2.2/questions/no-answers', params=question_request_payload)

print(question_request)

questions = question_request.json()["items"]

print(questions)

with open("questions.json",'w') as questions_file:
  for question in questions:
      print(json.dumps(question), file=questions_file)
