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
        self.flag = 0
        self.p1check, self.p2check = False, False
        self.goal = False

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
        if data[0] == "start":
            if data[1] == 1:
                self.p1check = True
            else:
                self.p2check = True
        elif data[0] == "player":
            if data[1] == 1:
                self.player1pos = data[2:4]
                self.player1posession = data[4]
                self.player1ballpos = data[5:]
            else:
                self.player2pos = data[2:4]
                self.player2posession = data[4]
                self.player2ballpos = data[5:]
                print(data)
            if self.player1posession == True and self.player2posession == True:
                if self.lastball == 1:
                    self.ballpos = self.player2ballpos
                else:
                    self.ballpos = self.player1ballpos
            elif self.player2posession == True:
                self.ballpos = self.player2ballpos
                self.lastball = 2

            elif self.player1posession == True:
                self.ballpos = self.player1ballpos
                self.lastball = 1

            elif self.player1posession == False and self.player2posession == False:
                if self.lastball == 1:
                    self.ballpos = self.player1ballpos
                else:
                    self.ballpos = self.player2ballpos
            self.flag = "coord"
        elif data[0]=="goal":
            self.player1pos = [(200,100),(200, 350)]
            self.player2pos = [(600,100),(600,350)]
            self.flag = "goal"
            if data[1] == 1:
                self.p1check = True
            else:
                self.p2check = True
        if (self.p1check or self.p2check) and not (self.p1check and self.p2check):
            self.flag = "goal"
        # (a or b) and not (a and b)
        if self.p1check and self.p2check:
            self.goal = False
            self.p1check, self.p2check = False, False
            self.flag = "go"
        if self.goal == True:
            self.player1pos = [(200,100),(200,350)]
            self.player2pos = [(600,100),(600,350)]
            self.flag = "goal"

            # self.callback_client_send(connection_object, ["goal", data[1]])
        print(self.posData)
        self.posData=[data[1],self.player1pos,self.player2pos, self.ballpos]
        self.callback_client_send(connection_object, [self.flag, self.posData])


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
