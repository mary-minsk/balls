import pygame

class Deleted_thing(pygame.sprite.Sprite):  # закручивающиеся n предметов на игровой поверхности или 3 шара в момент удаления
    def __init__(self, center, surf, angle = 0, score = 0, is_ball = False):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = center
        self.image = surf
        self.original_surf = surf
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.angle = angle
        self.decrease = 0.6  
        self.speed = 0
        self.score = score
        self.is_ball = is_ball

    def update(self, sc, settings):  # обновление /изменяем св-ва класса за его пределами

        self.speed += 1
        self.angle += self.speed

        if self.angle <=360:  # один оборот просто вращение
            self.image = pygame.transform.rotate(self.original_surf, self.angle)
            self.show_speed(self, settings, sc)

        elif self.angle <=2000 and min(self.rect.w, self.rect.h)>=3: # вращение и уменьшение изображения
            new_w, new_h = round(self.rect.w * self.decrease), round(self.rect.h * self.decrease)
            self.image = pygame.transform.scale(self.original_surf, (new_w, new_h))
            self.image = pygame.transform.rotate(self.image, self.angle)
        else:
            # if self.is_ball:
            #     settings.is_early_completion = True
            #     settings.attempts -= 1  # Минус одна из трех попыток
            #     print("settings.attempts = ", settings.attempts)
            self.kill()
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))

    @staticmethod
    def show_speed(self, settings, sc):
        
        if self.score != 0:
            # print(self.score)
            point = (self.x + 10, self.y - 20)
            self.y -= 1
            settings.show_text(sc, settings.white, 24, point, False, str(self.score))


     
    
