from __future__ import print_function
import json
from pandas.io.json import json_normalize
import pandas as pd
import graphlab
import socket
import sys



##combine models
def makeRecomendationPearson( id_user , numRec, itemModel):
	#Make Recommendations:
	item_sim_recomm = itemModel.recommend(users=[id_user],k=numRec)
	item_sim_recomm.print_rows(num_rows=numRec)

	with open("recomendationsPearson.csv",'w') as recommendationsPearson_csv:

		print(item_sim_recomm,file=recommendationsPearson_csv)

def makeRecomendationJaccard( id_user , numRec, itemModel):
	#Make Recommendations:
	item_sim_recomm = itemModel.recommend(users=[id_user],k=numRec)
	item_sim_recomm.print_rows(num_rows=numRec)

	with open("recomendationsJaccard.csv",'w') as recommendationsJaccard_csv:

		print(item_sim_recomm,file=recommendationsJaccard_csv)

def makeRecomendationCosine( id_user , numRec, itemModel):
	#Make Recommendations:
	item_sim_recomm = itemModel.recommend(users=[id_user],k=numRec)
	item_sim_recomm.print_rows(num_rows=numRec)

	with open("recomendationsCosine.csv",'w') as recommendationsCosine_csv:

		print(item_sim_recomm,file=recommendationsCosine_csv)

		
		
		
#pre-process data
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


#add more tags? python request for tags 			
tags = ['git', 'java', 'python', 'sql', 'android','r','jquery','panda','html','css']


with open("questions.csv",'w') as questions_csv:
	for line in questionData:
		mambo = [str(line['question_id']), str(line['answer_count']), str(line['score'])]
		for tag in tags:
			mambo.append("1" if tag in line['tags'] else "0")
		print("|".join(mambo), file = questions_csv)

		
		
##TODO : using fuzzy c-means do user-user similarity -> cluster users 


## prep users df
u_cols = ['user_id', 'age', 'user_type', 'reputation']
users = pd.read_csv('users.csv', sep='|', names=u_cols, encoding='latin-1')
#sprint(users)

##prep questions df
q_cols = ['question_id', 'answer_count', 'score'] + tags
questions = pd.read_csv('questions.csv', sep='|', names=q_cols, encoding='latin-1')
#print(questions)

##prep rating 
##combine users and questions 
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

##set training data
r_cols = ['user_id', 'question_id', 'rating']
ratings_base = pd.read_csv('ratings-base.csv', sep='|', names=r_cols, encoding='latin-1')
ratings_test = pd.read_csv('ratings-test.csv', sep='|', names=r_cols, encoding='latin-1')
print(ratings_base.shape, ratings_test.shape)
##cast to 
train_data = graphlab.SFrame(ratings_base)
test_data = graphlab.SFrame(ratings_test)



## TODO: Why not implement Simple Popularity Model and use it for result comparisson?? 1liner


#Train Model
item_sim_model_pearson = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='question_id', target='rating', similarity_type='pearson')
item_sim_model_cosine = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='question_id', target='rating', similarity_type='cosine')
item_sim_model_jaccard = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='question_id', target='rating', similarity_type='jaccard')
##compare models 
##                                              #data #models, #modelnames simple,pearson,cosine,jaccard  OPTIONAL #metric #target  
##graphlab.recommender.util.compare_models(test_data, [m1, m2], model_names=["m1", "m2"])
##util.compare_models



#Evaluating Recommendation Engines
##model_performance = graphlab.compare(test_data, [popularity_model, item_sim_model])
#show recall precision
##graphlab.show_comparison(model_performance,[popularity_model, item_sim_model])
#op Why not pass this values to Recomender Agent



HOST = 'localhost'
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# expects requests  userId,setSize,type[1,3] 
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code : ' , str(msg[0]) , ' Message ' , msg[1])
    sys.exit()
s.listen(10)
print ('Socket now listening')
#wait conections
while 1:
    connection, addr = s.accept()
    if connection :
		data = connection.recv(16)
		#print(data)
		split=str(data).split(' ')
		print(split[0]  , split[1], split[2])
		if int(split[2]) == 1:
			makeRecomendationPearson(int(split[0]),int(split[1]),item_sim_model_pearson)
			recommendationFile = open("recomendationsPearson.csv", 'r')
			recommendationData = recommendationFile.read();
			connection.send(recommendationData.encode())
		elif int(split[2]) == 2:
			makeRecomendationCosine(int(split[0]),int(split[1]),item_sim_model_cosine)
			recommendationFile = open("recomendationsCosine.csv", 'r')
			recommendationData = recommendationFile.read();
			connection.send(recommendationData.encode())
		else:
			makeRecomendationJaccard(int(split[0]),int(split[1]),item_sim_model_jaccard)
			recommendationFile = open("recomendationsJaccard.csv", 'r')
			recommendationData = recommendationFile.read();
			connection.send(recommendationData.encode())
s.close()





