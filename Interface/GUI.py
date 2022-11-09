import pygame
from pygame.locals import *
import pygame_widgets
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.selection import Radio
import pickle
import re
import pyautogui
#https://pygamewidgets.readthedocs.io/en/latest/widgets/toggle/
class Gui:
    def __init__(self, screen, events) -> None:
        self.backgroundColor = (240, 240, 240)
        self.screen = screen
        self.events = events
        self.connect_buttons = list() # Holds each button on our custom adapter selection list
        self.selected_value = None
        self.drone_img = pygame.image.load('Interface/drone.png').convert()

    def __call__(self) -> None:
        """Load GUI once every call on class"""
        self.__initialize()

    def __initialize(self):
        # Set background color
        self.screen.fill(Color(self.backgroundColor))

        # Add Custom Adapter Title
        self.__add_text(value='Available Drones', x=100,y=85, bold=True, fontsize=25)

        # Add Add Button to Custom Adapter
        self.add_button = self.__add_button(value='Add', x=300, y=85, radius=2, w=50, h=30, execfunction=self.__add_drone)

        # Add Custom Adapter
        self.__add_customAdapter_selection(values=['Tello EDU 1', 'Tello EDU 2', 'Tello EDU 3'], x=100, y=130, shadowDistance=2, execfuntion=self.__connect_event)

        # Add Connect to All Drones Button
        self.connectall_button = self.__add_button(value='Connect to All', x=100, y=self.__adapter_y, w=150, h=30, execfunction=self.__connnect_to_all_event)

        # Add Connect to All Drones Button
        self.mission_button = self.__add_button(value='Mission', x=100, y=self.__adapter_y+50, w=150, h=30, execfunction=self.__mission_event)

        # Add Stop Button
        self.stop_button = self.__add_button(value='STOP', x=100, y=700, execfunction=self.__stop_event, radius=20, shadowColour=(230, 158, 159), inactiveColour=(239, 142, 143), pressedColour=(207, 117, 118), hoverColour=(245, 125, 126))

    def reloadGui(self):
        self.__initialize()

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

        # Make Button for "Confirm"

        # This while loop is necessary so that the TextBox can get events and updates.
        while True:
            # Call once every loop to allow widgets to render and listen
            pygame_widgets.update(pygame.event.get())
            # Update now all changes from above to the screen
            pygame.display.update()

    def __add_customAdapter_selection(self, values=list(), x=0, y=0, shadowDistance=2, radius=4, execfuntion=None) -> None:
        width = 250
        height = 90

        for i in range(len(values)):
            # Shadow
            pygame.draw.rect(self.screen, (217,222,224, 10), pygame.Rect(x-shadowDistance, y-shadowDistance, width+(shadowDistance*2), height+(shadowDistance*2)),border_radius=radius)

            # Box
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x, y, width, height),border_radius=radius)

            # Draw Title Text
            self.__add_text(x=x+width/4+5, y=y+15, value=values[i], bold=True, fontsize=16, fontname='BostonBold')

            # Draw ID/MAC Text
            self.__add_text(x=x+width/4+5, y=y+40, value='ID', fontsize=12,color=(180,180,180), fontname='BostonRegular')
            self.__add_text(x=x+width/4+23, y=y+40, value='01-00-5e-7f-ff-fa', fontsize=12, fontname='BostonRegular')

            # Draw Type Text
            self.__add_text(x=x+width/4+5, y=y+55, value='Type', fontsize=12,color=(180,180,180), fontname='BostonRegular')
            self.__add_text(x=x+width/4+38, y=y+55, value='DJI Tello EDU', fontsize=12, fontname='BostonRegular')

            # Draw Drone Image
            self.drone_img = pygame.transform.smoothscale(self.drone_img, (60, 60))
            self.screen.blit(self.drone_img, (x+2, y+13))

            # Draw Connect Button (Store each button in a list, so we know which button is pressed)
            button = self.__add_button(value='Connect', x=295, y=y+12, w=40,h=20, fontsize=14, radius=2, shadowDistance=1, execfunction=execfuntion, execfunctionParams = values[i])
            self.connect_buttons.append([button, values[i]])

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

                # Convert list to base16 bytearray
                base16_data = bytearray(pickle.dumps(data))
                pass
            
            else:

                # Show red Border
                self.drone_mac.borderThickness=1






    def __connnect_to_all_event(self, *args) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function """
        print('Connect to All Drones!')
        pass

    def __connect_event(self, *args) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function """
        
        # Convert tuple (args) to str
        args = self.__convert_tuple(args)

        print('Connect to drone: ', args)

    def __mission_event(self, *args) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function """
        print('Start Mission')
        pass

    def __stop_event(self, *args) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function """
        print('STOP')
        pass

    def __close_popup(self) -> None:
        self.drone_name.hide()
        self.drone_mac.hide()
        self.drone_type.hide()
        self.drone_ip.hide()
        self.drone_cancel.hide()
        self.drone_confirm.hide()
        self.drone_close.hide()

        # Enable buttons after popup is closed
        self.add_button.enable()
        self.connectall_button.enable()
        self.stop_button.enable()
        self.mission_button.enable()
        for i in range(len(self.connect_buttons)):
            self.connect_buttons[i][0].enable()

        self.reloadGui()
        pygame.display.update()
        
    def __convert_tuple(self, tup: tuple) -> str:
        """ Converts a tuple to a string"""
        str = ''
        for char in tup:
            str = str + char
        return str

    def __validateInput(self, input: list, reference: list) -> bool:
        for i in range(len(input)):
            if input[i] is None or input[i] is '' or input[i] is ' ':

                # Change color of text field to red ish
                reference[i].borderColour=(255, 0, 0)
                reference[i].borderThickness=1
                return False
        return True

    def __reset_textbox_colors(self, reference: list):
        for i in range(len(reference)):
            reference[i].borderColour=(255, 0, 0)
            reference[i].borderThickness=0
    