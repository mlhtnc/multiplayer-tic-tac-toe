import socket
import struct
import threading

class Multicaster:
    MCAST_GROUP = '224.1.1.1'
    MCAST_PORT = 5004
    TTL = 1
    BUF_SIZE = 1024
    FORMAT = "utf-8"

    def __init__(self):
        # NIC (Network Interface Card)
        self.nicIp = Multicaster.getNicIp()

    def initSender(self):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, Multicaster.TTL)
        self.sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.nicIp))

    def initReceiver(self):
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.receiver.bind(('', Multicaster.MCAST_PORT))
        mreq = struct.pack("=4s4s", socket.inet_aton(Multicaster.MCAST_GROUP), socket.inet_aton(self.nicIp))
        self.receiver.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def send(self, message):
        message = message.encode(Multicaster.FORMAT)
        self.sender.sendto(message, (Multicaster.MCAST_GROUP, Multicaster.MCAST_PORT))

    def receive(self, onMessageReceived):
        thread = threading.Thread(target=self.__receive, args = (onMessageReceived,))
        thread.start()

    def __receive(self, onMessageReceived):
        buf, senderaddr = self.receiver.recvfrom(Multicaster.BUF_SIZE)
        message = buf.decode(Multicaster.FORMAT)
        onMessageReceived(message)

    def closeSender(self):
        self.sender.close()

    def closeReceiver(self):
        self.receiver.close()

    @staticmethod
    def getNicIp():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        nicIp = sock.getsockname()[0]
        sock.close()
        return nicIp