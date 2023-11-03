# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

#Librarys needed 
import socket
import threading      

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost need this

server.bind(("localhost", 12321))                               # Binds the sockets to host and port 
server.listen(5)                                                # listen to request of server from closer


clients = []                                                    # List to store clients

while len(clients) < 2:                                         # Making sure we have 2 clients connected
    print("Waiting for Player 1 to connect . . .")
    clientSocket, clientAddress = server.accept()
    print(f"Connecion from Player 1 {clientAddress}")           # verifies connection
    clients.append(clientSocket)                                # Store clients into list
    print("Waiting for Player 2 to connect . . .")
    clientSocket, clientAddress = server.accept()
    print(f"Connecion from Player 2 {clientAddress}")
    clients.append(clientSocket)

breakpoint                          



    

message = clientSocket.recv(1024)               # Expect "Hello Server"




print(f"Client sent: {message.decode()}")

clientSocket.send("Hello client.".encode())

clientSocket.close()
server.close()





# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games