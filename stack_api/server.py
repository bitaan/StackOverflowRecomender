#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Simple socket server using threads
'''
from StringIO import StringIO
import socket
import sys
import json
 



def getRecomendations( id_user , numRec ):
	print(id_user, "\t",numRec)
	return [1,2,3,4,5]


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
    	 print (split[0] , "  " , split[1])
    	 rec = getRecomendations( split[0] , split[1] )
    	 print(rec)
    	 msg =  StringIO()
    	 json.dump(rec,msg)
    	 connection.send(msg.getvalue())
s.close()



