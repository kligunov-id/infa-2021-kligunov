import pygame
from pygame.draw import *

# Инициализация библиотеки:
pygame.init()

FPS = 30
W = 1200 #ширина картинки
H = 600 #высота картинки
screen = pygame.display.set_mode((W, H))
screen.fill((255, 255, 255))

#цвета
SKY = (128, 255, 234)
WHITE = (255, 255, 255)
GRASS = (34, 204, 0)
LEAVES = (13, 77, 0)
BLACK = (0, 0, 0)
PINK = (255,51,51)
BROWN = (77, 38, 0)
GLASS = (0, 153, 153)

def background():
    """Рисует фон в виде двух прямоугольников размером W*H/2"""
    #небо
    rect(screen, SKY, (0, 0, W, H/2))
    #трава
    rect(screen, GRASS, (0, H/2, W, H/2))

def tree(x, y, radius = 30, scale = 1):
    """Рисует 5 кругов с центром в (x, y) со смещениями DELTA_X и DELTA_Y и палку в точке (x, y). 
    Радиус окружности (radius) равен 30 по умолчанию. Если необходимо изменить масштаб, используется
    параметр scale (по умолчанию равен 1)."""
    #ствол
    rect(screen, BLACK, (x - radius * scale / 5, y, 2 * radius * scale / 5, 2 * radius * scale * 3))
    #крона
    DELTA_Y = [-100, -70, -70, -40, -20, -20]
    DELTA_X = [0, -30, 30, 0, 30, -30]
    for dx, dy in zip(DELTA_X, DELTA_Y):
        circle(screen, LEAVES, (x + dx * scale, y + dy * scale), radius * scale)
        #oкантовка
        circle(screen, BLACK, (x + dx * scale, y + dy * scale), radius * scale, width = 1) 

def house(x, y, w = 100, h = 75, scale = 1):
    """Рисует домик. На вход принимаются параметры x, y - координаты центра большого прямоугольника домика, w, h - 
    ширина и высота домика соответственно. По умолчанию x = y = w = 100, h = 75. Также доступен параметр scale - масштаб.
    По умолчанию равен 1."""
    #основа с окантовкой
    rect(screen, BROWN, (x - w * scale, y - h * scale, 2 * w * scale, 2 * h * scale))
    rect(screen, BLACK, (x - w * scale, y - h * scale, 2 * w * scale, 2 * h * scale), width = 1)
    #окно
    rect(screen, GLASS, (x - w * scale / 3, y - h * scale / 3, 2 * w * scale / 3, 2 * h * scale / 3))
    rect(screen, PINK, (x - w * scale, y - h * scale, 2 *w * scale, 2*h * scale), width = 1)
    #крыша с окантовкой
    polygon(screen, PINK, [
         (x - w * scale, y - h * scale),
         (x + w * scale, y - h * scale),
         (x, y - 2 * h * scale)])
    polygon(screen, BLACK, [
         (x - w * scale, y - h * scale),
         (x + w * scale, y - h * scale),
         (x, y - 2 * h * scale)], width = 1)

def cloud(x, y, radius = 30, scale = 1):
    """Рисует 5 кругов с центром в (x, y) со смещениями DELTA_X и DELTA_Y. Радиус окружности (radius) равен 30 по умолчанию. 
    Если необходимо изменить масштаб, используется параметр scale (по умолчанию равен 1)."""
    DELTA_X = [-30, -10, 10, 30, -10, 10]
    DELTA_Y = [15, 15, 15, 15, -15, -15]
    for dx, dy in zip(DELTA_X, DELTA_Y):
        circle(screen, WHITE, (x + dx * scale, y + dy * scale), radius * scale)
        #окантовка
        circle(screen, BLACK, (x + dx * scale, y + dy * scale), radius * scale, width = 1)


def sun(x, y, radius = 40, scale = 1):
    """Рисует солнце такого же цвета, как и окно домика. На вход принимаются параметры x, y - координаты центра солнца, radius - 
    радиус солнца (по умолчанию принят за 40), scale - параметр масштаба (по умолчанию 1)."""
    circle(screen, GLASS, (x, y), radius * scale)

def picture():
    """Собирает всю картинку"""
    background()
    sun(50, 50)
    cloud(200, 80, scale = 1.2)
    cloud(600, 110, scale = 1)
    cloud(1000, 90, scale = 1.4)
    tree(500, 500, scale = 1.2)
    tree(1000, 400)
    house(200, 600)
    house(700, 500, scale = 0.8)

picture()

#обновление экрана
pygame.display.update()
clock = pygame.time.Clock()
finished = False

#цикл обработки событий
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()