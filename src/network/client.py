import sys
import socket
import threading

class Client:
    PORT = 5050
    BUF_SIZE = 1024
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "__disconnect__"

    def __init__(self, serverIp):
        self.serverIp = serverIp
        self.addr = (self.serverIp, Client.PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self, onConnectionClosed, onMessageReceived):
        thread = threading.Thread(target=self.__connect, args = (onConnectionClosed, onMessageReceived))
        thread.start()

    def __connect(self, onConnectionClosed, onMessageReceived):
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
                    onMessageReceived(message)

        except:
            connectionAborted = True
        
        if not connectionAborted:
            self.client.close()
            self.connected = False
            onConnectionClosed()
            Client.print_immediately("[Client] Disconnected")

    def send(self, message):
        message = message.encode(Client.FORMAT)
        self.client.send(message)

    def close(self):
        self.client.close()

    def isConnected(self):
        return self.connected

    @staticmethod
    def print_immediately(s):
        print(s)
        sys.stdout.flush()