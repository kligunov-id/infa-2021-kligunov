import pygame
from pygame.draw import *

# Инициализация библиотеки:
pygame.init()

FPS = 30
W = 1200
H = 800
screen = pygame.display.set_mode((W, H))
screen.fill((255, 255, 255))

# Цвета
SKY = (128, 255, 234)
WHITE = (255, 255, 255)
GRASS = (34, 204, 0)
LEAVES = (13, 77, 0)
BLACK = (0, 0, 0)
PINK = (255,51,51)
BROWN = (77, 38, 0)
GLASS = (0, 153, 153)

def background():
    polygon(screen, SKY, [
         (0, 0),
         (W, 0),
         (W, H / 2),
         (0, H / 2)])
    polygon(screen, GRASS, [
         (0, H / 2),
         (W, H / 2),
         (W, H),
         (0, W)])

def tree(x, y, radius = 30, scale = 1):
    """Рисует 5 кругов с центром в (x, y) со смещениями DELTA_X и DELTA_Y и палку в точке (x, y)"""
    polygon(screen, BLACK, [
         (x - radius * scale / 5, y),
         (x + radius * scale / 5, y),
         (x + radius * scale / 5, y + radius * scale * 3),
         (x - radius * scale / 5, y + radius * scale * 3)])

    DELTA_Y = [-100, -70, -70, -40, -20, -20]
    DELTA_X = [0, -30, 30, 0, 30, -30]
    for dx, dy in zip(DELTA_X, DELTA_Y):
        circle(screen, LEAVES, (x + dx * scale, y + dy * scale), radius * scale)
        circle(screen, BLACK, (x + dx * scale, y + dy * scale), radius * scale, width = 1) #Окантовка

def house(x, y, w = 300, h = 100, scale = 1):
        pass

def cloud(x, y, radius = 30, scale = 1):
    """Рисует 5 кругов с центром в (x, y) со смещениями DELTA_X и DELTA_Y"""
    DELTA_X = [-30, -10, 10, 30, -10, 10]
    DELTA_Y = [15, 15, 15, 15, -15, -15]
    for dx, dy in zip(DELTA_X, DELTA_Y):
        circle(screen, WHITE, (x + dx * scale, y + dy * scale), radius * scale)
        circle(screen, BLACK, (x + dx * scale, y + dy * scale), radius * scale, width = 1) #Окантовка


def sun(x, y, radius = 40, scale = 1):
    circle(screen, GLASS, (x, y), radius * scale)

def picture():
    """Собирает всю картинку"""
    background()
    sun(50, 50)
    cloud(200, 80, scale = 1)
    cloud(600, 110, scale = 0.8)
    cloud(1000, 90, scale = 1.2)
    tree(500, 500, scale = 1.2)
    tree(1000, 400)

picture()

# Обновление экрана
pygame.display.update()
clock = pygame.time.Clock()
finished = False

# Цикл обработки событий
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()