from button import Button
class Info():
    def __init__(self, is_active_panel):

        self.additional_panel_width = 300
        # self.is_displayed_lines = True
        self.is_displayed_lines = False  # Вывести все ячейки, используемые при генерации предметов и отобразить цветами границы изображений

        self.is_active_panel = is_active_panel
        self.hints = ["Сhoose the whirlwind!", "Drag the ball to things!","Use mouse to aim",\
            "Aim at things and press space!", \
            "Harvesting...", "Oops!...I did it again!"]
        

            # self.text_level = ["Level:", ""]
        
        if is_active_panel:

            self.text_game_info = ["Game info", ""]
            self.text_event = ["event.pos:", ""]
            self.text_prev_selected_ball = ["prev selected ball: ", "None"]
            self.text_selected_ball = ["selected ball: ", "None"]
            self.text_ball_in_game = ["ball in the game:", "None"]
            self.text_is_draw_line = ["is draw line: ", ""]


            self.text_mouse_xy = ["mouse: ", ""]
            self.text_line = ["______________________________", ""]
            self.text_number_things = ["number of things: ",""]  
            self.text_things_attempts = ["all attempts to generate the things: ",""]

            self.text_generated_things = ["Generated things", ""]
            self.attempts_one_cell = ["attempts to place thing in one color cell < ", ""]

            self.reset()
            self.reset_things_text()
            
            self.text_switch = ["Lines on", "Lines off"]
            self.show_lines = [427, 569, 90, 30]
            self.switch_lines = self.is_displayed_lines
            self.switch()
            self.message =["all things will be regenerated",""]
            self.show_lines_button = Button(self.show_lines, self.get_text_switch(), 22)

            self.generated_things_lines = False
            
    def check_click(self, mouse_xy, settings):
        if self.is_active_panel:
            if self.show_lines_button.isOver(mouse_xy):
                        
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

    def reset(self):
        
        self.text_mousebuttondown = ["MOUSEBUTTONDOWN: ", ""]
        self.text_mousebuttonup = ["MOUSEBUTTONUP: ", ""]  
        self.text_mousemotion = ["MOUSEMOTION: ", ""]
        self.text_else = ["other event type: ", ""]
        self.text_rotated_ball = ["rotated ball: ", "None"]
        self.text_not_equal = ["", ""]

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

    # def set_selected_ball(self, selected_ball, prev_selected_ball):
    #     if selected_ball is not None:
    #         self.text_selected_ball[1] = selected_ball.info
    #     else:
    #         self.text_selected_ball[1] = "None"

    #     if prev_selected_ball is not None:
    #         self.text_prev_selected_ball[1] = prev_selected_ball.info  
    #     else:
    #         self.text_prev_selected_ball[1] = "None"
            
    # def set_ball_in_game(self, ball_in_game):
    #     if ball_in_game is not None:
    #         self.text_ball_in_game[1] = ball_in_game.info
    #     else:
    #         self.text_ball_in_game[1] = "None"

    
    # Events

    def set_text_mousebuttondown(self, event_pos):
        if self.is_active_panel:
            self.text_mousebuttondown[1] = self.point_to_str((event_pos))

    def set_text_other_events(self):
        if self.is_active_panel:
            self.text_else[1] = "Yes"

    def point_to_str(self, point):  # строковое представление точки
        return "(" + str(point[0]) + ", " + str(point[1]) + ")"
    

    def set_text_mouse_event(self, settings, mouse_xy):
        if self.is_active_panel:
            self.text_mouse_xy[1] = self.point_to_str(mouse_xy)
           
            if settings.rotated_ball is None:        
                self.text_rotated_ball[1] = "None"
            else:                          
                self.text_rotated_ball[1] = settings.rotated_ball.info

            self.text_is_draw_line[1] = str(settings.is_draw_line)

            if settings.ball_in_game is not None: 
                center = settings.ball_in_game.rect.center
                self.text_ball_in_game[1] = settings.ball_in_game.info + ";  center = " + self.point_to_str(center)
            else:
                self.text_ball_in_game[1] = "None"

            if settings.selected_ball is not None:
                self.text_selected_ball[1] = settings.selected_ball.info
            else:
                self.text_selected_ball[1] = "None"

            if settings.prev_selected_ball is not None:
                self.text_prev_selected_ball[1] = settings.prev_selected_ball.info  
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

   

              
            




      
            
                
          
        

    
