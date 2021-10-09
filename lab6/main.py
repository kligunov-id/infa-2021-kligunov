import pygame
from pygame.draw import *
from random import randint

# Game initialization
pygame.init()

pygame.font.init()
score_font = pygame.font.SysFont('JetBrains Mono',  30)

FPS = 60
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))

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

# Ball speed
Vx, Vy = 0, 0

# Ball lifespan
t = 0

def dist2(p, q):
    """
    Returns distance squared between points p and q
    
    :param p: List of coordinates (x, y) of the first point
    :param q: List of coordinates (x, y) of the second point
    
    .. warning:: Distance returned is squared
    """
    x1, y1 = p
    x2, y2 = q
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def new_ball():
    """
    Randomly chooses position, velocity, radius and color for the ball
    
    :returns: List (x_center, y_center, velocity_x, velocity_y, radius, color, lifespan) 
    """
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    t = 60
    color = COLORS[randint(0, 5)]
    Vx = randint(-5, 5)
    Vy = randint(-5, 5)
    return (x, y, Vx, Vy, r, color, t)


# Current game score
score = 0

def click(ClickEvent):
    """
    Handles mouse clicks events
    Clicked balls should disapper

    :param ClickEvent: Mouse event to be handled
    """

    # Checking if we hit anything
    if dist2(ClickEvent.pos, (x, y)) <= r ** 2:
        global t, score

        # Score update: the smaller the ball and the faster it was clicked the better the score
        score += t // (r // 5)

        # Ball termination
        t = 0
    else :
        # Punishing for misses
        score -= 1


# Collison types
COLLISION_NEGATIVE = -1 # Ball's too far to the left/top
COLLISION_NONE     = 0  # Ball's inside the walls
COLLISION_POSITIVE = 1  # Ball's too far to the right/bottom

def check_collision(x, y, Vx, Vy):
    """
    Derermines if the ball hit the wall and returns collision type

    :param x: X coordinate of the ball
    :param y: Y coordinate of the ball
    :param Vx: X coordinate of the ball's velocity
    :param Vy: Y coordinate of the ball's velocity

    :returns: List (x_type, y_type), where x_type and y_type are
              one of the {COLLISION_NEGATIVE, COLLISION_NONE, COLLISION_POTIVE}

    ..warning:: This is a mock function
    """
    return (COLLISION_NONE, COLLISION_NONE)


def generate_velocity(x_type, y_type):
    """
    Generates random velocity for the ball after wall collision
    After velocity generation ball will move away from the wall

    :param x_type: Type of the collision with vertical walls,
                   one of the {COLLISION_NEGATIVE, COLLISION_NONE, COLLISION_POTIVE}
    :param y_type: Type of the collision with horizontal walls,
                   one of the {COLLISION_NEGATIVE, COLLISION_NONE, COLLISION_POTIVE}

    :returns: List (Vx, Vy) where Vx and Vy are projections of the new velocity
                                                        onto the corresponding axis
    ..warning:: This is a mock function
    """
    return (randint(0, 0), randint(0, 0))


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
        # Creation of a new ball
        x, y, Vx, Vy, r, color, t = new_ball()
    t -= 1

    # Ball movement
    x += Vx
    y += Vy
    
    # Collision handling
    if check_collision(x, y, Vx, Vy) != (COLLISION_NONE, COLLISION_NONE):
        print("Collision's happened")
        Vx, Vy = generate_velocity(*check_collision(x, y, Vx, Vy))

    # Ball rendering
    circle(screen, color, (x, y), r)
    
    # Score rendering
    textsurface = score_font.render(f"Score := {score}", True, BLACK)
    screen.blit(textsurface, (30, 10))

    # Display update
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()