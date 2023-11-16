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


def clientHandler(clientSocket, player, other_client ):
    #choosing sides
    if player == 0:
        side = "left"
    else:
        side = "right"
    #sending informationt to client
    sync_player = [0, 0]
    setup_info = {'screen_width': SCREEN_WIDTH, 'screen_height': SCREEN_HEIGHT, 'player_side': side}
    clientSocket.sendall(pickle.dumps(setup_info))
    data = " "
    while True:
        try:
            data = clientSocket.recv(1024)
            game_state = pickle.loads(data)

            if not data:
                print(f"Disconnected from player: {[player]}")
                break          
            else:
                print(f"received from player: {player}: ", game_state)
                print(f"sending from player : {player}: ", game_state)

# Update the server's internal game state

            server_player_paddle_y = game_state['player_paddle']
            server_opponent_paddle_y = game_state['opponent_paddle']
            server_ball_position = game_state['ball']
            server_l_score = game_state['l_score']
            server_r_score = game_state['r_score']


# Send the updated game state to both players
            game_state['player_paddle'] = server_player_paddle_y
            game_state['opponent_paddle'] = server_opponent_paddle_y
            game_state['ball'] = server_ball_position
            game_state['l_score'] = server_l_score
            game_state['r_score'] = server_r_score

            if other_client is not None:
                other_client.sendall(pickle.dumps(game_state))
            clientSocket.sendall(pickle.dumps(game_state))
        
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

    while True:
        clientSocket, clientAddress = server.accept()
        print(f"connected to: {clientAddress}")
        # Store the client socket in the list
        client_sockets[player] = clientSocket
    
    
        client_thread = threading.Thread(target=clientHandler, args=(clientSocket,player, client_sockets[1- player]) )
        client_thread.start()
        player += 1

        if player == 2:
            break

