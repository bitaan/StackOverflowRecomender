import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 6022))
while 1:
    data = input ( "Enter text to be upper-cased, q to quit\n")
    data += "\n"
    client_socket.send(data.encode())
    print ("data sent" , data.encode())
    if ( data == 'q' or data == 'Q'):
        client_socket.close()
        break;
    else:        
        data = client_socket.recv(5000)
        print ("Your upper cased text:" , data.decode())