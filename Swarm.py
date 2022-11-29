from DJITelloPySuper import Drone


class Swarm:
    
    drones = []
    old_drones = []

    def __init__(self, drones: dict[str, Drone]):
        self.drones: dict[str, Drone] = drones

    def updateConnections(self, current_drones):
        """ Updates Drone Status depending on the paramater arg (list)"""
        
        just_connected = current_drones[:]
        just_disconnected = self.old_drones[:]
        
        for i in current_drones:
            for j in self.old_drones:
                if i[1] == j[1]:
                    just_disconnected.remove(j)
                    just_connected.remove(i)
        
        if len(just_connected) > 0: print("New connection", just_connected)
        if len(just_disconnected) > 0: print("Disconnected", just_disconnected)
        self.old_drones = current_drones


    def startMission():
        pass

    def EMERGENCY():
        pass

    

