from math import cos, sin, pi, atan2
import pygame
from pygame.draw import *
from random import randint

from locals import *
from model import Spaceship, Meteorite
from button import Button

class GameManager:
    """ Controls all game elements:
        * Handles user input 
        * Progresses model and animation state
        * Renders screen
    """

    def __init__(self):
        self.spaceship = Spaceship(pos = (WIDTH / 2, HEIGHT / 2))
        self.meteorites = [Meteorite(x_range = (0, WIDTH), y_range = (0, 0)) for _ in range (2)]

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
        for meteorite in self.meteorites:
            meteorite.render(screen)
        return screen

    def progress(self):
        """ Calculates new model and animation states """
        self.spaceship.move()
        self.spaceship.handle_keys()
        for meteorite in self.meteorites:
            meteorite.move()
        if randint(0, 10) == 0:
            self.meteorites.append(Meteorite(x_range = (0, WIDTH), y_range = (0, 0)))

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
