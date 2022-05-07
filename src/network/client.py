import sys
import socket
import threading

class Client:
    PORT = 5050
    BUF_SIZE = 1024
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "__disconnect__"

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

        self.__messageReceivedCbs = []
        self.__connectionClosedCbs = []

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
            Client.print_immediately("[Client] Connected")

            while connected and not connectionAborted:
                message = self.client.recv(Client.BUF_SIZE)
                message = message.decode(Client.FORMAT)

                if message == Client.DISCONNECT_MESSAGE:
                    connected = False
                else:
                    self.notifyMessageReceivedCbs(message)

        except:
            connectionAborted = True
        
        if not connectionAborted:
            self.client.close()
            self.connected = False
            self.notifyConnectionClosedCbs()
            Client.print_immediately("[Client] Disconnected")

    def send(self, message):
        message = message.encode(Client.FORMAT)
        self.client.send(message)

    def close(self):
        self.client.close()

    def isConnected(self):
        return self.connected

    def notifyMessageReceivedCbs(self, message):
        for cb in self.__messageReceivedCbs:
            cb(message)

    def notifyConnectionClosedCbs(self):
        for cb in self.__connectionClosedCbs:
            cb()

    def addMessageReceivedCb(self, onMessageReceived):
        self.__messageReceivedCbs.append(onMessageReceived)

    def removeMessageReceivedCb(self, onMessageReceived):
        self.__messageReceivedCbs.remove(onMessageReceived)

    def addConnectionClosedCb(self, onConnectionClosed):
        self.__connectionClosedCbs.append(onConnectionClosed)

    def removeConnectionClosedCb(self, onConnectionClosed):
        self.__connectionClosedCbs.remove(onConnectionClosed)

    @staticmethod
    def print_immediately(s):
        print(s)
        sys.stdout.flush()