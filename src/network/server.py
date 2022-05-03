import sys
import socket 
import threading

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

    def listen(self, onConnected, onMessageReceived, onConnectionClosed):
        thread = threading.Thread(target=self.__listen, args = (onConnected, onMessageReceived, onConnectionClosed))
        thread.start()

    def __listen(self, onConnected, onMessageReceived, onConnectionClosed):
        self.server.listen()
        Server.print_immediately(f"[SERVER] Listening on {self.serverIp}")

        addr = None

        try:
            self.conn, addr = self.server.accept()
            onConnected(addr)
            
            connected = True
            connectionAborted = False
            while connected and not connectionAborted:
                message = self.conn.recv(Server.BUF_SIZE)
                message = message.decode(Server.FORMAT)

                if message == Server.DISCONNECT_MESSAGE:
                    connected = False
                else:
                    onMessageReceived(message)

        except:
            connectionAborted = True

        if not connectionAborted:
            self.conn.close()
        
        self.conn = None
        onConnectionClosed(addr)
            
    def send(self, message):
        if self.conn == None:
           Server.eprint_immediately(Server.NO_CONNECTION_MESSAGE)
           return

        self.conn.send(message.encode(Server.FORMAT))

    def close(self):
        if self.conn != None:
            self.conn.close()
        
        self.server.close()

    def isConnected(self):
        return self.conn != None

    def print_immediately(s):
        print(s)
        sys.stdout.flush()

    @staticmethod
    def eprint_immediately(s):
        print(s, file = sys.stderr)
        sys.stderr.flush()

    @staticmethod
    def getNicIp():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        nicIp = sock.getsockname()[0]
        sock.close()
        return nicIp
