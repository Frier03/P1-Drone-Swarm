# P1 Robot Swarm
P1 Project - Comtek 154 - C2-207 - 2022


## To-do list
- [x] Add button (Scan for drones)
- [x] Add emergency when drones are too close


## Description
A project which attempts to control multiple Tello EDU drones by tracking their location and plotting it in a GUI


## Contribute
In order to contribute with git
* Pick a branch or create a new one
* Update from main
* Write your change
* Commit
* Push to remote branch
* Create a pull request and merge it with main


## Code structure
- main.py       (Combines the entire thing, run this for execution)
- Drone.py      (Contains the class Drone() used to communicate with the drones)
- Swarm.py      (Contains the class Swarm() used to keep track of the individual drones and plan routes for them)
- Wifisetup.py  (Configures every nearby drone to your hotspot)
- GUI.py        (Renders the 2D map of the drones with PyGame)
- /Interface    (All files related to the GUI)
- /TestingFiles (Random files used for testing and trying stuff out)



## Requirements and Installation
**Your hotspot must be enabled on 2.4 GHz only**
- `python >= 3.10`
- `pygame >= 2.0.0`
- `pygame_widgets >= 1.1.0`
- 'pip install -r requirements.txt'
If PyGame gives errors, try `pip install pygame --pre`

If you want to try the class using TelloPy, install 'version 0.7.0' from github, not pip

## Guide
* Add your drones
  * (name, mac, type)
* Connect your drones
  * Either one by one, or everyone at the same time
* Start a mission
  * Current it is to navigate all the drones to a random space



