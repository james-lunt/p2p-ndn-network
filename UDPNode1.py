import socket
import threading
import random
import json


bufferSize  = 1024
file = open('interface_ports2.json')
references = json.load(file)


def find_port(name):
    for i in range(len(references)):
        if(name == list(references[i].keys())[0]):
            return i

########### Setup #########
def setup_sockets(listen_port,send_port):
    listen_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print ("Socket successfully created")
    listen_socket.bind(('', listen_port))
    send_socket.bind(('',send_port))
    return listen_socket,send_socket

########## Outbound #############
#Send interest packet
def outbound(socket, address, node_connection_list,lock):
    while True:
        interest = input('Ask the network for information: ') 
        lock.acquire()
        bytesToSend = str.encode(interest)
        neighbor = str(random.choice(node_connection_list))
        port = references[find_port(neighbor)][neighbor][0]["listen port"]
        socket.sendto(bytesToSend,(address,port))
        print("sent")
        lock.release()
        msgFromServer = socket.recvfrom(bufferSize)
        print(msgFromServer[0].decode())


########## Inbound ##############
# Listen for incoming datagrams
def inbound(socket,lock):
    while(True):
        bytesAddressPair = socket.recvfrom(bufferSize)
        lock.acquire()
        message = bytesAddressPair[0]
        rcv_address = bytesAddressPair[1]
        print("\n" + message.decode())
        lock.release()
        msgFromServer = "Received Interest"
        bytesToSend = str.encode(msgFromServer)
        socket.sendto(bytesToSend, rcv_address)


class p2p_node():
    def __init__(self,name,router,interface):
        #Thread Mutex
        self.lock = threading.Lock()

        #Set router and interface class
        self.router = router
        self.interface = interface

        #Find network details from json
        index=find_port(name)   
        network_details = references[index][name]
        self.listen_port = network_details[0]["listen port"]
        self.send_port = network_details[0]["send port"]
        self.address = network_details[0]["address"]
        self.neighbors = network_details[1]["neighbors"]
    
    def run(self):

        #setup inbound and outbound ports
        s_inbound,s_outbound = setup_sockets(self.listen_port,self.send_port)

        # creating thread
        t1 = threading.Thread(target=inbound, args=(s_inbound,self.lock))
        t2 = threading.Thread(target=outbound, args=(s_outbound,self.address,self.neighbors,self.lock))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
