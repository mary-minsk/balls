import pygame
from math import sqrt, hypot, sin, cos, atan2


def show_text(sc, settings, color, size, point, isCenter = False, str1="", str2=""):  # вывод на экран текста
    font = pygame.font.Font(None, size)
    text = str1+ " " + str2
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x, text_rect.y = point
    if isCenter:
        text_rect.centery = point[1]
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

    info.surf.fill(settings.black)

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


def display_info(sc, settings, info):
    if settings.is_used_additional_panel:
        sc.blit(info.surf, (settings.screen_width, 0))
        info.surf.fill(settings.black)
        info.display_additional_info()
        
    if info.is_displayed_lines:
        info.draw_cells(sc)

    display_level(sc, settings)

    if settings.is_used_hints:
        text = get_hints(settings) 
        font = pygame.font.Font(None, 23)
        text_surface = font.render(text, True, settings.white)
        text_rect = text_surface.get_rect()
        if not settings.is_triker_stop:
            text_rect.x, text_rect.y = (settings.triker_x, settings.screen_height - settings.height_bottom_panel - settings.bottom_margin + 5)
        else:
            text_rect.center = settings.ticker_rect.center
        sc.blit(text_surface, text_rect)
        
        if text_rect.centerx >= settings.ticker_rect.centerx:
            settings.triker_x -= 1
        else:
            settings.is_triker_stop = True
        
   
def get_hints(settings):  # Подсказки

#         # self.hints = ["Сhoose the whirlwind!", "Drag the ball to things!", "Use mouse to aim",
#         #               "Aim at things and press space!",
#         #               "Harvesting...", "Oops!...I did it again!"]
    if settings.ball_in_game is None:
        if settings.selected_ball is None:
            return settings.hints[0]
        else:
            return settings.hints[1]
    else:
        return settings.hints[2]
#         # elif settings.is_ball_selected:
        #     return self.hints[1]
        # elif not settings.is_draw_line and settings.is_ball_pressed and not ball.isRolling:
        #     return self.hints[2]
        # elif settings.is_draw_line and not ball.isRolling:
        #     return self.hints[3]
        # # elif
        # else:
        #     return self.hints[4]

def display_level(sc, settings):
    show_text(sc, settings, settings.white, 28, settings.level_point_xy, False, settings.text_level[0], settings.text_level[1])

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
def get_cartesian_mouse_xy_coordinates(settings):

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

# перевод координат из декартовых четвертей обратно в пигейм
def get_pygame_point(settings, point):

    x0, y0 = settings.ball_in_game.x, settings.ball_in_game.y

    x1 = point[0]  # декартова система координат
    y1 = point[1]

    if x1 >= 0 and y1 >= 0:  # Перевод из первой декартовой четверти в координаты пигейм
        x = x1 + x0
        y = settings.screen_height - y1 - (settings.screen_height - y0)

    elif x1 <= 0 and y1 >= 0:  # Перевод из второй декартовой четверти в координаты пигейм
        x = x0 + x1
        y = y0 - y1

    elif x1 <= 0 and y1 <= 0:  # Перевод из третьей декартовой четверти в координаты пигейм
        x = x0 + x1
        y = y0 - y1

    elif x1 >= 0 and y1 <= 0:  # Перевод из четвертой декартовой четверти в координаты пигейм
        x = x0 + x1
        y = y0 - y1

    return x, y

def get_dx_dy(settings):  # Смещение по осям x и y за один шаг. Одна ось = 1.

    a, b = settings.a, settings.b

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
        dx = da * abs(a / b)
        dy = db
    else:
        dx = da
        dy = db * abs(b / a)
        
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
            if x + dx + settings.right_margin > settings.screen_width - radius or x + dx - settings.left_margin < radius:
                dx = -dx
                is_new_point = True

            if y + dy + settings.bottom_margin + settings.height_bottom_panel > settings.screen_height - radius or y + dy - settings.up_margin < radius:
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

def draw_tips(sc, settings):  # На месте пересечения окружности шара с последующей траекторией движения

    # будет находиться наконечник. Но только в момент прицеливания и движения
    angle = atan2(settings.a, settings.b)
    ball = settings.ball_in_game
    center_ball_xy = settings.ball_in_game.x, settings.ball_in_game.y
    tip1_x, tip1_y = get_pygame_point(settings,
                                      (round(ball.radius * sin(angle)), round(ball.radius * cos(angle))))
    pygame.draw.circle(sc, settings.yellow, (tip1_x, tip1_y), 4, 0)
    z = 7/57.2958
    ang1 = angle-z
    ang2 = angle+z
    (arrow1_x, arrow1_y) = get_pygame_point(settings,
                                            (round(ball.radius * sin(ang1)), round(ball.radius * cos(ang1))))
    (arrow2_x, arrow2_y) = get_pygame_point(settings,
                                            (round(ball.radius * sin(ang2)), round(ball.radius * cos(ang2))))
    pygame.draw.circle(sc, settings.red, (arrow1_x, arrow1_y), 2, 0)
    pygame.draw.circle(sc, settings.red, (arrow2_x, arrow2_y), 2, 0)
    settings.tip_x, settings.tip_y = (tip1_x, tip1_y)









