# first of all import the socket library
import socket
import threading
import argparse

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

def send_outbound(send_socket,name, port):
    send_socket.connect((name,port))
    while True:
        message = input('send something')

        #message sent to node
        send_socket.send(message.encode('ascii'))
        data = send_socket.recv(1024)
        print('Received from the server :',str(data.decode('ascii')))
 
        # ask the client whether he wants to continue
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
    parser.add_argument('--destport', help='Node port you want to connect to', type=int)
    parser.add_argument('--make-connection', help='Do you want to connect or not', type=int)
    args = parser.parse_args()

    if args.listenport is None:
        print("Please specify the listen port")
        exit(1)
    if args.sendport is None:
        print("Please specify the send port")
        exit(1)
    if args.destport is None:
        print("Please specify the Destination port")
        exit(1)
    if args.make_connection is None:
        print("Pleace specify if you want to make a connection")
        exit(1)

    #Thread mutex
    print_lock = threading.Lock()

    #setup inbound and outbound ports
    s_inbound,s_outbound = setup_sockets(args.listenport,args.sendport)

    # creating thread
    t1 = threading.Thread(target=inbound, args=(s_inbound,print_lock,))
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