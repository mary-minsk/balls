from button import Button
class Info():
    def __init__(self, is_active_panel, is_displayed_lines):

        self.is_active_panel = is_active_panel
        self.hints = ["Сhoose the whirlwind!", "Drag the ball to things!","Use mouse to aim",\
            "Aim at things and press space!", \
            "Harvesting...", "Oops!...I did it again!"]
        
        if is_active_panel:

            self.text_game_info = ["Game info", ""]
            self.text_event = ["event.pos:", ""]
            self.text_prev_selected_ball = ["prev selected ball: ", "None"]
            self.text_selected_ball = ["selected ball: ", "None"]
            self.text_mouse_xy = ["mouse: ", ""]
            self.text_line = ["______________________________", ""]
            self.text_number_things = ["number of things: ",""]  
            self.text_things_attempts = ["attempts to generate the things: ",""]

            self.text_generated_things = ["Generated things", ""]
            self.attempts_one_cell = ["attempts to place thing in one color cell < ", ""]

            self.reset()
            self.reset_len_things()
            
            self.text_switch = ["Lines on", "Lines off"]
            self.show_lines = [427, 569, 90, 30]
            self.switch_lines = is_displayed_lines
            self.switch()
            self.message =["all things will be regenerated",""]
            self.show_lines_button = Button(self.show_lines, self.get_text_switch(), 22)
            
    def check_click(self, mouse_xy, settings):
        if self.is_active_panel:
            if self.show_lines_button.isOver(mouse_xy):
                        
                settings.is_displayed_lines = not settings.is_displayed_lines
                self.show_lines_button.text = self.switch()
                             
                if not settings.generated_things_lines:
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
        self.text_else = ["other motion: ", ""]
        self.text_rotated_ball = ["rotated ball: ", "None"]
        self.text_not_equal = ["", ""]

    def reset_len_things(self):
        
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
        
        self.unfit_2_3 = 0
        self.unfit_2_2 = 0
        self.unfit_1_5 = 0
        self.del_things_text_color = None
           

    def display_not_equal_balls(self):
        if self.is_active_panel:
            self.text_not_equal = ["prev selected ball!=selected ball", ""]

    def display_balls(self, selected_ball, prev_selected_ball):
        if self.is_active_panel:
            if selected_ball is not None:
                self.text_selected_ball[1] = selected_ball.info
            else:
                self.text_selected_ball[1] = "None"

            if prev_selected_ball is not None:
                self.text_prev_selected_ball[1] = prev_selected_ball.info  
            else:
                self.text_prev_selected_ball[1] = "None"   

    def display_mousebuttondown(self, text):
        if self.is_active_panel:
            self.text_mousebuttondown[1] = text

    def display_other(self):
        if self.is_active_panel:
            self.text_else[1] = "Yes"

    def display_mouse_xy(self, text):
        if self.is_active_panel:
            self.text_mouse_xy[1] = text

    def display_rotated_ball(self, text):
        if self.is_active_panel:
            self.text_rotated_ball[1] = text

    def display_text_mousemotion(self, text):
        if self.is_active_panel:
            self.text_mousemotion[1] = text

    def display_mousebuttonup(self, text):
        if self.is_active_panel:
            self.text_mousebuttonup[1] = text  

    def display_number_things(self, n):
        self.text_number_things[1] = str(n)

    def display_things_attempts(self, n):
        self.text_things_attempts[1] = str(n)

    def display_len_things_2_3(self, n):
        if self.is_active_panel:
            self.len_things_2_3= n
            self.text_len_things_2_3[1] = str(n) + "  "

    def display_len_things_2_2(self, n):
        if self.is_active_panel:
            self.len_things_2_2 = n
            self.text_len_things_2_2[1] = str(n)+ "  "

    def display_len_things_1_5(self, n):
        if self.is_active_panel:
            self.len_things_1_5 = n
            self.text_len_things_1_5[1] = str(n)+ "  "


    def display_unsuitable_things_2_3(self, n):
        if self.is_active_panel:
            self.unfit_2_3 = n
            self.text_unsuitable_things_2_3[1] = str(n) + " "

    def display_unsuitable_things_2_2(self, n):
        if self.is_active_panel:
            self.unfit_2_2 = n
            self.text_unsuitable_things_2_2[1] = str(n) + " "

    def display_unsuitable_things_1_5(self, n):
        if self.is_active_panel:
            self.unfit_1_5 = n
            self.text_unsuitable_things_1_5[1] = str(n) + " "

    def display_del_things(self, n, text, color):
        if self.is_active_panel:
            self.del_things = n
            if n >0: 
                self.text_deleted[0] = " excess "+ text + " things, (deleted): " + str(n) 
                self.text_deleted[1] = " "
                self.del_things_text_color = color  
            




      
            
                
          
        

    