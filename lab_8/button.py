import pygame
from locals import FONT_NAME

class Button:

    FONTSIZE_SMALL = 60
    FONTSIZE_BIG = 70
    ANIMATION_SPEED = 0.8
    FONT_NAME = FONT_NAME
    COLOR = (255, 255, 255)

    def __init__(self, text, center):
        """ Initializes new button
        :param text: Displayed button text
        :param center: List of coordinates (x, y) of the button text
        """
        self.center = center
        self.fontsize = Button.FONTSIZE_SMALL
        self.update_text(text)

    def render(self, screen: pygame.Surface):
        """ Blits button image onto given surface
        :param screen: pygame.Surface to render button on
        """
        screen.blit(self.text_surface, self.text_rect)
    
    def update_text(self, text=""):
        """ Redraws button with new fontsize and (optionaly) text
        :param text: New text
        """
        if text:
            self.text = text
        self.font = pygame.font.Font(Button.FONT_NAME, int(self.fontsize))
        self.text_surface = self.font.render(self.text, True, Button.COLOR)
        self.text_rect = self.text_surface.get_rect(center = self.center)

    def progress(self):
        """ Animates button """
        if self.is_mouse_on(pygame.mouse.get_pos()):
            self.fontsize += Button.ANIMATION_SPEED
        else:
            self.fontsize -= Button.ANIMATION_SPEED
        self.fontsize = max(Button.FONTSIZE_SMALL, self.fontsize)
        self.fontsize = min(Button.FONTSIZE_BIG, self.fontsize)
        self.update_text()

    def is_mouse_on(self, pos):
        """ Checks if mouse is hovering over the button
        :param pos: Mouse position (x, y)
        """
        x, y = pos
        return (self.text_rect.left <= x and x <= self.text_rect.right 
            and self.text_rect.top <= y and y <= self.text_rect.bottom)
