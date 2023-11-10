# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================


import socket                                                  # Library needed for sockets
import threading                                               # Library for threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost need this
server.bind(("localhost", 12321))                               # Binds the sockets to host and port 
server.listen(2)                                                # listen to request of server from closer


class Network:                                                  # where we can connect to server and manage data around
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost need this
        self.server = "localhost"
        self.port = 12321
        self.address = (self.server, self.port)
        self.position = self.connect()

    def getposition(self):                                      # to get posititon
        return self.position
    
    def connect(self):                                          # 
        try: 
            self.client.connect(self)
            return self.client.recv(1024).decode()
        except:
            pass
    def send(self,data):
        try:
            self.client.send(str.encode(data))
            return self.cleint.recv(1024).decode()
        except socket.error as e:
            print(e)
            



def threading_client(clientSocket, player):                     # threading funnction to communicate with client
    msg = ''
    while True:
        try:
            data = clientSocket.recv(1024)                      # Infromation trying to receive 
            msg = data.decode('utf-8')                          # We need to decode infromation from utf-8 format

            if not data:                                        # if information from client is not working, we disconect
                print(f"Disconnected from player {player}")                           
                break
            else:                                                
                print(f"Received from player {player}: {msg}")
                clientSocket.send(data)                         # echo data  if data was received from client 
        except:                                                 # breaks if running to errors to avouid infiinte loop
            break
    print("Connection closed")
    clientSocket.close()



def main():                                                     # main function for the server 

    player = 0                                                  # creating player varaible 
    while True:                                         
        print("Waiting for connection ...")
        (clientSocket, clientAddress) = server.accept()
        print(f"Connection from {clientAddress}")
        client_thread = threading.Thread(target= threading_client, args= (clientSocket,player))
        player += 1
        client_thread.start()

if __name__ == "__main__":
    main()
    
# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games