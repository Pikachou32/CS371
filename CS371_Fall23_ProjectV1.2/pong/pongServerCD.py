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

#define these ahead of time?
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
messages = [0, 0]

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

# Communication protocol for client-server
def clientHandler(clientSocket, clientAddress, clientNum):
    try:
        while (True):
            if (clientNum == 0):
                clientOneGameState = pickle.loads(clientSocket.recv(1024))
            else:
                clientTwoGameState = pickle.loads(clientSocket.recv(1024))
            
        # Variable to hold each sync variable to determine how out of sync
        clientOneSync = clientOneGameState[4]
        clientTwoSync = clientTwoGameState[4]

        # Determine which game state is sent back to each client
        if (clientOneSync < clientTwoSync):
            gameState = pickle.dumps(clientTwoGameState)
            clientSocket.send(gameState)
        else:
            gameState = pickle.dumps(clientOneGameState)
            clientSocket.send(gameState)

    finally:
        server.close()
        thread1.join()
        thread2.join()



if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create server
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 12321))
    print("Awaiting connection...")
    server.listen(5) #listen for 5 concurrent connection attempts

    #accept two connections
    clientOneSocket, clientOneAddress = server.accept()
    clientTwoSocket, clientTwoAddress = server.accept()
    print("Both clients have connected, running initial setup")

    clientOne = (clientOneSocket, clientOneAddress, 0)
    clientTwo = (clientTwoSocket, clientTwoAddress, 1)

    #assign sides, determine screen size
    msg = (SCREEN_WIDTH, SCREEN_HEIGHT, "left")
    message = pickle.dumps(msg)
    clientOneSocket.send(message)

    msgTwo = (SCREEN_WIDTH, SCREEN_HEIGHT, "right")
    messageTwo = pickle.dumps(msgTwo)
    clientTwoSocket.send(messageTwo)

    print("Initial setup complete, starting game loop")
    while (True): #repeat until connection is broken
        #receive data first
        thread1 = threading.Thread(target=clientHandler, args=(clientOne))
        thread2 = threading.Thread(target=clientHandler, args=(clientTwo))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        #check if the game is over
        #if so, end connections and break out of the loop
        if (messages[0][2] > 4 | messages[0][3] > 4):
            clientOneSocket.close()
            clientTwoSocket.close()
            server.close()
            break
