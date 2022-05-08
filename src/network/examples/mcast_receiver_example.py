import sys
sys.path.append('..')

from multicast_receiver import MulticastReceiver

def onMessageReceived(message, senderaddr):
    print(message)
    print(senderaddr)
    sys.stdout.flush()

    m.receive(onMessageReceived)

m = MulticastReceiver()
m.receive(onMessageReceived)

while True:
    inp = input()
    print(inp)
    sys.stdout.flush()

