import pygame
import pygame.font

class Button():
    def __init__(self, button_pos, text = '', size=20):
        self.x = button_pos[0]
        self.y = button_pos[1]
        self.width = button_pos[2]
        self.height = button_pos[3]
        self.text = text
        self.size = size

    def draw(self, sc, settings):
        pygame.draw.rect(sc, settings.bg_color, (self.x,self.y, self.width, self.height),2)
        font = pygame.font.Font(None, self.size)
        text_surface = font.render(self.text, True, settings.white)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.x + self.width/2+ 2, self.y + text_rect.h/2+2)
        sc.blit(text_surface, text_rect)   
       
    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

