import sys
import socket 
import threading

sys.path.append('../helpers/event')
sys.path.append('../helpers')

from event import Event
from logger import log, logError

class Server:
    PORT = 5050
    BUF_SIZE = 1024
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "__disconnect__"
    NO_CONNECTION_MESSAGE = "[SERVER] There is no connection, could not send the message"

    def __init__(self):
        self.serverIp = Server.getNicIp()
        self.addr = (self.serverIp, Server.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.addr)
        self.conn = None

        self.onConnected = Event()
        self.onMessageReceived = Event()
        self.onConnectionClosed = Event()

    def listen(self):
        thread = threading.Thread(target=self.__listen)
        thread.start()

    def __listen(self):
        self.server.listen()
        log(f"[SERVER] Listening on {self.serverIp}")

        addr = None

        try:
            self.conn, addr = self.server.accept()
            self.onConnected(addr)
            
            connected = True
            connectionAborted = False
            while connected and not connectionAborted:
                message = self.conn.recv(Server.BUF_SIZE)
                message = message.decode(Server.FORMAT)

                if message == Server.DISCONNECT_MESSAGE:
                    connected = False
                else:
                    self.onMessageReceived(message)

        except:
            connectionAborted = True

        if not connectionAborted:
            self.conn.close()
        
        self.conn = None
        self.onConnectionClosed(addr)
            
    def send(self, message):
        if self.conn == None:
           logError(Server.NO_CONNECTION_MESSAGE)
           return

        self.conn.send(message.encode(Server.FORMAT))

    def close(self):
        if self.conn != None:
            self.conn.close()
        
        self.server.close()

    def isConnected(self):
        return self.conn != None

    @staticmethod
    def getNicIp():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        nicIp = sock.getsockname()[0]
        sock.close()
        return nicIp
