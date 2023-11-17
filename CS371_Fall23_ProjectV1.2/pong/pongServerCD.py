#=======================================================================================
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
lock = threading.Lock()
BUFFER_SIZE = 1024
# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

# Declare the default server state
server_sync = 0
server_leftPaddle = 0
server_rightPaddle = 0
server_ballX = 55
server_ballY = 55
server_lScore = 0
server_rScore = 0

def clientHandler(clientSocket, player, other_client):
    # choosing sides
    if player == 0:
        side = "left"
        paddle = "left"
    else:
        side = "right"
        paddle = "right"

    # global variables to be updated with each client connection
    global server_sync, server_leftPaddle, server_rightPaddle, server_ballX, server_ballY, server_lScore, server_rScore

    server_currentPaddle = 55

    # sending information to client
    setup_info = {'screen_width': SCREEN_WIDTH, 'screen_height': SCREEN_HEIGHT, 'player_side': side}
    clientSocket.sendall(pickle.dumps(setup_info))
    
    while True:
        try:
            
            with lock:
                data = clientSocket.recv(BUFFER_SIZE)
                game_state = pickle.loads(data)

                if (game_state['sync'] > server_sync):
                    server_sync = game_state['sync']
                    server_currentPaddle = game_state['player_paddle']
                    server_ballX = game_state['ballX']
                    server_ballY = game_state['ballY']
                    server_lScore = game_state['l_score']
                    server_rScore = game_state['r_score']

                    # Determine which paddle is the current paddle
                    if (paddle == "left"):
                        server_leftPaddle = server_currentPaddle
                    else:
                        server_rightPaddle = server_currentPaddle


                if not data:
                    print(f"Disconnected from player: {[player]}")
                    break
                else:
                    print(f"received from player {player}: {game_state}")
                    server_state = {
                        'sync': server_sync,
                        'left_paddle': server_leftPaddle,
                        'right_paddle': server_rightPaddle,
                        'ballX': server_ballX,
                        'ballY': server_ballY,
                        'l_score': server_lScore,
                        'r_score': server_rScore
                    }

                    gameUpdate = pickle.dumps(server_state)
                    clientSocket.send(gameUpdate)


                # Update the other client with the received game state
                if other_client is not None:
                    other_client.sendall(pickle.dumps(game_state))

        except Exception as e:
            print(f"Error in player {player}: {e}")
            break

            


if __name__ == "__main__":    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          # create server
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        #allows us to use "Local host"
    server.bind(("localhost", 12321))
    server.listen(5)  # listen for 5 concurrent connection attempts

    print("Awaiting connection...")
    player = 0
    client_sockets = [None, None]
    with lock:
        clientSocket, clientAddress = server.accept()
        print(f"connected to: {clientAddress}")
        # Store the client socket in the list
        client_sockets[player] = clientSocket
        client_thread = threading.Thread(target=clientHandler, args=(clientSocket,player, client_sockets[1- player]) )
        player += 1
    with lock:
        clientSocket, clientAddress = server.accept()
        print(f"connected to: {clientAddress}")
        client_thread2 = threading.Thread(target=clientHandler, args=(clientSocket, player, client_sockets[1 - player]))
        client_thread.start()
        client_thread2.start()
