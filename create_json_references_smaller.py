import json

Addresses = ["10.35.70.14", "10.35.70.45"]

Networks = ["divers"]

Divers = ["diver1","diver2","diver3"]
DiverNeighborList = [["/divers/diver3","/divers/diver4"], ["/divers/diver4","/divers/diver5"], ["/divers/diver1"]]

DiverSensors = ["light", "oxygen"]

json_array = []

listen_port = 33001
send_port = 33002
neighbor_itertator = 0
for diver in Divers:
    diver_name = "/" + Networks[0] + "/" + diver
    json_array.append({diver_name : [{"listen port": listen_port,"send port": send_port,"address": Addresses[0]},{"neighbors" : DiverNeighborList[neighbor_itertator]}]})
    listen_port += 2
    send_port += 2
    neighbor_itertator +=1
    for sensor in DiverSensors:
        json_array.append({"/" + Networks[0] + "/" + diver + "/" + sensor : [{"listen port": listen_port,"send port": send_port,"address": Addresses[0]},{"neighbors" : [diver_name]}]})
        listen_port += 2
        send_port += 2


with open('interfaces_smaller.json', 'w') as f:
  json.dump(json_array, f, indent=4)

