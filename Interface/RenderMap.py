import pygame, json

def render_map(self, screen = None, realtimeDimension=(2,2)) -> None:
    """Create grid and make map"""

    # realtimeDimensions (2,2) [m] = 2x2 in meters
    mapX, mapY = 400, 75
    mapW, mapH = 600, 500
    rad = 2
    shadowDistance = 2

    # Set the position of the map
    mapStartpointX, mapStartpointY = mapX, mapY
    mapEndpointX, mapEndpointY = mapX + mapW, mapY + mapH

    #top left to top right x= -500
    #top left to bottom right y= -625

    # Calculate the 0,0 position of the map to the end points based on the mapStartpoint X + mapwidth (also for the Y)
    self.threshold_x, self.threshold_y = mapStartpointX, mapStartpointY 

    # Shadow
    pygame.draw.rect(self.screen, (217,222,224, 10), pygame.Rect(mapX-shadowDistance, mapY-shadowDistance, mapW+(shadowDistance*2), mapH+(shadowDistance*2)),border_radius=rad)

    # Box
    pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(mapX, mapY, mapW, mapH),border_radius=rad)

    # Point at 0,0 
    pygame.draw.circle(self.screen, (0,255,0), (self.threshold_x, self.threshold_y), 4)


def updatePoint(self, coordinates=(None, None), drone_id=None, screen=None, showSPD=True, showALT=True, showBAT=False, showSIG=False):
    if drone_id != None and coordinates != (None, None):

        # Get drone information from drone_id
        with open('drone_data.json', 'r') as fh:
            drone_data = json.load(fh)

            #----------try to change-----------------
            for key, value in drone_data.items():
                if key == drone_id:
                    droneX = drone_data[drone_id]['POS_X'] = coordinates[0]
                    droneY = drone_data[drone_id]['POS_Y'] = coordinates[1]
                else:
                    droneX          =       drone_data[key]['POS_X']
                    droneY          =       drone_data[key]['POS_Y']
                    
                droneStatus = drone_data[key]['STATUS']

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

                        # Check the status of the drone, and change color from that
                        if droneStatus == 'mission':
                            c = (0, 255, 0)
                        elif droneStatus == 'idle':
                            c = (255, 0, 0)
                                
                        pygame.draw.circle(screen, c, (droneX, droneY), self.droneSize)

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