from abc import ABC, abstractmethod
from math import cos, sin, pi, atan2
import pygame
from pygame.draw import *
from random import randint

from locals import *
from model import Spaceship, Meteorite
from button import Button

class GameState(ABC):
    """ Abstract class which derivatives are responsible for controlling all game elements:
        * Handling the user input 
        * Progression of the model and animation states
        * Rendering of the screen
    """
    def __init__(self):
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)

    @abstractmethod
    def render(self):
        """ Composes all visible objects
        :returns: pygame.Surface with the result
        """
        pass

    @abstractmethod
    def handle(self, event: pygame.event.Event):
        """ Handles all user input events
        :param event: pygame.event.Event to be handled
        """
        pass

    @abstractmethod
    def progress(self):
        """ Calculates new model and animation states """
        pass

class Game:
    """ Wrapper class which resposibility is to allow state switching """
    def __init__(self):
        """ Initializes the only memeber """
        self.switch_to(GameMenu())

    def switch_to(self, new_state):
        """ Changes game state
        :param new_state: New state, must be an instance of class derivated from GameState 
        """
        self.state = new_state
        self.state.game = self
        
        # Passes over function calls to state object
        self.render = self.state.render
        self.handle = self.state.handle
        self.progress = self.state.progress

class GameSession(GameState):
    """ Game state representing actual game """

    def __init__(self):
        """ Initializes all game elements """
        super().__init__()
        self.spaceship = Spaceship(pos = (WIDTH / 2, HEIGHT / 2))
        self.meteorites = [Meteorite(x_range = (0, WIDTH), y_range = (0, 0)) for _ in range (2)]

    def handle(self, event: pygame.event.Event):
        """ Handles all user input events
        :param event: pygame.event.Event to be handled
        ..warning:: Spaceship acceleration is handled without events
        """
        pass

    def render(self):
        """ Draws background, spaceships and meteorites
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

class GameMenu(GameState):
    """ Game state representing starting menu """
    
    def __init__(self):
        """ Initializes all buttons """
        super().__init__()
        self.start_button = Button("New Game", (WIDTH / 2, HEIGHT * 0.3))
        self.quit_button = Button("Quit", (WIDTH / 2, HEIGHT * 0.42))

        self.buttons = [self.start_button, self.quit_button]

    def render(self):
        """ Displays game title and buttons
        :returns: pygame.Surface with the result
        """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        text_surface = self.font.render(f"<Abstract_Name>", True, Color.WHITE)
        text_rect = text_surface.get_rect(center = (WIDTH // 2, int(HEIGHT * 0.07)))
        screen.blit(text_surface, text_rect)

        for button in self.buttons:
            button.render(screen)

        return screen

    def progress(self):
        """ Calculates new animation states """
        for button in self.buttons:
            button.progress()

    def handle(self, event: pygame.event.Event):
        """ Handles button clicks
        :param event: pygame.event.Event to be handled
        """
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if self.quit_button.is_mouse_on(event.pos):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif self.start_button.is_mouse_on(event.pos):
            self.game.switch_to(GameSession())

def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    game = Game()
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
