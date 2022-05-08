import sys
from client import Client

def print_immediately(s):
    print(s)
    sys.stdout.flush()

def onConnectionClosed():
    print_immediately("Connection is closed")

def onMessageReceived(message):
    print_immediately(message)

c = Client('192.168.1.31')
c.connect(onConnectionClosed, onMessageReceived)

while True:
    inp = input()

    if not c.isConnected():
        print("No connection, could not send the message")
        break

    c.send(inp)

    if inp == Client.DISCONNECT_MESSAGE:
        c.close()
        break