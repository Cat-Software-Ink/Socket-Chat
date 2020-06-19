#!/usr/bin/env python3
# Simple socket server test
# -*- coding: utf-8 -*-

import socket

# Initialize the socket
s = socket.socket()
# Set up port information
host = '127.0.0.1'#localhost
port = 12345
# Bind the socket to a local address.
s.bind((host, port))
# Enable a server to accept connections.
s.listen(5)
c, addr = s.accept()
print('Socket Up and running with a connection from', addr)
while True:
    rcvdData = c.recv(1024).decode()
    print('Recieved: '+rcvdData)
    if rcvdData.lower() == 'bye':
        break
    sendData = input("Send: ")
    c.send(sendData.encode())
    if sendData == "Bye" or sendData == "bye":
        break
c.close()
