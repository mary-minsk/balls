import pygame
class Thing(pygame.sprite.Sprite):  # класс вещей/предметов. 10 шт, которые надо сбить мячиками
    def __init__(self, x, y, surf):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = int(self.rect.width * .87 / 2)
        
        self.x = x
        self.y = y 
        # pygame.draw.circle(self.image, settings.red, (x, y), self.radius, 1)

    def update(self,sc, settings, things):  # обновление /изменяем св-ва класса за его пределами
        pass
        # self.rect = self.rect
        pygame.draw.circle(sc, settings.red, self.rect.center, self.radius, 1)
        pygame.draw.rect(sc, settings.bg_color, self.rect, 1)