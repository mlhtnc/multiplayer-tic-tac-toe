import sys
import socket
import threading

sys.path.append('../helpers/event')
sys.path.append('../helpers/logger')

from event import Event
from logger import log

class Client:
    PORT = 5050
    BUF_SIZE = 1024
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "__disconnect__"

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

        self.onConnected = Event()
        self.onMessageReceived = Event()
        self.onConnectionClosed = Event()

    def __setServerIp(self, serverIp):
        self.serverIp = serverIp
        self.addr = (self.serverIp, Client.PORT)

    def connect(self, serverIp):
        self.__setServerIp(serverIp)

        thread = threading.Thread(target=self.__connect)
        thread.start()

    def __connect(self):
        connected = True
        connectionAborted = False

        try:
            self.client.connect(self.addr)
            self.connected = True
            self.onConnected()
            log("[Client] Connected")

            while connected and not connectionAborted:
                message = self.client.recv(Client.BUF_SIZE)
                message = message.decode(Client.FORMAT)

                if message == Client.DISCONNECT_MESSAGE:
                    connected = False
                else:
                    self.onMessageReceived(message)

        except:
            connectionAborted = True
        
        if not connectionAborted:
            self.client.close()
            self.connected = False
            self.onConnectionClosed()
            log("[Client] Disconnected")

    def send(self, message):
        message = message.encode(Client.FORMAT)
        self.client.send(message)

    def close(self):
        self.client.close()

    def isConnected(self):
        return self.connected