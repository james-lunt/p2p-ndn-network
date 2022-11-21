# first of all import the socket library
import socket
import threading
import random

def new_connection(c,addr,print_lock):
    c.send(b'Thank you for connecting')
    while True:
        data = c.recv(1024)
        if not data:
            print('Bye')

            print_lock.release()
            break
        #will do something here with the message
        print('Received from : ', addr[1], str(data.decode('ascii')))
        c.send("Got your message")
    c.close() 

#Connects to port once one is listening
def attempt_connection(send_socket,node_connection_list,name):
    print("Checking for available ports")
    waiting_for_port_message = True
    while True:
        port = int(random.choice(node_connection_list))
        try:
            send_socket.connect((name,port))
            break
        except:
            if waiting_for_port_message:
                print("Waiting for a listening port.")
                waiting_for_port_message = False

def setup_sockets(listen_port,send_port):
    listen_socket = socket.socket()
    send_socket = socket.socket()
    print ("Socket successfully created")
    listen_socket.bind(('', listen_port))
    send_socket.bind(('',send_port))
    return listen_socket,send_socket

def new_connection(c,addr,print_lock):
    c.send(b'Thank you for connecting')
    while True:
        data = c.recv(1024)
        if not data:
            print('Bye')

            print_lock.release()
            break
        #will do something here with the message
        print('Received from : ', addr[1], str(data.decode('ascii')))
        c.send("Got your message")
    c.close()    

def inbound(listen_socket,print_lock):
    listen_socket.listen(5)   
    print ("socket is listening")
    while True:
        c, addr = listen_socket.accept()
        print_lock.acquire()
        print('Connected to: ', addr[0], ':', addr[1])
        threading.Thread(target=new_connection, args=(c,addr,print_lock)).start()
        #c.close()

def send_outbound(send_socket,name,node_connection_list):
    #Pick random connectable port to connect to 
    attempt_connection(send_socket,node_connection_list,name)
    while True:
        message = input('Ask the network for information: ')
        #check = a_socket.connect_ex(location)

        #message sent to node
        send_socket.send(message.encode('ascii'))
        data = send_socket.recv(1024)
        print('Received from the server :',str(data.decode('ascii')))

        # ask the node whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break
    send_socket.close()

class p2p_node():
    def __init__(self,listen_port,send_port, connection_list):
        self.listen_port = listen_port
        self.send_port = send_port
        self.connection_list = connection_list
    
    def run(self):
        #Makes a list of ports that the node is specified to be able to connect to
        node_connection_list = self.connection_list.split(",")
        #Thread mutex
        print_lock = threading.Lock()

        #setup inbound and outbound ports
        s_inbound,s_outbound = setup_sockets(self.listen_port,self.send_port)

        # creating thread
        t1 = threading.Thread(target=inbound, args=(s_inbound,print_lock,))

        #If this node is the first in the network then it should not try to make a connection
        t2 = threading.Thread(target=send_outbound, args=(s_outbound,'rasp-014',node_connection_list))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
