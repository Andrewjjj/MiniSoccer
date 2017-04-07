# from mastermind_import import *
from settings import *
from Mastermind import *
import threading
from time import gmtime, strftime

class ServerChat(MastermindServerTCP):
    def __init__(self):
        MastermindServerTCP.__init__(self, 0.5,0.5,10.0) #server refresh, connections' refresh, connection timeout

        # self.chat = [None]*scrollback
        self.mutex = threading.Lock()
        self.posData = []
        self.player1pos = [0]
        self.player2pos = [0]
        self.ballpos = []
        self.player1posession, self.player2posession = True, False
        self.player1ballpos, self.player2ballpos = [],[]
        self.lastball = 1

    def update_coordinate(self, data):
        # timestamp = strftime("%H:%M:%S",gmtime())

        # self.mutex.acquire()
        self.posData = [data]#[timestamp+" | "+msg]
        # self.mutex.release()

    def callback_connect          (self                                          ):
        #Something could go here
        return super(ServerChat,self).callback_connect()
    def callback_disconnect       (self                                          ):
        #Something could go here
        return super(ServerChat,self).callback_disconnect()
    def callback_connect_client   (self, connection_object                       ):
        #Something could go here
        return super(ServerChat,self).callback_connect_client(connection_object)
    def callback_disconnect_client(self, connection_object                       ):
        #Something could go here
        return super(ServerChat,self).callback_disconnect_client(connection_object)

    def callback_client_receive   (self, connection_object                       ):
        #Something could go here

        return super(ServerChat,self).callback_client_receive(connection_object)
    def callback_client_handle    (self, connection_object, data                 ):
        # print(data)
        if data[0] == "player":
            if data[1] == 1:
                self.player1pos = data[2:4]
                self.player1posession = data[4]
                self.player1ballpos = data[5:]
            else:
                self.player2pos = data[2:4]
                self.player2posession = data[4]
                self.player2ballpos = data[5:]
        print(self.lastball)
        if self.player1posession == True and self.player2posession == True:
            print("IN")
            if self.lastball == 1:
                print("1111111")
                self.ballpos = self.player2ballpos
                # self.lastball = 2
            else:
                print("2222222")
                self.ballpos = self.player1ballpos
                # self.lastball = 1
        elif self.player2posession == True:
            self.ballpos = self.player2ballpos
            self.lastball = 2

        elif self.player1posession == True:
            # if self.player2posession == True:
            #     self.lastball == 2:
            self.ballpos = self.player1ballpos
            self.lastball = 1

        elif self.player1posession == False and self.player2posession == False:
            if self.lastball == 1:
                self.ballpos = self.player1ballpos
            else:
                self.ballpos = self.player2ballpos


        self.posData=[data[1],self.player1pos,self.player2pos, self.ballpos]

        self.callback_client_send(connection_object, self.posData)

    def callback_client_send      (self, connection_object, data,compression=None):
        #Something could go here
        return super(ServerChat,self).callback_client_send(connection_object, data, compression)

if __name__ == "__main__":
    server = ServerChat()
    server.connect(server_ip,port)
    print("start")
    try:
        print("000")
        server.accepting_allow_wait_forever()

    except:
        print("111")
        #Only way to break is with an exception
        pass
    server.accepting_disallow()
    print("222")
    server.disconnect_clients()
    print("333")
    server.disconnect()
