import inspect
import NodeQingli
import socket


# initiate the p2p network
interface = 33007
names = globals()
device_name = []  # save the name of device


# write into fib of all device when there appears a new device
def connect_node(device):
    # get all device expect the new device
    other_device = list(filter(lambda a: globals()[device_name[a]] != device, range(len(device_name))))
    # write the prefix into fib
    for s in other_device:
        device.router.setFib("/" + device.getType() + "/" + globals()[device_name[s]].getName(),
                             globals()[device_name[s]].getInterface())
        globals()[device_name[s]].router.setFib("/" + device.getType() + "/" + device.getName(),
                                                device.getInterface())
    # map(lambda x: names[device_name[i]].router.setFib("/"+globals()[device_name[x]].getName(),
    #                                                   globals()[device_name[x]].getInterface()), other_device)
    # names[device_name[i]].router.setFib("/"+names[device_name[i]].getName(), names[device_name[i]].getInterface())


def p2p(device_type):
    for i in range(5):
        #
        names[device_type + str(i + 1)] = NodeQingli.Diver(device_type, device_type + str(i + 1), interface + i * 10,
                                                     1, 1, 1, 1, 1, 1, 1, 1, 1)
        # save the name of device
        device_name.append(device_type + str(i + 1))
        # add connection with other devices
        if i > 0:
            connect_node(names[device_type + str(i + 1)])
    #
    for i in range(len(device_name)):
        print("FIB of", device_name[i])
        print(names[device_name[i]].router.getFib())  #


# print(globals())

def type_to_otherPi():
    name = ''
    for i in range(len(device_name)):
        devices = globals()[device_name[i]]
        # print(globals()[device_name[i]])
        if i < len(device_name) - 1:
            name += "/" + devices.getType() + "/" + devices.getName() + ":" + str(devices.getInterface()) + '~'
        else:
            name += "/" + devices.getType() + "/" + devices.getName() + ":" + str(devices.getInterface())
    # print(name)
    return name


def data_split(data):
    # print(type(data))
    content = data.split('~')
    # print(content)
    key = list(map(lambda x: x.split(':')[0], content))
    value = list(map(lambda x: x.split(':')[1], content))
    for i in range(len(device_name)):
        devices = globals()[device_name[i]]
        for j in range(len(key)):
            devices.router.setFib(key[j], value[j])


def serve():
    # next create a socket object
    s = socket.socket()
    print("Socket successfully created")

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port = 33777

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind((socket.gethostname(), port))
    print("socket binded to %s" % (port))

    s.listen(5)
    print("socket is listening")
    print(socket.gethostname())

    # a forever loop until we interrupt it or
    # an error occurs
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)

        c.send('Thank you for connecting'.encode())

        data = c.recv(2048)

        # print(data.decode())

        data_split(data.decode())

        c.close()

        break

    s.close()


def client(data):
    s = socket.socket()
    hostname = socket.gethostbyname(socket.gethostname())
    print(hostname)

    # Define the port on which you want to connect
    port = 33777

    # connect to the server on local computer
    s.connect(("10.35.70.14", port))

    # receive data from the server and decoding to get the string.
    print(s.recv(1024).decode())

    s.send(data.encode())

    # close the connection
    s.close()


device_type1 = 'base'
p2p(device_type1)

data = type_to_otherPi()
client(data)

serve()
print(globals()[device_name[0]].router.getFib())

