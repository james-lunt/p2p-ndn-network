import json
import socket


# return the longest common prefix of Interest name and a name in fib table
def longestPrefix(str_packet, str_fib):
    re = ''
    # split the url with '/'
    packet_len = len(str_packet.split('/'))
    fib_len = len(str_fib.split('/'))
    # get the length of the shorter string
    loop_len = fib_len if packet_len > fib_len else packet_len
    prefix_len = 0
    # print(loop_len)
    for i in range(loop_len):
        if str_packet.split('/')[i] == str_fib.split('/')[i]:
            prefix_len += 1
        else:
            break
    # print(prefix_len)
    if loop_len == 1:
        return re
    else:
        for i in range(prefix_len):
            if i != 0:
                re += "/" + str_packet.split('/')[i]
        return re


class Router:
    def __init__(self, name, int_socket, data_socket):
        self.name = name  # device name
        self.int_socket = int_socket
        self.data_socket = data_socket
        self.cs = dict()  # name: data: freshness
        self.pit = list(tuple())  # name, ip address, coming interface
        self.fib = list(tuple())  # prefix, ip address, ongoing interface
        with open("interfaces.json", 'r') as load_f:
            load_dict = json.load(load_f)
        # get the current device's neighbours
        # print(self.name)
        neighbours_list = list()
        for i in range(len(load_dict)):
            device_name = list(load_dict[i].keys())[0]
            # print(device_name)
            if device_name == self.name:
                neighbours_dict = load_dict[i][device_name][1]  # neighbours dictionary
                neighbours_list = neighbours_dict[list(neighbours_dict.keys())[0]]  # neighbours list
                # print(neighbours_list)

        # add neighbours into the current fib
        for neighbour_name in neighbours_list:
            for i in range(len(load_dict)):
                device_name = list(load_dict[i].keys())[0]
                if device_name == neighbour_name:
                    device_detail = load_dict[i][device_name][0]
                    listen_port = device_detail[list(device_detail.keys())[0]]
                    addr = device_detail[list(device_detail.keys())[2]]
                    self.setFib(device_name, addr, listen_port)

        # add sensor
        for i in range(len(load_dict)):
            sensor_name = list(load_dict[i].keys())[0]
            if sensor_name != name:
                if sensor_name.startswith(name):
                    sensor_list = load_dict[i][sensor_name][0]
                    listen_port = list(sensor_list.values())[0]
                    addr = list(sensor_list.values())[2]
                    self.setFib(sensor_name, addr, listen_port)

    def getName(self):
        return self.name

    def getCS(self):
        return self.cs

    # cache new data
    def setCS(self, name, data):
        self.cs[name] = data

    def getPit(self):
        return self.pit

    # record the incoming interface of Interest Packet
    def setPit(self, name, addr, interface):  # incoming interface
        self.pit.append((name, addr, interface))

    def getFib(self):
        return self.fib

    # for scalable ????
    def setFib(self, prefix, addr, interface):  # ongoing interface
        t = (prefix, addr, interface)
        self.fib.append(tuple(t))

    # select_mode()
    # set Routing Jump
    # Note: 判定是否在同一个pi上 使用prefix第一个
    def forwarder(self, packet):
        fib = ''
        prefix = dict()
        prefix_sorted = dict()
        if self.getFib():
            fib = self.getFib()
            # print(fib.keys())

            for i in fib.keys():
                str1 = longestPrefix(i, packet.name)
                if str1:
                    prefix[str1] = packet.port

            if prefix:
                for i in sorted(prefix.keys()):
                    prefix_sorted[i] = prefix[i]
                    if packet.name == i:
                        # fib_client(addr, prefix[i], packet.name+'~'+str(packet.port))
                        break
                    elif i.split('/')[1] == self.name.split('/')[1]:
                        pass
                        # fib_client(addr, prefix[i], packet.name+'~'+str(packet.port))
                    else:
                        pass
                        # fib_client(other_addr, prefix[i], packet.name + '~' + str(packet.port))
        else:
            print("Interest packet is thrown!")
            pass

    def search_PIT(self, packet):
        # print(device.getInterface())
        # print(packet.port)
        info = self.getPit()
        if packet.name in info.keys():
            print(info[packet.name])
            for i in range(len(info[packet.name])):
                print(info[packet.name][i])
                if packet.port == info[packet.name][i]:
                    # print(packet.port)
                    # print(info[packet.name][i])
                    # print("0")
                    break
                if i + 1 == len(info[packet.name]) & packet.port != info[packet.name][i]:
                    self.setPit(packet.name, packet.addr, packet.port)
                    self.forwarder(packet)
                    # print("1")
                else:
                    self.setPit(packet.name, packet.addr, packet.port)
                    # print(device.router.getPit())
        else:
            self.setPit(packet.name, packet.addr, packet.port)
            self.forwarder(packet)
            # print(device.router.getPit())

    def search_CS(self, packet):
        # device = globals()[device]
        info = self.getCS()
        if packet.name in info.key():
            return info[packet.name]
            # 写一个返回data的方法代替return并删除else中的return--------rewrite
        else:
            self.search_PIT(packet)
            # if data_cs is not None:
            #    device.router.setCS(packet, data_cs)
            # else:
            data_cs = "There is no such value!!"
            return data_cs

    def fib_client(self, addr, port, packet):
        # Create a socket object
        s = socket.socket()
        hostname = socket.gethostbyname(socket.gethostname())

        # connect to the server on local computer
        s.connect((addr, port))

        # receive data from the server and decoding to get the string.
        s.send(packet).encode()
        # close the connection
        s.close()
