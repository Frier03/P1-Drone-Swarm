from DJITelloPySuper import Drone
from time import sleep
from threading import Thread
import enum
import random

class MissionStatus(enum.Enum):
    Idle = 0
    Debug = 1
    Emergency = 2
    Swap = 3
    RandomPad = 4


class Swarm:
    drones: list[Drone] = []
    old_drones = []
    status = MissionStatus.Idle
    droneTargets = {}

    def __init__(self, macs=["FF-FF-FF-FF-FF"], offset=50, distanceBetweenPads=57):
        for mac in macs:
            self.drones.append( Drone(mac, offset, distanceBetweenPads) )
        
        T = Thread(target=self.controller)
        T.daemon = True
        T.start()
    
    
    def CalcRoute(self, start, target, disabledSpots=[]):     #BREAD-th ALGORITHM
        if start <= 0 or target <= 0: return None
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
        allPaths = []          #Saves all paths

        # ORIGINAL BREAD'th algorithm
        while queue:
            path = queue.pop(0)
            allPaths.append(path)
            if path[-1] == target: return (path, 0)
            for nextPaths in pos_routes[path[-1] - 1]:
                if nextPaths not in seen and nextPaths not in disabledSpots:
                    queue.append(path + [nextPaths])
                    seen.append(nextPaths)
    
        # Expanded Bread. Nearest spot if no path found
        # Path is blocked
        nearestPath = ([1, 1, 1, 1], 9)    #Path, distance
        for p in allPaths:
            xRow = (p[-1]-1)//3 - (target-1)//3
            yRow = (p[-1]-1) % 3 - (target-1) % 3
            dist = abs(xRow) + abs(yRow)
            if dist < nearestPath[1]:
                nearestPath = (p, dist)
            elif dist == nearestPath and len(p) < len( nearestPath[0] ):
                nearestPath = (p, dist)
        return nearestPath


    def findDrone(self, mac):
        for drone in self.drones:
            if drone.mac.upper() == mac.upper():
                return drone
        return False


    def startMission(self, type):
        self.droneTargets = {}
        for drone in self.drones:
            drone.reset()
        
        if type == "Swap":
            self.status = MissionStatus.Swap
        elif type == "Random Pad":
            self.status = MissionStatus.RandomPad

        

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

        while True:
            if self.status == MissionStatus.Idle:
                pass
                #print(".", end="")
            
            if self.status == MissionStatus.Emergency:
                for drone in self.drones:
                    drone.dji.emergency()
                self.status = MissionStatus.Idle


            elif self.status == MissionStatus.Debug:
                for drone in self.drones:
                    print(f"{drone.mac} {drone.battery} {drone.abs_x:2} {drone.abs_y:2} |", end="")
                print("")



            elif self.status == MissionStatus.Swap or self.status == MissionStatus.RandomPad:
                activeDrones = 0

                #GENERATE TARGETS
                if len(self.droneTargets) == 0:             #If no targets found, generate random pad as target
                    if self.status == MissionStatus.RandomPad:
                        for drone in self.drones:
                            r = -1
                            while r == -1 or r in self.droneTargets.values() or r == drone.lastSeenPad:      #Generate a random position
                                r = random.randint(1, 9)
                            self.droneTargets[drone.mac] = r
                    if self.status == MissionStatus.Swap:
                        pass
                    
                        
                #DRONE LOOP LOGIC
                for drone in self.drones:
                    if drone.stage == drone.FlyingStage.Idle:
                        drone.shouldTakeoff = True
                        print("TAKEOFF")
                    
                    elif drone.stage == drone.FlyingStage.MissionActive:
                        
                        disabledSpots = []
                        for d in self.drones:
                            if drone.mac != d.mac:          #All other drones than "drone"
                                disabledSpots.append(d.nextPad)
                                disabledSpots.append(d.lastSeenPad)

                                #Emergency
                                if drone.mID == d.mID:
                                    drone.dji.emergency()
                            

                        target = self.droneTargets[drone.mac]
                        drone.route = self.CalcRoute(drone.mID, target, disabledSpots)

                        if drone.isCenter():
                            #print("Drone is center")
                            if drone.route != None:
                                if drone.route[0][-1] == drone.lastSeenPad and drone.route[1] == 0:
                                    print(drone.mac, "LANDING")
                                    drone.shouldLand = True
                                elif len(drone.route[0]) == 1 and drone.route[1] != 0:
                                    pass
                                else:
                                    #print("Route:", drone.route, "Next pad =", drone.route[0][1])
                                    drone.nextPad = drone.route[0][1]
                            else: drone.nextPad = drone.mID
                    


                    elif drone.stage == drone.FlyingStage.MissionDone:
                        activeDrones += 1
                    
                
                    print(f"\n{drone.mac[-2:]} | {drone.battery}%  STAGE: {drone.stage}  Route: {drone.route} MID: {drone.mID}")
                
                
                if activeDrones == len(self.drones):
                    self.status = MissionStatus.Idle
                    print("Mission complete")
                else:
                    #print("Active drones " + str(activeDrones))
                    pass
                
            sleep(0.5)



if __name__ == "__main__":
    SC = Swarm(["F6", "D8"])

    #print(SC.CalcRoute(1, 8, [8]) )

    SC.updateConnections( [("192.168.137.66", "D8"), ("192.168.137.12", "F6")] )     #

    SC.status = MissionStatus.Debug

    sleep(999)


