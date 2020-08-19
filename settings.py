import pygame
from game_render import get_images
from button import Button

class Settings():
    def __init__(self):
        self.text_caption = '12' 
        self.text_additional_panel_caption = "Flights control center"
        
        self.is_used_additional_panel = True  # Использовать панель с доп. иформацией об основных параметрах игры
        # self.is_used_additional_panel = False

        self.is_used_hints = True  # в ticker() подсказки отражаются бегущей строкой
        
        self.game_sizes()    # Размеры окна игры, игровой панели, отступы
        self.levels_and_scores() # Уровни и количество предметов на экране
        
        self.path_images()    # изображения предметов
        self.set_color()

        self.balls()   # Мяч 
        self.buttons()  # Кнопки
        self.ticker()  # бегущая строка

        self.mouse_xy = 0, 0  # тек пигейм координаты мыши
         # Направляющий вектор движения мяча. Декартова система координат
        self.a, self.b = 0, 0
        self.pos_center_ball = 0, 0
        self.attempts_place_thing = 3  #  Максимальное количество попыток разместить предмет в одну ячейку игрового поля

        self.ball_trajectory()  # Траектория движения

        # self.is_early_completion = False
        self.reset()  # Сброс основных параметров
        
    def reset(self):  
        self.selected_ball = None # Нажатие мышки для мяча. При перетаскивании мяча или его смене
        self.prev_selected_ball = None # При нажатии (выборе) на новый шар, шар на игровом поле перемещается на панель шаров
        self.rotated_ball = None # При наведении мыши на шары на панели шаров, текущий шар начинает вращаться
        
        self.ball_in_game = None # Один шар на игровои поле
        self.next_ball = None # При нажатии Табуляции на игровом поле помещается следующий шар
      
        self.is_draw_line = False     # 2. курсор выходит за границы шара (радус шара) => рисуем линию на игровой поверхности
        self.disappearance = 10  # Ускорение для стирания ломаной прямой. Увеличивающееся на единицу с каждым шагом
        
        # self.is_early_completion = False
        self.level_score = 5
    
    def set_color(self):
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.black = (0, 0, 0)
        self.bg_color = (100, 100, 100)
        self.white = (255, 255, 255)
        self.green = (0, 200, 0)
        self.aqua = (0,155,155)
        self.blue = (0, 191, 255)
        self.fuchsia = (255, 0, 255)

    def set_text_level(self):
        self.text_level[1] = str(self.current_level)
    
    def set_text_score(self):
        self.text_score[1] = str(self.score)    

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

    def levels_and_scores(self):

        self.number_balls = 3

        self.start_level = 1
        self.current_level = self.start_level
        self.start_things = 5
        self.current_number_things = self.start_things
        self.finish_things = 20
        self.last_level = self.finish_things - self.start_things

        self.difficulty_level = ["Easy", "Normal", "High", "Crazy"]
        self.balls_size_reduction = [0, 10, 20, 30] 
        self.current_difficulty = 0

        self.text_level = ["Level:", ""]
        self.set_text_level()
        self.level_point_xy = 20, 15

        self.score = 0  # total score
        self.score_point_xy = 120, 15
        self.text_score = ["Score:", ""]
        self.set_text_score()

        self.level_score = 5

        # self.max_score = 0
        # self.text_max_score = ["Level:", ""]
        # self.set_text_level()
        # self.level_point_xy = 20, 15
        
    def path_images(self):
        self.background_image_path = '/pict/background/sky_425_675.png'
        self.background_image = ""
        self.path_things = '/pict/things'
        self.max_things_images = 35
        self.path_spirals = '/pict/spiralls'
        self.system_image_path = '/pict/settings/settings.png'
        self.game_settings_image = ""
        self.game_settings_rect = None
        
    def balls(self):

        self.jump_height_ball = 5  # на 5 точек мяч будет подпрыгивать
        self.balls_offset = 20   # растояние между шарами на панели шаров
        self.left_offset = 20   # слева отступ от трех шаров

        self.balls_speed = [8, 6, 5]  # маленький - самый быстрый (скорость 4), большой шар самый медленный (скорость 2)

        # самый маленикий катится растояние - 3*H, средний - 2*H,  большой шар - H
        # self.balls_distance = [self.screen_height*3, self.screen_height*3, self.screen_height]   # растояния для маленького, среднего и большого шаров
        self.balls_distance = [3, 2, 1]  # *settings.screen_height
        self.balls_info = ["small", "medium", "large"]
        self.unit = self.screen_height - self.up_margin - self.bottom_margin - self.height_bottom_panel
        self.balls_center = []  # центы шаров. При разных уровнях(размеров шаров) центры шаров не смещаются
        
        self.initial_balls_surf = [] # изображения мячей. При повышении уровня сложности игры, их размеры уменьшаются 


    def buttons(self):

        self.button_next_level = [310,  self.screen_height - self.height_bottom_panel + 10, 90, 30]
        self.button_next_level_text = "Next level"

        self.button_difficulty = [310, self.screen_height - self.height_bottom_panel + 50, 90, 30]
        
        
        # self.button_difficulty_text = "easy"
       
        # self.button_ruler = [300, self.w - 115, 90, 30]
        # self.button_ruler_text = "Ruler"   

    def ticker(self):
        
        self.balls_panel_hints = ["Сhoose any whirlwind!", "Take the last whirlwind"]

        self.hints = ["Drag the ball to things!",
                      "Use keyboard arrows to aim, tab to change ball",
                      "After aiming, press spacebar or double click!",
                      "Harvesting... Press spacebar to select next hurricane",
                      "Harvesting... Press spacebar to select last hurricane",
                      "Oops!...I did it again! Press spacebar..."]


        self.ticker_rect = pygame.Rect(0, self.screen_height - self.height_bottom_panel - self.bottom_margin,
                            self.screen_width, self.bottom_margin)
        self.triker_margine = 5
        self.triker_reset()
        # self.info_surf = pygame.Surface((300, self.screen_height))  # settings.bottom_margin

    def triker_reset(self):
        self.triker_x = self.screen_width
        # self.is_triker_stop = False
        self.is_triker_stop = True
    
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
        self.path_acceleration = 0.15
        # последняя точка ломаной кривой = settings.all_path_points[-1]
        self.last_path_point = (0, 0)

    def show_text(self, sc, color, size, point, isCenter=False, str1="", str2=""):  # вывод на экран текста
        font = pygame.font.Font(None, size)
        text = str1 + " " + str2
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x, text_rect.y = point
        if isCenter:
            text_rect.centery = point[1]
        sc.blit(text_surface, text_rect)
       
    def set_original_balls_surf(self):
        surfaces = []
        balls_images = get_images(self.number_balls, self.path_spirals)
        for i in range(self.number_balls):
            surfaces.append(pygame.image.load(balls_images[i]).convert_alpha())

        self.initial_balls_surf = surfaces

    def create_buttons(self, sc):
        self.next_level_button = Button(sc, self.button_next_level,
                                self.button_next_level_text, self.white, self.bg_color, 22)
        self.difficulty_button = Button(sc, self.button_difficulty,
                               self.difficulty_level[self.current_difficulty], self.white, self.bg_color, 22)
        #  ruler_button = Button(settings.button_ruler, settings.button_ruler_text)



    # def get_center_balls(self):  # расположение центров шаров на панели шаров (self.balls_center)
       
    #     y = self.screen_height - self.bottom_margin_center_ball
    #     shift = self.left_offset
      
    #     for i in range(self.number_balls):
    #         w = self.initial_balls_surf[i].get_rect()[2]  # ширина изображения
    #         x = shift + self.balls_offset*i + w//2
    #         shift = shift + w
    #         self.balls_center.append((x, y))
    #     # print(self.balls_center)
