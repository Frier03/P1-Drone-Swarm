from DJITelloPySuper import Drone
from time import sleep
from threading import Thread
import enum
import random

class MissionStatus(enum.Enum):
    Idle = 0
    Emergency = 1
    Test = 2


class Swarm:
    drones: list[Drone] = []
    old_drones = []

    status = MissionStatus.Idle

    def __init__(self, macs=["FF-FF-FF-FF-FF"], offset=50, distanceBetweenPads=57):
        for mac in macs:
            self.drones.append( Drone(mac, offset, distanceBetweenPads) )
        
        T = Thread(target=self.controller)
        T.daemon = True
        T.start()
    
    def startMission(self):
        self.status = MissionStatus.Test

    def EMERGENCY(self):
        self.status = MissionStatus.Emergency


    def findDrone(self, mac):
        for drone in self.drones:
            if drone.mac.upper() == mac.upper():
                return drone
        return False


    def updateConnections(self, current_drones):
        """ Updates Drone Status depending on the paramater arg (list)"""
        just_connected = current_drones[:]
        just_disconnected = self.old_drones[:]
        #Do the magic
        for i in current_drones:
            for j in self.old_drones:
                if i[1] == j[1]:
                    just_disconnected.remove(j)
                    just_connected.remove(i)
        

        if len(just_connected) > 0:
            print("New connection", just_connected)
            for jc in just_connected:
                found = self.findDrone(jc[1])
                if found:                           #Reconnect
                    found.setIp(jc[0])
                
                elif found == False:                #New connect
                    drone = Drone(mac=jc[1])
                    drone.setIp(jc[0])
                    self.drones.append(drone)

        
        if len(just_disconnected) > 0:              #Disconnect
            print("Disconnected", just_disconnected)
            for jd in just_disconnected:
                found = self.findDrone(jd[1])
                found.connected = False
        
        self.old_drones = current_drones


    def controller(self):
        while True:
            if self.status == MissionStatus.Emergency:
                for drone in self.drones:
                    drone.dji.emergency()
                self.status = MissionStatus.Idle
            
            elif self.status == MissionStatus.Test:
                pass

                self.status = MissionStatus.Idle

            #Testing
            for drone in self.drones:
                #print(f"{drone.mac} {drone.abs_x:5} {drone.abs_y:5}   |", end="")
                pass
            #print("")
            
            sleep(1)

    def CalcRoute(self, start, target):
        pos_routes: list[int] = [ # Possible route combinations
        [2, 4], # Node 1
        [1, 5, 3], # Node 2
        [2, 6], # Node 3
        [1, 5, 7], # Node 4
        [2, 4, 8, 6], # Node 5
        [3, 5], # Node 6
        [4, 8], # Node 7
        [5, 7] # Node 8
        ]
        queue = [ [start] ]
        seen = [start]

        while queue:
            path = queue.pop(0)
            if path[-1] == target:
                return path
            for nextPaths in pos_routes[path[-1] - 1]:
                if nextPaths not in seen:
                    queue.append(path + [nextPaths])
                    seen.append(nextPaths)



if __name__ == "__main__":
    SC = Swarm()



