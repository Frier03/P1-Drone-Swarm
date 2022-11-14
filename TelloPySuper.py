
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
    tello = None
    pos_x, pos_y, pos_z = 0, 0, 0
    vel_x, vel_y = 0, 0
    
    ip = None
    mac = None

    def __init__(self, ip="192.168.10.1", port=9000, mac="aa:aa:aa:aa:aa"):        
        self.tello = Tello(port=port)
        #self.tello.subscribe(self.tello.EVENT_FLIGHT_DATA, self.handler)
        self.tello.subscribe(self.tello.EVENT_LOG_DATA, self.handler)
        self.tello.subscribe(self.tello.EVENT_FLIGHT_DATA, self.handler)
        self.tello.set_loglevel(Tello.LOG_WARN)

        self.tello.tello_addr = (ip, 8889)
        self.tello.video_enabled = False
        self.tello.connect()

        self.ip = ip
        self.mac = mac

    
    lastResponse = 0
    lastAcceleration = 0
    def handler(self, event, sender, data, **args):
        if event == Tello.EVENT_FLIGHT_DATA:
            self.pos_z = data.height                #protocol.py -> FlightData.height
            
        if event == Tello.EVENT_LOG_DATA:
            #drone = sender
            acc_x = data.imu.acc_x                  #protocol.py -> Logdata.LogImuAtti(log).acc_x
            acc_y = data.imu.acc_x                  #protocol.py -> Logdata.LogImuAtti(log).acc_y
            t = time() - self.lastResponse

            #Only calculate if new values and if time is reasonable
            if int(t) < 5 and acc_x != self.lastAcceleration:
                #Convert quaternions to roll, pitch and yaw in degrees
                roll, pitch, yaw = euler_from_quaternion(data.imu.q0, data.imu.q1, data.imu.q2, data.imu.q3)
                #Legendary formula - Corrigate for gravity
                realAccX = acc_x + (math.cos(math.radians(90-pitch)))
                realAccY = acc_y + (math.cos(math.radians(90-yaw)))
            
                #Calculate velocity
                self.vel_x = (realAccX * t) + self.vel_x
                self.vel_y = (realAccY * t) + self.vel_y
                
                #Calculate position
                self.pos_x = (0.5 * realAccX * (t**2) + self.vel_x * t) + self.pos_x
                self.pos_y = (0.5 * realAccY * (t**2) + self.vel_y * t) + self.pos_y
                
                print("Custom X :", self.pos_x, "Y :", self.pos_y, "Z :", self.pos_z)

            self.lastResponse = time()
            self.lastAcceleration = acc_x
            
        
        

    def goUp(self, centimeter):
        self.tello.up(centimeter)
        self.x += centimeter

    def emergencyStop(self):
        print("EMERGENCY STOP")



drone1 = Drone(ip="192.168.137.133", port=9000)

sleep(2)
print("OBJECT MADE")
for i in range(1):
    sleep(1)



