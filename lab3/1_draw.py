import pygame
from pygame.draw import *

# Инициализация библиотеки:
pygame.init()

FPS = 30
screen = pygame.display.set_mode((800, 800))
screen.fill((255, 255, 255))

# Цвета
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Отрисовка фигур
CENTER_X = 400
CENTER_Y = 400

DELTA_X = 70  # Зрачки на DELTA_Y пикселей левее/правее вертикали
DELTA_Y = -25 # Зрачки на DELTA_Y пикслелей выше центра

RADIUS_SMILE = 130
RADIUS_P = 12
RADIUS_EYE_SMALL = 24
RADIUS_EYE_BIG = 29

MOUTH_HALF_WIDTH = 70
MOUTH_HALF_D = 15
MOUTH_X, MOUTH_Y = 0 + CENTER_X, 80 + CENTER_Y 

# Смайлик, зрачки и глаза именно в таком порядке
X =      [0,            DELTA_X,          -DELTA_X,       DELTA_X,  -DELTA_X] 
Y =      [0,            DELTA_Y,          DELTA_Y,        DELTA_Y,  DELTA_Y]
RADIUS = [RADIUS_SMILE, RADIUS_EYE_SMALL, RADIUS_EYE_BIG, RADIUS_P, RADIUS_P]
COLOR =  [YELLOW,       RED,              RED,            BLACK,    BLACK]

for x, y, color, r in zip(X, Y, COLOR, RADIUS):
    circle(screen, color, (x + CENTER_X, y + CENTER_Y), r)
    circle(screen, BLACK, (x + CENTER_X, y + CENTER_Y), r, 1) # Окантовка

# Прямоугольник-рот
# TODO: циклик по всем прямоугольникам

polygon(screen, BLACK, [
    (MOUTH_X - MOUTH_HALF_WIDTH, MOUTH_Y - MOUTH_HALF_D),
    (MOUTH_X - MOUTH_HALF_WIDTH, MOUTH_Y + MOUTH_HALF_D),
    (MOUTH_X + MOUTH_HALF_WIDTH, MOUTH_Y + MOUTH_HALF_D),
    (MOUTH_X + MOUTH_HALF_WIDTH, MOUTH_Y - MOUTH_HALF_D)])


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