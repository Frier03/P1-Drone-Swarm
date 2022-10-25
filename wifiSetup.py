from distutils.command import check
from email.policy import default
import os
import subprocess
import socket
import requests as r
from time import sleep
import re           #Regex
import winwifi      #Used for ww.scan(), nothing else


def getCurrentWifi():
    wifi = subprocess.check_output("netsh wlan show interfaces")
    wifi = wifi.decode('utf-8').replace(" \r","")
    currentWifi = re.findall(r"(?:Profile *: )(.*)\n", wifi)
    if len(currentWifi) > 0:
        return currentWifi[0]
    else:
        return None


def connectWifi(SSID):
    name = SSID

    command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    resp = subprocess.run(command, capture_output=True)

#Not used
def disconnectWifi():
    command = "netsh wlan disconnect interface=Wi-Fi"
    resp = subprocess.run(command, capture_output=True)


#Pinger dronen indtil en forbindelse er nået
def checkDroneConnection():
    locaddr = ('', 8889)    #HOST and PORT
    tello_address = ('192.168.10.1', 8889)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)
    s.bind(locaddr)

    for i in range(10):
        s.sendto('command'.encode('utf-8'), tello_address)
        try:
            response, ip = s.recvfrom(1024)
            response = response.decode("utf-8")
            if response == "ok":
                return True
            elif response == "error":
                print("Fatal error on drone?")
                return False
        except Exception as e:
            pass
            #print("Error", str(e))
    return False






#Bruges på net med forbindelse til internet
def waitForConnection():
    print("[!] Searching for connection", end="")
    for i in range(10):   
        try:
            r.get("https://www.google.com")
            print("\n[+] Connection established")
            return True
        except:
            print(".", end="")

        sleep(1)
    print("")
    print("[-] No connection establed?!")



def getWifiNetworks():
    ww = winwifi.WinWiFi()
    nearbyWIfis = [i for i in ww.scan()]
    return nearbyWIfis


def generateProfile(ssid, key=None):
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


def connectToNewWifi(ssid, key=None):
    if not os.path.exists(wifi_profile_folder):
        os.makedirs(wifi_profile_folder)
    
    fileName = wifi_profile_folder + "\\" + ssid + ".xml"
    if not os.path.isfile(fileName):
        
        profile = generateProfile(ssid, key)

        with open(fileName, "w") as f:
            f.write(profile)
            f.close()


    command = r"netsh wlan add profile filename=" + fileName
    resp = subprocess.run(command, capture_output=True)
    connectWifi(ssid)






defaultWifi = "eduroam"
telloWIfiContains = "TELLO"
telloWIfiPassword = "gruppe154"
wifi_profile_folder = "wifi_profiles"

#The wifi to connect back to
#defaultWifi = getCurrentWifi()

print("Default wifi:", defaultWifi)

print("Scanning for nearby networks... ", end="")
wNetworks = getWifiNetworks()
print(f"({len(wNetworks)} networks found)")
for w in wNetworks:
    if telloWIfiContains in w.ssid:            #Ændres til "Tello Drone" bla bla
        print(f"\n--> Trying to connect to ({w.auth}) {w.ssid}")
        if w.auth == "Open" and w.encrypt == "None":
            connectToNewWifi(w.ssid)
            #Set password to telloWifiPassword
        else:
            connectToNewWifi(w.ssid, telloWIfiPassword)


        #waitForConnection()
        print("Probing drone at", w.ssid, "...")
        if checkDroneConnection():
            print("[+] Drone succesfully probed!\n")
        else:
            print("[-] Drone no connection")
        print("")


sleep(5)
print("Connecting back to default wifi " + defaultWifi)
connectWifi(defaultWifi)
waitForConnection()



