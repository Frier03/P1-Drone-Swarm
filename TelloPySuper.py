
from tellopy import Tello
from time import sleep, time
import atexit
import math

#fra Nicolai (selfmade)
def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    #return roll_x, pitch_y, yaw_z # in radians
    return math.degrees(roll_x), math.degrees(pitch_y), math.degrees(yaw_z)


class Drone(Tello):    

    def __init__(self, ip="192.168.10.1", port=9000, mac="aa:aa:aa:aa:aa"):        
        self.tello = Tello(port=port)
        #self.tello.subscribe(self.tello.EVENT_FLIGHT_DATA, self.handler)
        self.tello.subscribe(self.tello.EVENT_LOG_DATA, self.handler)
        self.tello.subscribe(self.tello.EVENT_FLIGHT_DATA, self.handler)
        #self.tello.subscribe(self.tello.EVENT_CONNECTED, self.connectedMethod)     #Til rapporten
        #self.tello.subscribe(self.tello.EVENT_DISCONNECTED, self.connectedMethod)  #Dette burde vi IKKE gøre
        self.tello.set_loglevel(Tello.LOG_WARN)

        self.tello.tello_addr = (ip, 8889)
        self.tello.video_enabled = False
        self.tello.connect()

        #Custom variables -----------------------
        self.mac = mac
        self.pos_x, self.pos_y, self.pos_z = 0, 0, 0
        self.vel_x, self.vel_y = 0, 0

        #Grabbed from logdata
        self.battery = 0

        #Calibration
        self.calibrateCounter = 0
        self.NOCTPET = 200               #Number of calibrations to perform each time
        self.avgACC = (0, 0, 0)
        self.avgROT = (0, 0, 0)
        self.CalibrateAcceleration()


    def CalibrateAcceleration(self):
        self.calibrateCounter = self.NOCTPET


    
    lastResponse, lastAcceleration = 0, 0
    def handler(self, event, sender, data, **args):
        if event == Tello.EVENT_FLIGHT_DATA:
            #drone = sender
            self.pos_z = data.height                #protocol.py -> FlightData.height
            self.battery = data.battery_percentage
            
        
        if event == Tello.EVENT_LOG_DATA:
            
            if self.calibrateCounter > 0:
                if self.calibrateCounter % 100 == 0 or (self.calibrateCounter % 10 == 0 and self.calibrateCounter <= 100):
                    print("Calibrating: ", self.calibrateCounter)
                #Acceleration
                ax, ay, az = data.imu.acc_x, data.imu.acc_y, data.imu.acc_z
                self.avgACC = (self.avgACC[0] + ax/self.NOCTPET, self.avgACC[1] + ay/self.NOCTPET, self.avgACC[2] + az/self.NOCTPET)

                #Rotation
                rr, rp, ry = euler_from_quaternion(data.imu.q0, data.imu.q1, data.imu.q2, data.imu.q3)
                self.avgROT = (self.avgROT[0] + rr/self.NOCTPET, self.avgROT[1] + rp/self.NOCTPET, self.avgROT[2] + ry/self.NOCTPET)

                self.calibrateCounter -= 1
                #print("Acc avgACC %20s ." % (self.avgACC,))
            else:
                t = time() - self.lastResponse

                #Only calculate if new values and if time is reasonable
                if int(t) < 5 and data.imu.acc_x != self.lastAcceleration:
                    acc_x = data.imu.acc_x - self.avgACC[0]                  #protocol.py -> Logdata.LogImuAtti(log).acc_x
                    acc_y = data.imu.acc_y - self.avgACC[1]
                    acc_z = data.imu.acc_z # - self.avgACC[2]

                    #Convert quaternions to roll, pitch and yaw in degrees
                    roll, pitch, yaw = euler_from_quaternion(data.imu.q0, data.imu.q1, data.imu.q2, data.imu.q3)
                    
                    roll -= self.avgROT[0]
                    pitch -= self.avgROT[1]
                    yaw -= self.avgROT[2]

                    #Legendary formula - Corrigate for gravity
                    realAccX = acc_x - (math.cos(math.radians(90-pitch))) * self.avgACC[2]
                    realAccY = acc_y - (math.cos(math.radians(90-yaw))) * self.avgACC[2]        #Skal måske være roll
                    #print("Acceleration %8f, %8f, %8f, %8f" % (abs(realAccX), abs(acc_x), acc_z, pitch))

                    #Calculate velocity
                    self.vel_x = (realAccX * t) + self.vel_x
                    self.vel_y = (realAccY * t) + self.vel_y
                    print("Velocity X:%8f    Y:%8f" % (self.vel_x, self.vel_y))
                    
                    #Calculate position
                    self.pos_x = (0.5 * realAccX * (t**2) + self.vel_x * t) + self.pos_x
                    self.pos_y = (0.5 * realAccY * (t**2) + self.vel_y * t) + self.pos_y

                    #print("Coords X:%8f | Y:%8f | Z:%8f" % (self.pos_x*10, self.pos_y*10, self.pos_z*10))

                self.lastResponse = time()
                self.lastAcceleration = data.imu.acc_x
        

    def goUp(self, centimeter):
        self.tello.up(centimeter)
        self.x += centimeter

    def emergencyStop(self):
        print("EMERGENCY STOP")


if __name__ == "__main__":

    drone1 = Drone(ip="192.168.137.150", port=9000)
    
    print("OBJECT MADE")
    for i in range(100):
        sleep(1)
        #print("Drone battery =", drone1.tello)
        drone1.tello.land()
    

    #Swarm kan bruge
    drone1.pos_x        #Position
    drone1.tello.state  #Connected, connecting

