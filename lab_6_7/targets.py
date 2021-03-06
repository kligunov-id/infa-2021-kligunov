import pygame
from pygame.draw import *
from random import randint, random
from math import pi, cos, sin

FPS = 60
WIDTH, HEIGHT = 1200, 900
MARGIN = 100

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
    MIN_R = 30
    MAX_R = 100
    DIFFICULTY_SCORE_FACTOR = 1

    # Collison types
    COLLISION_NEGATIVE = -1 # Ball's too far to the left/top
    COLLISION_NONE     = 0  # Ball's inside the walls
    COLLISION_POSITIVE = 1  # Ball's too far to the right/bottom

    def __init__(self):
        """ Randomly choses position (x, y), velocity (v_x, v_y), color and life counter t """
        self.reset()
    
    def reset(self):
        """ Randomly choses position (x, y), velocity (v_x, v_y), color and life counter t """
        self.x = randint(MARGIN, WIDTH - MARGIN)
        self.y = randint(MARGIN, HEIGHT - MARGIN)
        self.r = randint(Ball.MIN_R, Ball.MAX_R)
        self.t = randint(150, 250)
        self.color = COLORS[randint(0, 5)]
        self.v_x = randint(-Ball.MAX_V, Ball.MAX_V + 1)
        self.v_y = randint(-Ball.MAX_V, Ball.MAX_V + 1)

    def move(self):
        """ Calculates new position (x, y) """
        self.x += self.v_x
        self.y += self.v_y

    def reduce_life_clock(self):
        """ Reduces life clock
        When it reaches 0, target is considered to be dead
        """
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
        if x_type is Ball.COLLISION_NEGATIVE:
            self.v_x = randint(1, Ball.MAX_V + 1)
        elif x_type is Ball.COLLISION_POSITIVE:
            self.v_x = randint(-Ball.MAX_V, 0)

        self.v_y = randint(-Ball.MAX_V, Ball.MAX_V + 1)
        if y_type is Ball.COLLISION_NEGATIVE:
            self.v_y = randint(1, Ball.MAX_V + 1)
        elif y_type is Ball.COLLISION_POSITIVE:
            self.v_y = randint(-Ball.MAX_V, 0)

    def is_clicked(self, pos):
        """
        Checks if mouse click hit the ball

        :param pos: Mouse click position
        :returns: True if the ball was hit, False otherwise
        """
        return dist2(pos, (self.x, self.y)) <= self.r ** 2
    
    def get_score(self):
        """ Returns score awarded for a successful hit """
        return int((self.t / self.r) ** 0.5 * 4
            * Ball.DIFFICULTY_SCORE_FACTOR)
    
    def terminate(self):
        """ Marks the ball as dead """
        self.t = 0

    def is_dead(self):
        """ Returns True if the ball should be removed """
        return self.t <= 0
    
    def render(self, screen, transparency_factor = 1):
        """
        :param screen: PyGame screen to render ball on
        :param transparency_factor: Multiplies transparency by this
        """
        circle(screen,
            (*self.color, int(self.t * transparency_factor)),
            (self.x, self.y), self.r)


class Triangle:

    MOVING, TURNING_LEFT, TURNING_RIGHT = 'move', 'left', 'right'
    move_t, turn_t = 30, 10 # Average duration of movement states
    
    v_phi = 2 * pi / 60
    v = 5
    
    A, B = 60, 25 # Length and half width

    def __init__(self):
        """" Randomly chooses position and orientation for the ball """
        self.reset()

    def reset(self):
        """" Randomly chooses position and orientation for the ball """
        self.x = randint(MARGIN, WIDTH - MARGIN)
        self.y = randint(MARGIN, HEIGHT - MARGIN)
        self.t = 255
        self.phi = random() * 2 * pi
        self.state = Triangle.MOVING

    def move(self):
        """ Calculates new position (x, y), movement phase state and orientaion phi """
        if self.state is Triangle.MOVING:
            self.x += Triangle.v * cos(self.phi)
            self.y += Triangle.v * sin(self.phi)
            if randint(0, Triangle.move_t) == 0:
                self.state = Triangle.TURNING_LEFT if randint(0, 2) else Triangle.TURNING_RIGHT
        elif self.state is Triangle.TURNING_LEFT:
            self.phi += Triangle.v_phi
            if randint(0, Triangle.turn_t) == 0:
                self.state = Triangle.MOVING
        else:
            self.phi -= Triangle.v_phi
            if randint(0, Triangle.turn_t) == 0:
                self.state = Triangle.MOVING

    def reduce_life_clock(self):
        """ Reduces life clock
        When it reaches 0, target is considered to be dead
        """
        self.t -= randint(0, 3)
    
    def is_dead(self):
        """ Returns True if the ball should be removed """
        return self.t <= 0

    def terminate(self):
        """ Marks the ball as dead """
        self.t = 0

    def check_collision(self):
        """ Return True if triangle (almost) hit the wall """
        return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT

    def is_clicked(self, pos):
        """
        Checks if mouse click hit the ball

        :param pos: Mouse click position
        :returns: True if the ball was hit, False otherwise
        """
        click_x, click_y = pos
        click_x -= self.x
        click_y -= self.y
        """ Get vector in canonical basis
        (x axis towards vertice, y alongside shortest side)
        by rotation by -phi
        """
        click_x = cos(self.phi) * click_x + sin(self.phi) * click_y
        click_y = -sin(self.phi) * click_x + sin(self.phi) * click_y
        # Triangle is an intersection of x > 0, x + y > 0 and x - y > 0
        return click_x > 0 and click_x / Triangle.A + click_y / Triangle.B <= 1 and click_x / Triangle.A - click_y / Triangle.B <= 1
    
    def get_score(self):
        """ Returns score awarded for a successful hit """
        return randint(5, 25)
    
    def get_color(self, transparency_factor = 1):
        """
        :param transparency_factor: Multiplies transparency by this
        :returns: (R, G, B, A) color of triangle
        """
        transparency = max(0, self.t * transparency_factor)
        return (*SPECIAL, transparency)

    def render(self, screen, transparency_factor = 1):
        """
        :param screen: PyGame screen to render ball on
        :param transparency_factor: Multiplies transparency by this
        """
        vertices_r = [Triangle.A, Triangle.B, Triangle.B]
        vertices_phi = [self.phi, self.phi + pi / 2, self.phi - pi / 2]

        vertices = [(r * cos(phi), r * sin(phi)) for r, phi in zip(vertices_r, vertices_phi)]
        
        polygon(screen,
            self.get_color(transparency_factor),
            [(self.x + dx, self.y + dy) for dx, dy in vertices])
