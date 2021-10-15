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

# Ball characteristics
N = 5

x, y, v_x, v_y = [0] * N, [0] * N, [0] * N, [0] * N
r, color, t = [0] * N, [BLACK] * N, [0] * N

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
    
    :returns: List (center_x, center_y, velocity_x, velocity_y, radius, color, lifespan) 
    """
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    t = randint(50, 80)
    color = COLORS[randint(0, 5)]
    v_x = randint(-5, 5)
    v_y = randint(-5, 5)
    return (x, y, v_x, v_y, r, color, t)


# Current game score
score = 0

def click(ClickEvent):
    """
    Handles mouse clicks events
    Clicked balls should disapper

    :param ClickEvent: Mouse event to be handled
    """
    global t, score

    # Checking if we hit anything
    for i in range(N):
        if dist2(ClickEvent.pos, (x[i], y[i])) <= r[i] ** 2:
            
            # Score update:
            # the smaller the ball and the faster it was clicked the better the score
            score += t[i] // (r[i] // 5)

            # Ball termination
            t[i] = 0
        else :
            # Punishing for misses
            score -= 1


# Collison types
COLLISION_NEGATIVE = -1 # Ball's too far to the left/top
COLLISION_NONE     = 0  # Ball's inside the walls
COLLISION_POSITIVE = 1  # Ball's too far to the right/bottom

def check_collision(r, x, y, v_x, v_y):
    """
    Determines if the ball hit the wall and returns collision type

    :param r: Radius of the ball
    :param x: X coordinate of the ball
    :param y: Y coordinate of the ball
    :param v_x: X coordinate of the ball's velocity
    :param v_y: Y coordinate of the ball's velocity

    :returns: List (x_type, y_type), where x_type and y_type are
              one of the {COLLISION_NEGATIVE, COLLISION_NONE, COLLISION_POTIVE}
    """
    x_type = COLLISION_NONE
    if x < r and v_x < 0:
        x_type = COLLISION_NEGATIVE
    elif x > WIDTH - r and v_x > 0:
        x_type = COLLISION_POSITIVE
    
    y_type = COLLISION_NONE
    if y < r and v_y < 0:
        y_type = COLLISION_NEGATIVE
    elif y > HEIGHT - r and v_y > 0:
        y_type = COLLISION_POSITIVE

    return (x_type, y_type)


def generate_velocity(x_type, y_type):
    """
    Generates random velocity for the ball after wall collision
    After velocity generation ball will move away from the wall

    :param x_type: Type of the collision with vertical walls,
                   one of the {COLLISION_NEGATIVE, COLLISION_NONE, COLLISION_POTIVE}
    :param y_type: Type of the collision with horizontal walls,
                   one of the {COLLISION_NEGATIVE, COLLISION_NONE, COLLISION_POTIVE}

    :returns: List (v_x, v_y) where v_x and v_y are projections of the new velocity
                                                        onto the corresponding axis
    """
    v_x = randint(-5, 5)
    if x_type == COLLISION_NEGATIVE:
        v_x = randint(1, 5)
    elif x_type == COLLISION_POSITIVE:
        v_x = randint(-5, 0)

    v_y = randint(-5, 5)
    if y_type == COLLISION_NEGATIVE:
        v_y = randint(1, 5)
    elif y_type == COLLISION_POSITIVE:
        v_y = randint(-5, 0)

    return (v_x, v_y)


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
    for i in range(N):
        if t[i] <= 0:
            # Creation of a new ball
            x[i], y[i], v_x[i], v_y[i], r[i], color[i], t[i] = new_ball()
        t[i] -= 1

    # Ball movement
    for i in range(N):
        x[i] += v_x[i]
        y[i] += v_y[i]
    
    # Collision handling
    for i in range(N):
        collision_type = check_collision(r[i], x[i], y[i], v_x[i], v_y[i])
        if collision_type != (COLLISION_NONE, COLLISION_NONE):
            v_x[i], v_y[i] = generate_velocity(*collision_type)

    # Ball rendering
    for i in range(N):
        circle(screen, color[i], (x[i], y[i]), r[i])
    
    # Score rendering
    textsurface = score_font.render(f"Score := {score}", True, BLACK)
    screen.blit(textsurface, (30, 10))

    # Display update
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()