import sys
import time

sys.path.append('..')

from server import Server


def print_immediately(s):
    print(s)
    sys.stdout.flush()

def onConnected(addr):
    print_immediately(str(addr) + " is connected")

def onConnectionClosed(addr):
    if addr != None:
        print_immediately(str(addr) + " is disconnected")
    
    global waitForServerThread
    waitForServerThread = False

def onMessageReceived(message):
    print_immediately(message)


waitForServerThread = True

s = Server()
s.listen(onConnected, onMessageReceived, onConnectionClosed)

while True:
    inp = input()

    if not s.isConnected():
        print("No connection, could not send the message")
        s.close()
        break

    s.send(inp)

    if inp == Server.DISCONNECT_MESSAGE:
        s.close()
        break

while waitForServerThread:
    time.sleep(0.25)
