import pygame
from math import sqrt, hypot, sin, cos, atan2

def display_additional_info(sc, settings, info):

    info.set_number_things(settings.current_number_things)
    info.set_things_attempts()

    # pygame.event:
    show_add_text(sc, settings, info.text_game_info, settings.white, 25, 10, 90)
    show_add_text(sc, settings, info.text_event, settings.white, 20, 30)
    show_add_text(sc, settings, info.text_mousebuttondown, settings.white, 20, 50)
    show_add_text(sc, settings, info.text_mousebuttonup, settings.white, 20, 70)
    show_add_text(sc, settings, info.text_mousemotion, settings.white, 20, 90)
    show_add_text(sc, settings, info.text_else, settings.white, 20, 110)
    show_add_text(sc, settings, info.text_mouse_xy, settings.white, 20, 130)
    show_add_text(sc, settings, info.text_line, settings.white, 20, 140)
    
    # Основные параметры: выбранный мяч, вращающийся, предыдущий выбранный мяч и т. д.
    show_add_text(sc, settings, info.text_selected_ball, settings.white, 20, 180)
    show_add_text(sc, settings, info.text_prev_selected_ball, settings.white, 20, 200) 
    show_add_text(sc, settings, info.text_not_equal, settings.yellow, 20, 220)
    show_add_text(sc, settings, info.text_rotated_ball, settings.white, 20, 240)   
   
    show_add_text(sc, settings, info.text_ball_in_game, settings.white, 20, 260)
    show_add_text(sc, settings, info.text_is_draw_line, settings.white, 20, 280)

    
    # Generated things:
    h = 370
    show_add_text(sc, settings, info.text_line, settings.white, 20, h -20)
    show_generatet_things(sc, settings, info, h)
    
    # кнопка отображения решеток, ячеек, контуров предметов и зон соприкосновения предметов (для наложения)
    info.show_lines_button.draw(sc, settings)

    
    
def show_add_text(sc, settings, text, color, size, h, w = 0, is_border = False, white_border_color = None):  # вывод на экран текста
    # point = h, w
    # show_text(sc, settings, text, color, size, point)
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
    sc.blit(text_surface, text_rect)   
    if is_border:
        if white_border_color is not None :
            pygame.draw.rect(sc, white_border_color, text_rect, 1)
        else:
            pygame.draw.rect(sc, color, text_rect, 1)
    

def show_text(sc, settings, text, color, size, point):  # вывод на экран текста
    font = pygame.font.Font(None, size)
    str1, str2 = "", ""
    if text[0] is not None:
        str1 = text[0]
    if text[1] is not None:
        str2 = text[1]
    all_text = str1+ " " + str2
    text_surface = font.render(all_text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x, text_rect.y = point
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


def mouse_inside_ball_in_game(settings, mouse_pos):
    if settings.ball_in_game is not None:
        dx = settings.ball_in_game.x - mouse_pos[0]
        dy = settings.ball_in_game.y - mouse_pos[1]
        distance_square = dx ** 2 + dy ** 2
        
        if distance_square > settings.ball_in_game.radius**2:
            if pygame.Rect(settings.game_panel).collidepoint(mouse_pos):
                return True
    return False


def get_screen(settings, info):

    if settings.is_used_additional_panel:
        sc = pygame.display.set_mode((settings.screen_width + info.additional_panel_width, settings.screen_height))
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

def set_caption(settings):
    if settings.is_used_additional_panel:
        pygame.display.set_caption(settings.text_additional_panel_caption)
    else:
        pygame.display.set_caption(settings.text_caption)

def draw_cells(sc, settings, info):
    for rect in info.lines_2_3:
        pygame.draw.rect(sc, rect[1], rect[0], 1)

    if settings.current_number_things > 6: 
        for rect in info.lines_2_2:
            pygame.draw.rect(sc, rect[1], rect[0], 1)
            
    if settings.current_number_things > 10:
        for rect in info.lines_1_5:
            pygame.draw.rect(sc, rect[1], rect[0], 1)

    if len(info.deleted_things_rect) > 0:
        for rect in info.deleted_things_rect:
            # pygame.draw.rect(sc, settings.white, rect[0], 2)  
            pygame.draw.rect(sc, rect[1], rect[0], 1)  
            pygame.draw.aaline(sc, rect[1], rect[0].topleft, rect[0].bottomright)
            pygame.draw.aaline(sc, rect[1], rect[0].bottomleft, rect[0].topright)

    if len(info.random_deleted_things_rect) > 0:
        for rect in info.random_deleted_things_rect:
            pygame.draw.rect(sc, settings.white, rect[0], 2)   
            pygame.draw.line(sc, rect[1], rect[0].topleft, rect[0].bottomright, 2)
            pygame.draw.line(sc, rect[1], rect[0].bottomleft, rect[0].topright, 2)
    
def display_info(sc, settings, info):
    if settings.is_used_additional_panel:
        display_additional_info(sc, settings, info)

    if info.is_displayed_lines:
        draw_cells(sc, settings, info)

    display_level(sc, settings)

def display_level(sc, settings):
   
    show_text(sc, settings, settings.text_level, settings.white, 28, settings.level_point_xy)
   

def show_generatet_things(sc, settings, info, h):

    show_add_text(sc, settings, info.text_generated_things, settings.white, 24, h, 50)

    info.attempts_one_cell[1] = str(info.attempts_place_thing)
    # макс. количество попыток разместить предмет в одну выбранную ячейку решетки
    show_add_text(sc, settings, info.attempts_one_cell, settings.white, 20, h + 30)
                    
    # кол-во всех предметов на игровом поле
    show_add_text(sc, settings, info.text_number_things, settings.white, 20, h+50)
    
    
    h1 = h+50
    # решетка 2*3 предметов сгенерировано
    if info.len_things_2_3 > 0:
            show_add_text(sc, settings, info.text_len_things_2_3, settings.green, 22, h1 + 20, 0, True)
    # решетка 2*2 предметов сгенерировано
    if info.len_things_2_2 > 0:
        show_add_text(sc, settings, info.text_len_things_2_2, settings.yellow, 22,  h1 + 40, 0, True)
    # решетка 1*5
    if info.len_things_1_5 > 0:
        show_add_text(sc, settings, info.text_len_things_1_5, settings.blue, 22, h1 + 60, 0, True)
    # случайно сгенерированные предметы, общее количество
    if info.number_random_lines > 0:
        show_add_text(sc, settings, info.text_random_lines, settings.fuchsia, 22, h1 + 80, 0, True)

    # Отброшеные предметы (вышедшие за рамки игрового поля или наложенные на другие предметы)
    if info.unfit_2_3 > 0:
        show_add_text(sc, settings, info.text_unsuitable_things_2_3, settings.green, 22, h1 + 20, 120, True)

    if info.unfit_2_2 > 0:
        show_add_text(sc, settings, info.text_unsuitable_things_2_2, settings.yellow, 22, h1 + 40, 120, True)

    if info.unfit_1_5 > 0:
        show_add_text(sc, settings, info.text_unsuitable_things_1_5, settings.blue, 22, h1+ 60, 120, True)

    if info.random_unfit > 0:
        show_add_text(sc, settings, info.text_random_unfit, settings.fuchsia, 22, h1 + 80, 120, True)

    # сделанных попыток разместить все предметы
    show_add_text(sc, settings, info.text_things_attempts,
                  settings.white, 21, h1 + 100)

    # Случайным образом удаленные лишние предметы с последней наложенной решетки
    if info.del_things > 0:
        show_add_text(sc, settings, info.text_deleted,
                      info.del_things_text_color, 22, h1 + 120, 0, True, settings.white)
    
    # Надпись.Если дополнительные данные о предметах не были сгенерированы для заданного количества предметов, то при нажатии кнопки
    # перегенерировать заданное количество предметов
    if not info.generated_things_lines:
        show_add_text(sc, settings, info.message, settings.white, 20, info.show_lines[1] + 10, 105)


def get_next_ball(current_ball, balls):
    if len(balls)>1:
        if current_ball.index != 2:
            return balls.sprites()[current_ball.index + 1]
        else:
            return balls.sprites()[0]
    else:
        return None


def check_ball_border(settings):

    # Если при нажатии Таб следующий по сету мяч выходит за границы игрового поля, то корректируем его центр
    # Нижняя граница
    if settings.screen_height - settings.height_bottom_panel - settings.bottom_margin in range(settings.next_ball.rect.top, settings.next_ball.rect.bottom):
        if settings.next_ball.y < settings.screen_height - settings.height_bottom_panel - settings.bottom_margin:
            settings.next_ball.y = settings.screen_height - \
                settings.height_bottom_panel - settings.bottom_margin - settings.next_ball.radius
    # Верхняя граница
    if settings.next_ball.y < settings.up_margin + settings.next_ball.radius:
        settings.next_ball.y = settings.up_margin + settings.next_ball.radius

    # Левая граница
    if settings.next_ball.x < settings.left_margin + settings.next_ball.radius:
        settings.next_ball.x = settings.left_margin + settings.next_ball.radius

    # Правая граница
    if settings.next_ball.x > settings.screen_width - settings.right_margin - settings.next_ball.radius:
        settings.next_ball.x = settings.screen_width - settings.right_margin - settings.next_ball.radius


def check_correct_bottom_border(settings):

    if settings.screen_height - settings.height_bottom_panel - settings.bottom_margin in range(settings.selected_ball.rect.top, settings.selected_ball.rect.bottom):
        if settings.selected_ball.y < settings.screen_height - settings.height_bottom_panel - settings.bottom_margin:
            settings.selected_ball.y = settings.screen_height - settings.height_bottom_panel - \
                settings.bottom_margin - settings.selected_ball.radius
        else:
            settings.selected_ball.go_home(settings)

    elif settings.selected_ball.y > settings.screen_height - settings.height_bottom_panel - settings.bottom_margin:  # мяч оставлен снизу, не на панеле мячей
        settings.selected_ball.go_home(settings)


def check_correct_up_left_right_border(settings):

    if settings.selected_ball.y < settings.up_margin + settings.selected_ball.radius:
        settings.selected_ball.y = settings.up_margin + settings.selected_ball.radius

    if settings.selected_ball.x < settings.left_margin + settings.selected_ball.radius:
        settings.selected_ball.x = settings.left_margin + settings.selected_ball.radius

    if settings.selected_ball.x > settings.screen_width - settings.right_margin - settings.selected_ball.radius:
            settings.selected_ball.x = settings.screen_width - settings.right_margin - settings.selected_ball.radius


# Перевод точки (x,y) в декартову систему координат, где (0, 0) - центр тек. шара на игровой панели
def get_new_coordinates(settings):

    x0, y0 = settings.ball_in_game.x, settings.ball_in_game.y
    mouse_x, mouse_y = settings.mouse_xy

    if mouse_x >= x0 and mouse_y >= y0:  # 4 четверть
        x1 = (mouse_x - x0)
        y1 = -(mouse_y - y0)

    elif mouse_x <= x0 and mouse_y <= y0:  # 2 четверть
        x1 = -(x0 - mouse_x)
        y1 = y0 - mouse_y

    elif mouse_x <= x0 and mouse_y >= y0:  # 3 четверть
        x1 = -(x0 - mouse_x)
        y1 = -(mouse_y - y0)

    elif mouse_x >= x0 and mouse_y <= y0:  # 1 четверть
        x1 = mouse_x - x0
        y1 = y0 - mouse_y

    return x1, y1

def get_dx_dy(settings):  # Направляющий вектор. От центра шара на игровой панели до курсора мыши

    a, b = settings.a, settings.b
    da, db = 0, 0

    if a >= 0 and b >= 0:
        da = - 1
        db = 1
    elif a < 0 and b >= 0:
        da = 1
        db = 1
    elif a < 0 and b < 0:
        da = 1
        db = -1
    else:
        da = -1
        db = -1

    if abs(b) > abs(a):
        dx = da * abs(a/b)
        dy = db
    else:
        dx = da
        dy = db * abs(b/a)
    return dx, dy


def build_path(settings):  # определение траектории движения мяча

    radius, max_distance = settings.ball_in_game.radius, settings.ball_in_game.distance

    #  accumulated_distance + current_distance = max_distance. Траектория нужной длины построена: is_path_passed = True
    accumulated_distance = 0
    current_distance = 0
    is_path_passed = False  

    center_ball_xy = settings.ball_in_game.x, settings.ball_in_game.y
    x, y = center_ball_xy    # Начало траектории от центра шара
    prev_point = center_ball_xy

    # смещение по осям, направление последующего удара
    dx, dy = get_dx_dy(settings)

    # список крайних точек ломаной кривой (вершин) для рисования линии
    settings.edges = []
    # settings.edges.append((mouse_x, mouse_y))
    settings.edges.append(settings.mouse_xy)

    # список 5 точек подпрыгивания на месте мяча при прицеливании
    settings.bouncing_ball_points = []
    settings.bouncing_ball_points.append(center_ball_xy)
    balls_x, balls_y = center_ball_xy
    settings.center_ball_xy = center_ball_xy
   
    while not is_path_passed:   # Создание списков     1. для рисования ломанной кривой settings.edges
                                    # 2. подпрыгивания на одном месте во время прицеливания settings.bouncing_ball_points
        if accumulated_distance + current_distance <= max_distance:
            is_new_point = False
            if x + dx > settings.screen_width - radius or x + dx < radius:
                dx = -dx
                is_new_point = True

            if y + dy > settings.screen_height - radius or y + dy < radius:
                dy = -dy
                is_new_point = True

            if is_new_point:
                accumulated_distance += hypot(
                    prev_point[0]-x, prev_point[1]-y)
                settings.edges.append((round(x), round(y)))
                prev_point = (x, y)
                current_distance = 0

            # Первые точки траектории движени мяча сохранияем для подпрыгивания мяча на месте
            if len(settings.bouncing_ball_points) < settings.jump_height_ball:
                balls_x += dx
                balls_y += dy
                settings.bouncing_ball_points.append((round(balls_x), round(balls_y)))

            x += dx
            y += dy
            current_distance = hypot(prev_point[0]-x, prev_point[1]-y)
        else:
            is_path_passed = True

    settings.edges.append((round(x), round(y)))
    settings.last_path_point = (round(x), round(y))

# def draw_tips(sc, settings):  # На месте пересечения окружности шара с последующей траекторией движения

#     # будет находиться наконечник. Но только в момент прицеливания и движения
#     angle = atan2(settings.a, settings.b)
#     ball = settings.ball_in_game
#     pos_center_ball = settings.ball_in_game.x, settings.ball_in_game.y
#     tip1_x, tip1_y = get_pygame_point(pos_center_ball,
#                                       (round(ball.radius * sin(angle)), round(ball.radius * cos(angle))))
#     pygame.draw.circle(sc, settings.yellow, (tip1_x, tip1_y), 4, 0)
#     z = 7/57.2958
#     ang1 = angle-z
#     ang2 = angle+z
#     (arrow1_x, arrow1_y) = get_pygame_point(pos_center_ball,
#                                             (round(ball.radius * sin(ang1)), round(ball.radius * cos(ang1))))
#     (arrow2_x, arrow2_y) = get_pygame_point(pos_center_ball,
#                                             (round(ball.radius * sin(ang2)), round(ball.radius * cos(ang2))))
#     pygame.draw.circle(sc, settings.red, (arrow1_x, arrow1_y), 2, 0)
#     pygame.draw.circle(sc, settings.red, (arrow2_x, arrow2_y), 2, 0)
#     settings.tip_x, settings.tip_y = (tip1_x, tip1_y)







