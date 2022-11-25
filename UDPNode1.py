import socket
import threading
import random
import json

bufferSize  = 1024
file = open('interface_ports2.json')
references = json.load(file)

#Finds the node with the given name in the reference json and returns its index
def find_node(name):
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
def outbound(socket,node_connection_list,lock):
    while True:
        interest = input('Ask the network for information: ') 
        lock.acquire()
        bytesToSend = str.encode(interest)
        #Pick a random neighbor
        neighbor = str(random.choice(node_connection_list))
        #Lookup target port and address
        node_index = find_node(neighbor)
        port = references[node_index][neighbor][0]["listen port"]
        address = references[node_index][neighbor][0]["address"]
        #Send to neighbor
        socket.sendto(bytesToSend,(address,port))
        lock.release()
        msgFromServer = socket.recvfrom(bufferSize)
        print(msgFromServer[0].decode())


########## Inbound ##############
# Listen for incoming datagrams
def inbound(socket,name,lock):
    while(True):
        bytesAddressPair = socket.recvfrom(bufferSize)
        lock.acquire()
        message = bytesAddressPair[0]
        rcv_address = bytesAddressPair[1]
        print("\n" + message.decode() + " From ")
        lock.release()
        msgFromServer = name + "Received Interest"
        bytesToSend = str.encode(msgFromServer)
        socket.sendto(bytesToSend, rcv_address)


class p2p_node():
    def __init__(self,name,router,interface):
        #Interface name
        self.name = name

        #Thread Mutex
        self.lock = threading.Lock()

        #Set router and interface class
        self.router = router
        self.interface = interface

        #Find network details from json
        index=find_node(name)   
        network_details = references[index][name]
        self.listen_port = network_details[0]["listen port"]
        self.send_port = network_details[0]["send port"]
        self.address = network_details[0]["address"]
        self.neighbors = network_details[1]["neighbors"]
    
    def run(self):

        #setup inbound and outbound ports
        s_inbound,s_outbound = setup_sockets(self.listen_port,self.send_port)

        # creating thread
        t1 = threading.Thread(target=inbound, args=(s_inbound,self.name,self.lock))
        t2 = threading.Thread(target=outbound, args=(s_outbound,self.neighbors,self.lock))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
