from code import interact
from pygame import ACTIVEEVENT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, MOUSEWHEEL, QUIT, WINDOWFOCUSLOST, WINDOWLEAVE
import pygame
import json
from settings import *

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

    def is_map_calibrated(self):
        return MAP_CALIBRATED

    def map_has_been_calibrated(self):
        MAP_CALIBRATED=True
        return MAP_CALIBRATED

    def calibrate_map(self):
        pass
    
    def handler(self, event):
        #EventHandler.calibrate_map(self, event)
        pass

