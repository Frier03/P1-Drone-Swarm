#!/usr/bin/env python
import pygame
from pygame.locals import *
from threading import Thread
from queue import Queue
from time import sleep

from interface import Interface

class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        self.backgroundColor = (102,102,102) # gray dark background
        pygame.init()

        App.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption('Drone Fleet-Management Software')
        aau_img = pygame.image.load('aau.png').convert()
        pygame.display.set_icon(aau_img)

        App.running = True

        # Initialize classes
        self.interface = Interface

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
            sleep(10)

    def run(self):
        """Run the main event loop."""
        # Update screen background
        self.updateBackground()

        # Render Map
        self.interface.render_map(pygame=pygame, screen=App.screen)

        while App.running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False

        pygame.quit()

if __name__ == '__main__':
    App().run()