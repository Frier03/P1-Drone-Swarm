import pygame
class Interface:

    def render_map(self, fieldSize = 50, mapDimensionW = 300, screen = None, screenDimensions = (None, None)) -> None:
        """Create grid and make map"""

        mapW = mapDimensionW

        # Calculate the relative mapH from the mapW.
        mapH = mapW

        # Create optional variables for the position of the map
        bottom_right = (abs((screenDimensions[0] - mapW) - (fieldSize*2)), abs((screenDimensions[1] - mapH) - (fieldSize*2)))
        bottom_left = (fieldSize, abs((screenDimensions[1] - mapH) - (fieldSize*2)))
        top_right = (abs((screenDimensions[0] - mapW) - (fieldSize*2)), fieldSize)
        top_left = (fieldSize, fieldSize)
        mid = (abs(screenDimensions[0] - mapW) // 2, abs(screenDimensions[1] - mapH) // 2)

        # Set the position of the map from optional variables
        mapStartpointX, mapStartpointY = mid

        # Create class variables
        self.mapWidth = mapW
        self.mapHeight = mapH 
        self.mapX = mapStartpointX
        self.mapY = mapStartpointY

        # Calculate the 0,0 position of the map to the end points based on the mapStartpoint X + mapwidth (also for the Y)
        raw_coordinates_x = (mapStartpointX, mapStartpointX + (mapW + fieldSize)) # x1, x2: top left corner to top right corner coordinates
        raw_coordinates_y = (mapStartpointX, mapStartpointY + (mapH + fieldSize)) # y1, y2: bottom left corner to bottom right corner
        self.threshold_x = mapStartpointX # Use threshold when we have to convert our drone data coordinates to our grid
        self.threshold_y = mapStartpointY # Use threshold when we have to convert our drone data coordinates to our grid
        # We use converted_coordinates_x/y to check for out of bounds coordinates
        converted_coordinates_x = (0, raw_coordinates_x[1] - raw_coordinates_x[0])
        converted_coordinates_y = (0, raw_coordinates_y[1] - raw_coordinates_y[0])
        #print(converted_coordinates_x, converted_coordinates_y)
        #print(f'If the position from the drone is: (15, 88) then it would be converted to: ({15 + self.threshold_x}, {88 + self.threshold_y})')


        
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

    def set_point(self, coordinates=(None, None), screen=None):

        # Calculate if the circle is out of bounds from the map
        droneX, droneY = coordinates
        droneX += self.threshold_x
        droneY += self.threshold_y
        
        if droneX >= self.mapX and droneX <= self.mapX + self.mapWidth:
            if droneY >= self.mapY and droneY <= self.mapY + self.mapHeight:
                print('drone is inside the radar!')
                pygame.draw.circle(screen, (0, 150, 0), (coordinates[0] + self.threshold_x, coordinates[1] + self.threshold_y), 5)

        # Update screen
        pygame.display.update()