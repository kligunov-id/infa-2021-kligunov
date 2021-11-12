from math import cos, sin, pi, atan2
import pygame
from pygame.draw import *
from locals import Color
from random import randint, uniform

"""
Implement game objects

Classes:

    Spaceship
    Meteorite
    Laser

Functions:

    draw_polygon()

Variables:

"""

def draw_polygon(screen, color, x, y, vertices_r, vertices_phi, phi_0=0):
    """ Draw polygon with vertices given in polar coordinates
    :param screen: pygame.Surface to draw polygon on
    :param color: (R, G, B) color of polygon fill
    :param x: X coordinate of polygon's center
    :param y: Y coordinate of polygon's center
    :param vertices_r: List of R coordinates of veritces
    :param vertices_phi: List of phi coordinates of vertices
    :param phi_0: (option) Angle of the rotation of the whole polygon
    """
    vertices = [(r * cos(phi + phi_0), r * sin(phi + phi_0)) for r, phi in zip(vertices_r, vertices_phi)]
    
    polygon(screen,
            color,
            [(x + dx, y + dy) for dx, dy in vertices])

class Spaceship:
    """ Represents a movable, controllable and drawable spaceship """ 

    def __init__(self, pos=(0, 0)):
        """ Initializes spaceship parameters:
            * Position (x, y)
            * Orientaion phi
            * Velocity (v_x, v_y)
            * Shape of a starship (length, half_width)
            * Blaster percentage charge
            * Blaster status is_charging
        :param pos: List (x, y) of the initial coordinates
        """
        self.x, self.y = pos
        self.phi = 0
        self.v_x, self.v_y = 0, 0
        self.length = 60
        self.half_width = 25
        self.is_charging = False
        self.charge = 0

    def move(self):
        """ Calculates new coordinates and orientation, also charges blaster """
        self.x += self.v_x
        self.y += self.v_y

        # Apply gravity
        self.v_y += 0.4

        # Slows spaceship, so without acceleration it will stop
        self.v_x *= 0.9
        self.v_y *= 0.9

        # Turns spaceship towards mouse coursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.phi = atan2(mouse_y - self.y, mouse_x -self.x)

        if self.is_charging:
            self.charge += 2
            self.charge = min(100, self.charge)
    
    def start_charging(self):
        """ Starts blaster charging """
        self.is_charging = True

    def fire(self):
        """ Stops charging and fires a laser
        :returns: Laser object
        """
        self.is_charging = False
        if self.charge > 5:
            charge = self.charge
            self.charge = 0
            return Laser((self.x + self.length * cos(self.phi), self.y + self.length * sin(self.phi)), self.phi, charge)
        else:
            return None

    def handle_keys(self):
        """ Listens for WASD keys and accelerates starship """
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.v_y -= 1
        if pressed[pygame.K_s]:
            self.v_y += 1
        if pressed[pygame.K_a]:
            self.v_x -= 1
        if pressed[pygame.K_d]:
            self.v_x += 1

    def render(self, screen: pygame.Surface):
        """ Draws starship on the given surface
        :param screen: pygame.Surface to draw the spaceship on 
        """
        vertices_r = [self.length, self.half_width, self.half_width]
        vertices_phi = [0, pi / 2, -pi / 2]

        draw_polygon(screen, Color.DEEP_BLUE, self.x, self.y, vertices_r, vertices_phi, self.phi)

    def is_outside_field(self, screen_size):
        """ Checks if the starship is outside the game screen
        :param screen_size: List (width, height)
        :returns: True if spaceship is outside, False otherwise
        """
        width, height = screen_size
        return (self.x < 0 or width < self.x
            or self.y < 0 or height < self.y)

    def is_inside(self, point):
        """ Checks if a given point is inside the starship
        :param point: List (x, y) of point coordinates
        :returns: True if the point is inside, False otherwise
        """        
        x, y = point
        x -= self.x
        y -= self.y
        """ Get vector in canonical basis
        (x axis towards farthest vertice, y alongside shortest side)
        by rotation by -phi
        """
        x, y = cos(self.phi) * x + sin(self.phi) * y, -sin(self.phi) * x + cos(self.phi) * y

        # Scales
        x /= self.length
        y /= self.half_width

        # Triangle is an intersection of x > 0, x + y < 1 and x - y < 1
        return x >= 0 and x + y <= 1 and x - y <= 1

    def is_colliding(self, meteorite):
        """ Checks if the starship is touching a meteorite
        :param meteorite: Meteorite object to check collisions with
        :returns: True if spaceship is colliding, False otherwise
        """
        vertices = [(r * cos(phi + meteorite.phi) + meteorite.x,
            r * sin(phi + meteorite.phi) + meteorite.y) for r, phi in zip(meteorite.vert_r, meteorite.vert_phi)]
        for v in vertices:
            if self.is_inside(v):
                return True
        return False

class Meteorite:
    """ Represents meteorite which can be moved and rendered """
    MAX_V = 5
    MAX_V_PHI = 2 * pi / 30 * 0.5

    RGB_RANGE = (30, 60)

    R, D_R = 20, 3

    N, D_N = 15, 5

    def __init__(self, x_range, y_range):
        """ Initializes randomly metiorite parameters:
            * Position (x, y)
            * Velocity (v_x, v_y)
            * Orientation phi
            * Angular velocity v_phiif self.charge > 5:
            self.charge = 
            * Shape (Lists of vertices coordinates vert_r and vert_phi)
            * Color 
        :param x_range: List (x_min, x_max) of acceptable coordinates for the spawn
        :param y_range: List (y_min, y_max) of acceptable coordinates for the spawn  
        """
        self.x, self.y = randint(*x_range), randint(*y_range)
        self.v_x, self.v_y = uniform(-Meteorite.MAX_V, Meteorite.MAX_V), uniform(0, Meteorite.MAX_V)

        self.phi = 0
        self.v_phi = uniform(-Meteorite.MAX_V_PHI, Meteorite.MAX_V_PHI)

        self.color = ([randint(*Meteorite.RGB_RANGE) for _ in range(3)])
        self.n = randint(Meteorite.N - Meteorite.D_N, Meteorite.N + Meteorite.D_N)
        self.vert_phi = [2 * pi / self.n * i for i in range(self.n)]
        self.vert_r = [randint(Meteorite.R - Meteorite.D_R, Meteorite.R + Meteorite.D_R) for _ in range(self.n)]
        
        self.alive = True

    def move(self):
        """ Calculates new coordinates and orientation """
        self.x += self.v_x
        self.y += self.v_y
        self.phi += self.v_phi

        # Apply gravity
        self.v_y += 0.1

    def render(self, screen: pygame.Surface):
        """ Draws meteorite on the given surface
        :param screen: pygame.Surface to draw the meteorite on 
        """
        draw_polygon(screen, self.color, self.x, self.y, self.vert_r, self.vert_phi, self.phi)

class Laser:
    """ Represents laser impulses which destroy meteorites on impact """
    R = 5
    def __init__(self, pos, phi, charge):
        """ Initializes Laser parameters:
            * Position (x, y)
            * Velocity (v_x, v_y)
            * Color 
        :param pos: List (x, y) of coordinates of a center
        :param phi: Orientation angle
        :param charge: Charge percentage [0, 100] of the blaster
        """
        self.x, self.y = pos
        v = charge / 3
        self.v_x, self.v_y = v * cos(phi), v * sin(phi)

        self.color = Color.CITRINE
        self.alive = True

    def move(self):
        """ Calculates new coordinates and orientation """
        self.x += self.v_x
        self.y += self.v_y

        # Apply gravity
        self.v_y += 0.25

    def render(self, screen: pygame.Surface):
        """ Draws laser on the given surface
        :param screen: pygame.Surface to draw the laser on 
        """
        circle(screen, self.color, (self.x, self.y), Laser.R)
    
    def is_hitting(self, meteorite):
        """ Checks if the laser is touching meteorite
        :param meteorite: Meteorite to check collision with
        :returns: True if is hitting, False otherwise
        """
        pass