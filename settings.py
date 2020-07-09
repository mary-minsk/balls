import pygame

class Settings():
    def __init__(self):
        self.text_caption = '12' 
        self.text_additional_panel_caption = "Flights control center"
        
        self.is_used_additional_panel = True  # Использовать панель с доп. иформацией об основных параметрах игры
        # self.is_used_additional_panel = False

        self.is_used_hints = True  # в ticker() подсказки отражаются бегущей строкой
        
        self.game_sizes()    # Размеры окна игры, игровой панели, отступы
        self.levels_and_things() # Уровни и количество предметов на экране
        
        self.path_images()    # изображения предметов
        self.set_color()

        self.balls()   # Мяч 
        self.buttons()  # Кнопки
        self.ticker()  # бегущая строка

        self.mouse_xy = 0, 0  # тек пигейм координаты мыши
         # Направляющий вектор движения мяча. Декартова система координат
        self.a, self.b = (0, 0)
        self.ball_trajectory()  # Траектория движения
    
        self.reset()  # Сброс основных параметров
        
    def reset(self):  
        self.selected_ball = None # Нажатие мышки для мяча. При перетаскивании мяча или его смене
        self.prev_selected_ball = None # При нажатии (выборе) на новый шар, шар на игровом поле перемещается на панель шаров
        self.rotated_ball = None # При наведении мыши на шары на панели шаров, текущий шар начинает вращаться
        self.ball_in_game = None # Один шар на игровои поле
        self.next_ball = None # При нажатии Табуляции на игровом поле помещается следующий шар
       
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

    def game_sizes(self):

        self.screen_width = 425  # (25 + 375 + 25 = 425)
        self.screen_height = 675  # (40 + 520 + +25 + 90  = 675)

        self.up_margin = 40
        self.left_margin = 25
        self.right_margin = 25
        self.bottom_margin = 25

        self.height_bottom_panel = 90
        self.bottom_margin_center_ball = 40  #(Класс Ball панель шаров self.y = settings.screen_height - settings.bottom_margin_center_ball)

        game_panel_rect = (self.left_margin, self.up_margin,
                                self.screen_width - self.right_margin - self.left_margin, self.screen_height - self.height_bottom_panel - self.up_margin - self.bottom_margin)
        self.game_panel = pygame.Rect(game_panel_rect)

        game_panel_3_margins_rect = (0, 0,
                                self.screen_width, self.screen_height - self.height_bottom_panel - self.bottom_margin)
        self.game_panel_add_3_margins = pygame.Rect(game_panel_3_margins_rect)

        border_game_panel_rect = (0, 0,
                                self.screen_width, self.screen_height - self.height_bottom_panel)
        self.border_game_panel = pygame.Rect(border_game_panel_rect)

    def levels_and_things(self):

        self.number_balls = 3

        self.start_level = 1
        self.current_level = self.start_level
        self.start_things = 5
        self.current_number_things = self.start_things
        self.finish_things = 20
        self.last_level = self.finish_things - self.start_things

        self.difficulty_level = ["Easy", "Normal", "High", "Crazy"]
        self.text_level = ["Level:", ""]
        self.set_text_level()
        self.level_point_xy = 20, 15
        
    def path_images(self):
        self.background_image_path = '/pict/background/sky_425_675.png'
        self.background_image = ""
        self.path_things = '/pict/things'
        self.max_things_images = 35
        self.path_spirals = '/pict/spiralls'
        
    def balls(self):

        self.jump_height_ball = 5  # на 5 точек мяч будет подпрыгивать
        self.balls_offset = 20   # растояние между шарами на панели шаров
        self.left_offset = 20   # слева отступ от трех шаров

        self.balls_speed = [6, 5, 4]  # маленький - самый быстрый (скорость 4), большой шар самый медленный (скорость 2)

        # самый маленикий катится растояние - 3*H, средний - 2*H,  большой шар - H
        # self.balls_distance = [self.screen_height*3, self.screen_height*3, self.screen_height]   # растояния для маленького, среднего и большого шаров
        self.balls_distance = [3, 2, 1]  # *settings.screen_height
        self.balls_info = ["small", "medium", "large"]
        self.unit = self.screen_height - self.up_margin - self.bottom_margin - self.height_bottom_panel

    def buttons(self):

        self.button_level = [310,  self.screen_height - self.height_bottom_panel +10, 90, 30]
        self.button_level_text = "Next level..."
        # self.button_ruler = [300, self.w - 115, 90, 30]
        # self.button_ruler_text = "Ruler"   

    def ticker(self):

        self.hints = ["Сhoose the whirlwind!", "Drag the ball to things!", "Use mouse to aim",
                      "Aim at things and press space!",
                      "Harvesting...", "Oops!...I did it again!"]

        self.ticker_rect = (0, self.screen_height - self.height_bottom_panel - self.bottom_margin,
                            self.bottom_margin, self.bottom_margin)

        self.ticker_panel = pygame.Rect(self.ticker_rect)

        # self.ticker_surf = pygame.Surface((self.screen_width, self.bottom_margin))
        # self.ticker_surf = pygame.Surface((self.bottom_margin, self.bottom_margin))
        # player_rect = self.ticker_surf.get_rect(topleft=(0, self.screen_height - self.height_bottom_panel - self.bottom_margin))
        self.triker_margine = 5
        self.triker_reset()

    def triker_reset(self):
        self.triker_x = self.triker_margine = 5
    
    def ball_trajectory(self):
    
        self.disappearing_edges = []  # исчезающие вершины ломаной прямой
        self.is_points_erasing = False  # Удаление траектории движения шара.
        # Точка на окружности шара (наконечник), на одной линии с центром шара  и позицией мыши
        self.tip_x, self.tip_y = (0, 0)

        # список 5 точек подпрыгивания на месте мяча при прицеливании
        self.bouncing_ball_points = []
        self.edges = []  # все точки на ломаной кривой для рисования ломаной кривой
        # вначале содержит все точки пути (скорость мяча = 1),  но
        self.all_path_points = []
        # после запуска мяча часть точек будет отброшена для отображения движения
        # с ускорением или замедлением

        self.all_dx_dy = []  # все направляющие вектора движения
        # выборочные направляющие вектора движения (для отображения стягивающейся точки      траектории)
        self.dxy = (0, 0)

        # (20%) часть пути, когда мяч будет ускоряться и замедляться
        self.path_acceleration = 0.2
        # последняя точка ломаной кривой = settings.all_path_points[-1]
        self.last_path_point = (0, 0)
       
        
