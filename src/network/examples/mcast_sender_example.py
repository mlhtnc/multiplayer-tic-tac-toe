import sys
sys.path.append('..')

from multicaster import Multicaster

m = Multicaster()

m.initSender()
m.send("hello network!")
m.closeSender()