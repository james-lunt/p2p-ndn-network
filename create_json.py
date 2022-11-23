import json

Addresses = ["rasp-014", "rasp-045"]

Networks = ["divers", "scientists"]

Divers = ["diver1","diver2","diver3","diver4","diver5"]

Scientists = ["scientist1", "scientist2", "scientist3","scientist4","scientist5"]

DiverSensors = ["light", "oxygen", "position", "pressure", "radar", "heart rate", "battery", "danger alert", "notifier"]

ScientistSensors = ["ship recogniser", "fauna recogniser", "power optimisation", "wind power", "wind direction", "temperature", "precipitation", "diver alert"]

listen_port = 33001
send_port = 33002
json_array = []
for diver in Divers:
    for sensor in DiverSensors:
        json_array.append({"/" + Networks[0] + "/" + diver + "/" + sensor : [{"listen port": listen_port,"send port": send_port,"address": Addresses[0]}]})
        listen_port += 2
        send_port += 2

for scientist in Scientists:
    for sensor in ScientistSensors:
        json_array.append({"/" + Networks[1] + "/" + scientist + "/" + sensor : [{"listen port": listen_port,"send port": send_port,"address": Addresses[1]}]})
        listen_port += 2
        send_port += 2


with open('interface_ports1.json', 'w') as f:
  json.dump(json_array, f, indent=4)

"""
file = open('interface_ports.json')
data = json.load(file)
network_details = data[0]["/divers/diver1/light"]
listen_port = network_details[0]["listen port"]
print(listen_port)
"""
