import random
import threading
import time
import NodeQingli
import UDPNode

import numpy as np

# 当前device连接其他device
def connect_sensor(self, prefix, interface):
    self.router.setPit(prefix, interface)

class Oxygen():
    def __init__(self):
        self.oxygen = 100
    def update(self):
        if (random.random() < 0.5):
            self.oxygen = max(0, self.oxygen-1)

class Battery():
    def __init__(self):
        self.battery = 100
    def update(self):
        if (random.random() < 0.75):
            self.battery = max(0, self.battery-1)

class Radar():
    def __init__(self, fish, position):
        self.radar = {}
        key = 0
        for f in fish:
            if np.linalg.norm(position - f.position) < 50:
                self.radar[key] = [round(np.linalg.norm(self.position - f.position)), f.z, f.speed]
                key = key + 1

class Heart():
    def __init__(self):
        self.heart = random.randint(60, 150)
    def update(self):
        self.heart = (self.heart + random.randint(60, 150)) / 2

class Position():
    def __init__(self):
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.z = random.randint(0, 200)
        self.position = np.array((self.x, self.y, self.z))
    def update(self):
        self.x = min(500, max(0, self.x + sign(0.5) * random.randint(0, 20)))
        self.y = min(500, max(0, self.y + sign(0.5) * random.randint(0, 20)))
        self.z = min(200, max(0, self.z + sign(0.5) * random.randint(0, 10)))
        self.position = np.array((self.x, self.y, self.z))

class Pressure():
    def __init__(self, position):
        self.pressure = min(300, position[2] * 285 / 200 + 15 + random.randint(0,15))

class Light():
    def __init__(self, position):
        self.light = min(70, position[2] * 70 / 200 + random.randint(0,5))

class Danger():
    def __init__(self, fish, oxygen):
        self.danger = 0
        if (len(fish) > 2 or oxygen < 50):
            self.danger = 1
        if (oxygen < 25):
            self.danger = 2

class Notifier():
    pass

class WindS():
    def __init__(self):
        self.winds = random.randint(0,70)
    def update(self):
        new = random.randint(0,70)
        if (abs(new - self.winds) > 42):
            self.winds = round((self.winds + new) / 3)
        elif (abs(new - self.winds) > 21):
            self.winds = round((self.winds + new) / 2)
        else:
            self.winds = new

class WindD():
    def __init__(self):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        self.windd = directions[random.randint(0,7)]
    def update(self):
        if (random.random() < 0.5):
            self.windd = directions[(random.randint(0, 7) + sign(0.5)) % 8]

class Temperature():
    def __init__(self):
        self.temperature = random.randint(12, 24)
    def update(self):
        new = random.randint(12, 24)
        if (abs(new - self.winds) > 6):
            self.temperature = round((self.temperature + new) / 2.3)
        elif (abs(new - self.winds) > 3):
            self.temperature = round((self.temperatire + new) / 2)
        else:
            self.temperature = new

class Precipitation():
    def __init__(self):
        self.precipitation = 0
    def update(self):
        if (self.precipitation == 0 and random.random() > 0.8):
            self.precipitation = random.randint(1, 20)
        if (self.precipitation != 0):
            if (random.random() < 0.8):
                new = random.randint(1,20)
                if (abs(new - self.precipitation) > 12):
                    self.precipitation = round((self.precipitation + new) / 2.5)
                elif (abs(new - self.precipitation) > 6):
                    self.precipitation = round((self.precipitation + new) / 1.8)
                else:
                    self.precipitation = new
            else:
                self.precipitation = 0

class ShipRadar():
    def __init__(self, ships, position):
        self.radar = {}
        key = 0
        for s in ships:
            if np.linalg.norm(position - s.position) < 100:
                self.radar[key] = [round(np.linalg.norm(self.position - s.position)), s.size, s.speed]
                key = key + 1

class Fauna():
    def __init__(self, fish):
        self.radar = {}
        key = 0
        for f in fish:
            self.radar[key] = f.name
            key = key + 1

class Optimizer():
    def __init__(self, battery):
        self.message = "All OK"
        if (battery < 0.6):
            self.message = "Turn off photometer."
        elif (battery < 0.5):
            self.message = "Turn off barometer."
        elif (battery < 0.4):
            self.message = "Turn off fauna radar."
        elif (battery < 0.3):
            self.message = "Turn off heart rate monitor."

class Alert():
    def __init__(self, battery, fish, oxygen, ships):
        self.alert = np.zeros(3).tolist()
        if (battery < 50 or oxygen < 50):
            self.alert[0] = 1
        elif (battery < 20 or oxygen < 20):
            self.alert[0] = 2

        if (fish.count('puffer') > 0 or fish.count('eel') > 0 or fish.count('whale') > 0):
            self.alert[1] = 1
        elif (fish.count('shark') > 0 or fish.count('sawfish') > 0 or fish.count('swordfish') > 0):
            self.alert[1] = 2

        if (len(ships) > 1):
            self.alert[2] = 1

class Base():
    def __init__(self, fish, allShips):
        #self.id=id
        self.fish = fish
        self.allShips = allShips
    #classes of base: Alert, Fauna, Optimizer, Precipitation, ShipRadar, Temperature, WindD, WindS
    def update(self):
        pass

class Diver():
    def __init__(self, allFish):

        #self.id = id
        self.allFish = allFish
    #classes of diver: Battery, Danger, Heart, Light, Oxygen, Position, Pressure, Radar
    def update(self):
        pass

class Fish():
    names = ['tuna', 'cod', 'grouper', 'salmon', 'sturgeon',
             'marlin', 'hake', 'angler', 'barracuda', 'eel',
             'puffer', 'sunfish', 'snapper', 'halibut', 'seahorse',
             'sawfish', 'flounder', 'swordfish', 'shark', 'whale']

    def __init__(self):
        self.name = self.names[random.randint(0, len(self.names) - 1)]
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.z = random.randint(0, 200)
        self.position = np.array((self.x, self.y, self.z))
        self.speed = random.randint(0, 100)

    def update(self):
        self.x = min(500, max(0, self.x + sign(0.5) * round(self.speed / 2)))
        self.y = min(500, max(0, self.y + sign(0.5) * round(self.speed / 2)))
        new_z = min(200, max(0, self.z + sign(0.5) * round(self.speed / 4)))
        # change in z positive if they went deeper
        z_shift = new_z - self.z
        self.z = new_z
        new_position = np.array((self.x, self.y, self.z))
        total_shift = np.linalg.norm(new_position - self.position)
        self.position = np.copy(new_position)
        self.speed = random.randint(0, 100)

class Ship():
    sizes = ['small', 'medium', 'large']

    def __init__(self):
        self.size = self.sizes[random.randint(0, len(self.sizes) - 1)]
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.position = np.array((self.x, self.y, 0))
        self.speed = random.randint(0, 100)

    def update(self):
        self.x = min(500, max(0, self.x + sign(0.5) * round(self.speed / 2)))
        self.y = min(500, max(0, self.y + sign(0.5) * round(self.speed / 2)))
        self.position = np.array((self.x, self.y, 0))
        self.speed = random.randint(0, 100)

#common interface
def emit(node):
    pass

#auxiliary coinflip method
def sign(threshold):
    rand = random.random()
    if (rand < threshold):
        return -1
    return 1

def updateFish(fish):
    for f in fish:
        f.update()


"""
#test main
divers = []
bases = []
fish = []
ships = []

for i in range (0,200):
    fish.append(Fish())
    ships.append(Ship())


for i in range(1,6):
    divers.append(Diver(i, fish))
    bases.append(Base(i))


for i in range (1,11):
    print(divers[2].radar)
    divers[2].update()
    updateFish(fish)
    time.sleep(3)
"""
