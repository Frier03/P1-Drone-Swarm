
from djitellopy import Tello as dji
from time import sleep, time
import atexit
import math
import logging
from threading import Thread
import enum





class Drone():
    class FlyingStage(enum.Enum):
        MissionDone = -1
        Idle = 0
        MissionActive = 1

    def __init__(self, mac="aa:aa:aa:aa:aa", offset = 50, distanceBetweenPads = 57):
        self.dji : dji = None

        #--------- Info variables ----------------
        self.ip = 0
        self.mac = mac
        self.is_flying = False
        self.connected = False
        self.guiStatus: str = "Connect"     #Connect, Disconnected, Connecting, Calibrated, Calibrating, Failed
        self.stage = self.FlyingStage.Idle

        #--------- Swarm variables ----------------
        self.route = None
        self.nextPad = -1
        self.shouldTakeoff = False
        self.shouldLand = False

        #--------- Drone variables ----------------
        self.mID = -1
        self.localX = -100
        self.localY = -100
        self.localZ = -100
        self.abs_x = 0
        self.abs_y = 0
        self.abs_z = 0
        self.rotation = 0
        self.battery = 0
        self.totalSpeed = 0
        self.originalYaw = 0
        self.timeOfFlight = -1

        self.isMoving = False
        self.lastSeenPad = 0
        self.isDataNew = False
        self.distanceBetweenPads = distanceBetweenPads
        self.offset = offset
        

        self.reset()

        #Start position updater thread
        T = Thread(target=self.mainUpdater)
        T.daemon = True
        T.start()

        #Start mover thread
        TPad = Thread(target=self.padder)
        TPad.daemon = True
        TPad.start()


    def setIp(self, newIP):
        self.connected = False
        self.ip = newIP

        if self.dji:        #If already exists, delete before creating a new one
            del self.dji

        self.dji = dji(host=newIP.strip(), retry_count=1)   #Generates an error after x (3) retries
        self.dji.LOGGER.setLevel(logging.ERROR)              #For debugging and output in terminal

        for i in range(3):      #Try connect up to 3 times
            try:
                self.dji.connect()  #Is changed to timeout after 1 sec. Look package files
                #Connect generates an error if not connected
                self.dji.enable_mission_pads()
                self.dji.set_mission_pad_detection_direction(2)     #Forward and downward

                self.originalYaw = self.dji.get_yaw()               #Remember first yaw
                self.dji.TAKEOFF_TIMEOUT = 30
                self.connected = True
                return True
            except Exception as e:
                print("exception", e)
        return False

    def reset(self):
        self.route = None
        self.nextPad = -1
        self.stage = self.FlyingStage.Idle

    def isCenter(self):
        if -10 < self.localX < 10 and -10 < self.localY < 10:
            return True
        return False

    def mainUpdater(self):
        while True:
            try:
                if self.connected:
                    #self.is_flying = self.dji.is_flying        #We made our own
                    self.rotation = self.dji.get_yaw() - self.originalYaw
                    self.totalSpeed = math.sqrt(self.dji.get_speed_x()**2 + self.dji.get_speed_y()**2 + self.dji.get_speed_z()**2)
                    self.battery = self.dji.get_battery()
                    self.timeOfFlight = self.dji.get_flight_time()

                    #POSITION CALCULATIONS
                    self.mID = self.dji.get_mission_pad_id()
                    self.localX = self.dji.get_mission_pad_distance_x()
                    self.localY = self.dji.get_mission_pad_distance_y()
                    self.localZ = self.dji.get_mission_pad_distance_z()
                    
                    if self.mID != -1:               #If a pad is found
                        xRow = (self.mID-1)//3       #Just think about. Its very easy to understand
                        yRow = (self.mID-1) % 3
                        
                        self.abs_x = self.offset + (xRow * self.distanceBetweenPads) + (-self.localX)
                        self.abs_y = self.offset + (yRow * self.distanceBetweenPads) + (-self.localY)
                        self.abs_z = self.localZ

                        #print(f"{self.mID}  |  LOCAL {self.localX=:5} {self.localY=:5} {self.localZ=:5}   |  ABS {self.abs_x:5} {self.abs_y:5} {self.abs_z:5}")

                        self.lastSeenPad = self.mID
                        self.isDataNew = True
                    else:
                        self.isDataNew = False
                        #print("No pad?")
            except:
                pass
                #print("Is this updating the ip?")
            sleep(0.1)


    def GoToPad(self, pad):
        self.isMoving = True
        if self.mID == pad:             #Centering over pad
            #print("Centering over", pad)
            try:    self.dji.go_xyz_speed_mid(0, 0, 80, 15, pad) #Changed timeout to 11
            except: pass
        else:                           #Jumping to pad
            #print("Jump to pad", pad)
            xRow = (self.mID-1)//3 - (pad-1)//3
            yRow = (self.mID-1) % 3 - (pad-1) % 3
            xRow = xRow * self.distanceBetweenPads
            yRow = yRow * self.distanceBetweenPads
            try:    self.dji.go_xyz_speed_yaw_mid(xRow, yRow, 80, 50, 0, self.mID, pad)
            except: pass
            
        self.isMoving = False


    def padder(self):
        while True:
            if self.shouldTakeoff == True:
                try:
                    self.dji.takeoff()
                    self.stage = self.FlyingStage.MissionActive
                except: pass
                self.shouldTakeoff = False
                
            if self.shouldLand == True:
                try:
                    self.dji.go_xyz_speed_mid(0, 0, 30, 10, self.mID)
                except: pass
                try:
                    self.dji.land()
                except: pass
                self.stage = self.FlyingStage.MissionDone
                self.shouldLand = False
                
            
            #print("PADDER", self.is_flying and self.nextPad != -1 and not self.isMoving)
            if self.stage == self.FlyingStage.MissionActive and self.nextPad != -1 and not self.isMoving:
                self.GoToPad(self.nextPad)
            sleep(0.1)




def plotCoords(drone):
    # FOR PLOTTING coordinates
    import matplotlib.pyplot as plt
    plt.ion()
    plt.axis([-20, 100, -20, 100])

    xlist = []
    ylist = []

    for i in range(10000):
        plt.plot(drone.abs_x, drone.abs_y)
        if drone.connected and drone.isDataNew:
            plt.scatter(drone.abs_y, drone.abs_x)
            plt.draw()
            plt.pause(0.05)
        sleep(0.2)

def testJump(drone):
    if drone.connected:
        print('Hello')
        sleep(1)
        drone.dji.takeoff()
        drone.dji.go_xyz_speed_yaw_mid(0,-50,100,50,0,1,2)
        drone.dji.go_xyz_speed_yaw_mid(50,0,100,20,0,2,3)
        drone.dji.go_xyz_speed_yaw_mid(0,50,100,50,0,3,4)
        drone.dji.go_xyz_speed_yaw_mid(-50,0,100,50,0,4,1)
        print('Done')
        for i in range (5):
            print(f'Con={drone.connected:1} Bat:{drone.battery} | Mid={drone.lastSeenPad:3} | {drone.abs_x:2}, {drone.abs_y:2}, {drone.abs_z:2}')
            sleep(1)
            print('Well Done')
        drone.dji.land()



if __name__ == "__main__":
    drone = Drone()
    drone.setIp("192.168.137.236")
    print(f"{drone.battery=} {drone.mac=}")
    
    
    while not drone.stage == drone.FlyingStage.MissionActive:
        drone.shouldTakeoff = True
        print(".", end="")
        sleep(0.1)
    print("\nFlying")

    print(f"{drone.is_flying=}")

    path = [3, 2, 5, 8]
    for i, pad in enumerate(path):
        drone.nextPad = pad
        print(f"Target sat: {drone.mID=}    {drone.nextPad=}")
        while not ( drone.mID == drone.nextPad and drone.isCenter() ):
            sleep(0.1)
    
    print("MISSION ACCOMPLISHED")

    drone.shouldLand = True
    print("Done")
    sleep(1)

    sleep(999)


