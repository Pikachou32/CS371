# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================


import socket                                                  # Library needed for sockets
import threading                                               # Library for threading

def threading_client(clientSocket, clientAddress):
    print(f"Connected to {clientAddress}")

    while True:
        try:
            data = clientSocket.recv(1024)
            if not data:
                break                                         # Exit  loop if no data is received from client

            decoded_data = data.decode('utf-8')
            print(f"Received from {clientAddress}: {decoded_data}")
            clientSocket.sendall(data)
        except Exception as e:
            print(f"Error: {e}")
            break   
            






def main():                                                     # main function for the server 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost need this
    server.bind(("localhost", 12321))                               # Binds the sockets to host and port 
    server.listen(2)                                                # listen to request of server from closer


    while True:                                         
        print("Waiting for connection ...")
        (clientSocket, clientAddress) = server.accept()
        print(f"Connection from {clientAddress}")
        client_thread = threading.Thread(target= threading_client, args= (clientSocket,clientAddress))
        client_thread.start()


if __name__ == "__main__":
    main()
    
# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games