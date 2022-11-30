import pygame
from pygame.locals import *
import pygame_widgets
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import re
from . import fileManager as fm
from wifiSetup import DroneConnector
from time import sleep
from Swarm import Swarm
from DJITelloPySuper import Drone

#https://pygamewidgets.readthedocs.io/en
class Gui:
    def __init__(self, screen, events) -> None:
        self.backgroundColor = (240, 240, 240)
        self.screen = screen
        self.events = events
        self.connect_buttons = list() # Holds each button on our custom adapter selection list
        self.selected_value = None
        self.drone_img = pygame.image.load('Interface/drone.png').convert()
        self.popup_run = False

        # Init Drone Animation for each drone (groups)
        self.groups = []

        # Create drone objects
        drones: dict[str, Drone] = {}
        data = fm.request_data('drone_data.json')

        for key, _ in data.items():
            obj = Drone(ip=data[key]['CURRENT_IP'], mac=data[key]['MAC_ADDRESS'])
            drones.update( {data[key]['NAME'] : obj} )

            sprite = Sprite()
            group = pygame.sprite.Group(sprite)
            self.groups.append(group)

        self.SC = Swarm(drones)
        #print(self.SC.drones['Tello EDU 1'].ip)
        self.DC = DroneConnector(self.SC.updateConnections)

    def __call__(self) -> None:
        """Load GUI once every call on class"""
        self.__initialize()

    def __initialize(self):
        widgets = pygame_widgets.WidgetHandler.getWidgets()
        for _ in range(len(widgets)):
            pygame_widgets.WidgetHandler.removeWidget(widgets[0])

        # Request data to insert in custom adapter
        data = fm.request_data('drone_data.json')

        # Set background color
        self.screen.fill(Color(self.backgroundColor))

        # Add Custom Adapter Title
        self.__add_text(value='Available Drones', x=100,y=85, bold=True, fontsize=25)

        # Add Add Button to Custom Adapter
        self.add_button = self.__add_button(value='Add', x=300, y=85, radius=2, w=50, h=30, execfunction=self.__add_drone)

        # Add Custom Adapter
        self.__add_customAdapter_selection(values=data, x=100, y=130, shadowDistance=2, execfuntion=self.__connect_event)

        # Add Connect to All Drones Button
        self.connectall_button = self.__add_button(value='Connect to All', x=100, y=self.__adapter_y, w=150, h=30, execfunction=self.__connnect_to_all_event)

        # Add Connect to All Drones Button
        self.mission_button = self.__add_button(value='Mission', x=100, y=self.__adapter_y+50, w=150, h=30, execfunction=self.__mission_event)

        # Add Stop Button
        self.stop_button = self.__add_button(value='STOP', x=100, y=700, execfunction=self.__stop_event, radius=20, shadowColour=(230, 158, 159), inactiveColour=(239, 142, 143), pressedColour=(207, 117, 118), hoverColour=(245, 125, 126))

        # Add Map
        self.render_map()

    def reloadGui(self):
        self.__initialize()

        # Call once to allow widgets to render
        pygame_widgets.update(pygame.event.get())
                
        # Update now all changes from above to the screen
        pygame.display.update()

    def __show_custom_popup(self, width=None, height=None, title=None):
        # Font render
        font = pygame.font.Font(f'Interface/BostonThin.otf', 14)
        # Place a alpha 128 rectangle on top of everything
        s = pygame.Surface(self.screen.get_size())  # the size of your rect
        s.set_alpha(40)                # alpha level
        s.fill((0,0,0))           # this fills the entire surface
        self.screen.blit(s, (0,0))    # (0,0) are the top-left coordinates

        x,y = (self.screen.get_size()[0]/2-(width/2), 50)
        
        # Make rectangle in middle
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x,y, width, height),  border_radius=3)

        # Make Title Text
        self.__add_text(value=title, x=width-20, y=75, color=(0,0,0), fontsize=40)

        # Make Line under Title
        pygame.draw.line(self.screen, (180, 180, 180), (width+57, 128), (width+167, 128), width=2)

        # Make Text Box Title for "Drone Name"
        self.__add_text(value='Drone Name', x=width-(width/3)+60, y=165, color=(0,0,0), fontsize=17)
        
        # Make Text Box
        self.drone_name = TextBox(self.screen, x=width-(width/3)+60, y=195, width=200, height=32, font=font, textColour=(80,80,80), colour=(230, 230, 230), borderColour=(230, 230, 230), radius=2)

        # Make Text Box Title for "Drone Mac"
        self.__add_text(value='MAC Address', x=width-(width/3)+360, y=165, color=(0,0,0), fontsize=17)
        
        # Make Text Box
        self.drone_mac = TextBox(self.screen, x=width-(width/3)+360, y=195, width=200, height=32, font=font, textColour=(80,80,80), colour=(230, 230, 230), borderColour=(230, 230, 230), radius=2)

        # Make Text Box Title for "Drone Type"
        self.__add_text(value='Drone Type', x=width-(width/3)+60, y=250, color=(0,0,0), fontsize=17)
        
        # Make Text Box
        self.drone_type = TextBox(self.screen, x=width-(width/3)+60, y=285, width=200, height=32, font=font, textColour=(80,80,80), colour=(230, 230, 230), borderColour=(230, 230, 230), radius=2)

        # Make Text Box Title for "Drone IP"
        self.__add_text(value='Drone IP', x=width-(width/3)+360, y=250, color=(0,0,0), fontsize=17)
        
        # Make Text Box
        self.drone_ip = TextBox(self.screen, x=width-(width/3)+360, y=285, width=200, height=32, font=font, textColour=(80,80,80), colour=(230, 230, 230), borderColour=(230, 230, 230), radius=2)

        # Make Button for "Cancel"
        self.drone_cancel = self.__add_button(value='Cancel', x=width/2+220, y=height-20, w=160, h=30, radius=20, fontsize=17, shadowDistance=0, inactiveColour=(200, 200, 200), execfunction=self.__close_popup)

        # Make Button for "Confirm"
        self.drone_confirm = self.__add_button(value='Confirm', x=width/2+440, y=height-20, w=160, h=30, radius=20, fontsize=17, shadowDistance=0, inactiveColour=(200, 200, 200), execfunction=self.__add_drone_to_data)

        # Make Button for "X" - Close Popup Menu
        self.drone_close = self.__add_button(value='Close', y=75, x=width+330, w=50, h=20, shadowDistance=0, inactiveColour=(220, 220, 220), radius=20, fontsize=15, execfunction=self.__close_popup)

        # This while loop is necessary so that the TextBox can get events and updates.
        while self.popup_run:
            # Call once every loop to allow widgets to render and listen
            pygame_widgets.update(pygame.event.get())
            # Update now all changes from above to the screen
            pygame.display.update()

    def __add_customAdapter_selection(self, values=None, x=0, y=0, shadowDistance=2, radius=4, execfuntion=None) -> None:
        width = 250
        height = 90

        # Check if no drones has been added
        if len(values) < 1:
            self.__add_text(x=x, y=y+15, value='No Drones Added', fontsize=20, fontname='BostonBold', color=(255, 0, 0))
            y+=height+10

        else:
            for key, value in values.items():
                # Shadow
                pygame.draw.rect(self.screen, (217,222,224, 10), pygame.Rect(x-shadowDistance, y-shadowDistance, width+(shadowDistance*2), height+(shadowDistance*2)),border_radius=radius)

                # Box
                pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x, y, width, height),border_radius=radius)

                # Draw Title Text
                self.__add_text(x=x+width/4+5, y=y+15, value=values[key]['NAME'], bold=True, fontsize=16, fontname='BostonBold')

                # Draw ID/MAC Text
                self.__add_text(x=x+width/4+5, y=y+40, value='ID', fontsize=12,color=(180,180,180), fontname='BostonRegular')
                self.__add_text(x=x+width/4+23, y=y+40, value=values[key]['MAC_ADDRESS'], fontsize=12, fontname='BostonRegular')

                # Draw Type Text
                self.__add_text(x=x+width/4+5, y=y+55, value='Type', fontsize=12,color=(180,180,180), fontname='BostonRegular')
                self.__add_text(x=x+width/4+38, y=y+55, value=values[key]['TYPE'], fontsize=12, fontname='BostonRegular')

                # Draw Drone Image
                self.drone_img = pygame.transform.smoothscale(self.drone_img, (60, 60))
                self.screen.blit(self.drone_img, (x+2, y+13))

                # Check what status on drone is on (Connect, Connecting... or Connected)
                if self.SC.drones[values[key]['NAME']].guiStatus == 'Connect':
                    # Draw Connect Button (Store each button in a list, so we know which button is pressed)
                    button = self.__add_button(value='Connect', x=295, y=y+12, w=40,h=20, fontsize=14, radius=2, shadowDistance=1, execfunction=execfuntion, execfunctionParams = values[key]['NAME'])
                    self.connect_buttons.append([button, values[key]['NAME']])
                elif self.SC.drones[values[key]['NAME']].guiStatus == 'Connecting...':
                    # Draw Text
                    self.__add_text(x=275, y=y+12, fontsize=12, value='Connecting...', color=(205, 205, 80), fontname='BostonBold')

                elif self.SC.drones[values[key]['NAME']].guiStatus == 'Connected':
                    # Draw Text
                    self.__add_text(x=275, y=y+12, fontsize=12, value='Connected', color=(0, 255, 0), fontname='BostonBold')

                elif self.SC.drones[values[key]['NAME']].guiStatus == 'Calibrated':
                    # Draw Text
                    self.__add_text(x=275, y=y+12, fontsize=12, value='Calibrated', color=(168, 222, 96), fontname='BostonBold')

                elif self.SC.drones[values[key]['NAME']].guiStatus == 'Failed':
                    # Draw Text
                    self.__add_text(x=275, y=y+12, fontsize=12, value='Failed', color=(255, 0, 0), fontname='BostonBold')

                elif self.SC.drones[values[key]['NAME']].guiStatus == 'Disconnected':
                    # Draw Text
                    self.__add_text(x=260, y=y+12, fontsize=12, value='Disconnected', color=(255, 0, 0), fontname='BostonBold')

                y+=height+10
        self.__adapter_y = y

    def __add_text(self, value=None, x=0, y=0, fontsize=10, bold=False, italic=False, color=(0,0,0), fontname='BostonThin'):
        font = pygame.font.Font(f'Interface/{fontname}.otf', fontsize, bold=bold, italic=italic)
        text = font.render(value, True, color)
        self.screen.blit(text, (x, y))

    def __add_button(self, value=None, x=0, y=0, radius=7, w=150, h=50, fontsize=25, execfunction=None,execfunctionParams='', shadowDistance=2, shadowColour=(153, 193, 255), inactiveColour=(124, 176, 255), pressedColour=(112, 154, 217), hoverColour=(114, 170, 255)) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function"""
        # Creates the button with optional parameters
        new_button = Button(
            # Mandatory Parameters
            self.screen,  # Surface to place button on
            x, # Y coordinate
            y, # X coordinate
            w,  # Width
            h,  # Height

            # Optional Parameters
            text=value,  # Text to display
            textColour=(255, 255, 255),
            fontSize=fontsize,  # Size of font
            margin=5,  # Minimum distance between text/image and edge of button
            inactiveColour=inactiveColour,  # Colour of button when not being interacted with
            hoverColour=hoverColour,  # Colour of button when being hovered over
            pressedColour=pressedColour,  # Colour of button when being clicked
            textHAlign='centre',
            textVAlign='centre',
            shadowDistance=shadowDistance,
            shadowColour=shadowColour,
            radius=radius,  # Radius of border corners (leave empty for not curved)  
            onClickParams=execfunctionParams, # Function Parameters to be passed into execfuntion      
            onClick=execfunction  # Function to call when clicked on
        )
        return new_button
    
    def __add_drone(self) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function """
        # Disable buttons before loading popup
        self.add_button.disable()
        self.connectall_button.disable()
        self.stop_button.disable()
        self.mission_button.disable()

        for i in range(len(self.connect_buttons)):
            self.connect_buttons[i][0].disable()

        self.popup_run = True
        self.__show_custom_popup(width=600, height=375, title='Drone Overview')
    
    def __add_drone_to_data(self, *args) -> None:
        drone_name = self.drone_name.getText()
        drone_mac = self.drone_mac.getText() 
        drone_type = self.drone_type.getText()
        drone_ip = self.drone_ip.getText()

        # Reset Colors on each text box
        self.__reset_textbox_colors([self.drone_name, self.drone_mac, self.drone_type, self.drone_ip])

        
        # Basic validation of each input content
        if self.__validateInput([drone_name, drone_mac, drone_type, drone_ip], [self.drone_name, self.drone_mac, self.drone_type, self.drone_ip]):

            # Validate MAC Address by using RegEx margin match - Can match pattern using -: (00:00:00-00-00-00)
            if re.search(r"((([0-9a-fA-F]){2}[-:]){5}([0-9a-fA-F]){2})", drone_mac) is not None:
                # Add Data to database\
                data = [drone_name, drone_mac, drone_type, drone_ip]
                
                # Insert data to json
                res = fm.insert_data('drone_data.json', data)

                if res == 'OK':
                    print('Closing POPUP')
                    # Close Pop up
                    self.__close_popup()

                    #TODO: Show Success text message on screen after completion
            else:
                # Show red Border
                self.drone_mac.borderThickness=1

    def __connnect_to_all_event(self, *args) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function """
        print('Connect to All Drones!')

    def __connect_event(self, *args) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function """
        
        # Convert tuple (args) to str
        args = self.__convert_tuple(args)

        # Change button from Connect -> Connecting... (inherit into swarm -> drones and change guiStatus data member)
        self.SC.drones[args].guiStatus = 'Connecting...'

        # Reload GUI
        self.reloadGui()

        dMAC = self.SC.drones[args].mac

        if self.DC.calibrateDrone(dMAC):
            #print("Calibrated succeded")

            # Change from Connecting... -> Calibrating (green color)
            self.SC.drones[args].guiStatus = 'Calibrating'
        else:
            # Change from Connecting... -> Failed! (default colo)
            self.SC.drones[args].guiStatus = 'Failed'
            
            # Reload GUI
            self.reloadGui()
            sleep(2)

            # Change from Connecting... -> Connect (default colo)
            self.SC.drones[args].guiStatus = 'Connect'

            # Reload GUI
            self.reloadGui()

            self.DC.connectWifi(self.DC.defaultWifi)
            self.DC.waitForConnection()

    def __mission_event(self, *args) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function """
        print('Start Mission')
        pass

    def __stop_event(self, *args) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function """
        print('STOP')
        pass

    def __close_popup(self) -> None:
        pygame_widgets.WidgetHandler.removeWidget(self.drone_name)
        pygame_widgets.WidgetHandler.removeWidget(self.drone_mac)
        pygame_widgets.WidgetHandler.removeWidget(self.drone_type)
        pygame_widgets.WidgetHandler.removeWidget(self.drone_ip)
        pygame_widgets.WidgetHandler.removeWidget(self.drone_cancel)
        pygame_widgets.WidgetHandler.removeWidget(self.drone_confirm)
        pygame_widgets.WidgetHandler.removeWidget(self.drone_close)

        # Enable buttons after popup is closed
        self.add_button.enable()
        self.connectall_button.enable()
        self.stop_button.enable()
        self.mission_button.enable()
        for i in range(len(self.connect_buttons)):
            self.connect_buttons[i][0].enable()

        # Stop loop in popup
        self.popup_run = False
        # Reload GUI
        self.reloadGui()
        
    def __convert_tuple(self, tup: tuple) -> str:
        """ Converts a tuple to a string"""
        str = ''
        for char in tup:
            str = str + char
        return str

    def __validateInput(self, input: list, reference: list) -> bool:
        for i in range(len(input)):
            if input[i] == None or input[i] == '' or input[i] == ' ':

                # Change color of text field to red ish
                reference[i].borderColour=(255, 0, 0)
                reference[i].borderThickness=1
                return False
        return True

    def __reset_textbox_colors(self, reference: list) -> None:
        for i in range(len(reference)):
            reference[i].borderColour=(255, 0, 0)
            reference[i].borderThickness=0

    def render_map(self) -> None:
        """Create grid and make map"""
        mapX, mapY = 400, 85
        mapW, mapH = 800, 600
        rad = 2
        shadowDistance = 2

        # Set the position of the map
        mapStartpointX, mapStartpointY = mapX, mapY
        mapEndpointX, mapEndpointY = mapX + mapW, mapY + mapH

        # Calculate the 0,0 position of the map to the end points
        threshold_x, threshold_y = mapStartpointX, mapStartpointY 

        # Draw Shadow
        pygame.draw.rect(self.screen, (217,222,224, 10), pygame.Rect(mapX-shadowDistance, mapY-shadowDistance, mapW+(shadowDistance*2), mapH+(shadowDistance*2)),border_radius=rad)

        # Draw Box
        pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(mapX, mapY, mapW, mapH),border_radius=rad)

        # Get Each Drone id/name,position, yaw, battery, altitude, speed and connected status in a list?
        drones = self.SC.drones      

        drones['Tello EDU 1'].abs_x = 200

        # Sprite groups [] for each drone
        i=0
        for key, value in drones.items():
            drone_sprite = self.groups[i]
            x, y = (drones[key].abs_x + threshold_x, drones[key].abs_y + threshold_y)
            spd = drones[key].totalSpeed
            alt = drones[key].abs_z
            yaw = drones[key].rotation         

            drone_sprite.update(x, y, yaw)
            drone_sprite.draw(self.screen)

            if i < len(drones):
                i+=1
            else: i=0
            

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super(Sprite, self).__init__()

        drone0 = pygame.image.load('Interface/drone.png')
        drone0 = pygame.transform.smoothscale(drone0, (80, 80))
        drone1 = pygame.image.load('Interface/drone1.png')
        drone1 = pygame.transform.smoothscale(drone1, (80, 80))
        self.images = [drone0, drone1]
        self.index = 0
 
        self.image = self.images[self.index]
 
        self.rect = pygame.Rect(0, 0, 150, 198)
 
    def update(self, x, y, yaw):
        self.index += 1
 
        if self.index >= len(self.images):
            self.index = 0
        
        self.image = self.images[self.index]
        self.rect.x = x
        self.rect.y = y