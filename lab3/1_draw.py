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

DELTA_X = 40  # Зрачки на DELTA_Y пикселей левее/правее вертикали
DELTA_Y = -25 # Зрачки на DELTA_Y пикслелей выше центра

RADIUS_SMILE = 100
RADIUS_P = 12

X = [0, DELTA_X, - DELTA_X]
Y = [0, DELTA_Y, DELTA_Y]
RADIUS = [RADIUS_SMILE, RADIUS_P, RADIUS_P]
COLOR = [YELLOW, BLACK, BLACK]

for x, y, color, r in zip(X, Y, COLOR, RADIUS):
    circle(screen, color, (x + CENTER_X, y + CENTER_Y), r)


#circle(screen, YELLOW, CENTER, RADIUS)
#circle(screen, BLACK, LEFT_EYE, PUPIL_R)
#circle(screen, BLACK, RIGHT_EYE, PUPIL_R)

#rect(screen, (255, 0, 255), (100, 100, 200, 200))
#polygon(screen, (255, 255, 0), [(100,100), (200,50),
#circle(screen, (0, 255, 0), (200, 175), 50)

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