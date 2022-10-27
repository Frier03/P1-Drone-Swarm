import pygame, json, time


class Interface:

    def render_map(self, fieldSize = None, mapDimensionW = 500, screen = None, screenDimensions = (None, None)) -> None:
        """Create grid and make map"""

        mapW = mapDimensionW

        self.textSize = int(fieldSize/3)
        self.droneSize = int(fieldSize/10)

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
        # Create outline for left
        pygame.draw.line(screen, (0, 0 ,0), (mapStartpointX, mapStartpointY), (mapStartpointX, mapH + fieldSize), 1)
        # Create outline for right
        pygame.draw.line(screen, (0, 0 ,0), (mapW + fieldSize, mapStartpointY), (mapW + fieldSize, mapH + fieldSize), 1)
        # Create outline for top
        pygame.draw.line(screen, (0, 0 ,0), (mapStartpointX, mapStartpointY), (mapW + fieldSize, mapStartpointY), 2)
        # Create outline for bottom
        pygame.draw.line(screen, (0, 0 ,0), (mapStartpointX, mapH + fieldSize), (mapW + fieldSize, mapH + fieldSize), 2)


        # Set self render_map axis
        self.render_map_axis = ((mapStartpointX, mapStartpointY), (mapW + fieldSize, mapH + fieldSize)) 

        # Set self render_map x,y
        self.render_map_xy = (self.mapX, self.mapY)

        # Update screen
        pygame.display.update()

    def get_render_map_xy(self):
        return self.render_map_xy
    def get_render_map_axis(self):
        return self.render_map_axis

    def updatePoint(self, coordinates=(None, None), drone_id=None, screen=None, showSPD=True, showALT=True, showBAT=False, showSIG=False):
        if drone_id != None and coordinates != (None, None):

            # Get drone information from drone_id
            with open('drone_data.json', 'r') as fh:
                drone_data = json.load(fh)

                #----------try to change-----------------
                for key, value in drone_data.items():
                    if key == drone_id:
                        drone_data[drone_id]['POS_X'] = coordinates[0]
                        drone_data[drone_id]['POS_Y'] = coordinates[1]
                        droneX          =       drone_data[key]['POS_X']
                        droneY          =       drone_data[key]['POS_Y']
                    else:
                        droneX          =       drone_data[key]['POS_X']
                        droneY          =       drone_data[key]['POS_Y']

                    # Calculate if the updated drone is out of bounds from the map
                    droneX += self.threshold_x
                    droneY += self.threshold_y

                    textContent = []
                    self.droneCoords = (droneX, droneY)

                    textContent.append('SPD(m/s): ' + str(drone_data[key]['SPD(m/s)']))
                    textContent.append('ALT(m/s): ' + str(drone_data[key]['ALT(m/s)']))
            
                    if droneX >= self.mapX and droneX <= self.mapX + self.mapWidth*2:
                        if droneY >= self.mapY and droneY <= self.mapY + self.mapHeight*2:
                            #print('drone is inside the radar!')
                            pygame.draw.circle(screen, (255, 22, 12), (droneX, droneY), self.droneSize)

                    # Create text on the circle
                    # Default font
                    font = pygame.font.SysFont("Helvetica.ttf", self.textSize-2)

                    text_y = self.textSize

                    for i in range(len(textContent)):
                        # Render text
                        text = font.render(textContent[i], True, (255, 255, 255))

                        # text surface object
                        textRect = text.get_rect()

                        # set text slighty under drone
                        textRect.center = (droneX, droneY+text_y)
                        # copying the text surface objects
                        # to the display surface objects
                        # at the center coordinate.
                        screen.blit(text, textRect)

                        text_y += self.textSize-self.droneSize
                    
                    with open('drone_data.json', 'w') as fh:
                        json.dump(drone_data, fh)

                    

            # Update screen
            pygame.display.update()
