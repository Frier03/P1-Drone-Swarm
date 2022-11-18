import pygame
 
 
SIZE = WIDTH, HEIGHT = 600, 400 #the width and height of our screen
BACKGROUND_COLOR = pygame.Color('white') #The background colod of our window
FPS = 10 #Frames per second
 
class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        super(MySprite, self).__init__()

        drone0 = pygame.image.load('Interface/drone.png')
        drone0 = pygame.transform.smoothscale(drone0, (80, 80))
        drone1 = pygame.image.load('Interface/drone1.png')
        drone1 = pygame.transform.smoothscale(drone1, (80, 80))
        self.images = []
        self.images.append(drone0)
        self.images.append(drone1)
 
        self.index = 0
 
        self.image = self.images[self.index]
 
        self.rect = pygame.Rect(5, 5, 150, 198)
 
    def update(self, x, y):
        self.index += 1
 
        if self.index >= len(self.images):
            self.index = 0
        
        self.image = self.images[self.index]
        self.rect.x = x
        self.rect.y = y

    def moveToCoordinates(self, x, y):
        self.rect.x = x
        self.rect.y = y
 
def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    my_sprite = MySprite()
    my_group = pygame.sprite.Group(my_sprite)
    clock = pygame.time.Clock()
    x=200
    y=200
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
        my_group.update(x, y)
        screen.fill(BACKGROUND_COLOR)
        my_group.draw(screen)
        pygame.display.update()
        clock.tick(20)
 
if __name__ == '__main__':
    main()