import pygame
class Interface:

    def render_map(self, fieldSize = 50, mapDimensionW = 400, screen = None) -> None:
        """Create grid and make map"""

        mapW = mapDimensionW

        # Calculate the relative mapH from the mapW.
        mapH = mapW

        mapStartpointX, mapStartpointY = (500, 300)

        # Calculate the relative mapW and mapH to the mapStartpointX and mapStartpointY
        mapW = mapW + mapStartpointX
        mapH = mapH + mapStartpointY

        fieldColor = (107,107,107)

        # Create grid
        for x in range(mapStartpointX, mapW+1, fieldSize):
            for y in range(mapStartpointY, mapH+1, fieldSize):
                mapField = pygame.Rect(x, y, fieldSize, fieldSize)
                pygame.draw.rect(screen, fieldColor, mapField, 1)

        # Calculate mid point
        mid_x_coordinate = (mapStartpointX + mapW) // 2 + (fieldSize / 2)
        mid_y_coordinate = (mapStartpointY + mapH) // 2 + (fieldSize / 2)

        # Create outline for X
        pygame.draw.line(screen, (0, 150 ,0), (mid_x_coordinate, mapStartpointY), (mid_x_coordinate, mapH + fieldSize), 2)
        # Create outline for Y
        pygame.draw.line(screen, (0, 150, 0), (mapStartpointX, mid_y_coordinate), (mapW + fieldSize, mid_y_coordinate), 2)

        # Set self render_map axis
        self.render_map_axis = ((mapStartpointX, mapStartpointY), (mapW + fieldSize, mapH + fieldSize)) 

        # Update screen
        pygame.display.update()

    def get_render_map_axis(self):
        return self.render_map_axis
