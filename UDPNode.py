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
def outbound(send_socket, address, node_connection_list,lock):
    while True:
        interest = input('Ask the network for information: ') 
        bytesToSend = str.encode(interest)
        #print(node_connection_list)
        neighbor = str(random.choice(node_connection_list))
        #print(neighbor)
        port = references[find_port(neighbor)][neighbor][0]["listen port"]
        lock.acquire()
        send_socket.sendto(bytesToSend,(address,port))
        lock.release()
        with open('log.txt', 'a') as f:
            f.write('Sent')
        #msgFromServer = send_socket.recvfrom(bufferSize)
        #msg = "Message from Server {}".format(msgFromServer[0].decode())

#Send Data packet back to all neighbors
def send_data(send_socket, address, node_connection_list, data):
    bytesToSend = str.encode(data)
    for port in node_connection_list:
        send_socket.sendto(bytesToSend, (address,port))

########## Inbound ##############
# Listen for incoming datagrams
def inbound(send_socket, listen_socket, address, node_connection_list,lock):
    while(True):
        lock.acquire()
        print("LISTENING")
        bytesAddressPair = listen_socket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        rcv_address = bytesAddressPair[1]
        print(message.decode())
        lock.release()
        with open('log.txt', 'a') as f:
            f.write(message.decode())

        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(rcv_address)

        if message.decode()[0] == "/":
            with open('log.txt', 'a') as f:
                 f.write('interest')
        else:
            with open('log.txt', 'a') as f:
                 f.write('data')
        """
        msgFromServer = "Received Interest"
        bytesToSend = str.encode(msgFromServer)
        """


        #listen_socket.sendto(bytesToSend, rcv_address)

class p2p_node():
    def __init__(self,name,router,interface):
        #Print lock
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
        t1 = threading.Thread(target=inbound, args=(s_inbound,s_outbound, self.address, self.neighbors,self.lock,))
        t2 = threading.Thread(target=outbound, args=(s_outbound,self.address,self.neighbors,self.lock,))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
