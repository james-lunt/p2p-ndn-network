import socket
import threading
import random
import json
import Interfaces
import time

bufferSize  = 1024
file = open('interfaces_smaller.json')
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

########## Update ##############
def update(interface,router,name):
    while True:
        print(interface)
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
        if (interface.__class__.__name__ in ['Oxygen', 'Battery', 'Heart', 'Position', 'Camera', 'WindS', 'WindD', 'Temperature', 'Precipitation']):
            interface.update()
        elif (interface.__class__.__name__ == 'Light'):
            interface = Interfaces.Light(aux_position)
        elif (interface.__class__.__name__ == 'Pressure'):
            interface = Interfaces.Pressure(aux_position)
        elif (interface.__class__.__name__ == 'Radar'):
            interface = Interfaces.Radar(aux_fish, aux_position)
        elif (interface.__class__.__name__ == 'ShipRadar'):
            interface = Interfaces.ShipRadar(aux_ships, aux_position)
        elif (interface.__class__.__name__ == 'Fauna'):
            interface = Interfaces.Fauna(aux_fish)
        elif (interface.__class__.__name__ == 'Optimizer'):
            interface = Interfaces.Optimizer(aux_battery)
        elif (interface.__class__.__name__ == 'Alert'):
            interface = Interfaces.Alert(aux_battery, aux_fish, aux_oxygen, aux_ships)
        #Update content store with data
        router.setCS(name,interface.data)
        time.sleep(10)
        print(router.getCS())



########## Outbound #############
#Send interest packet
def outbound(socket,router,lock,interface):
    while True:
        interest = input('Ask the network for information: ') 
        lock.acquire()
        #Send to some neighbor given longest prefix protocol or FIB
        neighbor = router.longestPrefix(interest)
        print(neighbor)
        packet = (interest, interface)
        print(packet)
        socket.sendto(json.dumps(packet).encode(), (neighbor[0][1],neighbor[0][2]))
        lock.release()
        #msgFromServer = socket.recvfrom(bufferSize)
        #print(msgFromServer[0].decode())


########## Inbound ##############
def handle_packet(router, packet,socket):
    packet = json.loads(packet.decode())
    name = packet[0]
    print(packet)
    #Interest packet
    if len(packet) == 2:
        interface = packet[1]
        print("Interest Packet Received!")
        if name in router.getCS():
            print("I have the Data!")
            #Produce data packet name : data : freshness
            address = (interface[1],interface[2])
            packet = [name,router.getCS()[name],0]
            socket.sendto(json.dumps(packet).encode(), address)
            return
        elif packet not in router.getPit():
            print("I don't have the Data, updating PIT!")
            router.setPit(name,interface)
            #Forward Interest based on longest prefix
            next_node = router.longestPrefix(name)
            print(next_node)
            print("Forwarding to ", next_node[0])
            packet = (name, router.getLocation()[0])
            socket.sendto(json.dumps(packet).encode(),(next_node[0][1],next_node[0][2]))
            return

    #Data packet
    else:
        print("Data packet Received!")
        data = packet[1]
        inPit = False
        #Remove elements in PIT which contain interest
        for interest in router.getPit(): 
            if interest[0] == name:
                print("Satisfying interest table")
                router.popPit(interest)
                #Send data packet to requesters
                socket.sendto(json.dumps(packet).encode(), router.getAddress(interest[1]))
                inPit = True
                return
        if inPit:
            print("Updating Content store")
            router.setCS(name,data)
            return
        else:
            print("Not in interest table, ignore packet.")
            return
    
    return

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
        t3 = threading.Thread(target=update, args=(self.interface,self.router,self.name))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
        # starting thread 3
        t3.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()

        t3.join()
