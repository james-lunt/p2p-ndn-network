import json

class Router:
    def __init__(self, name):
        self.name = name  # device name
        self.cs = dict()  # name: data: freshness
        self.pit = list(tuple())  # name
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
    def setPit(self, name, interface):  # incoming interface
        self.pit.append((name, interface))

    def popPit(self,name,interface):
        self.pit.remove((name,interface))

    def getFib(self):
        return self.fib
    
    def getAddress(name,self):
        for address in self.fib:
            if name == address[0]:
                return(address[1],address[2])

    # for scalable ????
    def setFib(self, prefix, addr, interface):  # ongoing interface
        t = (prefix, addr, interface)
        self.fib.append(tuple(t))
    
    # The longest match between the name of the matched interest packet and the prefix in the fib,
    # returned with the fib storage format, and not contains urls that do not match at all
    def longestPrefix(self,str_packet):
        match_fib = dict()
        resorted = list()
        # split the url with '/'
        packet_len = len(str_packet.split('/'))
        # print(len(self.fib))

        # match how many strings between the packet name and fib
        for k in range(len(self.fib)):
            fib_len = len(self.fib[k][0].split('/'))
            # get the length of the shorter string
            loop_len = fib_len if packet_len > fib_len else packet_len
            prefix_len = 0
            # print(loop_len)
            for i in range(loop_len):
                if str_packet.split('/')[i] == self.fib[k][0].split('/')[i]:
                    prefix_len += 1
                else:
                    break
            # set the largest level if match completely
            if str_packet == self.fib[k][0]:
                loop_len = 9999
            # If matches more than one string, it is added to the dictionary
            if prefix_len > 1:
                match_fib[self.fib[k][0]] = loop_len

        # rank the dictionary
        resorted = sorted(match_fib.items(), key=lambda x: x[1], reverse=True)

        # return the data has the same format with fib table
        resorted_fib = list(tuple())
        for i in range(len(resorted)):
            for k in self.fib:
                if resorted[i][0] == k[0]:
                    resorted_fib.append(k)
        return resorted_fib




        