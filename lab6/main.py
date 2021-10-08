import pygame
from pygame.draw import *
from random import randint

# Game initialization
pygame.init()
FPS = 1
screen = pygame.display.set_mode((1200, 900))


RED  = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# Ball coordinates and creation

x, y, r = 0, 0, 0

def new_ball():
    """
    Draws new ball with randomly chosen position and color
    """
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

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
            print('Click!')
    
    # Game engine
    new_ball()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()