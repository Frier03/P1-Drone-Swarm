import pygame, json, time
from itertools import cycle
MOUSEBUTTONDOWN                     =   1025

corners = [] # x,y at each corner
lengths = [] # length at each line

def clean_up_skelenton(self):
    # Small algorithm to make some lines smoother and so on...
    pass

def render_calibrated_skeleton(self):
    for _ in range(len(corners)):
        # Redraw circles
        pygame.draw.circle(self.screen, (80, 80, 80), (corners[_][0]), 5)

        # Redraw lines
        pygame.draw.line(self.screen, 'gray', corners[_-1][0], corners[_][0])

        # Redraw text
        for _ in range(len(lengths)):
            # Create font
            font = pygame.font.SysFont("Helvetica.ttf", 20)

            text = font.render(f'{lengths[_][1]} [m]', True, (255, 255, 255))
            self.screen.blit(text, lengths[_][0])

        # Update
        pygame.display.update()

def calibrate_map(self, event):
    length = ''
    text_position = (0, 0)

    for _ in range(len(corners)):
        # Draw line from the first corner to the mouse position
        startPosition = corners[-1][0]
        mousePosition = event.pos

        # Redraw circles
        pygame.draw.circle(self.screen, (80, 80, 80), (corners[_][0]), 5)

        # Redraw lines
        pygame.draw.line(self.screen, 'gray', corners[_-1][0], corners[_][0])

        # Redraw text
        for _ in range(len(lengths)):
            # Create font
            font = pygame.font.SysFont("Helvetica.ttf", 20)

            text = font.render(f'{lengths[_][1]} [m]', True, (255, 255, 255))
            self.screen.blit(text, lengths[_][0])


        # Subtract startPosition and mousePosition tuples
        text_position = (startPosition[0] + ((mousePosition[0] - startPosition[0]) / 2), startPosition[1] + ((mousePosition[1] - startPosition[1]) / 2))
        length = str( ( round(abs(((mousePosition[0] - startPosition[0]) / 2) / 100 * 2), 2), round(abs(((mousePosition[1] - startPosition[1]) / 2) / 100 * 2), 2) ) )
        
        # Create font
        font = pygame.font.SysFont("Helvetica.ttf", 30)
        # Render text
        text = font.render(f'{length}  [m]', True, (255, 255, 255))
        self.screen.blit(text, text_position)

        # Draw current line
        pygame.draw.line(self.screen, 'yellow', startPosition, mousePosition)
        
        # Update lines
        pygame.display.update()

    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
            pygame.draw.circle(self.screen, (80, 80, 80), (event.pos), 5)
            corners.append([event.pos])
            
            if len(corners) > 1:
                lengths.append([text_position, length])
