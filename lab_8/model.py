from math import cos, sin, pi, atan2
import pygame
from pygame.draw import *
from locals import Color
"""
Implement game objects

Classes:

    Spaceship

Functions:

    draw_polygon()

Variables:

"""

def draw_polygon(screen, color, x, y, vertices_r, vertices_phi):
    """ Draw polygon with vertices given in polar coordinates
    :param screen: pygame.Surface to draw polygon on
    :param color: (R, G, B) color of polygon fill
    :param x: X coordinate of polygon's center
    :param y: Y coordinate of polygon's center
    :param vertices_r: List of R coordinates of veritces
    :param vertices_phi: List of phi coordinates of vertices 
    """
    vertices = [(r * cos(phi), r * sin(phi)) for r, phi in zip(vertices_r, vertices_phi)]
    
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
        :param pos: List (x, y) of the initial coordinates
        """
        self.x, self.y = pos
        self.phi = 0
        self.v_x, self.v_y = 0, 0
        self.length = 60
        self.half_width = 25

    def move(self):
        """ Calculates new coordinates and orientation """
        self.x += self.v_x
        self.y += self.v_y

        # Slows spaceship, so without acceleration it will stop
        self.v_x *= 0.9
        self.v_y *= 0.9

        # Turns spaceship towards mouse coursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.phi = atan2(mouse_y - self.y, mouse_x -self.x)

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
        vertices_phi = [self.phi, self.phi + pi / 2, self.phi - pi / 2]

        draw_polygon(screen, Color.DEEP_BLUE, self.x, self.y, vertices_r, vertices_phi)

