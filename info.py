class Info():
    def __init__(self, is_active_panel):

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

            self.reset()

    def reset(self):
        if self.is_active_panel:
            self.text_mousebuttondown = ["MOUSEBUTTONDOWN: ", ""]
            self.text_mousebuttonup = ["MOUSEBUTTONUP: ", ""]  
            self.text_mousemotion = ["MOUSEMOTION: ", ""]
            self.text_else = ["other motion: ", ""]
            self.text_rotated_ball = ["rotated ball: ", "None"]
            self.text_not_equal = ["", ""]

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
            
                
          
        

    