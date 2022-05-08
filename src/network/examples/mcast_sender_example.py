from multicast_sender import MulticastSender

m = MulticastSender()
m.send("hello network!")
m.close()