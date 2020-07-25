from button import Button
import pygame
# from func import get_cartesian_mouse_xy_coordinates
import func
class Info():
    def __init__(self, settings):
        self.settings = settings
        self.additional_panel_width = 300
        # self.is_displayed_lines = True
        self.is_displayed_lines = False  # Вывести все ячейки, используемые при генерации предметов и отобразить цветами границы изображений

        self.is_active_panel = self.settings.is_used_additional_panel
        # self.surf = pygame.Surface((300, self.settings.screen_height))

        if self.is_active_panel:
            
            self.set_color()
            self.surf = pygame.Surface((300, self.settings.screen_height))

            self.text_game_info = ["Game info", ""]
            self.text_event = ["event.pos:", ""]
            self.text_prev_selected_ball = ["prev selected ball: ", "None"]
            self.text_selected_ball = ["selected ball: ", "None"]
            self.text_ball_in_game = ["ball in the game:", "None"]
            self.text_is_draw_line = ["is draw line: ", ""]


            self.text_mouse_xy = ["mouse: ", ""]
            # self.text_cartesian_mouse_xy = ["mouse (cartesian): ", ""]
           
            self.text_line = ["______________________________", ""]
            self.text_number_things = ["number of things: ",""]  
            self.text_things_attempts = ["all attempts to generate the things: ",""]

            self.text_generated_things = ["Generated things", ""]
            self.attempts_one_cell = ["attempts to place thing in one color cell < ", ""]

            self.reset_event_info()
            self.reset_things_text()
            
            self.text_switch = ["Lines on", "Lines off"]
            self.show_lines = [2, 595, 90, 28]
            self.switch_lines = self.is_displayed_lines
            self.switch()
            self.message =["all things will be regenerated",""]
            self.show_lines_button = Button(self.surf, self.show_lines, self.get_text_switch(), self.white, self.bg_color, 22)

            self.generated_things_lines = False

    def display_additional_info(self):

        self.set_number_things(self.settings.current_number_things)
        self.set_things_attempts()
        
        self.show_add_text(self.text_game_info, self.white, 25, 10, 90)
        # pygame.event:
        self.show_add_text(self.text_game_info, self.white, 25, 10, 90)
        self.show_add_text(self.text_event, self.white, 20, 30)
        self.show_add_text(self.text_mousebuttondown, self.white, 20, 50)
        self.show_add_text(self.text_mousebuttonup, self.white, 20, 70)
        self.show_add_text(self.text_mousemotion, self.white, 20, 90)
        self.show_add_text(self.text_else, self.white, 20, 110)
        self.show_add_text(self.text_mouse_xy, self.white, 20, 130)

        self.show_add_text(self.text_cartesian_mouse_xy, self.white, 20, 150)
        self.show_add_text(self.text_line, self.white, 20, 160)

        # Основные параметры: выбранный мяч, вращающийся, предыдущий выбранный мяч и т. д.
        self.show_add_text(self.text_selected_ball, self.white, 20, 180)
        self.show_add_text(self.text_prev_selected_ball, self.white, 20, 200)
        self.show_add_text(self.text_not_equal, self.settings.yellow, 20, 220)
        self.show_add_text(self.text_rotated_ball, self.white, 20, 240)

        self.show_add_text(self.text_ball_in_game, self.white, 20, 260)
        self.show_add_text(self.text_is_draw_line, self.white, 20, 280)

        # Generated things:
        h = 370
        self.show_add_text(self.text_line, self.white, 20, h - 20)
        self.show_generated_things(h)

        # кнопка отображения решеток, ячеек, контуров предметов и зон соприкосновения предметов (для наложения)
        # if self.is_active_panel:
        self.show_lines_button.draw()

    def show_generated_things(self, h):

        self.show_add_text(self.text_generated_things, self.white, 24, h, 50)

        self.attempts_one_cell[1] = str(self.attempts_place_thing)
        # макс. количество попыток разместить предмет в одну выбранную ячейку решетки
        self.show_add_text(self.attempts_one_cell, self.white, 20, h + 30)

        # кол-во всех предметов на игровом поле
        self.show_add_text(self.text_number_things, self.white, 20, h+50)

        h1 = h+50
        # решетка 2*3 предметов сгенерировано
        if self.len_things_2_3 > 0:
            self.show_add_text(self.text_len_things_2_3, self.settings.green, 22, h1 + 20, 0, True)
        # решетка 2*2 предметов сгенерировано
        if self.len_things_2_2 > 0:
            self.show_add_text(self.text_len_things_2_2, self.settings.yellow, 22,  h1 + 40, 0, True)
        # решетка 1*5
        if self.len_things_1_5 > 0:
            self.show_add_text(self.text_len_things_1_5, self.settings.blue, 22, h1 + 60, 0, True)
        # случайно сгенерированные предметы, общее количество
        if self.number_random_lines > 0:
            self.show_add_text(self.text_random_lines, self.settings.fuchsia, 22, h1 + 80, 0, True)

        # Отброшеные предметы (вышедшие за рамки игрового поля или наложенные на другие предметы)
        if self.unfit_2_3 > 0:
            self.show_add_text(self.text_unsuitable_things_2_3, self.settings.green, 22, h1 + 20, 120, True)

        if self.unfit_2_2 > 0:
            self.show_add_text(self.text_unsuitable_things_2_2, self.settings.yellow, 22, h1 + 40, 120, True)

        if self.unfit_1_5 > 0:
            self.show_add_text(self.text_unsuitable_things_1_5, self.settings.blue, 22, h1 + 60, 120, True)

        if self.random_unfit > 0:
            self.show_add_text(self.text_random_unfit, self.settings.fuchsia, 22, h1 + 80, 120, True)

        # сделанных попыток разместить все предметы
        self.show_add_text(self.text_things_attempts, self.white, 21, h1 + 100)

        # Случайным образом удаленные лишние предметы с последней наложенной решетки
        if self.del_things > 0:
            self.show_add_text(self.text_deleted, self.del_things_text_color, 22, h1 + 120, 0, True, self.white)

        # Надпись.Если дополнительные данные о предметах не были сгенерированы для заданного количества предметов, то при нажатии кнопки
        # перегенерировать заданное количество предметов
        if not self.generated_things_lines:
            self.show_add_text(self.message, self.white, 20, self.show_lines[1] + 10, 105)

    def show_add_text(self,text, color, size, h, w=0, is_border=False, white_border_color=None):  # вывод на экран текста
        # point = h, w
        # show_text(self.surf, settings, text, color, size, point)
        font = pygame.font.Font(None, size)
        str1, str2 = "", ""
        if text[0] is not None:
            str1 = text[0]
        if text[1] is not None:
            str2 = text[1]
        all_text = str1 + " " + str2
        text_surface = font.render(all_text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x, text_rect.y =  3 + w, h
        self.surf.blit(text_surface, text_rect)
        if is_border:
            if white_border_color is not None:
                pygame.draw.rect(self.surf, white_border_color, text_rect, 1)
            else:
                pygame.draw.rect(self.surf, color, text_rect, 1)

    def check_click(self):
        if self.is_active_panel:
            pos = self.settings.mouse_xy[0] - self.settings.screen_width, self.settings.mouse_xy[1]
            if self.show_lines_button.isOver(pos):     
                self.is_displayed_lines = not self.is_displayed_lines
                self.show_lines_button.text = self.switch()
                             
                if not self.generated_things_lines:
                    return True
        return False
                        
    def switch(self):
        if self.switch_lines == False:
            self.switch_lines = True
            return self.text_switch[0]
        else:
            self.switch_lines = False
            return self.text_switch[1]

    def get_text_switch(self):
        if self.switch_lines: 
            return self.text_switch[0]
        else:
            return self.text_switch[1]

    def reset_event_info(self):
        
        self.text_mousebuttondown = ["MOUSEBUTTONDOWN: ", ""]
        self.text_mousebuttonup = ["MOUSEBUTTONUP: ", ""]  
        self.text_mousemotion = ["MOUSEMOTION: ", ""]
        self.text_else = ["other event type: ", ""]
        self.text_rotated_ball = ["rotated ball: ", "None"]
        self.text_not_equal = ["", ""]
        self.text_cartesian_mouse_xy = ["", ""]
        # self.text_cartesian_mouse_xy = ["mouse (cartesian): ", ""]

    def reset_things_text(self):
        
        self.text_len_things_2_3 = [" grid 2 x 3: ", ""]
        self.text_len_things_2_2 = [" grid 2 x 2: ", ""]
        self.text_len_things_1_5 = [" grid 1 x 5: ", ""]
        self.len_things_2_3 = 0
        self.len_things_2_2 = 0
        self.len_things_1_5 = 0
        self.del_things = 0

        self.text_deleted = ["", ""]

        self.text_unsuitable_things_2_3 = [" unfit: ", ""]
        self.text_unsuitable_things_2_2 = [" unfit: ", ""]
        self.text_unsuitable_things_1_5 = [" unfit: ", ""] 
        self.text_random_unfit = [" unfit: ", ""] 
        
        self.unfit_2_3 = 0
        self.unfit_2_2 = 0
        self.unfit_1_5 = 0
        self.random_unfit = 0
        self.del_things_text_color = None

        self.all_attempts = 0
        self.attempts_place_thing = 3 #  Максимальное количество попыток разместить предмет в одну ячейку игрового поля
        self.random_placement_attempts = 0 #
        self.lines_2_3 = []
        self.lines_2_2 = []
        self.lines_1_5 = []
        self.number_random_lines = 0
        self.text_random_lines = [" random:    ", ""]
        self.deleted_things_rect = []  
        self.random_deleted_things_rect = []       

    # Balls
    def set_text_not_equal_balls(self):
        if self.is_active_panel:
            self.text_not_equal = ["prev selected ball!=selected ball", ""]

    # Events

    def set_text_mousebuttondown(self, event_pos):
        if self.is_active_panel:
            self.text_mousebuttondown[1] = self.point_to_str((event_pos))

    def set_text_other_events(self):
        if self.is_active_panel:
            self.text_else[1] = "Yes"

    def point_to_str(self, point):  # строковое представление точки
        return "(" + str(point[0]) + ", " + str(point[1]) + ")"
    

    def set_text_events(self):
        if self.is_active_panel:

            self.text_mouse_xy[1] = self.point_to_str(self.settings.mouse_xy)
            self.text_is_draw_line[1] = str(self.settings.is_draw_line)

            if self.settings.rotated_ball is None:
                self.text_rotated_ball[1] = "None"
            else:
                self.text_rotated_ball[1] = self.settings.rotated_ball.info

            if self.settings.ball_in_game is not None:
                center = self.settings.ball_in_game.rect.center
                
                self.text_ball_in_game[1] = self.settings.ball_in_game.info + ";  center = " + self.point_to_str(center)
                cartesian_point = func.get_cartesian_mouse_xy_coordinates(self.settings)
                self.text_cartesian_mouse_xy[0] = "mouse (cartesian): "
                self.text_cartesian_mouse_xy[1] = self.point_to_str(cartesian_point)
            else:
                self.text_ball_in_game[1] = "None"

            if self.settings.selected_ball is not None:
                self.text_selected_ball[1] = self.settings.selected_ball.info
            else:
                self.text_selected_ball[1] = "None"

            if self.settings.prev_selected_ball is not None:
                self.text_prev_selected_ball[1] = self.settings.prev_selected_ball.info
            else:
                self.text_prev_selected_ball[1] = "None"


    def set_text_mousemotion(self, event_pos):
        if self.is_active_panel:
            self.text_mousemotion[1] = self.point_to_str(event_pos)

    def set_text_mousebuttonup(self, event_pos):
        if self.is_active_panel:
            self.text_mousebuttonup[1] = self.point_to_str(event_pos) 

    
    # Things
    def set_number_things(self, n):
        if self.is_active_panel:
            self.text_number_things[1] = str(n)

    def set_things_attempts(self):
        if self.is_active_panel:
            self.text_things_attempts[1] = str(self.all_attempts)

    def set_text_len_things_2_3(self, n):
        if self.is_active_panel:
            self.len_things_2_3= n
            self.text_len_things_2_3[1] = str(n) + "  "

    def set_text_len_things_2_2(self, n):
        if self.is_active_panel:
            self.len_things_2_2 = n
            self.text_len_things_2_2[1] = str(n)+ "  "

    def set_text_len_things_1_5(self, n):
        if self.is_active_panel:
            self.len_things_1_5 = n
            self.text_len_things_1_5[1] = str(n)+ "  "

    def set_text_unsuitable_things_2_3(self, n):
        if self.is_active_panel:
            self.unfit_2_3 = n
            self.text_unsuitable_things_2_3[1] = str(n) + " "

    def set_text_unsuitable_things_2_2(self, n):
        if self.is_active_panel:
            self.unfit_2_2 = n
            self.text_unsuitable_things_2_2[1] = str(n) + " "

    def set_text_unsuitable_things_1_5(self, n): 
        if self.is_active_panel:
            self.unfit_1_5 = n
            self.text_unsuitable_things_1_5[1] = str(n) + " "

    def set_text_del_things(self, n, text, color):
        if self.is_active_panel:
            self.del_things = n
            if n >0: 
                self.text_deleted[0] = " excess "+ text + " things, (deleted): " + str(n) 
                self.text_deleted[1] = " "
                self.del_things_text_color = color  

    def set_text_number_random_lines(self, n):
        if self.is_active_panel:
            self.number_random_lines = n
            self.text_random_lines[1] = str(n) + " "

    def display_random_unfit(self): #random_unfit
        if self.is_active_panel:
            self.text_random_unfit[1] = str(self.random_unfit) + " "

    def draw_cells(self, sc):

        for rect in self.lines_2_3:
            pygame.draw.rect(sc, rect[1], rect[0], 1)

        if self.settings.current_number_things > 6:
            for rect in self.lines_2_2:
                pygame.draw.rect(sc, rect[1], rect[0], 1)
                
        if self.settings.current_number_things > 10:
            for rect in self.lines_1_5:
                pygame.draw.rect(sc, rect[1], rect[0], 1)

        if len(self.deleted_things_rect) > 0:
            for rect in self.deleted_things_rect:
                # pygame.draw.rect(self.surf, white, rect[0], 2)  
                pygame.draw.rect(sc, rect[1], rect[0], 1)
                pygame.draw.aaline(sc, rect[1], rect[0].topleft, rect[0].bottomright)
                pygame.draw.aaline(sc, rect[1], rect[0].bottomleft, rect[0].topright)

        if len(self.random_deleted_things_rect) > 0:
            for rect in self.random_deleted_things_rect:
                pygame.draw.rect(sc, self.white, rect[0], 2)
                pygame.draw.line(sc, rect[1], rect[0].topleft, rect[0].bottomright, 2)
                pygame.draw.line(sc, rect[1], rect[0].bottomleft, rect[0].topright, 2)

    def set_color(self):
        self.white = (255, 255, 255)
        self.bg_color = (100, 100, 100)
       

   

      
            
                
          
        

    
