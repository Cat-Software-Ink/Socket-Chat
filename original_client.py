#!/usr/bin/env python3
# Simple socket client test
# -*- coding: utf-8 -*-

import os, socket

host = '127.0.0.1'
port = 12345
bufsize = 1040

# Initialize the socket
s = socket.socket()
# Setup the timeout time, in this none so it doesn't time out
s.settimeout(None)

# Connect the socket to a remote address.
#s.connect(('127.0.0.1',12345))

# This is like connect(address), but returns an error code (the errno value)
# instead of raising an exception when an error occurs.
connErrCode = s.connect_ex((host, port))

if connErrCode:
    print('Error: '+os.strerror(connErrCode), file=os.sys.stderr)
else:
    while True:
        sendData = input('Send: ')
        # Send a data string to the socket.
        # Return the number of bytes
        # sent; this may be less than len(data) if the network is busy.
        sentBytes = s.send(sendData.encode())
        #sendall sends everything
        if sendData.lower() == 'bye':
            break
        # Receive up to buffersize bytes from the socket.
        rcvdData = s.recv(bufsize).decode()
        print('Recieve: ' + rcvdData)
        if rcvdData.lower() == 'bye':
            break
    try:
        s.send(b'bye')
    except BaseException:
        pass
# Close the socket.  It cannot be used after this call.
s.close()
