from code import interact
from pygame import ACTIVEEVENT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, MOUSEWHEEL, QUIT, WINDOWFOCUSLOST, WINDOWLEAVE
import pygame
from interface import Interface

class EventHandler:

    def __init__() -> None:
        MOUSEMOTION                         =   1024
        MOUSEBUTTONDOWN                     =   1025
        MOUSEBUTTONUP                       =   1026
        MOUSEWHEEL                          =   1027
        ACTIVEEVENT                         =   32768
        WINDOWLEAVE                         =   32784
        WINDOWFOCUSLOST                     =   32786

    def collideDetect(mx, my, x, y, w, h):
        """
        mx = mouseX
        my = mouseY
        x = position x
        y = position y
        w = width
        h = height
        """
        if mx >= x and mx <= x + w:
                if my >= y and my <= y + h:
                    return True
        return False

    def checkDroneMapInteraction(self, event):
        # Get X,Y mouse coordinates
        mx, my = pygame.mouse.get_pos()

        if event.type == MOUSEBUTTONDOWN:
            x, y = Interface.get_drone_coords(self)
            w, h = (Interface.get_drone_size(self), Interface.get_drone_size(self))
            deviation = Interface.get_drone_size(self)
            onDrone = EventHandler.collideDetect(mx, my, x-deviation, y-deviation, w+deviation, h+deviation)

            if onDrone:
                print('show more information')
    
    def handler(self, event):
        EventHandler.checkDroneMapInteraction(self, event)

