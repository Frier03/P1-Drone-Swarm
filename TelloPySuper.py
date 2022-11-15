
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
        self.tello.subscribe(self.tello.EVENT_LOG_DATA, self.dataHandler)
        self.tello.subscribe(self.tello.EVENT_FLIGHT_DATA, self.dataHandler)
        #self.tello.subscribe(self.tello.EVENT_CONNECTED, self.connectedMethod)     #Til rapporten
        #self.tello.subscribe(self.tello.EVENT_DISCONNECTED, self.connectedMethod)  #Dette burde vi IKKE gøre
        self.tello.set_loglevel(Tello.LOG_WARN)

        self.tello.tello_addr = (ip, 8889)
        self.tello.video_enabled = False
        self.tello.connect()

        #Custom variables -----------------------
        self.mac = mac
        self.calibrated = False
        self.pos_x, self.pos_y, self.pos_z = 0, 0, 0
        self.vel_x, self.vel_y = 0, 0

        #Grabbed from logdata
        self.battery = 0

        #Calibration
        self.calibrateCounter = 0
        self.NOCTPET = 200               #Number of calibrations to perform each time
        self.avgACC = (0, 0, 0)
        self.avgROT = (0, 0, 0)
        self.avgVEL = (0, 0, 0)
        self.avgPOS = (0, 0, 0)
        self.CalibrateAcceleration()

        #Delete me
        self.sum1 = 0
        self.sum2 = 0
        self.sum3 = 0


    def CalibrateAcceleration(self):
        self.calibrateCounter = self.NOCTPET


    
    lastResponse, lastAcceleration = 0, 0
    def dataHandler(self, event, sender, data, **args):
        if event == Tello.EVENT_FLIGHT_DATA:
            #drone = sender
            self.pos_z = data.height                #protocol.py -> FlightData.height
            self.battery = data.battery_percentage
            
        
        if event == Tello.EVENT_LOG_DATA:
            t = time() - self.lastResponse

            #Only calculate if new values and if time is reasonable
            if int(t) < 5:# and data.imu.acc_x != self.lastAcceleration:
                
                if not self.calibrated:
                    if self.calibrateCounter % 50 == 0:
                        print(self.calibrateCounter)
                    
                    ax = data.imu.acc_x
                    ay = data.imu.acc_y
                    az = data.imu.acc_z
                    rr, rp, ry = euler_from_quaternion(data.imu.q0, data.imu.q1, data.imu.q2, data.imu.q3)

                    if 200 >= self.calibrateCounter > 100: #ACCELERATION AND ROTATION
                        nor = 100 # number of runs
                        self.avgACC = (self.avgACC[0] + data.imu.acc_x/nor, self.avgACC[1] + data.imu.acc_y/nor, self.avgACC[2] + data.imu.acc_z/nor)
                        self.avgROT = (self.avgROT[0] + rr/nor, self.avgROT[1] + rp/nor, self.avgROT[2] + ry/nor)
                        #print("avgACC %20s avgROT %20s." % (self.avgACC, self.avgROT))

                    elif 100 >= self.calibrateCounter > 50:  #VELOCITY
                        nor = 50
                        fax = ax - self.avgACC[0]
                        fay = ay - self.avgACC[1]
                        roll, pitch, yaw = euler_from_quaternion(data.imu.q0, data.imu.q1, data.imu.q2, data.imu.q3)
                        fpitch = pitch - self.avgROT[1]
                        fyaw = yaw - self.avgROT[2]
                        rfax = fax - (math.cos(math.radians(90-fpitch))) * self.avgACC[2]
                        rfay = fay - (math.cos(math.radians(90-fyaw))) * self.avgACC[2]
                        vx = (rfax * t)
                        vy = (rfay * t)
                        self.avgVEL = (self.avgVEL[0] + vx/nor, self.avgVEL[1] + vy/nor, 0)
                        #print(self.avgVEL)


                    elif 50 >= self.calibrateCounter:        #POSITION
                        nor = 50
                        fax = ax - self.avgACC[0]
                        fay = ay - self.avgACC[1]
                        roll, pitch, yaw = euler_from_quaternion(data.imu.q0, data.imu.q1, data.imu.q2, data.imu.q3)
                        fpitch = pitch - self.avgROT[1]
                        fyaw = yaw - self.avgROT[2]
                        rfax = fax - (math.cos(math.radians(90-fpitch))) * self.avgACC[2]
                        rfay = fay - (math.cos(math.radians(90-fyaw))) * self.avgACC[2]
                        vx = (rfax * t) - self.avgVEL[0]
                        vy = (rfay * t) - self.avgVEL[1]

                        sx = (0.5 * rfax * t**2) + (vx * t)
                        sy = (0.5 * rfay * t**2) + (vy * t)

                        self.avgPOS = (self.avgPOS[0] + sx/nor, self.avgPOS[1] + sy/nor, 0)
                        #print("AVGPOS =", self.avgPOS)


                    if self.calibrateCounter == 1:
                        self.calibrated = True
                    
                    self.calibrateCounter -= 1

                else:
                    ax = data.imu.acc_x              #protocol.py -> Logdata.LogImuAtti(log).acc_x
                    ay = data.imu.acc_y
                    az = data.imu.acc_z              #Dont adjust "gravity"              

                    fax = ax - self.avgACC[0]
                    fay = ay - self.avgACC[1]
                    roll, pitch, yaw = euler_from_quaternion(data.imu.q0, data.imu.q1, data.imu.q2, data.imu.q3)
                    fpitch = pitch - self.avgROT[1]
                    fyaw = yaw - self.avgROT[2]
                    rfax = fax - (math.cos(math.radians(90-fpitch))) * self.avgACC[2]
                    rfay = fay - (math.cos(math.radians(90-fyaw))) * self.avgACC[2]

                    tolerance = 0.0025
                    if rfax - tolerance > 0 or 0 > rfax + tolerance:
                        self.vel_x = ((rfax * t) - self.avgVEL[0]) + self.vel_x
                    else:
                        self.vel_x = 0
                    
                    if rfay - tolerance > 0 or 0 > rfay + tolerance:
                        self.vel_y = ((rfay * t) - self.avgVEL[1]) + self.vel_y
                    else:
                        self.vel_y = 0
                    
                    self.pos_x = (0.5 * rfax * t**2) + (self.vel_x * t) + self.pos_x
                    self.pos_y = (0.5 * rfay * t**2) + (self.vel_y * t) + self.pos_y
                    
                    self.pos_x -= self.avgPOS[0]
                    self.pos_y -= self.avgPOS[1]

                    #print("ACCEL X %8f   Y %8f    Z %8f" % (abs(rfax), abs(rfay), az))
                    #print("VEL X %8f   Y %8f    Z %8f" % (self.vel_x, abs(self.vel_y), az))
                    print("COORDS X %2f   Y %2f    Z %8f" % (round(self.pos_x*100, 2), round(self.pos_y*100, 2), self.pos_z))
            else:
                print("INVALID")

            self.lastResponse = time()
            self.lastAcceleration = data.imu.acc_x
    

    def goUp(self, centimeter):
        self.tello.up(centimeter)
        self.x += centimeter

    def emergencyStop(self):
        print("EMERGENCY STOP")


if __name__ == "__main__":

    drone1 = Drone(ip="192.168.137.56", port=9001)
    
    print("OBJECT MADE")
    for i in range(100):
        #print("Drone battery =", drone1.tello)
        drone1.tello.land()
        #print(drone1.tello.state)
        sleep(1)
    

    #Swarm kan bruge
    drone1.pos_x        #Position
    drone1.tello.state  #Connected, connecting

