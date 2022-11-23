from UDPNode import p2p_node
import argparse

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--listenport', help='Listen port', type=int)
    parser.add_argument('--sendport', help='Send port', type=int)
    parser.add_argument('--connection-list', help='List ports possible to connect to seperated by commas', type=str)
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

    diver1 = p2p_node(args.listenport,args.sendport,args.connection_list)
    diver1.run()