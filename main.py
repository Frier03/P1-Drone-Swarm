import sys
import os
import subprocess
import requests as r
from time import sleep
import re           #Regex

defaultWifi = "Tello"

def main(args = None) -> None:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]) # Download packages from requirements.txt
    except subprocess.CalledProcessError as e:
        pass

    os.system('cls')

    # Disconnect from current wifi connection
    disconnectWifi()

    # Wait for flush
    sleep(3)

    # Test wifi connection
    testConnection()

    # Get wifi networks
    networks = getWifiNetworks()
    print(len(networks), "networks found")
    for network in networks:
        if defaultWifi in network:
            print("     Wifi SSID:", network)

    # Connect to defaultWifi
    connectWifi(defaultWifi)

    # Wait for flush
    sleep(1)

    # Test wifi connection
    testConnection()


def connectWifi(SSID):
    name = SSID

    command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    resp = subprocess.run(command, capture_output=True)

def disconnectWifi():
    command = "netsh wlan disconnect interface=Wi-Fi"
    resp = subprocess.run(command, capture_output=True)

def testConnection():
    try:
        r.get("https://www.google.com")
        print("[+] Succesfully requested google")
        return True
    except:
        print("[!] Error when requesting google")
    return False

def getWifiNetworks():
    # using the check_output() for having the network term retrieval
    wifisRaw = subprocess.check_output(['netsh','wlan','show','network'])

    wifisRaw = wifisRaw.decode('utf-8').replace("\r","")    #ascii giver fejl?

    wifiRegQuery = r"(?:SSID [0-9]{0,3} : )(.*)\n"
    wifiList = re.findall(wifiRegQuery, wifisRaw)

    return wifiList

def generateWifiConfig(ssid, key):
    hex = ssid.encode("utf-8").hex()
    
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

def connectToNewWifi():
    wifiConfig = generateWifiConfig("The dark net", "65615027")

    with open(r"listwifi\newDarkwifi.xml", "w") as f:
        f.write(wifiConfig)
        f.close()

    command = r"netsh wlan add profile filename=\"C:\Users\Bear\Desktop\listwifi\newDarkwifi.xml"
    resp = subprocess.run(command, capture_output=True)

if __name__ == '__main__':
    main()

#pip install -U -i  https://pypi.org/simple package