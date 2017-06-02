from __future__ import print_function
import json
from pandas.io.json import json_normalize
import pandas as pd
import graphlab
import socket
import sys

def makeRecomendation( id_user , numRec, itemModel):
	#Make Recommendations:
	item_sim_recomm = itemModel.recommend(users=[id_user],k=numRec)
	item_sim_recomm.print_rows(num_rows=numRec)

	with open("recomendations.csv",'w') as recommendations_csv:

		print(item_sim_recomm,file=recommendations_csv)


userFile = open("users.json",'r')

userData = json.load(userFile)

questionFile = open("user-questions.json", 'r')

questionData = json.load(questionFile)

answerFile = open("answers.json", 'r')

answerData = json.load(answerFile)

with open("users.csv",'w') as users_csv:

	for line in userData:

		if "age" in line:
			print(line['user_id'],"|",line['age'] , "|",line['user_type'] ,"|" , line['reputation'], file = users_csv)

tags = ['git', 'java', 'python', 'sql', 'android','r','jquery','panda','html','css']

with open("questions.csv",'w') as questions_csv:
	
	for line in questionData:
		mambo = [str(line['question_id']), str(line['answer_count']), str(line['score'])]
		for tag in tags:
			mambo.append("1" if tag in line['tags'] else "0")
		print("|".join(mambo), file = questions_csv)


u_cols = ['user_id', 'age', 'user_type', 'reputation']
users = pd.read_csv('users.csv', sep='|', names=u_cols, encoding='latin-1')

#sprint(users)

q_cols = ['question_id', 'answer_count', 'score'] + tags
questions = pd.read_csv('questions.csv', sep='|', names=q_cols, encoding='latin-1')

#print(questions)

with open("ratings.csv", 'w') as ratings_csv:

	for user in userData:
		user_tags = [question["tags"] for question in questionData for answer in answerData if question["question_id"] == answer["question_id"] and answer["owner"]["user_id"] == user["user_id"]]
		user_tags = set([tag for user_tags_elem in user_tags for tag in user_tags_elem])

		if "age" in user:
			for question in questionData:
				tags_common = [tag for tag in user_tags if tag in question["tags"]]

				mambo = [str(user['user_id']), str(question['question_id']), str(len(tags_common))]

				print("|".join(mambo),file= ratings_csv)

r_cols = ['user_id', 'question_id', 'rating']
ratings = pd.read_csv('ratings.csv', sep='|', names=r_cols, encoding='latin-1')

#print(ratings)
	
r_cols = ['user_id', 'question_id', 'rating']
ratings_base = pd.read_csv('ratings-base.csv', sep='|', names=r_cols, encoding='latin-1')
ratings_test = pd.read_csv('ratings-test.csv', sep='|', names=r_cols, encoding='latin-1')
print(ratings_base.shape, ratings_test.shape)

train_data = graphlab.SFrame(ratings_base)
test_data = graphlab.SFrame(ratings_test)


#Train Model
item_sim_model = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='question_id', target='rating', similarity_type='pearson')

HOST = 'localhost'   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code : ' , str(msg[0]) , ' Message ' , msg[1])
    sys.exit()
     
print ('Socket bind complete:', s )
 
#Start listening on socket
s.listen(10)
print ('Socket now listening')
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    connection, addr = s.accept()
    if connection :
		data = connection.recv(16)
		#print(data)
		split=str(data).split(' ')
		print(split[0]  , split[1])
		makeRecomendation(int(split[0]),int(split[1]),item_sim_model)
		recommendationFile = open("recomendations.csv", 'r')
		recommendationData = recommendationFile.read();
		connection.send(recommendationData.encode())
s.close()

