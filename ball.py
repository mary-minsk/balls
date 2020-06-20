import pygame
from math import sqrt, hypot

# класс Мяч или Шар (при сталкновении с 10 предметами шар их лопает (уничтожает))
class Ball(pygame.sprite.Sprite):  # Всего 3 шара: маленький, средний и большой мяч (шар)
    def __init__(self, settings, x, surf):
        pygame.sprite.Sprite.__init__(self)
        
        self.x = x                      #координаты шара на панели шаров. 
                                        #Если шар не катится на поверхности, он возвращается вниз экрана к другим шарам
        self.y = settings.screen_height - settings.bottom_margin_center_ball
        self.balls_panel_x = x
        self.balls_panel_y = self.y
        self.prev_x = 0
        self.prev_y = 0

        self.image = surf
        self.original_surf = surf # для корректировки ценра вращения мяча (в прямоугольм контуре)
        self.rect = self.image.get_rect(center=(x, self.y))
        self.prev_rect_center = self.rect.center  # корректирование центра шара при вращении
        self.radius = int(self.rect.width * .87 / 2)  # радиус для определения границ столкновения с другими объектами
        
        self.isRolling = False # шар катится по поверхности
        self.isJump = False  # мяч подпрыгивает или не подпрыгивает на месте (на игровой поверхности)
        self.isDeleting = False
        self.decrease = 0.7
        
        self.x1 = 0   # координаты центра шара на игровой поверхности
        self.y1 = 0
        
        self.step = 1
        self.delta = 1
        self.delay = 1   # задержка при подпрыгивании мяча на месте
        self.is_rotated = False
        self.angle = 0  # текущий угол поворота мяча
        
        self.dx = 0  #  смещение по осям центра шара за один шаг
        self.dy = 0
        self.speed = 0 # скорость перемещения мяча по игровой поверхности
        
        self.is_new_point = False
        self.distance = 0
        self.current_distance = 0
        self.prev_point = (0, 0)
        self.last_path_distance = 0
        self.info = ""
        # self.isDisable = False
        
    def go_home(self):
        # self.rect.center = (self.balls_panel_x, self.balls_panel_y)
        self.x, self.y = self.balls_panel_x, self.balls_panel_y
       
    def update(self, settings, sc):
        
        pygame.draw.rect(sc, settings.bg_color, self.rect, 1)
 
        if self.isRolling:               # когда шар каится по поверхности
            if len(settings.all_path_points) >0:
                self.x1, self.y1 = settings.all_path_points.pop(0)
                self.rotate_rolling_ball(self, settings, sc) 
                self.is_new_point = False
                
                if self.x1 >= settings.screen_width - self.radius or self.x1 <= self.radius:
                    self.is_new_point = True 
                    self.current_distance += hypot(self.prev_point[0]-self.x1, self.prev_point[1]-self.y1)
                    self.prev_point = (self.x1, self.y1)
                    self.last_path_distance = 0
                        
                if self.y1 >= settings.screen_height- self.radius or self.y1 <= self.radius:
                    self.is_new_point = True
                    self.current_distance += hypot(self.prev_point[0]-self.x1, self.prev_point[1]-self.y1)
                    self.prev_point = (self.x1, self.y1)
                    self.last_path_distance = 0

                if not self.is_new_point:
                    self.last_path_distance = hypot(self.prev_point[0]-self.x1, self.prev_point[1]-self.y1)
                    # sum = self.current_distance + self.last_path_distance
                    # settings.text1 = str(round(sum/10)*10)
            else:
                self.isRolling = False 
                settings.is_points_erasing = True
                settings.is_deleted_ball = True
        else:
            if self.is_rotated:
                self.rotate_ball(self)
                self.rect.center = self.prev_rect_center # центр шара не должен смещаться во время вращения\
            else:
                self.rect.center = (self.x, self.y)
                
            if self.isJump:
                # pygame.draw.circle(sc, settings.yellow, (round(self.x1), round(self.y1)), 2, 0)
                self.delay +=1
                if self.delay==3: # мяч  подпрыгивает с небольшой задержкой
                    if self.step <=0 or self.step >=3:
                        self.delta = self.delta * -1       
                    self.step = self.step + self.delta
                    if not settings.is_draw_line:   # мяч вертикально подпрыгивает на игровой поверхности
                        self.rect.center = (self.x1, self.y1+self.step)
                        
                    else:   #  мяч двигается(подскакивает) в сторону возможной траектории движения при
                        self.rect.center = settings.bouncing_ball_points[self.step]  # движении мыши или стрелок
                    self.delay = 0


    @staticmethod
    def rotate_rolling_ball(self, settings, sc): # вращение мяча во время движения по ломаной траектории
        self.rotate_ball(self)
        self.rect = self.image.get_rect(center=(round(self.x1), round(self.y1)))
        pygame.draw.circle(sc, settings.yellow, (round(self.x1), round(self.y1)), 2, 0)
        
    @staticmethod
    def rotate_ball(self):          # мяч на панеле шаров при приближении к нему мыши и на 
        self.angle +=1              # игровой поверхности во время прицеливания
        self.image = pygame.transform.rotate(self.original_surf, self.angle)
        self.rect = self.image.get_rect()
        
        if self.angle ==360:
            self.angle = 0

    def move_balls_panel(self):
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.isJump = False

