Contact Info
============

Group Members & Email Addresses:

    Victor Avalos-Lopez 1, vhav222@uky.edu
    Willow Jordan 2, wtjo230@uky.edu
    Clayton Davis 3, cada231@uky.edu


Versioning
==========

Github Link: https://github.com/Pikachou32/CS371 

General Info
============
This file describes how to install/run your program and anything else you think the user should know

You'll also want to find your ip and put it in the pongServer.py before running any of the code:
server.bind(("172.20.10.2", 12321))
where the "172.20.10.2" would be changed to be your IP

To run, you'll need be able to run the server and client. running the client is by downloads everything and opening the folder. while in the folder you'll want to do : 

cd pong

This will allow you to be able to acess the client and server code
After those changes are made, you'll need to do type this command line while inside your "cd pong" to run the server
python3 pongServer.py

it'll display the ip and port when ran so you don't have to look into your code again

On a seperate terminal you'll need to run "cd pong" as well and run:
python3 pongClient.py

This will allow you to run the client, you'll have to type in the port number and IP for it to connect to the server after that, you click join and enjoy



Install Instructions
====================

Run the following line to install the required libraries for this project:

`pip3 install -r pygame`

Known Bugs
==========
- ball goes crazy on zigzaggs
- ball doesn't reset after a score 

