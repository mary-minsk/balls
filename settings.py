import pygame

class Settings():
    def __init__(self):
        self.text_caption = '12' 
        self.text_additional_panel_caption = "Flights control center"

        # Использовать панель с доп. иформацией об основных параметрах игры
        self.is_used_additional_panel = True
        # self.is_used_additional_panel = False 
        # self.is_displayed_lines = True
        self.is_displayed_lines = False
        self.additional_panel_width = 300

        self.number_balls = 3

        self.start_level = 1
        self.current_level = self.start_level
        self.start_things = 5
        self.current_number_things = self.start_things
        self.finish_things = 20
        self.last_level = self.finish_things - self.start_things

        self.screen_width = 425   #(25 + 375 + 25 = 425)
        self.screen_height = 650  #(40 + 520 + 90 = 650)

        self.up_margin = 40
        self.left_margin = 25
        self.right_margin = 25 
        self.height_bottom_panel = 90
        self.bottom_margin_center_ball = 40

        self.game_panel_rect = (self.left_margin, self.up_margin, \
            self.screen_width - self.right_margin - self.left_margin, self.screen_height - self.height_bottom_panel - self.up_margin)
        self.game_panel = pygame.Rect(self.game_panel_rect)

        self.game_panel_rect2 = (0, 0,
                                self.screen_width, self.screen_height - self.height_bottom_panel)
        self.game_panel2 = pygame.Rect(self.game_panel_rect2)
        
        self.difficulty_level = ["Easy", "Normal", "High", "Crazy"]
        self.text_level = ["Level:", ""]
        self.set_text_level()
        self.level_point_xy = 20,15

        
        
         # изображения предметов
        self.background_image_path = '/pict/background/sky_425_650.jpg'
        self.background_image = ""
        self.path_things = '/pict/things'  
        self.max_things_images = 35
        self.path_spirals = '/pict/spiralls' 

        self.set_color()

        # Мяч
        self.jump_height_ball = 5  # на 5 точек мяч будет подпрыгивать
        self.balls_offset= 20   # растояние между шарами на панели шаров
        self.left_offset = 20   # слева отступ от трех шаров

        self.balls_speed = [6,5,4]  # маленький - самый быстрый (скорость 4), большой шар самый медленный (скорость 2)

                                # самый маленикий катится растояние - 3*H, средний - 2*H,  большой шар - H
        # self.balls_distance = [self.screen_height*3, self.screen_height*3, self.screen_height]   # растояния для маленького, среднего и большого шаров
        self.balls_distance = [3, 2, 1]  # *settings.screen_height
        self.balls_info = ["small", "medium", "large"]
        self.unit = self.screen_height

        
        # Кнопки
        self.button_level = [310,  self.screen_height - self.height_bottom_panel +10, 90, 30]
        self.button_level_text = "Next level..."
        # self.button_ruler = [300, self.w - 115, 90, 30]
        # self.button_ruler_text = "Ruler"


        # Траектория движения
        self.disappearing_edges = []  # исчезающие вершины ломаной прямой
        self.is_points_erasing = False # Удаление траектории движения шара. 
        self.tip_x, self.tip_y = (0, 0) # Точка на окружности шара (наконечник), на одной линии с центром шара  и позицией мыши

        self.bouncing_ball_points =[]  # список 5 точек подпрыгивания на месте мяча при прицеливании
        self.edges = [] # все точки на ломаной кривой для рисования ломаной кривой
        self.all_path_points = [] # вначале содержит все точки пути (скорость мяча = 1),  но
                                 # после запуска мяча часть точек будет отброшена для отображения движения
                                 # с ускорением или замедлением

        self.all_dx_dy = [] # все направляющие вектора движения
        self.dxy = (0, 0)  # выборочные направляющие вектора движения (для отображения стягивающейся точки      траектории)

        self.path_acceleration = 0.2 #(20%) часть пути, когда мяч будет ускоряться и замедляться
        self.last_path_point = (0, 0) # последняя точка ломаной кривой = settings.all_path_points[-1] 
        self.a, self.b = (0, 0)  # направление последующего движения мяча (позиция курсора мыши 
                                 # относительно центра выбранного шара в декартовой систете координат

        # self.text1 = "" 
        
        self.reset()   # Сброс основных параметров
        
    def reset(self):  
        self.selected_ball = None
        self.prev_selected_ball = None
        self.rotated_ball = None
        self.ball_in_game = None
        # self.index_current_ball = None  # индекс выбранного шара(мяча)
        # self.index_prev_ball = None     # индекс предыдущего выбранного шара(мяча)
        # self.index_prev_selected_ball = None 

        # self.is_ball_selected = False # шар на нижней панеле выбран мышкой

        # self.is_ball_pressed = False  # шар на игровой поверхности:
        # self.is_ball_down = False     # 1. курсор мыши не выходит за пределы окружности шара, траектория движения мяча не отображается 
        self.is_draw_line = False     # 2. курсор выходит за границы шара (радус шара) => рисуем линию на игровой поверхности
        self.disappearance = 1 # Ускорение для стирания ломаной прямой. Увеличивающееся на единицу с каждым шагом
    
    def set_color(self):
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.black = (0, 0, 0)
        self.bg_color = (100, 100, 100)
        self.white = (255, 255, 255)
        self.green = (0, 200, 0)
        self.aqua = (0,155,155)
        self.blue = (0, 191, 255)
        # Fuchsia	#FF00FF	255, 0, 255
        self.fuchsia = (255, 0, 255)

    def set_text_level(self):
        self.text_level[1] = str(self.current_level)
       

       

       
        


        
        
