# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
import pickle 

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

#global variables
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
messages = [0, 0]

# receive data from the given client
def receiveData(clientSocket, clientNum): 
    messages[clientNum-1] = pickle.loads(clientSocket.recv(1024)) #clientNum-1 because arrays are 0-indexed

#send data to the given client
def sendData(clientSocket, data):
    data_bytes = pickle.dumps(data)
    clientSocket.send(data_bytes)

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create server
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 12321))
    server.listen(5) #listen for 5 concurrent connection attempts

    #accept two connections
    print("Waiting for connection . . .")
    clientOneSocket, clientOneAddress = server.accept()
    print(f"received connection from {clientOneAddress}")

    print("Waiting for connection . . .")
    clientTwoSocket, clientTwoAddress = server.accept()
    print(f"received connection from {clientTwoAddress}")

    #assign sides, determine screen size
    msg = (SCREEN_WIDTH, SCREEN_HEIGHT, "left")
    msg_bytes = pickle.dumps(msg)
    clientOneSocket.send(msg_bytes)

    msg = (SCREEN_WIDTH, SCREEN_HEIGHT, "right")
    msg_bytes = pickle.dumps(msg)
    clientTwoSocket.send(msg_bytes)

    spectatorSockets = []
    
    while (True): #repeat until connection is broken
        #listen for spectator connections
        server.listen(5)
        

        #receive data first
        thread1 = threading.Thread(target=receiveData, args=(clientOneSocket, 1,))
        thread2 = threading.Thread(target=receiveData, args=(clientTwoSocket, 2,))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        #then send data
        thread1 = threading.Thread(target=sendData, args=(clientOneSocket, messages[1],))
        thread2 = threading.Thread(target=sendData, args=(clientTwoSocket, messages[0],))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        #check if the game is over
        #if so, end connections and break out of the loop
        if (messages[0][2] > 4 or messages[0][3] > 4):
            clientOneSocket.close()
            clientTwoSocket.close()
            server.close()
            break