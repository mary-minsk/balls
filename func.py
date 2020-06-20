import pygame

def display_additional_info(sc, settings, info):

    display_text(sc, settings, info.text_game_info, settings.white, 25, 10, 100)
    display_text(sc, settings, info.text_event, settings.white, 20, 30)
    display_text(sc, settings, info.text_mousebuttondown, settings.white, 20, 50)
    display_text(sc, settings, info.text_mousebuttonup, settings.white, 20, 70)
    display_text(sc, settings, info.text_mousemotion, settings.white, 20, 90)
    display_text(sc, settings, info.text_else, settings.white, 20, 110)
    display_text(sc, settings, info.text_mouse_xy, settings.white, 20, 130)
    display_text(sc, settings, info.text_line, settings.white, 20, 140)
    

    display_text(sc, settings, info.text_selected_ball, settings.white, 22, 180)
    display_text(sc, settings, info.text_prev_selected_ball, settings.white, 22, 200) 
    display_text(sc, settings, info.text_not_equal, settings.yellow, 22, 220)
    display_text(sc, settings, info.text_rotated_ball, settings.white, 22, 240) 
    
def display_text(sc, settings, text, color, size, h, w = 0):  # вывод на экран текста
    font = pygame.font.Font(None, size)
    all_text = text[0]+ " " + text[1]
    text_surface = font.render(all_text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x, text_rect.y = settings.screen_width + 3 + w, h
    # pygame.draw.rect(sc, settings.bg_color, text_rect, 1)
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


    


  