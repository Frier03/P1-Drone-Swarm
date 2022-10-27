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

        # get x, y coordinates from drone
        x, y = (50, 50)
        drone_id = "Drone_AV1"
        self.fieldSize = 100

        # Update map
        self.updateMap(coordinates=(x, y), drone_id=drone_id, fieldSize=self.fieldSize)

        while App.running:
            for event in pygame.event.get():
                # We use self to access other classes in our eventhandler
                EventHandler.handler(self, event)

                if event.type == QUIT:
                    App.running = False


                
        pygame.quit()

    def updateMap(self, coordinates=None, drone_id=None, fieldSize=None):
        # Update screen background
        self.updateBackground()

        # Render Map
        self.interface.render_map(self, screen=App.screen, fieldSize=fieldSize, screenDimensions = (self.screenWidth, self.screenHeight))

        # Render drone
        self.interface.updatePoint(self, coordinates=coordinates, drone_id=drone_id, screen=App.screen)


if __name__ == '__main__':
    App().run()