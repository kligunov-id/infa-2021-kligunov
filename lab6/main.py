import pygame
from pygame.draw import *
from random import randint

# Game initialization
pygame.init()
pygame.font.init()
score_font = pygame.font.SysFont('JetBrains Mono',  30)
FPS = 60
screen = pygame.display.set_mode((1200, 900))

# Colors
RED  = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# Ball coordinates, radius and color
x, y, r, color = 0, 0, 0, RED

# Ball lifespan
t = 0

def dist2(p, q):
    """
    Returns distance squared between points p and q
    
    :param p: Pair of coordinates (x, y) of the first point
    :param q: Pair of coordinates (x, y) of the second point
    
    .. warning:: Distance returned is squared
    """
    x1, y1 = p
    x2, y2 = q
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def new_ball():
    """
    Randomly chooses position, radius and color for the ball
    
    :returns: (x_center, y_center, radius, color, lifespan) 
    """
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    t = 60
    color = COLORS[randint(0, 5)]
    return (x, y, r, color, t)

# Current game score
score = 0

def click(ClickEvent):
    """
    Handles mouse clicks events
    Clicked balls should disapper

    :param ClickEvent: mouse event to be handled
    """

    # Checking if we hit anything
    if dist2(ClickEvent.pos, (x, y)) <= r ** 2:
        global t, score

        # Score update. The smaller the ball and the faster it was clicked the better the score
        score += t // (r // 5)

        # Ball termination
        t = 0
    else :
        # Punishing for misses
        score -= 1

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
            click(event)
    
    # Game engine
    if t <= 0:
        # Initializing new ball
        x, y, r, color, t = new_ball()
    t -= 1

    # Render circles
    circle(screen, color, (x, y), r)
    
    # Render score
    textsurface = score_font.render(f"Score := {score}", True, BLACK)
    screen.blit(textsurface, (30, 10))

    # Apply changes
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()