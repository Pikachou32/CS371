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
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
messages = [0, 0]
lock = threading.Lock()

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

# Communication protocol for client-server
def clientHandler(clientOneSocket, clientTwoSocket):
    try:
        while (True):
                clientOneGameState = pickle.loads(clientOneSocket.recv(1024))
                clientTwoGameState = pickle.loads(clientTwoSocket.recv(1024))
            
                # Thread lock to prevent sync updates during calculation
                with lock:
                
                    # Variable to hold each sync variable to determine how out of sync
                    clientOneSync = clientOneGameState['sync']
                    clientTwoSync = clientTwoGameState['sync']
                

                    # Determine which game state is sent back to each client
                    if (clientOneSync < clientTwoSync):
                        gameState = pickle.dumps(clientTwoGameState)
                        clientOneSocket.send(gameState)
                    else:
                        gameState = pickle.dumps(clientOneGameState)
                        clientTwoSocket.send(gameState)

    finally:
        server.close()



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


    #assign sides, determine screen size
    msg = {'screen_width': SCREEN_WIDTH, 'screen_height': SCREEN_HEIGHT, 'player_side': 'left'}
    message = pickle.dumps(msg)
    clientOneSocket.send(message)

    msgTwo = {'screen_width': SCREEN_WIDTH, 'screen_height': SCREEN_HEIGHT, 'player_side': 'right'}
    messageTwo = pickle.dumps(msgTwo)
    clientTwoSocket.send(messageTwo)

    print("Initial setup complete, starting game loop")
        #receive data first
    thread1 = threading.Thread(target=clientHandler, args=(clientOneSocket, clientTwoSocket))
    thread2 = threading.Thread(target=clientHandler, args=(clientTwoSocket, clientOneSocket))
    thread1.start()
    thread2.start()
