
class Settings():
    def __init__(self):

        self.number_balls = 3
        self.number_things = 10

        self.screen_width = 425
        self.screen_height = 650

        self.up_margin = 40
        self.left_margin = 25
        self.right_margin = 25 
        self.height_bottom_panel = 90
        self.bottom_margin_center_ball = 40
        self.additional_panel_width = 300
        self.is_used_additional_panel = True
        
        self.w = self.screen_height + self.up_margin + self.height_bottom_panel
        # self.w = self.height_up_panel + self.screen_height + self.height_bottom_panel
        
        self.text_caption = 'Balls' 

        self.background_image_path = '/pict/background/sky_425_650.jpg'
        self.background_image = ""
        self.path_things = '/pict/things'   # изображения предметов
        self.path_spirals = '/pict/spiralls' 

        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.black = (0, 0, 0)
        self.bg_color = (100, 100, 100)
        self.white = (255, 255, 255)

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

        self.hints = ["Сhoose the whirlwind!", "Drag the ball to things!","Use mouse to aim",\
            "Aim at things and press space!", \
            "Harvesting...", "Oops!...I did it again!"]
        
        # Кнопки
        self.button_level = [300,  self.w - 70, 90, 30]
        self.button_level_text = "Next level..."
        self.button_ruler = [300, self.w - 115, 90, 30]
        self.button_ruler_text = "Ruler"

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
     
        self.text0 = ["Game info", ""]
        self.text_event = ["event.pos:", ""]
        self.text_mousebuttondown = ["MOUSEBUTTONDOWN: ", ""]
        self.text_mousebuttonup = ["MOUSEBUTTONUP: ", ""]  
        self.text_mousemotion = ["MOUSEMOTION: ", ""]
        self.text_else = ["other event.pos: ", ""]
        self.text_prev_selected_ball = ["prev selected ball: ", "None"]
        self.text_selected_ball = ["selected ball: ", "None"]


        self.text1 = [" ", ""]
        self.text2 = ["ball: ", "None"]
        self.text_not_equal = ["", ""]
        self.text_rotated_ball = ["rotated ball: ", "None"]
        self.text_prev_rotated_ball = ["prev rotated ball: ", "None"]
        self.text_rotated_ball_not_equal = ["", ""]
        # self.text1 = "" 
        # self.text2 = "" 
        # self.text3 = ""  
        # self.text5 = "" 
        # self.text4 = "" 
        # self.text6 = "" 
        
        self.reset()   # Сброс основных параметров
    def reset_text(self):
        self.text0 = ["Game info", ""]
        self.text_event = ["event.pos:", ""]
        self.text_mousebuttondown = ["MOUSEBUTTONDOWN: ", ""]
        self.text_mousebuttonup = ["MOUSEBUTTONUP: ", ""]  
        self.text_mousemotion = ["MOUSEMOTION: ", ""]
        self.text_else = ["other event.pos: ", ""]
        self.text_rotated_ball = ["rotated ball: ", "None"]
        self.text_prev_rotated_ball = ["prev rotated ball: ", "None"]

        self.text_not_equal = ["", ""]
        self.text_rotated_ball_not_equal = ["", ""]
        self.text1 = [" ", ""]
        # self.text_prev_selected_ball = ["prev selected ball: ", "None"]
        # self.text_selected_ball = ["selected ball: ", "None"]
        
    def reset(self):  
        self.index_current_ball = None  # индекс выбранного шара(мяча)
        self.index_prev_ball = None     # индекс предыдущего выбранного шара(мяча)
        self.index_prev_selected_ball = None 

        self.is_ball_selected = False # шар на нижней панеле выбран мышкой

        self.is_ball_pressed = False  # шар на игровой поверхности:
        self.is_ball_down = False     # 1. курсор мыши не выходит за пределы окружности шара, траектория движения мяча не отображается 
        self.is_draw_line = False     # 2. курсор выходит за границы шара (радус шара) => рисуем линию на игровой поверхности
        self.disappearance = 1 # Ускорение для стирания ломаной прямой. Увеличивающееся на единицу с каждым шагом
    

       

       
        


        
        