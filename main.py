#!/usr/bin/env python
import pygame
from pygame.locals import *
from threading import Thread
from time import sleep
import pygame_widgets
from pygame_widgets.button import Button
from Interface import RenderMap
from Interface import CalibrateMap
from Interface import GUI
import Interface.fileManager as fm
from pygame_widgets.textbox import TextBox
import pyautogui

class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screenWidth = 1420
        self.screenHeight = 800

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), pygame.NOFRAME)
        pygame.display.set_caption('')
        aau_img = pygame.image.load('Interface/aau.png')
        pygame.display.set_icon(aau_img)

        # Initialize interface classes
        self.gui = GUI.Gui(self.screen, pygame.event.get())

        App.running = True

        # Start Worker thread
        worker = Thread(target=self.worker)
        worker.daemon = True
        worker.start()

    def worker(self):
        """Run the worker event loop for all other protocols (drone related stuff)"""
        while True:
            print('Worker: Ready')
            sleep(10)


    def run(self):
        """Run the main event loop."""
    
        # Load GUI
        self.gui() # Calls "__call__" inside gui class

        try:
            while App.running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        App.running = False
            
                # Call once every loop to allow widgets to render and listen
                pygame_widgets.update(pygame.event.get())
                
                # Update now all changes from above to the screen
                pygame.display.update()

        except Exception as e:
            print(e)
                    
        pygame.quit()

if __name__ == '__main__':
    App().run()









    #def updateMap(self, coordinates=(None, None), drone_id=None, fieldSize=None):
        # Update screen background
        #self.updateBackground()

        # Render Map
        #self.interface.render_map(self, screen=self.screen, fieldSize=fieldSize, screenDimensions = (self.screenWidth, self.screenHeight))

        # Render drone
        #self.interface.updatePoint(self, coordinates=coordinates, drone_id=drone_id, screen=self.screen)


        #drone_1 = "Drone_AV1"
        #drone_2 = "Drone_AV2"
        #drone_3 = "Drone_AV3"
        #self.fieldSize = 50

        # Update map for drone_1
        #self.updateMap(coordinates=(93, 48), drone_id=drone_1, fieldSize=self.fieldSize)

        # Update map for drone_2
        #self.updateMap(coordinates=(167, 203), drone_id=drone_2, fieldSize=self.fieldSize)

        # Update map for drone_3
        #self.updateMap(coordinates=(0, 0), drone_id=drone_3, fieldSize=self.fieldSize)
