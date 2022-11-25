import socket
import threading
import random
import json
import Router

bufferSize  = 1024
file = open('interface_reference.json')
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
def outbound(socket,node_connection_list,lock,router):
    while True:
        interest = input('Ask the network for information: ') 
        lock.acquire()
        bytesToSend = str.encode(interest)
        #Pick a random neighbor
        neighbor = str(random.choice(node_connection_list))
        #Lookup target port and address
        for i in router.getFib():
            if i[0] == neighbor:
                address = i[1]
                port = i[2]
        """       
        node_index = find_node(neighbor)
        port = references[node_index][neighbor][0]["listen port"]
        address = references[node_index][neighbor][0]["address"]
        """
        #Send to neighbor
        socket.sendto(bytesToSend,(address,port))
        lock.release()
        msgFromServer = socket.recvfrom(bufferSize)
        print(msgFromServer[0].decode())


########## Inbound ##############
# Listen for incoming datagrams
def inbound(socket,name,lock,interface,router,node_connection_list):
    while(True):
        bytesAddressPair = socket.recvfrom(bufferSize)
        lock.acquire()
        message = bytesAddressPair[0]
        rcv_address = bytesAddressPair[1]
    
        #msgFromServer = name + "Received Interest"
        #bytesToSend = str.encode(msgFromServer)
        #socket.sendto(bytesToSend, rcv_address)
        #print("\n" + message.decode() + " From ")
        print(message.decode())


        #Interest packet
        if message.decode() in router.getCS():
            #Return Data
            bytesToSend = str.encode(router.getCS()[message.decode()])
            socket.sendto(bytesToSend, rcv_address)
            print("Return Data")
        else:
            #Forward Interest
            #Pick a random neighbor
            for node in router.getFib():
                neighbor = Router.longestPrefix(message.decode(),node[0])

            for i in router.getFib():
                if i[0] == neighbor:
                    address = i[1]
                    port = i[2]
            #send to neighbor
            socket.sendto(message,(address,port))
            print("Forwarded interest packet")


        lock.release()



class p2p_node():
    def __init__(self,name,router,interface):
        #Interface name
        self.name = name

        #Thread Mutex
        self.lock = threading.Lock()

        #Set router
        self.router = router
        self.router.setCS(name, "5")
        #print(self.router.getFib())

        #Set up interface class
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
        t1 = threading.Thread(target=inbound, args=(s_inbound,self.name,self.lock,self.interface,self.router, self.neighbors))
        t2 = threading.Thread(target=outbound, args=(s_outbound,self.neighbors,self.lock, self.router))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
