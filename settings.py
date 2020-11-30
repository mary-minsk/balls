import pygame
from game_render import get_images
from button import Button

class Settings():
    def __init__(self):
        self.text_caption = 'Balls' 
        self.text_additional_panel_caption = "Flights control center"
        
        self.is_used_additional_panel = True  # Использовать панель с доп. иформацией об основных параметрах игры
        # self.is_used_additional_panel = False

        self.is_used_hints = True  # в ticker() подсказки отражаются бегущей строкой
        
        self.game_sizes()    # Размеры окна игры, игровой панели, отступы
        self.levels_and_scores() # Уровни и количество предметов на экране
        
        self.path_images()    # изображения предметов
        self.set_color()

        self.balls()   # Мяч 
        self.ticker()  # бегущая строка

        self.mouse_xy = 0, 0  # тек пигейм координаты мыши
         # Направляющий вектор движения мяча. Декартова система координат
        self.a, self.b = 0, 0
        self.pos_center_ball = 0, 0
        self.attempts_place_thing = 3  #  Максимальное количество попыток разместить предмет в одну ячейку игрового поля

        self.ball_trajectory()  # Траектория движения

        self.reset()  # Сброс основных параметров
        self.clock = pygame.time.Clock()
      
        self.level_box("Level " + str(self.current_level))

        self.copy_things = None
        self.copy_balls = None

        self.game_3()
        
    def reset(self):  
        self.selected_ball = None # Нажатие мышки для мяча. При перетаскивании мяча или его смене
        self.prev_selected_ball = None # При нажатии (выборе) на новый шар, шар на игровом поле перемещается на панель шаров
        self.rotated_ball = None # При наведении мыши на шары на панели шаров, текущий шар начинает вращаться
        
        self.ball_in_game = None # Один шар на игровои поле
        self.next_ball = None # При нажатии Табуляции на игровом поле помещается следующий шар
      
        self.is_draw_line = False     # 2. курсор выходит за границы шара (радус шара) => рисуем линию на игровой поверхности
        self.disappearance = 10  # Ускорение для стирания ломаной прямой. Увеличивающееся на единицу с каждым шагом
        
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
        self.dark_blue_options = (71, 91, 117)
        self.dark_blue = (33, 50, 81)

    def set_text_level(self):
        self.text_level[1] = str(self.current_level)
    
    def set_text_score(self):
        self.text_score[1] = str(self.score)

    def set_number_things(self):
        self.text_number_things[1] = str(self.current_number_things)

    def game_sizes(self):

        self.screen_width = 425  # (25 + 375 + 25 = 425)
        self.screen_height = 675  # (40 + 520 + +25 + 90  = 675)

        self.up_margin = 40
        self.left_margin = 25
        self.right_margin = 25
        self.bottom_margin = 25

        self.left_up_margin = (self.left_margin, self.up_margin)

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

        self.difficulty_level = ["Easy", "Normal", "High", "Crazy"]
        self.balls_size_reduction = [100, 80, 100, 70] 
        self.current_difficulty = 2
        self.attempts = 3  # = number_balls
        self.min_ball_size = 0 # Минимальный размер шара, после которого размер изображения не уменьшается (при повышении сложности игры)

        self.score_point_xy = 250, 15
        self.text_score = ["Score:", ""]
        self.text_level = ["Level:", ""]
       
        self.set_easy_params()  # Установка параметров уровней, количество вещей нв первом уровне и на последнем
        self.easy_normal_action()
        self.is_easy_normal = True

        self.level_point_xy = 20, 15

        self.number_things_point = 120, 15
        self.text_number_things = ["Things:", ""]
        self.set_number_things()

        self.level_score = 5
        self.is_show_finish = False
       
        self.text_result_level = ""
       
        self.is_start_next_level = False
        self.is_restart_level = False

        self.is_early_completion = False
        self.is_start_finish_timer = False

        self.is_level_win = False
        self.is_level_defeat = False
        self.win_message = "Win!"
        self.defeat_message = "Defeat..."
        self.is_start_level_again_timer = False
        self.is_show_level_try_again = False

        self.is_got_level_result = False
        self.center_text_messages = (self.screen_width // 2, 140)
        self.is_change_level = False

    def set_easy_params(self):
        self.start_number_things = 3
        self.finish_things = 7

    def set_normal_params(self):
        self.start_number_things = 4
        self.finish_things = 12

    def set_difficulty_params(self):
        if self.difficulty_level[self.current_difficulty] == "Easy":
            self.set_easy_params()
            self.easy_normal_action()

        elif self.difficulty_level[self.current_difficulty] == "Normal":
            self.set_normal_params()
            self.easy_normal_action()

    def set_text_level_params(self):
        self.text_level_params = "(things: " + str(self.start_number_things) + ".." + str(self.finish_things) + ")"

    def show_difficulty_params(self):
        if self.difficulty_level[self.current_difficulty] == "Easy":
            self.set_text_level_params()
            
        elif self.difficulty_level[self.current_difficulty] == "Normal":
            self.set_text_level_params()       
   
    def easy_normal_action(self):
        self.current_number_things = self.start_number_things
        self.score = 0
        self.set_text_score()
        self.current_level = 1
        self.is_two_balls = self.two_balls()
        self.last_level = self.finish_things - self.current_number_things
        self.text_level = ["Level:", ""]
        self.set_text_level()
        self.text_level_params = "(things: " + str(self.start_number_things) + ".." + str(self.finish_things) + ")"
        
    def two_balls(self):
        return True if self.current_level < 4 else False
        # return True if self.current_level < 4 and self.current_difficulty < 2 else False

        

    def path_images(self):
        self.background_image_path = '/pict/background/sky_425_675.png'
        self.background_image = ""
        self.path_things = '/pict/things'
        self.max_things_images = 35
        self.path_spirals = '/pict/spiralls'
        self.system_image_path = '/pict/settings/settings.png'
        self.game_settings_image = ""
        self.options_icon = None
        
    def level123_balls(self):

        # self.level_123_exclude_ball = ["small", "medium", "large"]

        self.level_123_balls = [["medium.png", "large.png"], ["small.png", "large.png"],  ["medium.png", "small.png"]]
        
        self.level123_distance = [[1, 0.4],     # medium, large balls / level 1
                                  [2, 0.4],   # small, large balls  / level 2
                                  [1, 2]]  # small, medium balls / level 3
                                  
        self.level123_speed = [[7, 5],   # medium, large balls / level 1
                               [6, 5],   # small, large balls  / level 2
                               [7, 6]]   # small, medium balls / level 3
                                
    
    def balls(self):

        self.jump_height_ball = 5  # на 5 точек мяч будет подпрыгивать
        self.balls_offset = 20   # растояние между шарами на панели шаров
        self.left_offset = 20   # слева отступ от трех шаров

        self.balls_speed = [8, 6, 5]  # маленький - самый быстрый (скорость 4), большой шар самый медленный (скорость 2)

        # самый маленикий катится растояние - 3*H, средний - 2*H,  большой шар - H
        # self.balls_distance = [self.screen_height*3, self.screen_height*3, self.screen_height]   # растояния для маленького, среднего и большого шаров
        self.balls_distance = [2.5, 1.5, 0.5]  # *settings.screen_height
        self.balls_info = ["small", "medium", "large"]

        self.level123_balls()
       
        self.unit = self.screen_height - self.up_margin - self.bottom_margin - self.height_bottom_panel
        self.balls_center = []  # центы шаров. При разных уровнях(размеров шаров) центры шаров не смещаются
        
        self.initial_balls_surf = [] # изображения мячей. При повышении уровня сложности игры, их размеры уменьшаются 


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

    def show_text(self, sc, color, size, point, isCenter=False, str1="", str2=""):  # вывод текста
        font = pygame.font.Font(None, size)
        text = str1 + " " + str2
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x, text_rect.y = point
        if isCenter:
            text_rect.centery = point[1]
        sc.blit(text_surface, text_rect)

    def center_text(self, color, size, point, str):  # текст по центру поверхности ("Options")
        font = pygame.font.Font(None, size)
        text_surface = font.render(str, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = point
        return text_surface, text_rect
          
    def set_original_balls_surf(self):
        surfaces = []
        balls_images = get_images(self.number_balls, self.path_spirals)
        # icons = game_render.find_ball_icons(ball_images, "small")
        
        for i in range(self.number_balls):
            surfaces.append(pygame.image.load(balls_images[i]).convert_alpha())
           

        self.initial_balls_surf = surfaces
        self.min_ball_size = min(ball.get_width() for ball in surfaces)

    def create_buttons(self, sc):
        button_next_level = [310,  self.screen_height - self.height_bottom_panel + 10, 90, 30]
        self.button_next_level_text = "Next level"


        self.next_level_button = Button(sc,button_next_level,
                                self.button_next_level_text, self.white, self.dark_blue, 22, 3)
       
    def message_box(self):  # Общее окно для настроек и для сообщений игры

        options_surf_w, options_surf_h = 300, 300
        options_surf_margin_top = 100
        left_margin = 10
        top_margin = 15

        self.options_menu_surf = pygame.Surface((300, 250))
        self.options_menu_surf.fill(self.dark_blue)
        
        self.options_menu_left_top = (self.screen_width // 2 - self.options_menu_surf.get_width() // 2, options_surf_margin_top)
        self.options_menu_surf_rect = self.options_menu_surf.get_rect()
        self.sc_options_menu_rect = pygame.Rect(self.screen_width // 2 - self.options_menu_surf.get_width() // 2, options_surf_margin_top, \
                                                options_surf_w, options_surf_h)
    
        options_border = (left_margin, top_margin, self.options_menu_surf.get_width() - 2 * left_margin,
                          self.options_menu_surf.get_height() - 2 * top_margin)
        self.inner_border = pygame.Rect(options_border)  

    def level_box(self, text):
        point = self.center_text_messages
    
        if self.is_level_defeat or self.is_show_level_try_again:
            size = 60
        else:
            size = 80

        self.text_level_box_surf, self.text_level_box_rect = self.center_text(self.white, size, point, text)

    def game_settings(self, sc):

        self.is_show_options_menu = False
        self.message_box()
    
        self.text_option_surf, self.text_option_rect = self.center_text(self.white, 28, (self.options_menu_surf.get_width()//2, 40), "Options")
        text_difficulty = "Select the difficulty of the game:"
        self.select_difficulty_surf, self.select_difficulty_rect = self.center_text(self.white, 23, (self.options_menu_surf.get_width()//2, 80), text_difficulty)
        
        button_difficulty_rect = [97, 210, self.select_difficulty_rect.w, 30]
        self.difficulty_button = Button(sc, button_difficulty_rect,
                                        self.difficulty_level[self.current_difficulty], self.white, self.dark_blue_options, 22)

        button_restart_game_rect = [97, 290, self.select_difficulty_rect.w, 30]
        self.restart_game_button = Button(sc, button_restart_game_rect,
                                          "Restart game", self.white, self.dark_blue_options, 22)
        
    def set_timer(self, millisec):
        self.timer = pygame.time.get_ticks()
        self.deadline = self.timer + millisec
        
    def set_level_time(self):  #  Включение таймера
        self.set_timer(1000)
        self.is_show_level = True

    def set_finish_time(self):  # Включение таймера
        self.set_timer(1700)
        self.is_show_finish = True

    def set_try_level_again_timer(self):
        self.set_timer(900)
        self.is_show_level_try_again = True

    def game_3(self):
        self.large_ball_png = "large.png"
        self.ball_speed = [8, 8, 7, 8, 9]  # скорость мяча в зависимости от уровня
        self.ball_distance = [1000, 1100, 1200, 1300, 1400]  # points расстояния


 
