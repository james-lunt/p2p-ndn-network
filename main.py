from TCPNode1 import p2p_node1
from NodeQingli import Router
import Interfaces
import argparse
import random

#Create initial values for this node
def create_initial_values():
    fish = []
    for i in range (random.randint(0,200)):
        fish.append(Interfaces.Fish())

    ships = []
    for i in range (random.randint(0,200)):
        fish.append(Interfaces.Ship())

    battery = random.uniform(0,1)
    position = [random.randint(0,500),random.randint(0,500),random.randint(0,500)]
    oxygen = random.uniform(0,1)

    return fish,position,oxygen,ships,battery

# Assign class based on interface        
def assign_class(node_interface):
    split_interface = node_interface.split('/')
    length_interface = len(split_interface)

    fish, position, oxygen, ships, battery = create_initial_values()

    #If actuator or sensor
    if length_interface == 4:
        if(split_interface[3] == 'oxygen'):
            return Interfaces.Oxygen()
        elif(split_interface[length_interface-1] == 'battery'):
            return Interfaces.Battery()
        elif(split_interface[length_interface-1] == 'radar'):
            return Interfaces.Radar(fish,position)
        elif(split_interface[length_interface-1] == 'heart rate'):
            return Interfaces.Heart()
        elif(split_interface[length_interface-1] == 'position'):
            return Interfaces.Position()
        elif(split_interface[length_interface-1] == 'light'):
            return Interfaces.Light(position)
        elif(split_interface[length_interface-1] == 'danger alert'):
            return Interfaces.Danger(fish,oxygen)
        elif(split_interface[length_interface-1] == 'precipitation'):
            return Interfaces.Precipitation()
        elif(split_interface[length_interface-1] == 'ship recogniser'):
            return Interfaces.ShipRadar(ships,position)
        elif(split_interface[length_interface-1] == 'pressure'):
            return Interfaces.Pressure(position)
        elif(split_interface[length_interface-1] == 'notifier'):
            return Interfaces.Notifier()
        elif(split_interface[length_interface-1] == 'wind power'):
            return Interfaces.WindS()
        elif(split_interface[length_interface-1] == 'wind direction'):
            return Interfaces.WindD()
        elif(split_interface[length_interface-1] == 'temperature'):
            return Interfaces.Temparature()
        elif(split_interface[length_interface-1] == 'fauna recogniser'):
            return Interfaces.Fauna(fish)
        elif(split_interface[length_interface-1] == 'power optimisation'):
            return Interfaces.Optimizer(battery)
        elif(split_interface[length_interface-1] == 'diver alert'):
            return Interfaces.Alert(battery,fish,oxygen,ships)

    #If diver or scientist
    else:
        if(split_interface[1] == 'scientists'):
            return Interfaces.Base(node_interface)
        elif(split_interface[1] == 'divers'):
            return Interfaces.Diver(node_interface)

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', help='Node Interface', type=str)
    args = parser.parse_args()

    if args.name is None:
        print("Please specify node name")
        exit(1)

    router = Router()
    interface = assign_class(args.name)
    node = p2p_node1(args.name,router,interface)
    node.run()
    