#!/usr/bin/env python
import pygame
from pygame.locals import *
import pygame_widgets
from Interface import GUI

class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screenWidth = 1420
        self.screenHeight = 800

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), pygame.NOFRAME)

        # Initialize interface classes
        self.gui = GUI.Gui(self.screen, pygame.event.get())
        
        App.running = True

    def run(self):
        """Run the main event loop."""
        while App.running:          #Could be encapsuled in a try except
            # Load GUI
            self.gui() # Calls "__call__" inside gui class
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False
        
            # Call once every loop to allow widgets to render and listen
            pygame_widgets.update(pygame.event.get())
            
            # Update now all changes from above to the screen
            pygame.display.update()

            self.clock.tick(20)

        self.onClose()

    def onClose(self):
        pygame.quit()

if __name__ == '__main__':
    App().run()
