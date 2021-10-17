import pygame
from pygame.draw import *
from random import randint, random
from math import pi, cos, sin

# Game initialization
pygame.init()

pygame.font.init()
score_font = pygame.font.SysFont('JetBrains Mono',  30)

FPS = 60
WIDTH, HEIGHT = 1200, 900
MARGIN = 100
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
SPECIAL = (0, 17, 102)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# Ball characteristics
N = 5

x, y, v_x, v_y = [0] * N, [0] * N, [0] * N, [0] * N
r, color, t = [0] * N, [BLACK] * N, [0] * N

# Triangle characteristics
x2, y2, phi = 10, 10, 0
A, B = 60, 25 # Length and half width
t2 = 0

V2 = 6

MOVING, TURNING = 'move', 'turn'
state = MOVING

move_t, turn_t = 30, 10

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


MAXV = 4

def new_ball():
    """
    Randomly chooses position, velocity, radius and color for the ball
    
    :returns: List (center_x, center_y, velocity_x, velocity_y, radius, color, lifespan) 
    """
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(30, 100)
    t = randint(150, 250)
    color = COLORS[randint(0, 5)]
    v_x = randint(-MAXV, MAXV + 1)
    v_y = randint(-MAXV, MAXV + 1)
    return (x, y, v_x, v_y, r, color, t)


def new_triangle():
    """
    Randomly chooses position and orientation for the ball
    
    :returns: List (center_x, center_y, orientation, lifespan) 
    """
    x = randint(MARGIN, WIDTH - MARGIN)
    y = randint(MARGIN, HEIGHT - MARGIN)
    t = 255
    phi = random() * 2 * pi
    return (x, y, phi, t)


def move_triangle(x, y, v, phi, state):
    """
    Returns new state of the triangle
    
    :param x: X coordinate 
    :param y: Y coordinate
    :param v: Velocity
    :param phi: Current orientation
    :param state: Current state, either MOVING or TURNING
    
    :returns: List (new_x, new_y, new_phi, new_state)

    ..warning: Mock function
    """
    new_x, new_y, new_phi, new_state = x, y, phi, state
    if state == MOVING:
        #new_x += v * cos(phi)
        #new_y += v * sin(phi)
        pass
    else :
        pass
    return (new_x, new_y, new_phi, new_state)


def check_triangle_click(click_pos, x, y, phi):
    """
    Checks if mouse click hit the triangle

    :returns: True if the click hit, False otherwise
    """
    return False

# Current game score
score = 0

def click(ClickEvent):
    """
    Handles mouse clicks events
    Clicked balls should disapper

    :param ClickEvent: Mouse event to be handled
    """
    global t, score, t2

    # Checking if we hit anything
    hit = False
    for i in range(N):
        if dist2(ClickEvent.pos, (x[i], y[i])) <= r[i] ** 2:
            # The smaller the ball and the faster it was clicked the better the score
            score += int((t[i] / r[i]) ** 0.5 * 4)
            hit = True
            
            # Ball termination
            t[i] = 0
    if check_triangle_click(ClickEvent.pos, x2, y2, phi):
        score += randint(5, 15)
        hit = True
        # Triangle termination
        t2 = 0

    # Punishing for misses
    if not hit:
        score -= 3
        score = max(score, 0)


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
    v_x = randint(-MAXV, MAXV + 1)
    if x_type == COLLISION_NEGATIVE:
        v_x = randint(1, MAXV + 1)
    elif x_type == COLLISION_POSITIVE:
        v_x = randint(-MAXV, 0)

    v_y = randint(-MAXV, MAXV + 1)
    if y_type == COLLISION_NEGATIVE:
        v_y = randint(1, MAXV + 1)
    elif y_type == COLLISION_POSITIVE:
        v_y = randint(-MAXV, 0)

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
    
    # Target lifespan management
    for i in range(N):
        t[i] -= 1
        if t[i] <= 0:
            # Creation of a new ball
            x[i], y[i], v_x[i], v_y[i], r[i], color[i], t[i] = new_ball()
    
    t2 -= randint(0, 3)
    if t2 <= 0:
        # Creation of a new triangle
        x2, y2, phi, t2 = new_triangle()

    # Ball movement
    for i in range(N):
        x[i] += v_x[i]
        y[i] += v_y[i]
    
    # Triangle movement
    x2, y2, phi, state = move_triangle(x2, y2, V2, phi, state)

    # Collision handling
    for i in range(N):
        collision_type = check_collision(r[i], x[i], y[i], v_x[i], v_y[i])
        if collision_type != (COLLISION_NONE, COLLISION_NONE):
            v_x[i], v_y[i] = generate_velocity(*collision_type)

    # Ball rendering
    ball_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i in range(N):
        circle(ball_surface, (*color[i], t[i]), (x[i], y[i]), r[i])
    screen.blit(ball_surface, (0, 0))

    # Triangle rendering
    trinagle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    vertices = [
                (A * cos(phi), A * sin(phi)),
                (B * cos(phi + pi / 2), B * sin(phi + pi / 2)),
                (B * cos(phi - pi / 2), B * sin(phi - pi / 2)),
                ]
    polygon(trinagle_surface, (*SPECIAL, t2), [(x2 + dx, y2 + dy) for dx, dy in vertices])
    screen.blit(trinagle_surface, (0, 0))

    # Score rendering
    textsurface = score_font.render(f"Score := {score}", True, BLACK)
    screen.blit(textsurface, (30, 10))

    # Display update
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()