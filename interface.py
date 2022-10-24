
import pygame
class Interface:

    def render_map(fieldSize = 40, mapDimensions = (850, 650), pygame = None, screen = None) -> None:
        """Create grid and make map"""
        pointX = None
        pointY = None
        pointSubX = None

        mapX, mapY = mapDimensions
        #300, 200
        mapStartpointX, mapStartpointY = (300, 200)
        fieldColor = (107,107,107)
        # Create grid
        for x in range(mapStartpointX, mapX, fieldSize):
            for y in range(mapStartpointY, mapY, fieldSize):
                mapField = pygame.Rect(x, y, fieldSize, fieldSize)
                pygame.draw.rect(screen, fieldColor, mapField, 1)

                if x == 580:
                    pointX = x
                    pygame.draw.circle(screen,(0, 0, 0),(x,mapStartpointY),2) # DRAW CIRCLE
                elif x == 300 and y == 440:
                    pointY = y
                    pointSubX = x
                    pygame.draw.circle(screen,(0, 0, 0),(x,y),2) # DRAW CIRCLE

        # Create outline for X
        pygame.draw.line(screen, (0, 150 ,0), (pointX, mapStartpointY), (pointX, mapY + (fieldSize-10)), 2)
        # Create outline for Y
        pygame.draw.line(screen, (0, 150, 0), (pointSubX, pointY), (mapX + 10, pointY), 2)

        # Update
        pygame.display.update()

