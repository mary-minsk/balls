import pygame
from math import sqrt, hypot
import func

# класс Мяч или Шар (при сталкновении с 10 предметами шар их лопает (уничтожает))
class Ball(pygame.sprite.Sprite):  # Всего 3 шара: маленький, средний и большой мяч (шар)
    def __init__(self, settings, x, surf, index):
        pygame.sprite.Sprite.__init__(self)
        
        self.x = x                      #координаты шара на панели шаров. 
                                        #Если шар не катится на поверхности, он возвращается вниз экрана к другим шарам
        self.y = settings.screen_height - settings.bottom_margin_center_ball
        self.balls_panel_x = x
        self.balls_panel_y = self.y
        self.index = index

        self.image = surf
        self.original_surf = surf # для корректировки ценра вращения мяча (в прямоугольм контуре)
        self.rect = self.image.get_rect(center=(x, self.y))
        self.prev_rect_center = self.rect.center  # корректирование центра шара при вращении
        self.radius = int(self.rect.width * .87 / 2)  # радиус для определения границ столкновения с другими объектами
        
        self.isRolling = False # шар катится по поверхности
        self.isJump = False  # мяч подпрыгивает или не подпрыгивает на месте (на игровой поверхности)
        self.isDeleting = False
        
        self.x1 = 0   # координаты центра шара на игровой поверхности  ????
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

        self.stop_moving()
       
    def set_xy(self, point):
        self.x,self.y = point
        self.rect.center = self.x, self.y
        
    def center(self):
        return self.x, self.y
        
    def go_home(self, stop_moving = False):
        
        self.x, self.y = self.balls_panel_x, self.balls_panel_y
        self.isJump = False

    def stop_moving(self):
       
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
       
    def finish_action(self, settings):
        self.isRolling = False
        settings.is_points_erasing = True
        settings.is_deleted_ball = True

    def update(self, settings, sc):
        
        # pygame.draw.rect(sc, settings.bg_color, self.rect, 1)
 
        if self.isRolling:  # когда шар каится по поверхности
           
            if len(settings.all_path_points) >0:
                self.x, self.y = settings.all_path_points.pop(0)
                self.rotate_rolling_ball(self, settings, sc) 
            
            else:
                self.finish_action(settings)

        self.check_rotation_balls_panel(self)   # вращение шаров напанели шаров
        self.check_movings(self, settings)      # перемещение шара на игровом поле клавишами (стрелки вверх, вниз и т. д.)
        self.check_jump(self, settings)         # подпрыгивание шара 
                
    @staticmethod
    def rotate_rolling_ball(self, settings, sc): # вращение мяча во время движения по ломаной траектории
        self.rotate_ball(self, 2)
        self.rect = self.image.get_rect(center=(round(self.x1), round(self.y1)))
        pygame.draw.circle(sc, settings.yellow, (round(self.x1), round(self.y1)), 2, 0)
        
    @staticmethod
    def rotate_ball(self, angle = 1):          # мяч на панеле шаров при приближении к нему мыши и на 
        self.angle += angle              # игровой поверхности во время прицеливания
        self.image = pygame.transform.rotate(self.original_surf, self.angle)
        self.rect = self.image.get_rect()
        
        if self.angle ==360:
            self.angle = 0

    @staticmethod
    def check_rotation_balls_panel(self):
        if self.is_rotated:
            self.rotate_ball(self)
            self.rect.center = self.prev_rect_center  # центр шара не должен смещаться во время вращения
        else:
            if not self.isJump:
                self.rect.center = (self.x, self.y)
    
    @staticmethod
    def check_movings(self, settings):
        if self.moving_right:
            self.x += 1
            func.check_correct_up_left_right_border(self, settings, True)
            self.rect.center = (self.x, self.y)

        if self.moving_left:
            self.x -= 1
            func.check_correct_up_left_right_border(self, settings, True)
            self.rect.center = (self.x, self.y)

        if self.moving_up:
            self.y -= 1
            func.check_correct_up_left_right_border(self, settings, True)
            self.rect.center = (self.x, self.y)

        if self.moving_down:
            self.y += 1
            func.check_correct_up_left_right_border(self, settings, True)
            self.rect.center = (self.x, self.y)

    @staticmethod
    def check_jump(self, settings):
        if self.isJump:
            pass
            self.delay += 1
            if self.delay==2: # мяч  подпрыгивает с небольшой задержкой
                if self.step <= 0 or self.step >= 3:
                    self.delta = self.delta * -1
                self.step = self.step + self.delta
                self.delay = 0

            if settings.is_draw_line:   # мяч подпрыгивает в направлении движения мыши
                self.rect.center = settings.bouncing_ball_points[self.step]
            else:                       #вертикальное подпрыгивание 
                self.rect.center = (self.x, self.y + self.step)



