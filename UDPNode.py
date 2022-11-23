import socket
import threading
import random

bufferSize  = 1024

########### Socket Setup #########
def setup_sockets(listen_port,send_port):
    listen_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print ("Socket successfully created")
    listen_socket.bind(('', listen_port))
    send_socket.bind(('',send_port))
    return listen_socket,send_socket


########## Outbound #############
#Connects to port once one is listening
def outbound(send_socket, address, node_connection_list):
    while True:
        interest = input('Ask the network for information: ') 
        bytesToSend = str.encode(interest)
        port = int(random.choice(node_connection_list))
        send_socket.sendto(bytesToSend,(address,port))
        msgFromServer = send_socket.recvfrom(bufferSize)
        msg = "Message from Server {}".format(msgFromServer[0].decode())
        print(msg)


########## Inbound ##############
# Listen for incoming datagrams
def inbound(listen_socket):
    while(True):
        bytesAddressPair = listen_socket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)

        msgFromServer = "Received Interest"
        bytesToSend = str.encode(msgFromServer)


        listen_socket.sendto(bytesToSend, address)

class p2p_node():
    def __init__(self,listen_port,send_port, connection_list):
        self.listen_port = listen_port
        self.send_port = send_port
        self.connection_list = connection_list
    
    def run(self):
        #Makes a list of ports that the node is specified to be able to connect to
        node_connection_list = self.connection_list.split(",")

        #setup inbound and outbound ports
        s_inbound,s_outbound = setup_sockets(self.listen_port,self.send_port)

        # creating thread
        t1 = threading.Thread(target=inbound, args=(s_inbound,))
        t2 = threading.Thread(target=outbound, args=(s_outbound,'rasp-014',node_connection_list,))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
