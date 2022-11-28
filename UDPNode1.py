import socket
import threading
import random
import json
import time

bufferSize  = 1024
file = open('interfaces.json')
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
def outbound(socket,router,lock,interface):
    while True:
        interest = input('Ask the network for information: ') 
        lock.acquire()
        #Send to some neighbor given longest prefix protocol or FIB
        forwarding_list = router.longestPrefix(interest)
        if forwarding_list:
            neighbor = forwarding_list[0]
        else:
            neighbor = random.choice(router.getFib())
        print("Sending to " + neighbor[0])
        socket.sendto(json.dumps((interest, interface)).encode(), (neighbor[1],neighbor[2]))
        lock.release()
        #msgFromServer = socket.recvfrom(bufferSize)
        #print(msgFromServer[0].decode())


########## Inbound ##############
def handle_packet(router, packet,socket):
    name = packet[0]
    forward_addresses = router.longestPrefix(name,router.getFib())
    #Interest packet
    if len(packet) == 2:
        if name in router.getCS:
            #Produce data packet name : data : freshness
            packet = [name,router.getCS[name],0]
        elif packet not in router.getPit:
            router.setPit(packet)
        #Forward packet given longest prefix policy
        for node in forward_addresses():
            socket.sendto(json.dumps(packet).encode(),node)

    #Data packet
    else:
        data = packet[1]
        inPit = False
        #Remove elements in PIT which contain interest
        for interest in router.getPit(): 
            if interest[0] == name:
                router.popPit(interest)
                #Send data packet to requesters
                socket.sendto(json.dumps(packet).encode(), router.getAddress(interest[1]))
                inPit = True
        if inPit:
            router.setCS(name,data)

# Listen for incoming datagrams
def inbound(socket,name,lock,router):
    while(True):
        bytesAddressPair = socket.recvfrom(bufferSize)
        lock.acquire()
        message = bytesAddressPair[0]
        rcv_address = bytesAddressPair[1]
        msgFromServer = name + "Received Message"
        bytesToSend = str.encode(msgFromServer)
        socket.sendto(bytesToSend, rcv_address)
        handle_packet(router,message,socket)
        lock.release()


class p2p_node():
    def __init__(self,name,router,interface):
        #Interface name
        self.name = name

        #Thread Mutex
        self.lock = threading.Lock()

        #Set router and interface class
        self.router = router
        self.interface = interface

        #Update content store with data
        router.setCS(name,interface.data)

        #Find network details from json
        index=find_node(name)   
        network_details = references[index][name]
        self.listen_port = network_details[0]["listen port"]
        self.send_port = network_details[0]["send port"]
        self.address = network_details[0]["address"]
    
    def run(self):
        #setup inbound and outbound ports
        s_inbound,s_outbound = setup_sockets(self.listen_port,self.send_port)
        # creating thread
        t1 = threading.Thread(target=inbound, args=(s_inbound,self.name,self.lock,self.router))
        t2 = threading.Thread(target=outbound, args=(s_outbound,self.router,self.lock,self.name))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
        
        while True:
            #auxiliaries for the classes that need it
            aux_position = [random.randint(0,500),random.randint(0,500),random.randint(0,200)]
            aux_oxygen = random.randint(0,100)
            aux_battery = random.randint(0,100)
            aux_fish = []
            for i in range (random.randint(0,300)):
                aux_fish.append(Interfaces.Fish())
            aux_ships = []
            for i in range (random.randint(0,50)):
                aux_ships.append(Interfaces.Ship())
            #updating every 10 seconds
            if (self.interface.__name__ in ['Oxygen', 'Battery', 'Heart', 'Position', 'Camera', 'WindS', 'WindD', 'Temperature', 'Precipitation']):
                self.interface.update()
            elif (self.interface.__name__ == 'Light'):
                self.interface = Interfaces.Light(aux_position)
            elif (self.interface.__name__ == 'Pressure'):
                self.interface = Interfaces.Pressure(aux_position)
            elif (self.interface.__name__ == 'Radar'):
                self.interface = Interfaces.Radar(aux_fish, aux_position)
            elif (self.interface.__name__ == 'ShipRadar'):
                self.interface = Interfaces.ShipRadar(aux_ships, aux_position)
            elif (self.interface.__name__ == 'Fauna'):
                self.interface = Interfaces.Fauna(aux_fish)
            elif (self.interface.__name__ == 'Optimizer'):
                self.interface = Interfaces.Optimizer(aux_battery)
            elif (self.interface.__name__ == 'Alert'):
                self.interface = Interfaces.Alert(aux_battery, aux_fish, aux_oxygen, aux_ships)
            time.sleep(10)
             
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
