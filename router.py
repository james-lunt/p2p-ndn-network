#NDN component
class Router:
    def __init__(self):
        self.cs = dict()  # name:data
        self.pit = dict()  # name: coming interface 接口不需要分辩路由还是主机
        self.fib = dict()  # prefix:face list

    def getCS(self):
        return self.cs

    # cache new data
    def setCS(self, name, data):
        self.cs[name] = data

    def getPit(self):
        return self.pit

    # record the incoming interface of Interest Packet
    def setPit(self, name, interface):  # incoming interface
        self.pit[name] = interface

    def getFib(self):
        return self.fib

    # for scalable ????
    def setFib(self, prefix, interface):  # ongoing interface
        self.fib[prefix] = interface