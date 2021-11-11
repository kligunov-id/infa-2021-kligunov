from math import cos, sin, pi, atan2
import pygame
from pygame.draw import *

from locals import FPS, WIDTH, HEIGHT, Color
from model import Spaceship

class GameManager:
    """ Controls all game elements:
        * Handles user input 
        * Progresses model and animation state
        * Renders screen
    """

    def __init__(self):
        self.spaceship = Spaceship(pos = (WIDTH / 2, HEIGHT / 2))

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
