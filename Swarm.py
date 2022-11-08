import pygame_widgets
import pygame
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

def output():
    # Get text in the textbox
    print(textbox.getText())


pygame.init()
win = pygame.display.set_mode((1000, 600))

textbox = TextBox(win, 100, 100, 800, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=output, radius=10, borderThickness=5)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))
    print(events)
    pygame_widgets.update(events)
    pygame.display.update()