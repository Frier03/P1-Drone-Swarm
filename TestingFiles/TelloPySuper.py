
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
        self.pitch = 0
        self.battery = 0

        #Grabbed from logdata
        self.battery = 0

        #Calibration
        self.calibrateCounter = 0
        self.NOCTPET = 250               #Number of calibrations to perform each time
        self.avgACC = (0, 0, 0)
        self.avgROT = (0, 0, 0)
        self.avgVEL = (0, 0, 0)
        self.avgPOS = (0, 0, 0)
        self.CalibrateAcceleration()
        self.standingStillCounter = 0

        self.dillerx = []
        self.dillery = []


    def CalibrateAcceleration(self):
        self.calibrateCounter = self.NOCTPET
        self.calibrated = False


    
    lastResponseTime, lastDataRecieved = 0, 0
    def dataHandler(self, event, sender, data, **args):
        if event == Tello.EVENT_FLIGHT_DATA:
            #drone = sender
            self.pos_z = data.height                #protocol.py -> FlightData.height
            self.battery = data.battery_percentage
            
        
        if event == Tello.EVENT_LOG_DATA:
            t = time() - self.lastResponseTime

            #Only calculate if new values and if time is reasonable
            if int(t) < 5:# and data.imu.acc_x != self.lastDataRecieved:
                
                if not self.calibrated:
                    if self.calibrateCounter % 50 == 0:
                        print(self.calibrateCounter)
                    
                    ax = data.imu.acc_x
                    ay = data.imu.acc_y
                    az = data.imu.acc_z
                    rr, rp, ry = euler_from_quaternion(data.imu.q0, data.imu.q1, data.imu.q2, data.imu.q3)

                    if 250 >= self.calibrateCounter > 150: #ACCELERATION AND ROTATION
                        nor = 100 # number of runs
                        self.avgACC = (self.avgACC[0] + data.imu.acc_x/nor, self.avgACC[1] + data.imu.acc_y/nor, self.avgACC[2] + data.imu.acc_z/nor)
                        self.avgROT = (self.avgROT[0] + rr/nor, self.avgROT[1] + rp/nor, self.avgROT[2] + ry/nor)
                        #print("avgACC %20s avgROT %20s." % (self.avgACC, self.avgROT))

                    elif 150 >= self.calibrateCounter > 50:  #VELOCITY
                        nor = 100
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

                    tolerance = 0.006
                    if (rfax - tolerance > 0 or 0 > rfax + tolerance) and (rfay - tolerance > 0 or 0 > rfay + tolerance):
                        self.vel_x = ((rfax * t) + self.vel_x) - self.avgVEL[0]
                        self.vel_y = ((rfay * t) + self.vel_y) - self.avgVEL[1]
                        #print("Accelerated")
                        self.standingStillCounter = 0
                    else:
                        self.standingStillCounter += 1
                        print(50*"-" + "STANDING STILL")

                        if self.standingStillCounter >= 10:
                            self.vel_x = 0
                            self.vel_y = 0

                            self.standingStillCounter = 0
                            print(60*"-" + "RESET VELOCITY")
                        #print("Same")
                    
                    self.pos_x = (0.5 * rfax * t**2) + (self.vel_x * t) + self.pos_x
                    self.pos_y = (0.5 * rfay * t**2) + (self.vel_y * t) + self.pos_y
                    
                    self.pos_x -= self.avgPOS[0]
                    self.pos_y -= self.avgPOS[1]

                    #print("ACCEL X %8f   Y %8f    Z %8f" % (abs(rfax*100), abs(rfay*100), az))
                    #print("VEL X %8f   Y %8f    Z %8f" % (self.vel_x, abs(self.vel_y), az))
                    print("COORDS X %2f   Y %2f    Z %8f" % (round(self.pos_x*100, 2), round(self.pos_y*100, 2), self.pos_z))


                    self.pitch = fpitch
                    self.dillerx.append(self.pos_x*100)
                    self.dillery.append(self.pos_y*100)



            self.lastResponseTime = time()
            self.lastDataRecieved = data.imu.acc_x
    

    def goUp(self, centimeter):
        self.tello.up(centimeter)
        self.x += centimeter

    def emergencyStop(self):
        print("EMERGENCY STOP")


if __name__ == "__main__":

    drone1 = Drone(ip="192.168.137.146", port=9001)
    
    print("OBJECT MADE")
    for i in range(50):
        if drone1.calibrated == True:
            break
        print("Still sleeping")
        sleep(1)
    
    
    drone1.tello.takeoff()
    sleep(5)
    print("FORWARD")
    drone1.tello.forward(10)
    sleep(5)
    print("BACKWARD")
    drone1.tello.backward(10)
    sleep(5)
    print("LAND")
    drone1.tello.land()
    print("PLOTTING IN 5 SECONDS")
    sleep(5)
    print("PLOTTING NOW")
    import matplotlib.pyplot as plt
    plt.plot(drone1.dillerx, drone1.dillery, 'bo', label="PATH")
    plt.legend()
    plt.show()


    #Swarm kan bruge
    drone1.pos_x        #Position
    drone1.tello.state  #Connected, connecting

