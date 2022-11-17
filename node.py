# first of all import the socket library
import socket
import threading
import argparse

def setup_sockets(port):
    listen_socket = socket.socket()
    send_socket = socket.socket()
    print ("Socket successfully created")
    listen_port = port    
    listen_socket.bind(('', listen_port))
    return listen_socket,send_socket
 
def new_connection(c,addr):
    #while True:
    print ('Got connection from', addr )    
    c.send(b'Thank you for connecting')
    #c.close()    

def inbound(listen_socket):
    listen_socket.listen(5)   
    print ("socket is listening")
    while True:
        c, addr = listen_socket.accept()
        
        threading.Thread(target=new_connection, args=(c,addr)).start()
        #c.close()

def send_outbound(send_socket,name, port): 
    send_socket.connect((name, port))
    print (send_socket.recv(1024).decode())

    send_socket.close()

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', help='Node port', type=int)
    parser.add_argument('--destport', help='Node port you want to connect to', type=int)
    parser.add_argument('--make-connection', help='Do you want to connect or not', type=int)
    args = parser.parse_args()
    if args.port is None:
        print("Please specify the Node port")
        exit(1)
    if args.destport is None:
        print("Please specify the Destination port")
        exit(1)
    if args.make_connection is None:
        print("Pleace specify if you want to make a connection")
        exit(1)

    #setup inbound and outbound ports
    s_inbound,s_outbound = setup_sockets(args.port)

    # creating thread
    t1 = threading.Thread(target=inbound, args=(s_inbound,))
    connection = False
    if args.make_connection==1:
        print("Connection True")
        connection=True
        t2 = threading.Thread(target=send_outbound, args=(s_outbound,'rasp-014',args.destport))

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