
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
    vel_x, vel_y, vel_z = 0, 0, 0
    
    ip = None
    mac = None
    lastResponse = 0
    lastAcceleration = 0

    def __init__(self, ip="192.168.10.1", port=9000, mac="aa:aa:aa:aa:aa"):        
        self.tello = Tello(port=port)
        #self.tello.subscribe(self.tello.EVENT_FLIGHT_DATA, self.handler)
        self.tello.subscribe(self.tello.EVENT_LOG_DATA, self.handler)
        self.tello.set_loglevel(Tello.LOG_WARN)

        self.tello.tello_addr = (ip, 8889)
        self.tello.video_enabled = False
        self.tello.connect()

        self.ip = ip
        self.mac = mac


    def handler(self, event, sender, data, **args):
        drone = sender

        a = data.imu.acc_x
        t = time() - self.lastResponse

        #We use pitch only
        roll, pitch, yaw = euler_from_quaternion(data.imu.q0, data.imu.q1, data.imu.q2, data.imu.q3)
        #Legendary formula
        realAccX = a + (math.cos(math.radians(90-pitch)))
        #print("RealX", realAccX, "| Acc |", a, "Pitch", pitch)
        
        if int(t) < 5 and a != self.lastAcceleration:
            self.vel_x = (realAccX * t) + self.vel_x
            self.pos_x = (0.5 * realAccX * (t**2) + self.vel_x * t) + self.pos_x
            print("Custom VelX =", self.vel_x, "Custom PosX", self.pos_x)
        else:
            #print("Skipped")
            pass

        self.lastResponse = time()
        self.lastAcceleration = a
        
        
        

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



