from DJITelloPySuper import Drone
from time import sleep
from threading import Thread
import enum
import random

class MissionStatus(enum.Enum):
    Idle = 0
    Debug = 1
    Emergency = 2
    Test = 3


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
    
    
    def CalcRoute(self, start, target, disabledSpots=[]):     #BREAD-th ALGORITHM
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
                if nextPaths not in seen and nextPaths not in disabledSpots:
                    queue.append(path + [nextPaths])
                    seen.append(nextPaths)

    def findDrone(self, mac):
        for drone in self.drones:
            if drone.mac.upper() == mac.upper():
                return drone
        return False


    def startMission(self):
        self.status = MissionStatus.Test

    def EMERGENCY(self):
        self.status = MissionStatus.Emergency

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
                sleep(3)
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


    def controller(self):       #THREAD
        controllerCounter = 0
        
        target = 0

        while True:
            if self.status == MissionStatus.Emergency:
                for drone in self.drones:
                    drone.dji.emergency()
                self.status = MissionStatus.Idle

            elif self.status == MissionStatus.Debug:
                if controllerCounter == 0:
                    print([drone.battery for drone in self.drones])
                controllerCounter += 1

                for drone in self.drones:
                    print(f"{drone.mac} {drone.battery} {drone.abs_x:2} {drone.abs_y:2} |", end="")
                print("")
            

            elif self.status == MissionStatus.Test:
                for drone in self.drones:
                    if drone.lastSeenPad != drone.nextPad and not drone.is_flying:
                        drone.shouldTakeoff = True
                    else:
                        print("MOVING")
                        if "F6" in drone.mac: target = 1
                        if "C6" in drone.mac: target = 8
                        disabledSpots = []
                        for d in self.drones:
                            if drone.mac != d.mac:
                                disabledSpots.append(d.nextPad)
                                disabledSpots.append(d.lastSeenPad)

                        drone.route = self.CalcRoute(drone.mID, target, disabledSpots)

                        print(f"{drone.mID=}   {drone.route=}")
                        if drone.isCenter():
                            print("Drone is center")
                            if drone.route != None:
                                if drone.route[-1] == drone.lastSeenPad:
                                    print(drone.mac, "LANDING")
                                    drone.shouldLand = True
                                else:
                                    print("Route:", drone.route, "Next pad =", drone.route[1])
                                    drone.nextPad = drone.route[1]
                            else: drone.nextPad = drone.mID
                                
            
            sleep(1)



if __name__ == "__main__":
    SC = Swarm(["F6"])

    SC.updateConnections( [("192.168.137.199", "F6"), ("192.168.137.61", "C6")] )     #

    SC.status = MissionStatus.Test

    sleep(999)


