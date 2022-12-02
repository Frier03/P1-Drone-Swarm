
from djitellopy import Tello as dji
from time import sleep, time
import atexit
import math
import logging
from threading import Thread


class Drone():
    def __init__(self, mac="aa:aa:aa:aa:aa", offset = 50, distanceBetweenPads = 57):
        self.dji : dji = None

        #Custom variables -----------------------
        self.ip = 0
        self.mac = mac
        self.is_flying = False
        self.connected = False
        self.guiStatus: str = "Connect"     #Connect, Disconnected, Connecting, Calibrated, Calibrating, Failed

        self.mID = -1
        self.abs_x = 0
        self.abs_y = 0
        self.abs_z = 0
        self.rotation = 0
        self.battery = 0
        self.totalSpeed = 0
        self.originalYaw = 0

        self.lastSeenPad = 0
        self.isDataNew = False
        self.distanceBetweenPads = distanceBetweenPads
        self.offset = offset

        #Start position updater thread
        T = Thread(target=self.mainUpdater)
        T.daemon = True
        T.start()


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
                self.dji.set_mission_pad_detection_direction(0)     #Forward and downward

                self.originalYaw = self.dji.get_yaw()               #Remember first yaw

                self.connected = True
                return True
            except Exception as e:
                print("exception", e)
        return False


    def mainUpdater(self):
        while True:
            try:
                if self.connected:
                    self.is_flying = self.dji.is_flying
                    self.rotation = self.dji.get_yaw() - self.originalYaw
                    self.totalSpeed = math.sqrt(self.dji.get_speed_x()**2 + self.dji.get_speed_y()**2 + self.dji.get_speed_z()**2)
                    self.battery = self.dji.get_battery()

                    #POSITION CALCULATIONS
                    self.mID = self.dji.get_mission_pad_id()
                    x = self.dji.get_mission_pad_distance_x()
                    y = self.dji.get_mission_pad_distance_y()
                    z = self.dji.get_mission_pad_distance_z()
                    
                    if self.mID != -1:               #If a pad is found
                        xRow = (self.mID-1)//3       #Just think about. Its very easy to understand
                        yRow = (self.mID-1) % 3
                        
                        self.abs_x = self.distanceBetweenPads * xRow + -x + self.offset
                        self.abs_y = self.distanceBetweenPads * yRow + -y + self.offset
                        self.abs_z = z

                        print(f"{self.mID}  |  LOCAL {x=:5} {y=:5} {z=:5}          |          ABS {self.abs_x:5} {self.abs_y:5} {self.abs_z:5}")


                        self.lastSeenPad = self.mID
                        self.isDataNew = True
                    else:
                        self.isDataNew = False
                        #print("No pad?")
            except:
                pass
                #print("Is this updating the ip?")
            sleep(0.5)


    def jumpToPad(self, pad):
        pass
    
    



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
    droneF = Drone()

    while droneF.connected == False:
        droneF.setIp("192.168.137.252")
        print("connecting")

    print("established")
    sleep(999)
