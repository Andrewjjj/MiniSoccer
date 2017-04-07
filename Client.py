from Mastermind import *
from game import *
import time
ip_add = "127.0.0.1"
# ip_add = "172.28.230.149"
port = 6317
def connect():
    global client, server

    client = MastermindClientTCP(5.0,10.0)
    try:
        client.connect(ip_add,port)
        print("Connected!")
    except MastermindError:
        print("Cannot find a Server; Starting Server!!")
        client.connect(ip_add,port)
        # server =
    # i=0
    asd=[]
    x1, y1 = 0,0
    i=0
    j=0
    while 1:
        client.send([1,i,x1,y1])
        x1+=1
        y1+=1
        i+=1
        asd=client.receive()

        print("DATA RECIEVED:",asd)
        # time.sleep(0.1)
        # i+=1
    print("Disconencting!")
    client.disconnect()
if __name__ == "__main__":
    connect()
