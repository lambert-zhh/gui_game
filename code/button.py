import pygame

from settings import *

# 按钮类
class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen, is_active=True):
        mouse_pos = pygame.mouse.get_pos()
        if is_active:
            if self.rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, self.rect)
            else:
                pygame.draw.rect(screen, BUTTON_COLOR, self.rect)
        else:
            pygame.draw.rect(screen, BUTTON_DISABLE_COLOR, self.rect)

        text_surface = self.font.render(self.text, True, 'black')
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)