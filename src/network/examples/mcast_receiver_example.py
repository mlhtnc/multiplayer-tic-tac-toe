import sys
sys.path.append('..')

from multicaster import Multicaster

def onMessageReceived(message):
    print(message)
    sys.stdout.flush()

    m.receive(onMessageReceived)

m = Multicaster()

m.initReceiver()

m.receive(onMessageReceived)

while True:
    inp = input()
    print(inp)
    sys.stdout.flush()

