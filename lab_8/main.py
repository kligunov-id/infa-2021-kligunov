from abc import ABC, abstractmethod
from math import cos, sin, pi, atan2, log
import pygame
from pygame.draw import *
from random import randint, uniform

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
        self.meteorites = []
        self.score = 0
        self.lasers = []

    def handle(self, event: pygame.event.Event):
        """ Handles all user input events
        :param event: pygame.event.Event to be handled
        ..warning:: Spaceship acceleration is handled without events
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.spaceship.start_charging()
        elif event.type == pygame.MOUSEBUTTONUP:
            new_laser = self.spaceship.fire()
            if new_laser is not None:
                self.lasers.append(new_laser)

    def render(self):
        """ Draws background, spaceships, meteoritesand, the score and the charge bar
        :returns: pygame.Surface with the result
        """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.spaceship.render(screen)
        for meteorite in self.meteorites:
            meteorite.render(screen)

        for laser in self.lasers:
            laser.render(screen)

        text_surface = self.font.render(f"Your score: {int(self.score)}", True, Color.WHITE)
        text_rect = text_surface.get_rect(topright = (WIDTH * 0.98, int(HEIGHT * 0.02)))
        screen.blit(text_surface, text_rect)

        text_surface = self.font.render(f"Blaster charge: {self.spaceship.charge}%", True, Color.WHITE)
        text_rect = text_surface.get_rect(topleft = (WIDTH * 0.02, int(HEIGHT * 0.02)))
        screen.blit(text_surface, text_rect)

        return screen
    
    def manage_laser_destruction(self):
        """ Deletes meteorites and lasers which have collided """
        for laser in self.lasers:
            for meteorite in self.meteorites:
                if laser.is_hitting(meteorite):
                    laser.alive = False
                    meteorite.alive = False
        prev_num = len(self.meteorites)
        self.meteorites[:] = [m for m in self.meteorites if m.alive]
        self.lasers[:] = [m for m in self.lasers if m.alive]
        new_num = len(self.meteorites)
        self.score += new_num - prev_num

    def progress(self):
        """ Calculates new model and animation states """
        self.score += .1
        self.spaceship.move()
        self.spaceship.handle_keys()
        for meteorite in self.meteorites:
            meteorite.move()
        new_meteorite_number = int(uniform(0, log(30 + self.score) / log(30)))
        for _ in range(new_meteorite_number):
            self.meteorites.append(Meteorite(x_range = (0, WIDTH), y_range = (0, 0)))

        for laser in self.lasers:
            laser.move()

        for meteorite in self.meteorites:
            if self.spaceship.is_colliding(meteorite):
                self.game.switch_to(GameOver("You have crashed into a meteorite", int(self.score)))

        if self.spaceship.is_outside_field((WIDTH, HEIGHT)):
            self.game.switch_to(GameOver("You have flown out of screen", int(self.score)))

        self.manage_laser_destruction()

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


class GameOver(GameState):
    """ Game state representing screen results """
    
    def __init__(self, death_message="", score=0):
        """ Initializes the exit button, the death cause message and the result """
        super().__init__()
        self.menu_button = Button("Back to menu", (WIDTH / 2, HEIGHT * 0.52))
        self.death_message = death_message
        self.score = score

    def render(self):
        """ Displays the death cause message, the result and  the exit button
        :returns: pygame.Surface with the result
        """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        text_surface = self.font.render(f"Game Over", True, Color.WHITE)
        text_rect = text_surface.get_rect(center = (WIDTH // 2, int(HEIGHT * 0.1)))
        screen.blit(text_surface, text_rect)
        
        text_surface = self.font.render(self.death_message, True, Color.WHITE)
        text_rect = text_surface.get_rect(center = (WIDTH // 2, int(HEIGHT * 0.2)))
        screen.blit(text_surface, text_rect)
        
        if self.score:
            text_surface = self.font.render(f"Your score is: {self.score}", True, Color.WHITE)
            text_rect = text_surface.get_rect(center = (WIDTH // 2, int(HEIGHT * 0.3)))
            screen.blit(text_surface, text_rect)

        self.menu_button.render(screen)

        return screen

    def progress(self):
        """ Calculates new animation states """
        self.menu_button.progress()

    def handle(self, event: pygame.event.Event):
        """ Handles button clicks
        :param event: pygame.event.Event to be handled
        """
        if event.type != pygame.MOUSEBUTTONDOWN:
            return
        if self.menu_button.is_mouse_on(event.pos):
            self.game.switch_to(GameMenu())


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
