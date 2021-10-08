import pygame
from pygame.draw import *
from random import randint

# Game initialization
pygame.init()
FPS = 60
screen = pygame.display.set_mode((1200, 900))


RED  = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# Ball coordinates, radius and color
x, y, r, color = 0, 0, 0, RED

# Ball lifespan
t = 0

def new_ball():
    """
    Creates new ball with randomly chosen position and color
    
    :returns: (x_center, y_center, radius, color, lifespan) 
    """
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    t = 60
    color = COLORS[randint(0, 5)]
    return (x, y, r, color, t)


def click():
    """
    Handles mouse clicks events
    Clicked balls should disapper
    """
    print('Click')


# Pygame setup
pygame.display.update()
clock = pygame.time.Clock()
finished = False

# Main cycle
while not finished:
    clock.tick(FPS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click()
    
    # Game engine
    if t <= 0:
        x, y, r, color, t = new_ball()
    t -= 1

    # Graphics
    circle(screen, color, (x, y), r)
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()