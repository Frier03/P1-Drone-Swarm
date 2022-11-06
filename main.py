#!/usr/bin/env python
import pygame
from pygame.locals import *
from threading import Thread
from time import sleep
from eventHandler import EventHandler
from settings import *
from Interface import RenderMap
from Interface import CalibrateMap

class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        self.backgroundColor = (102,102,102) # gray dark background
        pygame.init()
        self.screenWidth = 1200
        self.screenHeight = 800

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('Drone Fleet-Management Software')
        aau_img = pygame.image.load('aau.png').convert()
        pygame.display.set_icon(aau_img)

        App.running = True

        # Initialize classes
        self.eventHandler = EventHandler

        # Start the worker (thread)
        thread = Thread(target=self.worker)
        thread.daemon = True
        thread.start()

    def updateBackground(self):
        """Method to update background"""
        self.screen.fill(Color(self.backgroundColor))

        pygame.display.update()

    def worker(self):
        """Run the worker event loop for all other protocols (drone related stuff)"""
        while True:
            print('Worker: Ready')
            sleep(60)

    def run(self):
        """Run the main event loop."""
        # Update screen background
        self.updateBackground()

        # Is there a map calibrated?
        calibrated = EventHandler.is_map_calibrated(self)

        try:
            while App.running:
                for event in pygame.event.get():
                    # Recolor background
                    self.screen.fill(Color(self.backgroundColor))
                    
                    # Check if map is not calibrated!
                    if not calibrated:
                        if event.type == MOUSEBUTTONDOWN and event.button == 3:
                            print('skeleton map done!')
                            calibrated=True

                            # Re-render screen
                            self.updateBackground()

                            # Pre preview of calibrated skeleton
                            CalibrateMap.render_calibrated_skeleton(self)
                        else:
                            CalibrateMap.calibrate_map(self, event)

                    if event.type == QUIT:
                        App.running = False
        
        except AttributeError as ae:
            print(ae)
                    
        pygame.quit()

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

if __name__ == '__main__':
    App().run()