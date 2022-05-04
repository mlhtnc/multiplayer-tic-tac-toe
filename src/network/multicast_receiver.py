import socket
import struct
import threading

class MulticastReceiver:
    MCAST_GROUP = '224.1.1.1'
    MCAST_PORT = 5004
    BUF_SIZE = 1024
    FORMAT = "utf-8"

    def __init__(self):
        # NIC (Network Interface Card)
        self.nicIp = MulticastReceiver.getNicIp()
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.receiver.bind(('', MulticastReceiver.MCAST_PORT))
        mreq = struct.pack("=4s4s", socket.inet_aton(MulticastReceiver.MCAST_GROUP), socket.inet_aton(self.nicIp))
        self.receiver.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def receive(self, onMessageReceived):
        thread = threading.Thread(target=self.__receive, args = (onMessageReceived,))
        thread.start()

    def __receive(self, onMessageReceived):
        try:
            buf, senderaddr = self.receiver.recvfrom(MulticastReceiver.BUF_SIZE)
            if senderaddr[0] != self.nicIp:
                message = buf.decode(MulticastReceiver.FORMAT)
                onMessageReceived(message, senderaddr)
        except:
            pass

    def close(self):
        self.receiver.close()

    @staticmethod
    def getNicIp():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        nicIp = sock.getsockname()[0]
        sock.close()
        return nicIp