from DJITelloPySuper import Drone
from time import sleep



class Swarm:
    drones: list[Drone] = []
    old_drones = []    

    def __init__(self, macs):
        for m in macs:
            self.drones.append( Drone(mac=m) )
    

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


    def startMission():
        pass

    def EMERGENCY():
        pass

    

from wifiSetup import DroneConnector
if __name__ == "__main__":
    SC = Swarm()
    DC = DroneConnector(SC.updateConnections)
    print("Starting")

    for i in range(10000):
        for drone in SC.drones:
            pass
            #print(drone.mID, f"{drone.connected=} | Absolute", drone.abs_x, "|", drone.abs_y, "|", drone.abs_z)
        sleep(0.2)
    
    sleep(1000)
