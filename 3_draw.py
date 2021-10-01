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