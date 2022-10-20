import os
import subprocess
import requests as r
from time import sleep
import re           #Regex



def getCurrentWifi():
    wifi = subprocess.check_output("netsh wlan show interfaces")
    wifi = wifi.decode('utf-8').replace(" \r","")
    currentWifi = re.findall(r"(?:Profile *: )(.*)\n", wifi)
    return currentWifi[0]


def connectWifi(SSID):
    name = SSID

    command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    resp = subprocess.run(command, capture_output=True)


def disconnectWifi():
    command = "netsh wlan disconnect interface=Wi-Fi"
    resp = subprocess.run(command, capture_output=True)


def waitForConnection():
    for i in range(10):   
        try:
            r.get("https://www.google.com")
            print("[+] Connection established")
            return True
        except:
            print("[!] Searching for connection")

        sleep(1)


def getWifiNetworks():
    # using the check_output() for having the network term retrieval
    wifisRaw = subprocess.check_output("netsh wlan show network")

    wifisRaw = wifisRaw.decode('utf-8').replace("\r","")    #ascii giver fejl?

    wifiRegQuery = r"(?:SSID [0-9]{0,3} : )(.*)\n"
    wifiList = re.findall(wifiRegQuery, wifisRaw)

    return wifiList

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
        print("[!] Generating new profile for", ssid)
        
        profile = generateProfile(ssid, key)

        with open(fileName, "w") as f:
            f.write(profile)
            f.close()
    else:
        print("[!] Profile already exists for", ssid)


    command = r"netsh wlan add profile filename=" + fileName
    resp = subprocess.run(command, capture_output=True)
    connectWifi(ssid)







defaultWifi = "eduroam"
wifi_profile_folder = "wifi_profiles"

#The wifi to connect back to
defaultWifi = getCurrentWifi()
print("Default wifi set to", defaultWifi)

#(I DONT KNOW WHY) Makes other wifi's visible only if disconnected first
disconnectWifi()
sleep(0.5)

wNetworks = getWifiNetworks()
print(len(wNetworks), "networks found!")
for w in wNetworks:
    if "bbb" in w:            #Ændres til "Tello Drone" bla bla
        print("---> Found matching SSID:", w)
        connectToNewWifi(w)
        waitForConnection()

sleep(5)
print("Connecting back to default wifi " + defaultWifi)
connectWifi(defaultWifi)
waitForConnection()



