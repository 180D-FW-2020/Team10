import socket
import random
from time import sleep

def randomLocation():
    s = socket.socket()

    #connect to server on local computer
    s.connect(('192.168.0.197', 1755))
    s.send((
        "0"+","+
        "0"+","+
        str(random.randint(0,360))).encode())
    s.close()

for i in range(100):
    randomLocation()
    sleep(1)

