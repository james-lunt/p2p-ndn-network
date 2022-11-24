import socket
import threading
import random
import json
from threading import Lock

bufferSize  = 1024
file = open('interface_ports2.json')
references = json.load(file)


def find_port(name):
    for i in range(len(references)):
        if(name == list(references[i].keys())[0]):
            return i

########### Socket Setup #########

def setup_sockets(listen_port,send_port):
    listen_socket = socket.socket()
    send_socket = socket.socket()
    print ("Socket successfully created")
    listen_socket.bind(('', listen_port))
    send_socket.bind(('',send_port))
    return listen_socket,send_socket


########## Outbound #############
#Send interest packet
def outbound(send_socket, address, node_connection_list,lock):
    while True:
        interest = input('Ask the network for information: ') 
        lock.acquire()
        neighbor = str(random.choice(node_connection_list))
        port = references[find_port(neighbor)][neighbor][0]["listen port"]
        send_socket.connect((address,port))
        send_socket.send(interest.encode('ascii'))
       # send_socket.close()
        lock.release()

########### Inbound #############
def inbound(self,listen_socket,lock):
    listen_socket.listen(5)   
    print ("socket is listening")
    while True:
        c, addr = listen_socket.accept()
        lock.acquire()
        #print('Connected to: ', addr[0], ':', addr[1])
        #c.send(b'Connected to ', self.listen_port)
        data = c.recv(1024)
        #will do something here with the message
        #print('Received from : ', addr[1], str(data.decode('ascii')))
        #print("Closing Connection with ", addr)
        lock.release()
        c.close()

class p2p_node1():
    def __init__(self,name,router,interface):
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
        print_lock = threading.Lock()
        #setup inbound and outbound ports
        s_inbound,s_outbound = setup_sockets(self.listen_port,self.send_port)

        # creating thread
        t1 = threading.Thread(target=inbound, args=(self,s_inbound,print_lock))
        t2 = threading.Thread(target=outbound, args=(s_outbound,self.address,self.neighbors,print_lock))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
