#!/usr/bin/env python3
# Threaded server allowing multiple connections
# -*- coding: utf-8 -*-

import os
import socket
import time
from threading import Thread, Event

# Set up port information
host = '127.0.0.1'#localhost
port = 12345
BUFSIZE = 1040
MAXCONNS = 2

class Client(Thread):
    """Client handling, given the socket, address, a name to use, a wait event, and chat data."""
    def __init__(self, socket, address, name, chatData):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.name = name
        self.data = chatData
        self.active = False
        self.recvData = None
        self.start()
    
    def run(self):
        self.active = True
        while self.active:
            try:
                self.recvData = self.sock.recv(BUFSIZE)
            except OSError as e:
                self.data.append([self.name, '[S] bye'])
                self.active = False
            else:
                if not self.recvData or self.recvData == b'' or closeWaitEvent.is_set():
                    self.data.append([self.name, '[S] bye'])
                    self.active = False
                else:
                    self.data.append([self.name, self.recvData.decode('utf-8')])
        self.sock.close()
        print('Client Connection Terminated', file=os.sys.stderr)
    
    def send_all(self, data):
        if self.active:
            self.sock.sendall(data)
    pass

def getServer():
    # Initialize the socket
    s = socket.socket()
    
    print('Attempting to bind socket to %s:%i...' % (host, port))

    # Bind the socket to a local address.
    s.bind((host, port))
        
    # Enable a server to accept connections.
    # specifies the number of unaccepted connections that the
    # system will allow before refusing new connections.
    s.listen(MAXCONNS)
    return s

def run():
    global clients
    global closeWaitEvent
    global serversocket
    global chatData
    clients = {}
    closeWaitEvent = Event()
    # Set up a list to hold chat data
    chatData = []
    
    # Get the ip address we are working on
    ip_addr = ':'.join([str(i) for i in serversocket.getsockname()])
    
    print('Server and running on.', ip_addr)
    print('Awaiting %i connections.' % MAXCONNS)
    
    # Server should only permit a certain number of connections; No more, no less
    cid = 0
    idToAddr = {}
    # While there are spots to be filled,
    while len(clients) < MAXCONNS:
        # Accept any new connections
        clientSock, addr = serversocket.accept()
        print('New Connection', addr, 'id is', cid)
        print(cid, 'Of', MAXCONNS, 'Achieved')
        # Remember the address based on client id
        idToAddr[cid] = addr
        # Initialize a new client thread and add it to the list of clients
        clients[cid] = Client(clientSock, addr, int(cid), chatData)
        # Increment the client id value
        cid += 1
    print('All connections established.')
    # Tell all connected clients all connected users
    # Get the client names and seperate them by slashes
    clientNames = '/'.join([str(i) for i in clients.keys()])
    # For each connected client,
    for client in clients.values():
        # Get the text ready to send
        send = 'You: "%s" Clients: "%s";' % (str(client.name), clientNames)
        # Send the text to the client with the utf-8 encoding
        client.send_all(send.encode('utf-8'))
    
    print('Beginning Chat')
    # While no inactive clients exist,
    while not (False in [client.is_alive() for client in clients.values()]):
        try:
            # If there is chat data,
            if chatData:
                # For each message, print it
                for i in ['From: '+str(i[0])+' : '+i[1] for i in chatData]:
                    print(i)
                # Seperate message data from client id data
                messages = [i[1]+';' for i in chatData]
                # Get the "To" address lines from each message
                to_ids = [m.split(' ')[0][1:-1] for m in messages]
                # If there are messages addressed to server,
                if 'S' in to_ids:
                    # Get the server message
                    srvrmsg = messages[to_ids.index('S')]
                    # If the message contains the word 'bye',
                    if 'bye' in srvrmsg.split(' '):
                        # Close the server.
                        cidx = chatData[messages.index(srvrmsg)][0]
                        print("Client %s said 'bye'. Closing server." % str(cidx))
                        break
                # For each client,
                for client in iter(clients.values()):
                    # Get the client's id
                    cid = client.name
                    # If the client's id is the "to" address line in a message,
                    if cid in to_ids:
                        # Send that client the message addressed to them
                        print('Sending', cid, 'Message', messages[to_ids.index(cid)])
                        client.send_all(messages[to_ids.index(cid)].encode('utf-8'))
                # When done processing chat data, delete it all
                del chatData[:]
        except KeyboardInterrupt:
            break
    # Once there is an inactive client,
    for client in clients.values():
        # Tell all clients to disconnect
        client.send_all(b';bye')
    # Close the server socket
    serversocket.close()
    # Tell all client threads that may still be active to close
    closeWaitEvent.set()
    print('Server shutting down... Waiting five secconds for all threads to stop.')
    time.sleep(5)
    # Find any clients that didn't listen
    alives = [i for i in clients.values() if i.is_alive()]
    # If any threads aren't listening,
    if alives:
        print('%i client(s) is still active!' % len(alives))
        # Tell all alive clients to close their sockets
        for client in alives:
            client.sock.close()
        # Try to wait for child processes to quit
        try:
            os.wait()
        except ChildProcessError as e:
            # If it breaks (most of the time because everything quit),
            # Print the error message
            print(e)
    print('All connections should now be terminated.')

if __name__ == '__main__':
    try:
        serversocket = getServer()
    except OSError as e:
        print(str(e), file=os.sys.stderr)
        input('Press Enter to Continue.\n')
    else:
        try:
            run()
        except BaseException as e:
            print(e, os.sys.stderr)
    # Ensure the server socket closes no matter what.
    try:
        serversocket.close()
    except BaseException:
        pass
