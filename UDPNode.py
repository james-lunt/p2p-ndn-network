import socket
import threading
import random
import json
import Interfaces

bufferSize  = 1024
class_dict = {"oxygen" : Interfaces.Oxygen(), "battery" : Interfaces.Battery(),
            "radar" : Interfaces.Radar(), "heart rate" : Interfaces.Heart(),
            "position" : Interfaces.Position(), "pressure" : Interfaces.Pressure(),
            "light" : Interfaces.Light(), "danger alert" : Interfaces.Danger(),
            "notifier" : Interfaces.Notifier(), "wind power" : Interfaces.WindS(),
            "widn direction" : Interfaces.WindD(), "temperature" : Interfaces.Temperature(),
            "precipitation" : Interfaces.Precipitation(), "ship recogniser" : Interfaces.ShipRadar(),
            "fauna recogniser" : Interfaces.Fauna(), "power optimisation" : Interfaces.Optimizer(),
            "diver alert" : Interfaces.Alert(), "scientists" : Interfaces.Base(),
            "divers" : Interfaces.Diver()}


########### Setup #########
def setup_sockets(listen_port,send_port):
    listen_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print ("Socket successfully created")
    listen_socket.bind(('', listen_port))
    send_socket.bind(('',send_port))
    return listen_socket,send_socket

# Assign class based on interface        
def assign_class(node_interface):
    split_interface = node_interface.split('/')
    length_interface = len(split_interface)

    #If actuator or sensor
    if length_interface == 4:
        return class_dict[split_interface[length_interface]]
    #If diver or scientist
    else:
        return class_dict[split_interface[1]]
    

########## Outbound #############
#Send interest packet
def outbound(send_socket, address, node_connection_list):
    while True:
        interest = input('Ask the network for information: ') 
        bytesToSend = str.encode(interest)
        port = int(random.choice(node_connection_list))
        send_socket.sendto(bytesToSend,(address,port))
        msgFromServer = send_socket.recvfrom(bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0].decode())
        print(msg)

#Send Data packet back to all neighbors
def send_data(send_socket, address, node_connection_list, data):
    bytesToSend = str.encode(data)
    for port in node_connection_list:
        send_socket.sendto(bytesToSend, (address,port))

########## Inbound ##############
# Listen for incoming datagrams
def inbound(send_socket, listen_socket, address, node_connection_list):
    while(True):
        bytesAddressPair = listen_socket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        rcv_address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(rcv_address)

        if message.decode() == "d":
            send_data(send_socket,address,node_connection_list)

        msgFromServer = "Received Interest"
        bytesToSend = str.encode(msgFromServer)


        listen_socket.sendto(bytesToSend, rcv_address)

class p2p_node():
    def __init__(self,node_interface):
        file = open('interface_ports2.json')
        data = json.load(file)

        #Find network details from json
        index=0
        for i in range(len(data)):
            if(node_interface == list(data[i].keys())[0]):
                index = i        

        network_details = data[index][node_interface]
        self.listen_port = network_details[0]["listen port"]
        self.send_port = network_details[0]["send port"]
        self.address = network_details[0]["address"]
        self.neighbors = network_details[1]["neighbors"]
        self.device = assign_class(node_interface)
    
    def run(self):
        print(self.device)

        #setup inbound and outbound ports
        s_inbound,s_outbound = setup_sockets(self.listen_port,self.send_port)

        # creating thread
        t1 = threading.Thread(target=inbound, args=(s_inbound,s_outbound, self.address, self.neighbors,))
        t2 = threading.Thread(target=outbound, args=(s_outbound,self.address,self.neighbors,))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
