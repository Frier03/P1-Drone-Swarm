import os
import subprocess
import requests as r
from time import sleep
import re           #Regex


defaultWifi = "eduroam"
wifiProfileFolder = "wifi_profiles"

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
    if not os.path.exists(wifiProfileFolder):
        os.makedirs(wifiProfileFolder)
    
    d = wifiProfileFolder + "\\" + ssid + ".xml"

    with open(d, "w") as f:
        f.write(profileXML)
        f.close()

    command = r"netsh wlan add profile filename=" + d
    resp = subprocess.run(command, capture_output=True)
    connectWifi(ssid)




disconnectWifi()
sleep(0)

wNetworks = getWifiNetworks()
print(len(wNetworks), "networks found!")
for w in wNetworks:
    if "Net420" in w:            #Ændres til "Tello Drone" bla bla
        print("     Wifi SSID:", w)
        connectToNewWifi(w, "Wilback123")
        waitForConnection()

sleep(5)
print("Connecting back to " + defaultWifi)
connectWifi(defaultWifi)        #Er asynkron desværre!?
waitForConnection()



