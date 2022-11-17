import pygame, json

def render_map(self, screen = None, realtimeDimension=(2,2)) -> None:
    """Create grid and make map"""

    # realtimeDimensions (2,2) [m] = 2x2 in meters
    mapX, mapY = 400, 85
    mapW, mapH = 800, 600
    rad = 2
    shadowDistance = 2

    # Set the position of the map
    mapStartpointX, mapStartpointY = mapX, mapY
    mapEndpointX, mapEndpointY = mapX + mapW, mapY + mapH

    #top left to top right x= -500
    #top left to bottom right y= -625

    # Calculate the 0,0 position of the map to the end points
    threshold_x, threshold_y = mapStartpointX, mapStartpointY 

    # Draw Shadow
    pygame.draw.rect(self.screen, (217,222,224, 10), pygame.Rect(mapX-shadowDistance, mapY-shadowDistance, mapW+(shadowDistance*2), mapH+(shadowDistance*2)),border_radius=rad)

    # Draw Box
    pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(mapX, mapY, mapW, mapH),border_radius=rad)

    # Get Each Drone id/name,position, yaw, battery, altitude, speed and connected status in a list?
    #....
    #....
    drones = [ ['Tello EDU 1', 133.4, 82.3, 45, 87, 34, 3, 'C'] ] # c = connected | d = disconnected

    for drone in drones:
        
        drone_name = drone[0]
        x = drone[1] + threshold_x  # aligns to the 0,0 pointer of the map
        y = drone[2] + threshold_y 
        battery = drone[3]
        altitude = drone[4]
        speed = drone[5]
        status = drone[6]

        # Draw Drone Marker on Map at x, y position
        pygame.draw.circle(screen, (0, 255, 0), (x, y), 5)

        # Draw ALT + SPD text under Drone Marker
        text_content = ['SPD(m/s): ' + str(speed), 'ALT(m/s): ' + str(altitude)]
        fontsize = 20
        font = pygame.font.SysFont("Helvetica.ttf", fontsize)
        text_y = 15
        for text in text_content:
            # Render text
                text = font.render(text, True, (100, 100, 100))

                # text surface object
                textRect = text.get_rect()

                # set text slighty under drone
                textRect.center = (x, y+text_y)
                # copying the text surface objects
                # to the display surface objects
                # at the center coordinate.
                screen.blit(text, textRect)

                text_y += fontsize-2