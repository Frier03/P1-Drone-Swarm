#!/usr/bin/env python
import pygame
from pygame.locals import *
from threading import Thread
from queue import Queue
from time import sleep
from eventHandler import EventHandler

from interface import Interface
from eventHandler import EventHandler

class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        self.backgroundColor = (102,102,102) # gray dark background
        pygame.init()
        self.screenWidth = 1200
        self.screenHeight = 800

        App.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('Drone Fleet-Management Software')
        aau_img = pygame.image.load('aau.png').convert()
        pygame.display.set_icon(aau_img)

        App.running = True

        # Initialize classes
        self.interface = Interface
        self.eventHandler = EventHandler

        # Start the worker (thread)
        thread = Thread(target=self.worker)
        thread.daemon = True
        thread.start()

    def updateBackground(self):
        """Method to update background"""
        App.screen.fill(Color(self.backgroundColor))

        pygame.display.update()

    def worker(self):
        """Run the worker event loop for all other protocols (drone related stuff)"""
        while True:
            print('Worker: Ready')
            sleep(60)

    def run(self):
        """Run the main event loop."""

        drone_1 = "Drone_AV1"
        drone_2 = "Drone_AV2"
        drone_3 = "Drone_AV3"
        self.fieldSize = 50

        # Update map for drone_1
        self.updateMap(coordinates=(93, 48), drone_id=drone_1, fieldSize=self.fieldSize)

        # Update map for drone_2
        self.updateMap(coordinates=(167, 203), drone_id=drone_2, fieldSize=self.fieldSize)

        # Update map for drone_3
        self.updateMap(coordinates=(0, 0), drone_id=drone_3, fieldSize=self.fieldSize)

        while App.running:
            for event in pygame.event.get():
                EventHandler.handler(self, event)

                if event.type == QUIT:
                    App.running = False


                
        pygame.quit()

    def updateMap(self, coordinates=(None, None), drone_id=None, fieldSize=None):
        # Update screen background
        self.updateBackground()

        # Render Map
        self.interface.render_map(self, screen=App.screen, fieldSize=fieldSize, screenDimensions = (self.screenWidth, self.screenHeight))

        # Render drone
        self.interface.updatePoint(self, coordinates=coordinates, drone_id=drone_id, screen=App.screen)


if __name__ == '__main__':
    App().run()