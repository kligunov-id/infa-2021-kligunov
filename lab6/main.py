import pygame
from pygame.draw import *
from random import randint, random
from math import pi, cos, sin
from button import *
from targets import Ball, Triangle
import json

FPS = 60
WIDTH, HEIGHT = 1200, 900
MARGIN = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT_NAME = "JetBrains Mono"

class Config:

    def __init__(self):
        self.data = json.load(open("config.json"))
        GameSession.N = self.data["GameSession"]["N"]
        GameSession.M = self.data["GameSession"]["M"]
        GameSession.T = self.data["GameSession"]["Session_Time"]

    def set_difficulty(self, difficulty):
        Ball.MAX_V = self.data["Ball"]["MAX_V"][difficulty]
        Ball.MIN_R = self.data["Ball"]["MIN_R"][difficulty]
        Ball.MAX_R = self.data["Ball"]["MAX_R"][difficulty]
        Ball.MAX_V = self.data["Ball"]["MAX_V"][difficulty]
        Ball.DIFFICULTY_SCORE_FACTOR = self.data["Ball"]["DIFFICULTY_SCORE_FACTOR"][difficulty]

        Triangle.DIFFICULTY_SCORE_FACTOR = self.data["Triangle"]["DIFFICULTY_SCORE_FACTOR"][difficulty]
        Triangle.v = self.data["Triangle"]["v"][difficulty]
        Triangle.v_phi = self.data["Triangle"]["v_phi"][difficulty]

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
    STATE_MENU = "menu"

    FINISHED_GAME_TRANSPARENCY = 0.15

    SOFTCORE = "Softcore"
    MEDIUMCORE = "Mediumcore"
    HARDCORE = "Hardcore"

    @staticmethod
    def get_instance():
        return Game.__instance

    def __init__(self):
        Game.__instance = self
        self.config = Config()
        self.state = Game.STATE_MENU
        self.game_session = GameSession()
        self.game_over_screen = GameOverScreen()
        self.menu = Menu() 

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state is Game.STATE_PLAYING:
                self.game_session.handle_click(event.pos)
            elif self.state is Game.STATE_FINISHED:
                self.game_over_screen.handle_click(event.pos)
            elif self.state is Game.STATE_MENU:
                self.menu.handle_click(event.pos)

    def progress(self):
        if self.state is Game.STATE_MENU:
            self.menu.progress()
        elif self.state is Game.STATE_PLAYING:
            self.game_session.progress()
        else:
            self.game_session.progress()
            self.game_over_screen.progress()
        
        if self.game_session.is_finished() and self.state is Game.STATE_PLAYING:
            self.set_state(Game.STATE_FINISHED)

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
        elif self.state is Game.STATE_MENU:
            self.menu.render(screen)
        return screen

    def set_state(self, new_state):
        if new_state is self.state:
            return
        self.state = new_state
        if new_state is Game.STATE_PLAYING:
            self.game_session = GameSession()

    def get_score(self):
        return self.game_session.score

    def set_difficulty(self, difficulty):
        self.config.set_difficulty(difficulty)

class GameOverScreen:
    
    FONTSIZE = 50

    def __init__(self):
        self.font = pygame.font.SysFont(FONT_NAME,  GameOverScreen.FONTSIZE)
        self.restart_button = Button("Back to menu", (WIDTH / 2, HEIGHT * 0.3)) 

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
            Game.get_instance().set_state(Game.STATE_MENU)
    
    def progress(self):
        self.restart_button.progress()


class Menu:

    FONTSIZE = 50
    DIFFICULTIES = [Game.SOFTCORE, Game.MEDIUMCORE, Game.HARDCORE]

    def __init__(self):
        self.font = pygame.font.SysFont(FONT_NAME,  GameOverScreen.FONTSIZE)
        
        self.start_button = Button("New Game", (WIDTH / 2, HEIGHT * 0.3))

        self.difficulty_i = 1
        self.difficulty_button = Button(Game.MEDIUMCORE, (WIDTH / 2, HEIGHT * 0.4))
        Game.get_instance().set_difficulty(Game.MEDIUMCORE)
        
        self.quit_button = Button("Quit", (WIDTH / 2, HEIGHT * 0.5))


    def render(self, screen: pygame.Surface):
        text_surface = self.font.render(f"<Abstract_Name>", True, BLACK)
        text_rect = text_surface.get_rect(center = (WIDTH // 2, int(HEIGHT * 0.07)))
        screen.blit(text_surface, text_rect)

        self.start_button.render(screen)
        self.difficulty_button.render(screen)
        self.quit_button.render(screen)

    def handle_click(self, pos):
        """
        Handles mouse clicks events
        Restarts game when restart button is clicked

        :param pos: Position (x, y) of mouse click
        """
        if self.start_button.is_mouse_on(pos):
            Game.get_instance().set_state(Game.STATE_PLAYING)
        elif self.difficulty_button.is_mouse_on(pos):
            self.difficulty_i = (self.difficulty_i + 1) % 3
            Game.get_instance().set_difficulty(Menu.DIFFICULTIES[self.difficulty_i])
            self.difficulty_button.update_text(Menu.DIFFICULTIES[self.difficulty_i])
        elif self.quit_button.is_mouse_on(pos):
            pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def progress(self):
        self.start_button.progress()
        self.difficulty_button.progress()
        self.quit_button.progress()

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
