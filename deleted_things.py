import pygame
class Deleted_thing(pygame.sprite.Sprite):  # класс вещей/предметов. 10 шт, которые надо сбить мячиками
    def __init__(self, x, y, surf, angle = 0):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = surf
        self.original_surf = surf
        self.rect = self.image.get_rect(center=(x, y))

        self.angle = angle
        self.decrease = 0.6  
        self.speed = 0
        
    def update(self,settings):  # обновление /изменяем св-ва класса за его пределами
        self.speed += 1
        self.angle += self.speed

        if self.angle <=360:  # один оборот просто вращение
            self.image = pygame.transform.rotate(self.original_surf, self.angle)

        elif self.angle <=2000 and min(self.rect.w, self.rect.h)>=3: # вращение и уменьшение изображения
            new_w, new_h = round(self.rect.w * self.decrease), round(self.rect.h * self.decrease)
            self.image = pygame.transform.scale(self.original_surf, (new_w, new_h))
            self.image = pygame.transform.rotate(self.image, self.angle)
        else:
            self.kill()
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
     
    