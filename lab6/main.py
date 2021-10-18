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


class Ball:

    MAX_V = 4

    # Collison types
    COLLISION_NEGATIVE = -1 # Ball's too far to the left/top
    COLLISION_NONE     = 0  # Ball's inside the walls
    COLLISION_POSITIVE = 1  # Ball's too far to the right/bottom

    def __init__(self):
        """ Randomly choses position (x, y), velocity (v_x, v_y), color and life counter t """
        self.x = randint(100, 1100)
        self.y = randint(100, 900)
        self.r = randint(30, 100)
        self.t = randint(150, 250)
        self.color = COLORS[randint(0, 5)]
        self.v_x = randint(-Ball.MAX_V, Ball.MAX_V + 1)
        self.v_y = randint(-Ball.MAX_V, Ball.MAX_V + 1)
    
    def reset(self):
        """ Randomly choses position (x, y), velocity (v_x, v_y), color and life counter t """
        self.x = randint(100, 1100)
        self.y = randint(100, 900)
        self.r = randint(30, 100)
        self.t = randint(150, 250)
        self.color = COLORS[randint(0, 5)]
        self.v_x = randint(-Ball.MAX_V, Ball.MAX_V + 1)
        self.v_y = randint(-Ball.MAX_V, Ball.MAX_V + 1)

    def move(self):
        self.x += self.v_x
        self.y += self.v_y

    def reduce_life_clock(self):
        """ Reduces life clock (when it reaches 0, target is considered to be dead) """
        self.t -= 1

    def check_collision(self):
        """
        Determines if the ball hit the wall and returns collision type

        :returns: List (x_type, y_type), where x_type and y_type are
              one of the {COLLISION_NEGATIVE, COLLISION_NONE, COLLISION_POTIVE}
        """
        x_type = Ball.COLLISION_NONE
        if self.x < self.r and self.v_x < 0:
            x_type = Ball.COLLISION_NEGATIVE
        elif self.x > WIDTH - self.r and self.v_x > 0:
            x_type = Ball.COLLISION_POSITIVE
    
        y_type = Ball.COLLISION_NONE
        if self.y < self.r and self.v_y < 0:
            y_type = Ball.COLLISION_NEGATIVE
        elif self.y > HEIGHT - self.r and self.v_y > 0:
            y_type = Ball.COLLISION_POSITIVE

        return (x_type, y_type)

    def generate_velocity(self, x_type, y_type):
        """
        Generates random velocity for the ball after wall collision
        After velocity generation ball will move away from the wall

        :param x_type: Type of the collision with vertical walls,
                   one of the {COLLISION_NEGATIVE, COLLISION_NONE, COLLISION_POTIVE}
        :param y_type: Type of the collision with horizontal walls,
                   one of the {COLLISION_NEGATIVE, COLLISION_NONE, COLLISION_POTIVE}
         """
        self.v_x = randint(-Ball.MAX_V, Ball.MAX_V + 1)
        if x_type == Ball.COLLISION_NEGATIVE:
            self.v_x = randint(1, Ball.MAX_V + 1)
        elif x_type == Ball.COLLISION_POSITIVE:
            self.v_x = randint(-Ball.MAX_V, 0)

        self.v_y = randint(-Ball.MAX_V, Ball.MAX_V + 1)
        if y_type == Ball.COLLISION_NEGATIVE:
            self.v_y = randint(1, Ball.MAX_V + 1)
        elif y_type == Ball.COLLISION_POSITIVE:
            self.v_y = randint(-Ball.MAX_V, 0)

    def is_clicked(self, pos):
        """
        Checks if mouse click hit the ball

        :param pos: Mouse click position
        :returns: True if the ball was hit, False otherwise
        """
        return dist2(pos, (self.x, self.y)) <= self.r ** 2
    
    def get_score(self):
        """ Returns score awarded for successful hit """
        return int((self.t / self.r) ** 0.5 * 4)
    
    def terminate(self):
        """ Marks the ball as dead by setting life counter to zero """
        self.t = 0

    def is_dead(self):
        """ Returns true if the ball should be removed """
        return self.t <= 0
    
    def render(self, screen):
        """
        :param screen: PyGame screen to render ball on
        """
        if self.t <= 0:
            print ("wtf")
        circle(screen, (*self.color, self.t), (self.x, self.y), self.r)
N = 5

targets = [Ball() for _ in range(N)]

# Triangle characteristics
M = 2
x2, y2, phi = [10] * M, [10] * M, [0] * M
A, B = 60, 25 # Length and half width
t2 = [0] * M

v2 = 5
v_phi = 2 * pi / 60

MOVING, TURNING_LEFT, TURNING_RIGHT = 'move', 'left', 'right'
state = [MOVING] * M
move_t, turn_t = 30, 10

def new_triangle():
    """
    Randomly chooses position, orientation and movement state for the ball
    
    :returns: List (center_x, center_y, orientation, state, lifespan) 
    """
    x = randint(MARGIN, WIDTH - MARGIN)
    y = randint(MARGIN, HEIGHT - MARGIN)
    t = 255
    phi = random() * 2 * pi
    state = MOVING
    return (x, y, phi, state, t)


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
        new_x += v2 * cos(phi)
        new_y += v2 * sin(phi)
        if randint(0, move_t) == 0:
            new_state = TURNING_LEFT if randint(0, 2) else TURNING_RIGHT
    elif state == TURNING_LEFT:
        new_phi += v_phi
        if randint(0, turn_t) == 0:
            new_state = MOVING
    else:
        new_phi -= v_phi
        if randint(0, turn_t) == 0:
            new_state = MOVING
    return (new_x, new_y, new_phi, new_state)


def check_triangle_click(click_pos, x, y, phi):
    """
    Checks if mouse click hit the triangle

    :returns: True if the click hits, False otherwise
    """
    # Get click position relative to the center of shortest side
    x_click, y_click = click_pos
    x_click -= x
    y_click -= y
    # Get vector in canonical basis(x axis towards vertice, y alongside shortest side) by rotation by -phi
    x_click, y_click = cos(phi) * x_click + sin(phi) * y_click, - sin(phi) * x_click + cos(phi) * y_click
    # Triangle is an intersection of x > 0, x + y > 0 and x - y > 0
    return x_click > 0 and x_click / A + y_click / B <= 1 and x_click / A - y_click / B <= 1

# Current game score
score = 0

def click(ClickEvent):
    """
    Handles mouse clicks events
    Clicked targets should disapper

    :param ClickEvent: Mouse event to be handled
    """
    global score, t2

    # Checking if we hit anything
    hit = False
    for ball in targets:
        if ball.is_clicked(ClickEvent.pos):
            score += ball.get_score()
            ball.terminate()
            hit = True
    for i in range(M):
        if check_triangle_click(ClickEvent.pos, x2[i], y2[i], phi[i]):
            score += randint(5, 25)
            hit = True
            # Triangle termination
            t2[i] = 0

    # Punishing for misses
    if not hit:
        score -= 3
        score = max(score, 0)


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
    
    for ball in targets:
        ball.reduce_life_clock()
        if ball.is_dead():
            ball.reset()

    for i in range(M):
        t2[i] -= randint(0, 3)
        if t2[i] <= 0:
            # Creation of a new triangle
            x2[i], y2[i], phi[i], state[i], t2[i] = new_triangle()

    # Ball movement
    for ball in targets:
        ball.move()
    
    # Triangle movement
    for i in range(M):
        x2[i], y2[i], phi[i], state[i] = move_triangle(x2[i], y2[i], v2, phi[i], state[i])

    # Collision handling
    for ball in targets:
        collision_type = ball.check_collision()
        if collision_type != (Ball.COLLISION_NONE, Ball.COLLISION_NONE):
            ball.generate_velocity(*collision_type)
    for i in range(M):
        if x2[i] < 0 or x2[i] > WIDTH or y2[i] < 0 or y2[i] > HEIGHT:
            t2[i] = 0

    # Ball rendering
    ball_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for ball in targets:
        ball.render(ball_surface)
    screen.blit(ball_surface, (0, 0))

    # Triangle rendering
    trinagle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i in range(M):
        vertices = [
                    (A * cos(phi[i]), A * sin(phi[i])),
                    (B * cos(phi[i] + pi / 2), B * sin(phi[i] + pi / 2)),
                    (B * cos(phi[i] - pi / 2), B * sin(phi[i] - pi / 2)),
                   ]
        polygon(trinagle_surface, (*SPECIAL, t2[i]), [(x2[i] + dx, y2[i] + dy) for dx, dy in vertices])
    screen.blit(trinagle_surface, (0, 0))

    # Score rendering
    textsurface = score_font.render(f"Score := {score}", True, BLACK)
    screen.blit(textsurface, (30, 10))

    # Display update
    pygame.display.update()
    screen.fill(WHITE)

pygame.quit()