from wifiSetup import DroneConnector
from time import sleep


DC = DroneConnector()
DC.hotspotSSID = "Bear3"
DC.hotspotPASS = "joinTheNet"


DC.getConnectedDrones_Start_Thread()



avaiDrones = DC.findDrones()


if len(avaiDrones) >= 1:
    print("Available drones", [i.ssid for i in avaiDrones])
    for droneWifi in avaiDrones:

        print(f"\n--- Calibrating drone {droneWifi.ssid} ---")
        if droneWifi.auth == "Open" and droneWifi.encrypt == "None":
            
            if DC.calibrateDrone(droneWifi.ssid[-6:]) == True:
                print(f"---- {droneWifi.ssid} calibrated ----")
            else:   # If not calibrated
                print(f"---- {droneWifi.ssid} ERROR ----")
        else:
            print("DroneWifi has encryption enabled??", droneWifi.ssid)
    

    print()
    DC.connectWifi(DC.defaultWifi)
    DC.waitForConnection()
else:
    print("No available drones found")



for i in range(5):
    sleep(1)
    print(DC.connectedDrones)

sleep(5)
print("SIDST", DC.connectedDrones)
