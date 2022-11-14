import os
import subprocess
import socket
import requests as r
from time import sleep
from threading import Thread
import re           #Regex
import winwifi      #Used for ww.scan(), nothing else
from access_modifiers import privatemethod

class DroneConnector():
    defaultWifi = "eduroam"                 #Wifi'et man er forbundet til lige nu
    telloWIfiContains = "TELLO"         
    telloWIfiPassword = "gruppe154"
    wifi_profile_folder = "wifi_profiles"   #Mappen hvor vores wifi-profiler er gemt
    hotspotSSID = "Bear"                    #
    hotspotPASS = "joinTheNet"              #Navnet og pass på dit hotspot som du laver

    connectedDrones = []



    def __init__(self, callback):
        #Save your current wifi to connect back to later
        self.defaultWifi = self.getCurrentWifi()

        #Constantly update connectedDrones[] with the currently online drones
        T = Thread(target=self.getConnectedDrones, args=(callback, ))
        T.daemon = True
        T.start()


    @privatemethod
    def getCurrentWifi(self):
        """Returns your currently connected Wifi"""
        wifi = subprocess.check_output("netsh wlan show interfaces")
        wifi = wifi.decode('utf-8').replace(" \r","")
        currentWifi = re.findall(r"(?:Profile *: )(.*)\n", wifi)
        if len(currentWifi) > 0:
            return currentWifi[0]       #Return e.g. "eduroam"
        else:
            return None

    #@privatemethod
    def connectWifi(self, SSID):
        """Connect to a wifi, which you already have a wifi-profile for"""
        name = SSID
        command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
        resp = subprocess.run(command, capture_output=True)


    #@privatemethod
    def waitForConnection(self):
        """Waits until a connection to www.google.com is established"""
        print("[!] Searching for connection", end="")
        for i in range(10):
            try:
                r.get("https://www.google.com")
                print(" --> Ok!")
                return True
            except:
                print(".", end="")

            sleep(1)
        print("")
        print(" --> Error?")
        return False
    

    @privatemethod
    def getAvailableWifiNetworks(self):
        """Gets nearby wifi networks with WinWifi. Takes an estimated 5 seconds"""
        ww = winwifi.WinWiFi()
        nearbyWIfis = ww.scan()
        return nearbyWIfis


    @privatemethod
    def generateWifiProfile(self, ssid, key=None):
        """Generates a Wifi profile with or without a password. Stores it in the wifi_profiles folder"""
        hex = ssid.encode("utf-8").hex()
        if key == None:
            print("Generating profile for open network (no key)")
            profile = """<?xml version="1.0"?>
    <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
        <name>""" + ssid + """</name>
        <SSIDConfig>
            <SSID>
                <hex>""" + hex + """</hex>
                <name>""" + ssid + """</name>
            </SSID>
        </SSIDConfig>
        <connectionType>ESS</connectionType>
        <connectionMode>manual</connectionMode>
        <MSM>
            <security>
                <authEncryption>
                    <authentication>open</authentication>
                    <encryption>none</encryption>
                    <useOneX>false</useOneX>
                </authEncryption>
            </security>
        </MSM>
        <MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">
            <enableRandomization>false</enableRandomization>
        </MacRandomization>
    </WLANProfile>
        """
        else:
            print("Generating profile for closed network (with key)")

            profile = """<?xml version="1.0"?>
            <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                <name>""" + ssid + """</name>
                <SSIDConfig>
                    <SSID>
                        <hex>""" + hex + """</hex>
                        <name>""" + ssid + """</name>
                    </SSID>
                </SSIDConfig>
                <connectionType>ESS</connectionType>
                <connectionMode>auto</connectionMode>
                <MSM>
                    <security>
                        <authEncryption>
                            <authentication>WPA2PSK</authentication>
                            <encryption>AES</encryption>
                            <useOneX>false</useOneX>
                        </authEncryption>
                        <sharedKey>
                            <keyType>passPhrase</keyType>
                            <protected>false</protected>
                            <keyMaterial>""" + key + """</keyMaterial>
                        </sharedKey>
                    </security>
                </MSM>
                <MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">
                    <enableRandomization>false</enableRandomization>
                </MacRandomization>
            </WLANProfile>
            """
        return profile


    @privatemethod
    def connectToNewWifi(self, ssid, key=None):
        """Connect to a new wifi"""
        if not os.path.exists(self.wifi_profile_folder):
            os.makedirs(self.wifi_profile_folder)
        
        fileName = self.wifi_profile_folder + "\\" + ssid + ".xml"
        # fileName = "wifi_profiles\\TELLO-ABCDEF.xml"
        if not os.path.isfile(fileName):                #If there is NO wifi profile already, make a new one
            profile = self.generateWifiProfile(ssid, key)
            with open(fileName, "w") as f:
                f.write(profile)
                f.close()

        command = r"netsh wlan add profile filename=" + fileName
        resp = subprocess.run(command, capture_output=True)
        self.connectWifi(ssid)



    #Bliver lavet en thread af denne
    def getConnectedDrones(self, callback):
        while True:
            # Hotspot is always on 192.168.137.0/24
            arp_a_regex = r"""(192\.168\.137\.[0-9]{0,3}) *([0-9a-z-]*)  """

            arping = subprocess.check_output("arp -a")
            arping = arping.decode('utf-8').replace(" \r","")
            macsHotspot = re.findall(arp_a_regex, arping)
            # macsHotspot = [(192.168.137.36, 34-d2-62-f2-51-f6), (ip, mac)]
            # Remove the subnet entry
            #  macsHotspot.remove(('192.168.137.255', 'ff-ff-ff-ff-ff-ff'))

            for m in macsHotspot[:]:            #Lav en ny kopi for ikke at slette i macsHotspot mens vi itererer i den. Spørg Bjørn hvis forvirret
                pingCommand = f"ping -w 500 {m[0]}"
                #print(pingCommand)
                pinging = subprocess.run(pingCommand, capture_output=True)
                pinging = pinging.stdout.decode('utf-8').replace(" \r","")
                if "Received = 0" in pinging:
                    macsHotspot.remove(m)

            # Call GUI
            #if self.connectedDrones != macsHotspot: # If the list has changed, we want to update it in our GUI by calling callback
            callback(macsHotspot)

            #Update so other modules knows what methods are connected
            self.connectedDrones = macsHotspot
            sleep(0.1)





    ########################################################################
    #                                                                      #
    #   NEDENFOR ER PUBLIC FUNKTIONERNE MENT til AT BLIVE KALDT I GUI-en   #
    #                                                                      #
    ########################################################################
    def findDrones(self):
        #Sometimes if will only find 1 network. Keep trying until it works
        for i in range(5):
            print("Scanning for nearby networks... ", end="")
            wNetworks = self.getAvailableWifiNetworks()
            print(f"({len(wNetworks)} networks found)")
            if len(wNetworks) > 1:
                break
        
        drones = []
        for w in wNetworks:
            if self.telloWIfiContains in w.ssid:
                drones.append(w)
        return drones
        

    def calibrateDrone(self, droneMAC):
        """Opretter forbindelse, sætter i SDK mode og forbinder dronen til hotspottet"""

        droneSSID = "TELLO-" + droneMAC
        self.connectToNewWifi(droneSSID)

        #Wait until wifi is connected
        print("Connecting to drone wifi", end="")
        isWifiConnected = False
        for i in range(10):
            if self.getCurrentWifi() == droneSSID:
                print(" --> Connected")
                isWifiConnected = True
                break
            else:
                print(".", end="")
                sleep(0.5)
        if isWifiConnected == False: return False
        

        # ---------------------------------------------
        # VI ER PÅ DRONENS WIFI NU

        #SOCKET SETUP
        locaddr = ('', 8889)                        #HOST and PORT ME
        tello_address = ('192.168.10.1', 8889)      #HOST AND PORT FOR TELLO
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)         #FRA STACKOVERFLOW. https://stackoverflow.com/questions/41208720/python-sockets-not-really-closing
        s.bind(locaddr)

        #KEEPING TRACK OF DRONE CONNECTION
        conEstablished = False

        # First make it enter SDK command mode
        print("Sending <command>", end="")
        
        for i in range(5):
            try:
                s.sendto('command'.encode('utf-8'), tello_address)
                response, ip = s.recvfrom(1024)
                response = response.decode("utf-8")
                if response == "ok":
                    conEstablished = True
                    print(" --> ok")
                    break
                elif response == "error":
                    print(" --> error")
            except Exception as e:
                pass
                #print("Error", str(e))

        
        if conEstablished == True:     # If drone actually is connected
            # Make it connect to the hotspot
            apCommand = f"ap {self.hotspotSSID} {self.hotspotPASS}"  # The (ap ssid pass) command
            #apCOmmand = "ap Bear joinTheNet"
            print(f"Sending <{apCommand}> --> ", end="")
            for i in range(5):
                s.sendto(apCommand.encode('utf-8'), tello_address)
                try:
                    response, ip = s.recvfrom(1024)
                    response = response.decode("utf-8")
                    if response == "error":
                        conEstablished = False
                        print("error")
                except Exception as e:
                    print("assumed to be <ok>")
                    break
        
        
        s.close()
        return conEstablished           #True eller False

    

if __name__ == "__main__":
    print("Import med DC = DroneConnector()")


