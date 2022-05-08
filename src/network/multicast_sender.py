import socket

class MulticastSender:
    MCAST_GROUP = '224.1.1.1'
    MCAST_PORT = 5004
    TTL = 1
    BUF_SIZE = 1024
    FORMAT = "utf-8"

    def __init__(self):
        # NIC (Network Interface Card)
        self.nicIp = MulticastSender.getNicIp()
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MulticastSender.TTL)
        self.sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self.nicIp))
        
    def send(self, message):
        message = message.encode(MulticastSender.FORMAT)
        self.sender.sendto(message, (MulticastSender.MCAST_GROUP, MulticastSender.MCAST_PORT))

    def close(self):
        self.sender.close()

    @staticmethod
    def getNicIp():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        nicIp = sock.getsockname()[0]
        sock.close()
        return nicIp