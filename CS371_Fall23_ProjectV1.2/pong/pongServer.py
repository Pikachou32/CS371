# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import pickle 
import threading
#define these ahead of time?
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
messages = [0, 0]




# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

# receive data from the given client
def receiveData(clientSocket, clientNum): 
    try:
        while True:
            data = clientSocket.recv(1024)
            if not data:
                break
            data_received = pickle.loads(data)
            
            messages[clientNum -1] = data_received
    except Exception as e:
        print(f"Error receiving data from client {clientNum}: {e}")
    

#send data to the given client
def sendData(clientSocket, data):
    try:
        msg_bytes = pickle.dumps(data)
        clientSocket.send(msg_bytes)
    except  Exception as e:
        print(f"Error sending data to client: {e}")


def handle_client(client_socket, client_num):
    try:
        # Your code to send initial information to the client (e.g., screen size and side)
        initial_info = (SCREEN_WIDTH, SCREEN_HEIGHT, "left" if client_num == 1 else "right")
        msg_bytes = pickle.dumps(initial_info)
        client_socket.send(msg_bytes)

        while True:
            # Your main game loop logic goes here
            # Update game state, handle synchronization, etc.

            # Send data to the client
            data_to_send = messages[1 - client_num]  # Send the other client's data
            sendData(client_socket, data_to_send)

            # Receive data from the client
            receiveData(client_socket, client_num)
    except Exception as e:
        print(f"Error handling client {client_num}: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create server
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 12321))
    server.listen(5) #listen for 5 concurrent connection attempts

    #accept two connections
    print("Waiting for connection . . .")
    ClientOneSocket, clientOneAddress = server.accept()
    print(f"received connection from {clientOneAddress}")

    print("Waiting for connection . . .")
    ClientTwoSocket, clientTwoAddress = server.accept()
    print(f"received connection from {clientTwoAddress}")

        




   
    try:
        while (True): #repeat until connection is broken
        #receive data first
            thread1 = threading.Thread(target=handle_client, args=(ClientOneSocket, 1,))
            thread2 = threading.Thread(target=handle_client, args=(ClientTwoSocket, 2,))
            thread1.start()
            thread2.start()
            thread1.join()
            thread2.join()
    except Exception as e:
        print("An error occured: {e}")
    finally:
        ClientOneSocket.close()
        ClientTwoSocket.close()
        server.close()

