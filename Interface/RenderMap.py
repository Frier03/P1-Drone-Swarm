import pygame, json

def render_map(self, screen = None, realtimeDimension=(2,2), sprite_groups: list() = None) -> None:
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
    pygame.draw.rect(screen, (217,222,224, 10), pygame.Rect(mapX-shadowDistance, mapY-shadowDistance, mapW+(shadowDistance*2), mapH+(shadowDistance*2)),border_radius=rad)

    # Draw Box
    pygame.draw.rect(screen, (255,255,255), pygame.Rect(mapX, mapY, mapW, mapH),border_radius=rad)

    # Get Each Drone id/name,position, yaw, battery, altitude, speed and connected status in a list?
    # GET THE LIST FROM LAST TO FIRST ADDED DRONES
    drones = [ ['Tello EDU 2', 133.4, 82.3, 0, 87, 34, 3, 'C'], ['Tello EDU 1', 256.3, 142.3, 0, 87, 34, 3, 'C'] ] # c = connected | d = disconnected

    # Sprite groups [] for each drone
    for data in drones:
        drone_sprite = sprite_groups[drones.index(data)]
        drone_name = data[0]
        x = data[1] + threshold_x  # aligns to the 0,0 pointer of the map
        y = data[2] + threshold_y 
        yaw = data[3]
        battery = data[4]
        altitude = data[5]
        speed = data[6]
        status = data[7]

        drone_sprite.update(x, y)
        drone_sprite.draw(screen)


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super(Sprite, self).__init__()

        drone0 = pygame.image.load('Interface/drone.png')
        drone0 = pygame.transform.smoothscale(drone0, (80, 80))
        drone1 = pygame.image.load('Interface/drone1.png')
        drone1 = pygame.transform.smoothscale(drone1, (80, 80))
        self.images = [drone0, drone1]
        self.index = 0
 
        self.image = self.images[self.index]
 
        self.rect = pygame.Rect(0, 0, 150, 198)
 
    def update(self, x, y):
        self.index += 1
 
        if self.index >= len(self.images):
            self.index = 0
        
        self.image = self.images[self.index]
        self.rect.x = x
        self.rect.y = y