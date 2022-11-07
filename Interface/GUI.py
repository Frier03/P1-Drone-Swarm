import pygame
from pygame.locals import *
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
#https://pygamewidgets.readthedocs.io/en/latest/widgets/toggle/
class Gui:
    def __init__(self, screen, events) -> None:
        self.backgroundColor = (102,102,102)
        self.screen = screen
        self.events = events

    def __call__(self) -> None:
        # Load GUI once every call on class
        print('loading gui..')

        # Set background color
        self.screen.fill(Color(self.backgroundColor))

        # Add Text
        self.__add_text('Hammond Robotics', x=50, y=20, fontsize=30)

        # Add Connect button
        self.__add_button(value='Connect', x=100, y=300, execfunction=self.__connect_event)
        
        # Add Mission Button
        self.__add_button(value='Mission', x=100, y=400, execfunction=self.__mission_event)

        # Add Stop Button
        self.__add_button(value='Stop', x=100, y=600, execfunction=self.__stop_event, radius=20, inactiveColour=(200, 10, 0), pressedColour=(180, 0, 10), hoverColour=(230, 10, 0))

        # Add DropDown
        self.__add_dropdown(['Drone1', 'Drone2', 'Drone3', 'Drone4'], [1,2,3,4], x=100, y=50)

        # Update now all changes from above to the screen
        pygame.display.update()

    def __add_text(self, value, x=0, y=0, fontsize=10):
        font = pygame.font.SysFont("Helvetica.ttf", fontsize)
        text = font.render(value, True, (255, 255, 255))
        self.screen.blit(text, (x, y))

    def __add_dropdown(self, choices:list, values:list, x=0, y=0) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function"""
        self.dropdown = Dropdown(
            self.screen, x, y, 150, 50, name='Available drones',
            choices=choices,
            borderRadius=3, colour=pygame.Color('lightgray'), values=values, direction='down', textHAlign='centre'
        )



    def __add_button(self, value=None, x=0, y=0, radius=7, execfunction=None, inactiveColour=(90, 90, 90), pressedColour=(0, 200, 20), hoverColour=(135, 135, 135)) -> None:
        """ Private method. No other function than updateGui or __call__ needs this function"""
        
        # Creates the button with optional parameters
        Button(
            # Mandatory Parameters
            self.screen,  # Surface to place button on
            x, # Y coordinate
            y, # X coordinate
            150,  # Width
            50,  # Height

            # Optional Parameters
            text=value,  # Text to display
            fontSize=25,  # Size of font
            margin=5,  # Minimum distance between text/image and edge of button
            inactiveColour=inactiveColour,  # Colour of button when not being interacted with
            hoverColour=hoverColour,  # Colour of button when being hovered over
            pressedColour=pressedColour,  # Colour of button when being clicked
            textHAlign='centre',
            textVAlign='centre',
            radius=radius,  # Radius of border corners (leave empty for not curved)
            onClick=execfunction  # Function to call when clicked on
        )
    

    def __connect_event(self) -> None:
        print('On Connect Button Click')
        pass

    def __mission_event(self) -> None:
        print('On Mission Button Click')
        pass

    def __stop_event(self) -> None:
        print('On Stop Button Click')
        pass
    