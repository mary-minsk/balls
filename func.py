import pygame

def display_additional_info(sc, settings, info):

    display_text(sc, settings, info.text_game_info, settings.white, 25, 10, 90)
    display_text(sc, settings, info.text_event, settings.white, 20, 30)
    display_text(sc, settings, info.text_mousebuttondown, settings.white, 20, 50)
    display_text(sc, settings, info.text_mousebuttonup, settings.white, 20, 70)
    display_text(sc, settings, info.text_mousemotion, settings.white, 20, 90)
    display_text(sc, settings, info.text_else, settings.white, 20, 110)
    display_text(sc, settings, info.text_mouse_xy, settings.white, 20, 130)
    display_text(sc, settings, info.text_line, settings.white, 20, 140)
    

    display_text(sc, settings, info.text_selected_ball, settings.white, 20, 180)
    display_text(sc, settings, info.text_prev_selected_ball, settings.white, 20, 200) 
    display_text(sc, settings, info.text_not_equal, settings.yellow, 20, 220)
    display_text(sc, settings, info.text_rotated_ball, settings.white, 20, 240)   
    display_text(sc, settings, info.text_line, settings.white, 20, 250)

    # Generated things
    display_text(sc, settings, info.text_generated_things, settings.white, 24, 280, 50)  

    info.attempts_one_cell[1] = str(settings.attempts_place_thing)
    display_text(sc, settings, info.attempts_one_cell, settings.white, 20, 310)

    display_text(sc, settings, info.text_number_things, settings.white, 20, 330)  

    if info.len_things_2_3 > 0:
        display_text(sc, settings, info.text_len_things_2_3, settings.green, 22, 360, 0, True)
    
    if info.len_things_2_2 > 0:
        display_text(sc, settings, info.text_len_things_2_2, settings.yellow, 22, 380, 0, True)

    if info.len_things_1_5 > 0:
        display_text(sc, settings, info.text_len_things_1_5, settings.blue, 22, 400, 0, True)

    if info.unfit_2_3 > 0:
        display_text(sc, settings, info.text_unsuitable_things_2_3, settings.green, 22, 360, 120, True)
    if info.unfit_2_2 > 0:
        display_text(sc, settings, info.text_unsuitable_things_2_2, settings.yellow, 22, 380, 120, True)
    if info.unfit_1_5 > 0:
        display_text(sc, settings, info.text_unsuitable_things_1_5, settings.blue, 22, 400, 120, True) 
    
    display_text(sc, settings, info.text_things_attempts, settings.white, 21, 420)

    if info.del_things > 0:
        display_text(sc, settings, info.text_deleted, info.del_things_text_color, 22, 440, 0, True, settings.white)

    if not settings.generated_things_lines:
        display_text(sc, settings, info.message, settings.white, 20, info.show_lines[1] + 10, 105)
    
def display_text(sc, settings, text, color, size, h, w = 0, is_border = False, white_border_color = None):  # вывод на экран текста
    font = pygame.font.Font(None, size)
    str1, str2 = "", ""
    if text[0] is not None:
        str1 = text[0]
    if text[1] is not None:
        str2 = text[1]
    all_text = str1+ " " + str2
    text_surface = font.render(all_text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x, text_rect.y = settings.screen_width + 3 + w, h
    if is_border:
        if white_border_color is not None :
            pygame.draw.rect(sc, white_border_color, text_rect, 1)
        else:
            pygame.draw.rect(sc, color, text_rect, 1)
    sc.blit(text_surface, text_rect)   

def get_ball(mouse_pos, balls): # индекс выбранного шара с панели шаров
    
    active_ball = None

    for i, ball in enumerate(balls):
        dx = ball.x - mouse_pos[0] 
        dy = ball.y - mouse_pos[1] 
        distance_square = dx**2 + dy**2 

        if distance_square <= ball.radius**2:
            active_ball = ball

    return active_ball

def get_screen(settings):

    if settings.is_used_additional_panel:
        sc = pygame.display.set_mode((settings.screen_width + settings.additional_panel_width, settings.screen_height))
    else:
        sc = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    return sc

def rotation_balls_off(balls):
    for i, ball in enumerate(balls):
        ball.is_rotated = False

def rotation_ball_on(balls, rotated_ball):

    for i, ball in enumerate(balls):
        if ball != rotated_ball:
            ball.is_rotated = False
        else:
            ball.is_rotated = True

def get_game_panel(settings):
    return pygame.Rect((settings.left_margin, settings.up_margin, \
        settings.screen_width - settings.right_margin - settings.left_margin, settings.screen_height - settings.height_bottom_panel - settings.up_margin))
           


    


  