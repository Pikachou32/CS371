# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

#define these ahead of time?
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

# function to communicate with a given client
def func(clientSocket, clientAddress) #XXX: CHANGE FUNCTION NAME
    while (true)



if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create server
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 12321))
    server.listen(5) #listen for 5 concurrent connection attempts

    #accept two connections
    clientOneSocket, clientOneAddress = server.accept()
    clientTwoSocket, clientTwoAddress = server.accept()

    #assign sides, determine screen size
    msg = (SCREEN_WIDTH, SCREEN_HEIGHT, "left")
    clientOneSocket.send(msg)

    msg = (SCREEN_WIDTH, SCREEN_HEIGHT, "right")
    clientTwoSocket.send(msg)

    #create threads
    thread1 = threading.Thread(target=func, args=(clientOneSocket, clientOneAddress,))
    thread2 = threading.Thread(target=func, args=(clientTwoSocket, clientTwoAddress,))

    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()

    #print exit message or something
    #basically do whatever needs to be done after the game is over