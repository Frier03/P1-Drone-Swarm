import pygame
from pygame.locals import *
import pygame_widgets
from pygame_widgets.button import Button
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

        # Add Connect button
        self.__add_button(value='Connect', x=100, y=300)
        
        # Add Mission Button
        self.__add_button(value='Mission', x=100, y=400)

        # Add Stop Button
        self.__add_button(value='Stop', x=100, y=600, inactiveColour=(200, 10, 0), pressedColour=(180, 0, 10), hoverColour=(230, 10, 0))

        # Update now all changes from above to the screen
        pygame.display.update()

    def __add_button(self, value='', x=0, y=0, inactiveColour=(90, 90, 90), pressedColour=(0, 200, 20), hoverColour=(135, 135, 135)):
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
            radius=7,  # Radius of border corners (leave empty for not curved)
            onClick= lambda: print(value)  # Function to call when clicked on
        )
    

    def __button_event(self, value):
        print('event on button', value)
    