# first of all import the socket library
import socket
import threading
import argparse
import random

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

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--listenport', help='Listen port', type=int)
    parser.add_argument('--sendport', help='Send port', type=int)
    parser.add_argument('--connection-list', help='List ports possible to connect to seperated by commas', type=str)
    parser.add_argument('--base-node', help="Specify if this is the first node in the network",type=int)
    args = parser.parse_args()

    if args.listenport is None:
        print("Please specify the listen port")
        exit(1)
    if args.sendport is None:
        print("Please specify the send port")
        exit(1)
    if args.connection_list is None:
        print("Please specify List of ports to connect to seperated by commas")
        exit(1)
    if args.base_node is None:
        print("Pleace specify if this is a base node")
        exit(1)

    #Makes a list of ports that the node is specified to be able to connect to
    node_connection_list = args.connection_list.split(",")
    print(node_connection_list)
    #Thread mutex
    print_lock = threading.Lock()

    #setup inbound and outbound ports
    s_inbound,s_outbound = setup_sockets(args.listenport,args.sendport)

    # creating thread
    t1 = threading.Thread(target=inbound, args=(s_inbound,print_lock,))

    #If this node is the first in the network then it should not try to make a connection
    connection = False
    if args.base_node==1:
        print("Connection True")
        connection=True
        t2 = threading.Thread(target=send_outbound, args=(s_outbound,'rasp-014',node_connection_list))

    # starting thread 1
    t1.start()
    if connection:
    # starting thread 2
        t2.start()
 
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    if connection:
        t2.join()