import pygame
from math import sqrt, hypot, sin, cos, atan2
import game_render
from deleted_things import Deleted_thing


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

def mouse_inside_ball_in_game(settings):
    mouse_xy = settings.mouse_xy
    if settings.ball_in_game is not None:
        dx = settings.ball_in_game.x - mouse_xy[0]
        dy = settings.ball_in_game.y - mouse_xy[1]
        distance_square = dx ** 2 + dy ** 2

        if distance_square > settings.ball_in_game.radius**2:
            if pygame.Rect(settings.border_game_panel).collidepoint(mouse_xy):
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


# def jump_ball_on(balls, next_ball):

#     for i, ball in enumerate(balls):
#         if ball != next_ball:
#             ball.go_home(True)
#         else:
#             ball.isJump = True


def jump_ball_on(ball_in_game, next_ball):

    ball_in_game.go_home(True)
    next_ball.isJump = True

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
    
    index = current_ball.index
    if len(balls) > 1:
        if  index  + 1 != len(balls):
            return balls.sprites()[index + 1]
        else:
            return balls.sprites()[0]
    else:
        return None
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
            settings.selected_ball.go_home()
            settings.ball_in_game = None
            

    elif settings.selected_ball.y > settings.screen_height - settings.height_bottom_panel - settings.bottom_margin:  # мяч оставлен снизу, не на панеле мячей
        settings.selected_ball.go_home()
        settings.ball_in_game = None

def check_correct_up_left_right_border(ball, settings, check_bottom_border = False):

    if ball.y < settings.up_margin + ball.radius:
        ball.y = settings.up_margin + ball.radius

    if ball.x < settings.left_margin + ball.radius:
        ball.x = settings.left_margin + ball.radius

    if ball.x > settings.screen_width - settings.right_margin - ball.radius:
        ball.x = settings.screen_width - settings.right_margin - ball.radius

    if check_bottom_border:   # проверка для класса Ball. При нажатии стрелок мяч не должен выйти за пределы игрового поля
        if ball.y + ball.radius > settings.screen_height - settings.height_bottom_panel - settings.bottom_margin:
            ball.y = settings.screen_height - settings.height_bottom_panel - \
                settings.bottom_margin - ball.radius

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


# def get_pygame_point(pos_center_ball, pos_edge):  # перевод координат из декартовых четвертей обратно в пигейм
#     x0 = pos_center_ball[0]  # центр шара в пигейм координатах
#     y0 = pos_center_ball[1]
#     x1 = pos_edge[0]  # декартова система координат
#     y1 = pos_edge[1]
#     (x, y) = (0, 0)

# перевод координат из декартовых четвертей обратно в пигейм
def get_pygame_point(settings, pos_center_ball, point):

    x0, y0 = pos_center_ball
    x1, y1 = point  # декартова система координат

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
    # print(center_ball_xy)
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

def draw_tips(sc, settings, pos_center_ball):  # На месте пересечения окружности шара с последующей траекторией движения
                             # будет находиться наконечник. Но только в момент прицеливания и движения
    ball = settings.ball_in_game

    angle = atan2(settings.a, settings.b)
    tip1_x, tip1_y = get_pygame_point(settings, pos_center_ball,
                                      (round(ball.radius * sin(angle)), round(ball.radius * cos(angle))))
    pygame.draw.circle(sc, settings.yellow, (tip1_x, tip1_y), 4, 0)

    z = 7/57.2958
    ang1 = angle-z
    ang2 = angle+z
    (arrow1_x, arrow1_y) = get_pygame_point(settings, pos_center_ball,
                                            (round(ball.radius * sin(ang1)), round(ball.radius * cos(ang1))))
    (arrow2_x, arrow2_y) = get_pygame_point(settings, pos_center_ball,
                                            (round(ball.radius * sin(ang2)), round(ball.radius * cos(ang2))))
    pygame.draw.circle(sc, settings.red, (arrow1_x, arrow1_y), 2, 0)
    pygame.draw.circle(sc, settings.red, (arrow2_x, arrow2_y), 2, 0)
    settings.tip_x, settings.tip_y = tip1_x, tip1_y

def draw_tips2(sc, settings, pos_center_ball):  # На месте пересечения окружности шара с последующей траекторией движения
                             # будет находиться наконечник. Но только в момент прицеливания и движения
    ball = settings.ball_in_game

    angle = atan2(settings.a, settings.b)
    tip1_x, tip1_y = get_pygame_point(settings, pos_center_ball,
                                      (round(ball.radius * sin(angle)), round(ball.radius * cos(angle))))
    pygame.draw.circle(sc, settings.yellow, (tip1_x, tip1_y), 4, 0)

    z = 7/57.2958
    ang1 = angle-z
    ang2 = angle+z
    (arrow1_x, arrow1_y) = get_pygame_point(settings, pos_center_ball,
                                            (round(ball.radius * sin(ang1)), round(ball.radius * cos(ang1))))
    (arrow2_x, arrow2_y) = get_pygame_point(settings, pos_center_ball,
                                            (round(ball.radius * sin(ang2)), round(ball.radius * cos(ang2))))
    pygame.draw.circle(sc, settings.red, (arrow1_x, arrow1_y), 2, 0)
    pygame.draw.circle(sc, settings.red, (arrow2_x, arrow2_y), 2, 0)
    # settings.tip_x, settings.tip_y = tip1_x, tip1_y



def build_speedway(settings, speed):  # Построение пути движения шара с учетом его скорости

    n = len(settings.all_path_points)  # количество всех точек траектории
    len_path_acceleration = round(settings.path_acceleration * n)

    acceleration, slowdown = game_render.get_acceleration(len_path_acceleration, speed-1)
    acceleration_sum = sum(acceleration)

    constant_number_points = (n - 2 * acceleration_sum)//speed
    constant_speed_list = [speed for i in range(constant_number_points)]

    generated_list = acceleration + constant_speed_list + slowdown  # какие точки не будут отброшены (каждая вторая, третья)
    total_sum = sum(generated_list)
    diference = n - total_sum
    # print("diference = %d" %(diference))
    if diference in range(1, speed):  # в сгенерированном списке всех точек траектории мяча добавляем
        # один недостающий элемент, чтобы суммы точек совпали
        if diference in generated_list:
                ind = len(generated_list) - 1 - generated_list[::-1].index(diference)  # дополнительная точка при торможении
                generated_list.insert(ind, diference)

    temp = []
    result = []

    while (len(generated_list)) > 0:  # Отбрасываем лишние точки и нужные точки заносим в список result
        elem = generated_list.pop(0)
        for i in range(0, elem):
            temp.append(i)
            if i == 0:
                result.append(settings.all_path_points[len(temp)-1])
    # print(temp)
    if (len(temp) != n):
        print("Error! len(temp)!=n")
    return result

def launch_ball(settings):  # Пробел или двойное нажатие мыши запускает шар  (создает вихрь). Определение всех точек пути движения шаря
    
    ball = settings.ball_in_game
    ball.isRolling = True
    ball.isJump = False
    point = settings.ball_in_game.center()
    # print(point)
    settings.pos_center_ball = point
    # списки точек (траектории и соответствующих направляющих для последующего движения мяча и исчезновения всех линий)
    # settings.all_path_points, settings.all_dx_dy, settings.disappearing_points = get_all_points(ball.radius, ball.distance, settings.pos_center_ball)
    settings.all_path_points, settings.all_dx_dy, settings.disappearing_points = get_all_points(settings, ball.radius, ball.distance, point)

    settings.disappearing_edges = []  # исчезающие вершины ломаной прямой
    settings.all_path_points = build_speedway(settings, ball.speed)  # отвеиваются точки для скоростного движения
    settings.edges.pop(0)  # Траектория движения начинается не из в позиции мыши,
    settings.edges.insert(0, (settings.tip_x, settings.tip_y))  # а из наконечника ломаной прямой

def get_all_points(settings, radius, max_distance, start_point):  # в момент запуска шара получение всех точек траектории и смещений
    # по осям (для последующего движения наконечника)
    accumulated_distance, last_distance = 0, 0
    is_distance_found = False
    x1, y1 = start_point
    prev_point = start_point
    dx, dy = get_dx_dy(settings)  # смещение по осям, направление последующего удара
    all_path_points = []
    all_dx_dy = []
    x, y = settings.tip_x, settings.tip_y
    tip_distance = 0
    tips = []
    tips_dx_dy = []

    while tip_distance < radius and (round(x), round(y)) != start_point:# Начало исчезающей траектории не из центра мяча, 
                                                                        # а их точки на окружности (наконечник)
        x += dx  
        y += dy
        tip_distance = hypot(settings.tip_x - x, settings.tip_y - y)
        tips.append((round(x), round(y)))
        tips_dx_dy.append((dx, dy))

        while not is_distance_found:   # Создание 1) списка ускорения/движения/замедления settings.all_path_points
            # 2) списка точек для исчезающей траектории settings.disappearing_points
            # 3) направление наконечников во время схлопывания траектории движения settings.all_dx_dy
            if accumulated_distance + last_distance <= max_distance:
                is_new_point = False
            
                if x1 + dx + settings.right_margin > settings.screen_width - radius or x1 + dx - settings.left_margin < radius:
                    dx = -dx
                    is_new_point = True

                if y1 + dy + settings.bottom_margin + settings.height_bottom_panel > settings.screen_height - radius or y1 + dy - settings.up_margin < radius:
                    dy = -dy
                    is_new_point = True

                if is_new_point:
                    accumulated_distance += hypot(prev_point[0]-x1, prev_point[1]-y1)
                    prev_point = (x1, y1)
                    last_distance = 0

                x1 += dx
                y1 += dy
                last_distance = hypot(prev_point[0]-x1, prev_point[1]-y1)
                all_path_points.append((round(x1), round(y1)))
                all_dx_dy.append((dx, dy))
            else:
                is_distance_found = True

        # if settings.last_path_point != all_path_points[-1]:
        #     print("Error! get_all_points:")
        #     print("Ok settings.last_path_point != settings.all_path_points[-1]")

    return all_path_points, tips_dx_dy + all_dx_dy, tips + all_path_points

def check_holding_arrow_keys(settings):

    if settings.ball_in_game is not None:
        if settings.ball_in_game.moving_right or settings.ball_in_game.moving_left or \
        settings.ball_in_game.moving_up or settings.ball_in_game.moving_down: 
            settings.is_draw_line = mouse_inside_ball_in_game(settings)
            if settings.is_draw_line:
                settings.a, settings.b = get_cartesian_mouse_xy_coordinates(settings)

def continue_ball_moving(ball_in_game, next_ball): # При постояном нажатии стрелок при нажатии Таб следующий мяч продолжает движение
    
    next_ball.moving_right = ball_in_game.moving_right
    next_ball.moving_left = ball_in_game.moving_left
    next_ball.moving_up = ball_in_game.moving_up
    next_ball.moving_down = ball_in_game.moving_down

def draw_tips_disappearing(sc, settings, a, b, pos_center_ball):  # После движения мяча траектория исчезает, наконечник следует за ней
    angle = atan2(-a, b)
    pygame.draw.circle(sc, settings.yellow, pos_center_ball, 3, 0)
    z = 1.571
    ang1 = angle-z
    ang2 = angle+z
    l = 4
    (arrow1_x, arrow1_y) = get_pygame_point(settings, pos_center_ball, (round(l * sin(ang1)), round(l * cos(ang1))))
    (arrow2_x, arrow2_y) = get_pygame_point(settings, pos_center_ball, (round(l * sin(ang2)), round(l * cos(ang2))))
    r = 2
    pygame.draw.circle(sc, settings.red, (arrow1_x, arrow1_y), r, 0)
    pygame.draw.circle(sc, settings.red, (arrow2_x, arrow2_y), r, 0)


def get_disappearing_path(settings):  # Построение исчезающей ломаной прямой. Перед исчезновением мяча на игровой поверхности
    newpoints = []
    if len(settings.disappearing_points) > settings.disappearance:

        del_list = settings.disappearing_points[0:settings.disappearance]
        del_set = settings.all_dx_dy[0:settings.disappearance]  # Также соответствующие направляющие для отображения наконечника

        if settings.edges[0] in del_list:
            settings.edges.pop(0)

        point = del_list[0]
        settings.dxy = del_set[0]

        del settings.disappearing_points[0:settings.disappearance]
        del settings.all_dx_dy[0:settings.disappearance]

        newpoints.append(point)
        newpoints.extend(settings.edges)

        settings.disappearing_edges = newpoints
        settings.disappearance += 1  # Ускорение для стирания ломаной прямой
        # settings.disappearance = 2 # Поточечно
        # print(settings.disappearance)


def draw_disappearing_path(sc,settings):  # Отображение исчезающего пути послеостановки шара
    if len(settings.disappearing_points) > settings.disappearance:
        pygame.draw.aalines(sc, settings.bg_color, False, settings.disappearing_edges)
        draw_tips_disappearing(sc, settings, settings.dxy[0], settings.dxy[1], settings.disappearing_edges[0])
    else:
        settings.is_points_erasing = False

def is_ball_rolling(settings):
    if settings.ball_in_game is not None:
        if settings.ball_in_game.isRolling:
            return True
    return False

def display_last_path_point(sc, settings):  # Отображение конца траектории движения. После вывода на экран всех изображений, чтобы
    #  финальная точка пути не скрывалась за изображениями предметов
    if settings.is_draw_line or is_ball_rolling(settings):
        pygame.draw.circle(sc, settings.yellow, settings.ball_in_game.center(), 2, 0)

    if settings.is_draw_line or is_ball_rolling(settings) or settings.is_points_erasing:
        pygame.draw.circle(sc, settings.red, settings.last_path_point, 4, 0)
        pygame.draw.circle(sc, settings.yellow, settings.last_path_point, 2, 0)

def set_balls_index(balls):

    for i, ball in enumerate(balls):
        ball.index = i

def del_ball(settings, balls, deleted_balls):
    if settings.is_deleted_ball:
        deleted_balls.add(Deleted_thing(settings.ball_in_game.center(), settings.ball_in_game.image, settings.ball_in_game.angle))  # Создание исчезающего вращающегося мяча
        balls.remove(settings.ball_in_game)
        set_balls_index(balls)
        settings.is_deleted_ball = False
        settings.reset()
        settings.edges.pop(0)   # Траектория мяча начинается не с позиции мыши, а с точки на окружности шара
