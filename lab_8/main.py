from math import cos, sin, pi, atan2
import pygame
from pygame.draw import *

from locals import FPS, WIDTH, HEIGHT, Color


class Spaceship:
    """ Represents a movable, controllable and drawable spaceship """ 

    def __init__(self, pos=(WIDTH / 2, HEIGHT / 2)):
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
        
        vertices = [(r * cos(phi), r * sin(phi)) for r, phi in zip(vertices_r, vertices_phi)]
        
        polygon(screen,
            Color.DEEP_BLUE,
            [(self.x + dx, self.y + dy) for dx, dy in vertices])

class GameManager:
    """ Controls all game elements:
        * Handles user input 
        * Progresses model and animation state
        * Renders screen
    """

    def __init__(self):
        self.spaceship = Spaceship()

    def handle(self, event: pygame.event.Event):
        """ Handles all user input events
        :param event: pygame.event.Event to be handled
        ..warning:: Spaceship acceleration is handled without events
        """
        pass

    def render(self):
        """ Composes all visible objects
        :returns: pygame.Surface with the result
        """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.spaceship.render(screen)
        return screen

    def progress(self):
        """ Calculates new model and animation states """
        self.spaceship.move()
        self.spaceship.handle_keys()


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    game = GameManager()
    clock = pygame.time.Clock()
    finished = False

    # Main cycle
    while not finished:
        clock.tick(FPS)
        # Handles events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            else:
                game.handle(event)

        game.progress()

        # Renders game
        screen.blit(game.render(), (0, 0))

        # Updates screen
        pygame.display.update()
        screen.fill(Color.BLACK)
    pygame.quit()

if __name__ == '__main__':
    main()
