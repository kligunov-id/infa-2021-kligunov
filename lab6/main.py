import pygame
from pygame.draw import *
from random import randint, random
from math import pi, cos, sin
from button import *
from targets import Ball, Triangle

FPS = 60
WIDTH, HEIGHT = 1200, 900
MARGIN = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT_NAME = "JetBrains Mono"

class GameSession:

    N, M = 5, 2
    T = 2 * FPS
    
    def __init__(self):
        self.balls = [Ball() for _ in range(GameSession.N)]
        self.triangles = [Triangle() for _ in range(GameSession.M)]
        self.score = 0
        self.time = self.T
        self.font = pygame.font.SysFont(FONT_NAME,  30)

    def handle_click(self, pos):
        """
        Handles mouse clicks events
        Clicked targets should disapper

        :param pos: Position (x, y) of mouse click
        """
        hit = 0
        for target in self.balls + self.triangles:
            if target.is_clicked(pos):
                self.score += target.get_score()
                target.terminate()
                hit += 1

        # Punishing for misses
        if not hit:
            self.score -= 3
            self.score = max(self.score, 0)

    def progress(self):
        """ Moves targets, handles colissions and creates new targets """
        self.time -= 1

        for target in self.balls + self.triangles:
            target.move()
        
        for ball in self.balls:
            collision_type = ball.check_collision()
            if collision_type != (Ball.COLLISION_NONE, Ball.COLLISION_NONE):
                ball.generate_velocity(*collision_type)
        for triangle in self.triangles:
            if triangle.check_collision():
                triangle.terminate()

        for target in self.balls + self.triangles:
            target.reduce_life_clock()
            if target.is_dead():
                target.reset()

    def render(self, screen, render_text=True, transparency_factor=1):
        """ Renders all targets, the score and the timer
        :param screen: PyGame screen to render on
        :param render_text: True if requested to render score and timer
        :pararm transparency_factor: Multiplies transparency
        """       
        for target in self.balls + self.triangles:
            target.render(screen, transparency_factor)

        if render_text:
            score_surface = self.font.render(f"Score := {self.score}", True, BLACK)
            timer_surface = self.font.render(f"Time left := {self.time // FPS}", True, BLACK)
            screen.blit(score_surface, (30, 10))
            screen.blit(timer_surface, (30, 50))

    def is_finished(self):
        return self.time <= 0


class Game:

    __instance = None

    STATE_PLAYING = "play"
    STATE_FINISHED = "finished"
    FINISHED_GAME_TRANSPARENCY = 0.15

    @staticmethod
    def get_instance():
        return Game.__instance

    def __init__(self):
        Game.__instance = self
        self.state = Game.STATE_PLAYING
        self.game_session = GameSession()
        self.game_over_screen = GameOverScreen()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state is Game.STATE_PLAYING:
                self.game_session.handle_click(event.pos)
            if self.state is Game.STATE_FINISHED:
                self.game_over_screen.handle_click(event.pos)

    def progress(self):
        self.game_session.progress()
        if self.game_session.is_finished():
            self.set_state(Game.STATE_FINISHED)
            self.game_over_screen.progress()

    def render(self):
        """
        :returns: PyGame screen
        """
        screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        if self.state is Game.STATE_PLAYING:
            self.game_session.render(screen)
        elif self.state is Game.STATE_FINISHED:
            self.game_session.render(screen, False, Game.FINISHED_GAME_TRANSPARENCY)
            self.game_over_screen.render(screen)
        return screen

    def set_state(self, new_state):
        if new_state is self.state:
            return
        self.state = new_state
        if new_state is Game.STATE_PLAYING:
            self.game_session = GameSession()
    
    def get_score(self):
        return self.game_session.score


class GameOverScreen:
    
    FONTSIZE = 50

    def __init__(self):
        self.font = pygame.font.SysFont(FONT_NAME,  GameOverScreen.FONTSIZE)
        self.restart_button = Button("Play again", (WIDTH / 2, HEIGHT * 0.3)) 

    def render(self, screen: pygame.Surface):
        text_surface_1 = self.font.render(f"Game Over", True, BLACK)
        text_rect_1 = text_surface_1.get_rect(center = (WIDTH // 2, int(HEIGHT * 0.07)))
        screen.blit(text_surface_1, text_rect_1)
        
        text_surface_2 = self.font.render(f"Your score is {Game.get_instance().get_score()}", True, BLACK)
        text_rect_2 = text_surface_2.get_rect(center = (WIDTH // 2, int(HEIGHT * 0.15)))
        screen.blit(text_surface_2, text_rect_2)

        self.restart_button.render(screen)
    
    def handle_click(self, pos):
        """
        Handles mouse clicks events
        Restarts game when restart button is clicked

        :param pos: Position (x, y) of mouse click
        """
        if self.restart_button.is_mouse_on(pos):
            Game.get_instance().set_state(Game.STATE_PLAYING)
    
    def progress(self):
        self.restart_button.progress()


def main():
    # Initialize PyGame, clock and GameSession
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
            else :
                game.handle_event(event)

        game.progress()
        
        # Renders game
        screen.blit(game.render(), (0, 0))

        # Updates screen
        pygame.display.update()
        screen.fill(WHITE)
    pygame.quit()


main()