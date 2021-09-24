import pygame
from pygame.draw import *

# Инициализация библиотеки:
pygame.init()

# Создание окна:
screen = pygame.display.set_mode((300, 200))

# здесь будут рисоваться фигуры
# ...

# Обновление экрана
pygame.display.update()


# Цикл отслеживания событий
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
        	#Выход из программы
            pygame.quit()
