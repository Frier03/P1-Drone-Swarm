import os
import subprocess
import requests as r
from time import sleep
import re           #Regex



def getCurrentWifi():
    wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
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
    wifisRaw = subprocess.check_output(['netsh','wlan','show','network'])

    wifisRaw = wifisRaw.decode('utf-8').replace("\r","")    #ascii giver fejl?

    wifiRegQuery = r"(?:SSID [0-9]{0,3} : )(.*)\n"
    wifiList = re.findall(wifiRegQuery, wifisRaw)

    return wifiList


def connectToNewWifi(ssid, key):
    if not os.path.exists(wifiProfileFolder):
        os.makedirs(wifiProfileFolder)
    
    fileName = wifiProfileFolder + "\\" + ssid + ".xml"
    if not os.path.isfile(fileName):
        print("[!] Generating new profile for", ssid)
        hex = ssid.encode("utf-8").hex()
        profileXML = """<?xml version="1.0"?>
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
        with open(fileName, "w") as f:
            f.write(profileXML)
            f.close()
    else:
        print("[!] Profile already exists for", ssid)


    command = r"netsh wlan add profile filename=" + fileName
    resp = subprocess.run(command, capture_output=True)
    connectWifi(ssid)


defaultWifi = "eduroam"
wifiProfileFolder = "wifi_profiles"

#The wifi to connect back to
defaultWifi = getCurrentWifi()
print("Default wifi set to", defaultWifi)

#(I DONT KNOW WHY) Makes other wifi's visible
disconnectWifi()
sleep(0.5)

wNetworks = getWifiNetworks()
print(len(wNetworks), "networks found!")
for w in wNetworks:
    if "P10" in w:            #Ændres til "Tello Drone" bla bla
        print("---> Found matching SSID:", w)
        connectToNewWifi(w, "mechabad")
        waitForConnection()

sleep(5)
print("Connecting back to default wifi " + defaultWifi)
connectWifi(defaultWifi)
waitForConnection()



