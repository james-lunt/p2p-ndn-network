from UDPNode import p2p_node
import argparse

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='Listen port', type=str)
    args = parser.parse_args()

    if args.name is None:
        print("Please specify node name")
        exit(1)

    diver1 = p2p_node(args.name)
    diver1.run()