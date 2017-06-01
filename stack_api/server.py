#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Simple socket server using threads
'''
 
import socket
import sys
 
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
    	 print (data)
s.close()