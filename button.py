import pygame
import pygame.font

class Button():
    def __init__(self, sc, rect, text, text_color, border_color, text_size, border_size = 2):
        self.sc = sc
        self.rect = pygame.Rect(rect)
        self.text = text
        self.text_color = text_color
        self.border_color = border_color
        self.text_size = text_size
        self.border_size = border_size

    def draw(self):
        pygame.draw.rect(self.sc, self.border_color, self.rect, self.border_size)
        font = pygame.font.Font(None, self.text_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        self.sc.blit(text_surface, text_rect)
       
    def isOver(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:    
            return False

