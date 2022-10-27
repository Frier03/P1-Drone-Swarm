from pygame import ACTIVEEVENT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, MOUSEWHEEL, QUIT, WINDOWFOCUSLOST, WINDOWLEAVE


class EventHandler:

    def __init__(self) -> None:
        MOUSEMOTION                         =   1024
        MOUSEBUTTONDOWN                     =   1025
        MOUSEBUTTONUP                       =   1026
        MOUSEWHEEL                          =   1027
        ACTIVEEVENT                         =   32768
        WINDOWLEAVE                         =   32784
        WINDOWFOCUSLOST                     =   32786

    def handler(event):
        print(event)