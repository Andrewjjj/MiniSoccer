from Mastermind import *
import threading

class Server(MastermindServerTCP):
    def __init__(self):
        MastermindServerTCP.__init__(self, 0.5, 0.5, 10.0)
        # self.mutex = threading.Lock()

    def add_coordinates(self, coords):
        # self.mutex.acquire()
        # self.mutex.release()
    def callback_client_handle    (self, connection_object, data                 ):
        # cmd = data[0]
        # if cmd == "introduce":
        #     self.add_message("Server: "+data[1]+" has joined.")
        # elif cmd == "add":
        #     # print(data[1])
        #     self.add_message(data[1])
        # elif cmd == "update":
        #     pass
        # elif cmd == "leave":
        #     self.add_message("Server: "+data[1]+" has left.")
        # self.callback_client_send(connection_object, self.chat)

ip_add = "127.0.0.1"
port = 6317
if __name__ == "__main__":
    server = Server()
    server.connect(ip_add,port)
    try:
        # print("Waiting")
        # print(server.accepting_allow())
        server.accepting_allow_wait_forever()
    except:
        pass
    print("Disconnecting!")
    server.accepting_disallow()
    server.disconnect_clients()
    server.disconnect()
