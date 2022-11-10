from wifiSetup import DroneConnector
from time import sleep


DC = DroneConnector()
DC.hotspotSSID = "Bear"

avaiDrones = DC.findDrones()
if len(avaiDrones) >= 1:
    print("Available drones", [i.ssid for i in avaiDrones])
    for w in avaiDrones:
        if DC.calibrateDrone(w) == True:
            print(f"---- {w.ssid} calibrated ----")
    print()
    DC.connectWifi(DC.defaultWifi)
    DC.waitForConnection()
else:
    print("No available drones found")


DC.getConnectedDrones_Start_Thread()
