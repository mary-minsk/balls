
from random import randint
import pygame
import random
from math import sqrt, hypot, sin, cos, atan2


from settings import Settings
import game_render
from ball import Ball
from thing import Thing
from deleted_things import Deleted_thing
from button import Button

def draw_text(surf, text, color, size, point):  # вывод на экран текста
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = point
    surf.blit(text_surface, text_rect)   

def render_n_things(n, things, THINGS_SURF): # генерация settings.number_thingsнепересекающихся спрайтов с изображениями предметов  на игровай панели
    index_things = 0
    attempt = 0
    offset = 30
    points_list = game_render.get_points_list(settings.screen_width - 2 * offset, settings.screen_height- 2 * offset)
    while index_things < n and attempt < n*3:
        if len(points_list)>0: # заранее подготовленный список точек в разных частях поля
            point = points_list.pop()
            new_thing = Thing(point[0] + offset, point[1] + offset, THINGS_SURF[index_things])
        else:
            new_thing = Thing(randint(offset, settings.screen_width - offset), randint(offset, settings.screen_height +
                                                     settings.height_bottom_panel - settings.height_bottom_panel - offset), THINGS_SURF[index_things])
        blocks_hit_list = pygame.sprite.spritecollide(
            new_thing, things, False, pygame.sprite.collide_circle)
        if len(blocks_hit_list) == 0:
            things.add(new_thing)
            index_things += 1
        attempt += 1
    # print(attempt)    
    return things

def get_index_current_ball(mouse_pos): # индекс выбранного шара с панели шаров
    index = -1
    i = 0
    flag = False
    while i < len(balls) and not flag:
        ball_rect = balls.sprites()[i].rect
        if ball_rect.collidepoint(mouse_pos):
            flag = True
            index = i
        i = i+1
    return index

def get_new_coordinates(x0, y0, x, y): #Перевод точки (x,y) в декартову систему координат, где (0, 0) - центр тек. шара
    (x2, y2) = (0, 0)
    if x >= x0 and y >= y0:  # 4 четверть
        x2 = (x-x0)
        y2 = -(y-y0)
    elif x <= x0 and y <= y0:  # 2 четверть
        x2 = -(x0-x)
        y2 = y0-y
    elif x <= x0 and y >= y0:  # 3 четверть
        x2 = -(x0-x)
        y2 = -(y-y0)
    elif x >= x0 and y <= y0:  # 1 четверть
        x2 = x-x0
        y2 = y0-y
    return (x2, y2)

def point_to_str(point): # строковое представление точки
    return "(" + str(point[0])+ ", " + str(point[1]) + ")"

def get_dx_dy(a, b):
    da = 0
    db = 0
    if a >=0 and b>=0:
        da = - 1
        db = 1
    elif a<0 and b>=0:
        da = 1
        db = 1
    elif a<0 and b<0:
        da = 1
        db = -1
    else:
        da = -1
        db = -1

    if abs(b) > abs(a):
        dx = da* abs(a/b)
        dy = db 
    else:
        dx = da
        dy = db * abs(b/a)
    return dx, dy

def build_path(radius, max_distance): # рисование траектории движения мяча
    
    #  accumulated_distance + last_distance = max_distance Когда траектория будет построена и is_distance_found = True
    accumulated_distance = 0    
    last_distance = 0
    is_distance_found = False
    
    x1, y1 = pos_center_ball    # Начало траектории от центра шара
    prev_point = pos_center_ball
    dx, dy = get_dx_dy(settings.a, settings.b)  # смещение по осям, направление последующего удара

    settings.edges = []   # список крайних точек ломаной кривой (вершин) для рисования линии
    settings.edges.append((mouse_x, mouse_y))

    settings.bouncing_ball_points = []  # список 5 точек подпрыгивания на месте мяча при прицеливании
    settings.bouncing_ball_points.append(pos_center_ball) 
    balls_x, balls_y = pos_center_ball
    settings.pos_center_ball = pos_center_ball
    settings.a, settings.b = get_new_coordinates(pos_center_ball[0], pos_center_ball[1], mouse_x, mouse_y)
           
               
    while not is_distance_found:   # Создание списков     1. для рисования ломанной кривой settings.edges
                                                        # 2. подпрыгивания на одном месте во время прицеливания settings.bouncing_ball_points                      
        if accumulated_distance + last_distance <= max_distance:
            is_new_point = False
            if x1 + dx > settings.screen_width - radius or x1 + dx < radius:
                dx = -dx
                is_new_point = True

            if y1 + dy > settings.screen_height - radius or y1 + dy < radius:
                dy = -dy
                is_new_point = True

            if is_new_point:
                accumulated_distance += hypot(prev_point[0]-x1, prev_point[1]-y1)
                settings.edges.append((round(x1), round(y1)))
                prev_point = (x1, y1)
                last_distance = 0
    
            # Первые точки траектории движени мяча сохранияем для подпрыгивания мяча на месте
            if len(settings.bouncing_ball_points)< settings.jump_height_ball: 
                balls_x += dx  
                balls_y += dy
                settings.bouncing_ball_points.append((round(balls_x), round(balls_y)))

            x1 += dx  
            y1 += dy
            last_distance = hypot(prev_point[0]-x1, prev_point[1]-y1)
        else:
            is_distance_found = True

    settings.edges.append((round(x1), round(y1)))
    settings.last_path_point = (round(x1), round(y1))   
   
def get_all_points(radius, max_distance, start_point): # в момент запуска шара получение всех точек траектории и смещений 
                                          # по осям (для последующего движения наконечника)
    accumulated_distance, last_distance  = 0, 0    
    is_distance_found = False
    x1, y1 = start_point    
    prev_point = start_point
    dx, dy = get_dx_dy(settings.a, settings.b)  # смещение по осям, направление последующего удара
    all_path_points = []
    all_dx_dy = []
    x, y = settings.tip_x, settings.tip_y
    tip_distance = 0
    tips = []
    tips_dx_dy = []

    while tip_distance < radius and (round(x), round(y)) != start_point:#Начало исчезающей траектории не из центра мяча, 
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
            if x1 + dx > settings.screen_width - radius or x1 + dx < radius:
                dx = -dx
                is_new_point = True

            if y1 + dy > settings.screen_height - radius or y1 + dy < radius:
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
            all_dx_dy.append((dx,dy))
        else:
            is_distance_found = True
          
    if settings.last_path_point != all_path_points[-1]:
        print("Error! get_all_points:")  
        print("Ok settings.last_path_point != settings.all_path_points[-1]")
    
    return all_path_points, tips_dx_dy + all_dx_dy, tips + all_path_points

def build_speedway(speed):  # Построение пути движения шара с учетом его скорости 
   
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
        if  diference in generated_list:
            ind = len(generated_list) - 1 - generated_list[::-1].index(diference) # дополнительная точка при торможении
            generated_list.insert(ind, diference)
   
    temp = []
    result = []

    while (len(generated_list))>0: # Отбрасываем лишние точки и нужные точки заносим в список result
        elem = generated_list.pop(0)
        for i in range(0, elem):
            temp.append(i)
            if i == 0:
                result.append(settings.all_path_points[len(temp)-1]) 
    # print(temp)
    if (len(temp)!=n):
        print("Error! len(temp)!=n")
    return result

def get_pygame_point(pos_center_ball, pos_edge): # перевод координат из декартовых четвертей обратно в пигейм
    x0 = pos_center_ball[0] #центр шара в пигейм координатах
    y0 = pos_center_ball[1]
    x1 = pos_edge[0]  # декартова система координат
    y1 = pos_edge[1]
    (x, y) = (0, 0)
    if x1 >= 0 and y1 >= 0: # Перевод из первой декартовой четверти в координаты пигейм
        x = x1 + x0
        y = settings.screen_height - y1- (settings.screen_height - y0)
    elif  x1 <= 0 and y1 >= 0: # Перевод из второй декартовой четверти в координаты пигейм
        x = x0 + x1
        y = y0 - y1
    elif  x1 <= 0 and y1 <= 0: # Перевод из третьей декартовой четверти в координаты пигейм
        x = x0 + x1
        y = y0 - y1
        
    elif  x1 >= 0 and y1 <= 0: # Перевод из четвертой декартовой четверти в координаты пигейм
        x = x0 + x1
        y = y0 - y1
        
    return (x, y)

def draw_tips(a, b, pos_center_ball): # На месте пересечения окружности шара с последующей траекторией движения 
                                        # будет находиться наконечник. Но только в момент прицеливания и движения
    angle = atan2(a, b)
    tip1_x, tip1_y = get_pygame_point(pos_center_ball, \
                                            (round(ball.radius * sin(angle)), round(ball.radius * cos(angle))))
    pygame.draw.circle(sc,settings.yellow,(tip1_x, tip1_y), 4,0)
    z=7/57.2958
    ang1 = angle-z
    ang2 = angle+z
    (arrow1_x, arrow1_y) = get_pygame_point(pos_center_ball, (round(ball.radius * sin(ang1)), round(ball.radius * cos(ang1))))
    (arrow2_x, arrow2_y) = get_pygame_point(pos_center_ball, (round(ball.radius * sin(ang2)), round(ball.radius * cos(ang2))))
    pygame.draw.circle(sc, settings.red, (arrow1_x, arrow1_y), 2, 0)
    pygame.draw.circle(sc, settings.red, (arrow2_x, arrow2_y), 2, 0)
    settings.tip_x, settings.tip_y = (tip1_x, tip1_y)

def draw_tips_disappearing(a, b, pos_center_ball): # После движения мяча траектория исчезает, наконечник следует за ней
    angle = atan2(-a, b)
    pygame.draw.circle(sc,settings.yellow, pos_center_ball, 4,0)
    z = 1.571
    ang1 = angle-z
    ang2 = angle+z
    l = 4
    (arrow1_x, arrow1_y) = get_pygame_point(pos_center_ball, (round(l * sin(ang1)), round(l * cos(ang1))))
    (arrow2_x, arrow2_y) = get_pygame_point(pos_center_ball, (round(l * sin(ang2)), round(l * cos(ang2))))
    r = 2
    pygame.draw.circle(sc, settings.red, (arrow1_x, arrow1_y), r, 0)
    pygame.draw.circle(sc, settings.red, (arrow2_x, arrow2_y), r, 0)

def create_balls(): # создание трех шаров, определени6 их скорости движения (settings.balls_speed[i]) и растояния (settings.balls_distance[i])
    BALLS = game_render.get_images(settings.number_balls, settings.path_spirals)
    BALLS_SURF = []

    balls = pygame.sprite.Group()  # создание группы шаров
    shift = settings.left_offset
    list = []
    
    for i in range(settings.number_balls):
        BALLS_SURF.append(pygame.image.load(BALLS[i]).convert_alpha()) # добавление изображения
        w  = BALLS_SURF[i].get_rect()[2] # ширина изображения
        balls.add(Ball(settings, shift + settings.balls_offset*i + w//2, BALLS_SURF[i])) # добавляем в группу три шара
        shift = shift + w 
        list.append((w, i)) 
    
    list = sorted(list)  #сортируем по размеру изображения шара
    distance_dictionary = {}   # маленький шар имеет самую большую скорость и прокатится на самое 
    speed_dictionary = {}      # большое растояние
    
    for i in range(settings.number_balls):
        distance_dictionary[list[i][1]] = settings.balls_distance[i]
        speed_dictionary[list[i][1]] = settings.balls_speed[i]
    
    for i in range(settings.number_balls):  # большой шар катится растояние - H, средний - 2*H, самый маленикий - 3*H                  
        balls.sprites()[i].distance = distance_dictionary.get(i)*settings.unit  # длина пути последующего движения шара 
        balls.sprites()[i].speed = speed_dictionary.get(i) 
        # print(balls.sprites()[i].distance)
    return balls

def create_things(): # создание n (settings.number_things) предметов

    THINGS = game_render.get_images(settings.number_things, settings.path_things)
    THINGS_SURF = []

    for i in range(settings.number_things): # добавление изображения 10 вещей
        THINGS_SURF.append(pygame.image.load(THINGS[i]).convert_alpha())
    
    things = pygame.sprite.Group()
    # генерация n непересекающихся предметов на поверхности
    things = render_n_things(settings.number_things, things, THINGS_SURF)
    return things

def launch_ball():  # Пробел или двойное нажатие мыши запускает шар  (создает вихрь). Определение всех точек пути движения шаря
    ball = balls.sprites()[settings.index_current_ball]
    ball.isRolling = True
    # списки точек (траектории и соответствующих направляющих для последующего движения мяча и исчезновения всех линий)
    settings.all_path_points, settings.all_dx_dy, settings.disappearing_points = get_all_points(ball.radius, ball.distance, settings.pos_center_ball)
    settings.disappearing_edges = []  # исчезающие вершины ломаной прямой
    settings.all_path_points = build_speedway(ball.speed) # отвеиваются точки для скоростного движения
    settings.edges.pop(0)  # Траектория движения начинается не из в позиции мыши, 
    settings.edges.insert(0, (settings.tip_x, settings.tip_y)) # а из наконечника ломаной прямой
       
def get_hints(): # Подсказки
    
    if not settings.is_ball_pressed: return settings.hints[0]
    elif settings.is_ball_selected: return settings.hints[1]
    elif not settings.is_draw_line and settings.is_ball_pressed and not ball.isRolling: return settings.hints[2]
    elif settings.is_draw_line and not ball.isRolling: return settings.hints[3]
    # elif 
    else: return settings.hints[4]

def draw_path_and_tips(pos_center_ball): # Конечные точки ломаной кривой - траектории движения мяча (наконечники)
                                            # и сам путь
    pygame.draw.aalines(sc, settings.bg_color, False, settings.edges)
    draw_tips(settings.a, settings.b, pos_center_ball)

def get_things_hit(): # Мяч сталкивается с предметами. Создается группа удаленных с игровой поверхности предметов
                         # которые поле непродолжительного вращения и уменьшения быстро исчезнут м экрана

    things_set = set(things)
    hit_list_things = pygame.sprite.spritecollide(ball, things, True, pygame.sprite.collide_circle)
    
    for thing in hit_list_things:
        if thing in things_set:
            deleted_balls.add(Deleted_thing(thing.x, thing.y, thing.image))
            things.remove(thing)
    
def create_groups(balls, things, deleted_balls, setting):  # Создание групп вещей и мячей вначале кажного нового уровня
    balls.empty()
    things.empty()
    deleted_balls.empty()
    setting.reset()

    things = create_things()
    balls = create_balls()
    deleted_balls = pygame.sprite.Group()
    
    return balls, things, deleted_balls

def get_disappearing_path(): # Построение исчезающей ломаной прямой. Перед исчезновением мяча на игровой поверхности
    newpoints = []
    if len(settings.disappearing_points) > settings.disappearance:

        del_list = settings.disappearing_points[0:settings.disappearance]
        del_set = settings.all_dx_dy[0:settings.disappearance] # Также соответствующие направляющие для отображения наконечника

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
        
def display_last_path_point():  # Отображение конца траектории движения. После вывода на экран всех изображений, чтобы 
                               #  финальная точка пути не скрывалась за изображениями предметов

    is_display = False
    if settings.is_ball_down:
        if settings.is_draw_line and not ball.isRolling or ball.isRolling:
            is_display = True
    elif settings.is_points_erasing:
        is_display = True

    if is_display:
        pygame.draw.circle(sc, settings.red, settings.last_path_point, 4, 0)
        pygame.draw.circle(sc, settings.yellow, settings.last_path_point, 2, 0)

def draw_disappearing_path(): # Отображение исчезающего пути послеостановки шара
    if len(settings.disappearing_points)>settings.disappearance:
        pygame.draw.aalines(sc, settings.bg_color, False, settings.disappearing_edges)
        draw_tips_disappearing(settings.dxy[0], settings.dxy[1], settings.disappearing_edges[0])
    else:
        settings.is_points_erasing = False

pygame.init()
import os
print(os.getcwd())
print(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.basename)
print(print(os.path.join(os.path.dirname(__file__))) )
print(os.path.dirname(os.path.realpath(__file__)))

settings = Settings()
sc = pygame.display.set_mode((settings.screen_width, settings.screen_height + settings.height_bottom_panel))
sc.fill(settings.black)
pygame.display.update()
pygame.display.set_caption(settings.text_caption)
namef = os.path.dirname(os.path.abspath(__file__)) + settings.background_image
print(namef)
# background_image = pygame.image.load(settings.background_image)
background_image = pygame.image.load(namef)

next_level_button = Button(settings.button_level, settings.button_level_text)
ruler_button = Button(settings.button_ruler, settings.button_ruler_text)

things = create_things()
balls = create_balls()
deleted_balls = pygame.sprite.Group()
 
pos_center_ball = (0, 0)            # пигейм координаты центра выбранного шара в момент выбора направления удара
(mouse_x, mouse_y) = (0, 0)         # тек пигейм координаты мыши
                    
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        settings.is_draw_line = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouse_x, mouse_y) = event.pos
            if event.button == 1:     # нажатием мыши берем шар (ball)
                
                if settings.is_ball_pressed:  # опущен шар на игровую плоскость для последующего движения по ней
                    pos_center_ball = mouse_x, mouse_y
                    ball = balls.sprites()[settings.index_current_ball]
                    ball.isPressed = False
                    ball.isJump = True
                    ball.x1, ball.y1 = mouse_x, mouse_y
                    settings.is_ball_down = True  # при последующем выходе мыши за пределы шара появляется линия - направление последующего удара

                else:   # выбираем один из трех шаров на нижней панели
                    index = get_index_current_ball((mouse_x, mouse_y))
                    if index > -1:
                        ball = balls.sprites()[index]
                        settings.is_ball_pressed = True
                        ball.isPressed = True
                        ball.is_rotated = False
                if next_level_button.isOver((mouse_x, mouse_y)):
                    balls, things, deleted_balls = create_groups(balls, things, deleted_balls, settings)
            
            elif event.button == 3:  # шарик начинает катиться по столу, собирая все предметы на своем пути
                launch_ball()
                
        else:  # отслеживаем все движения мыши
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if not settings.is_ball_down:
                if mouse_y > settings.screen_height:  # область трех шаров(ball) визу экрана
                    index = get_index_current_ball((mouse_x, mouse_y))
                    if index > -1:  # курсор мышки находится над одним из трех шаров внизу экрана, видна рамка
                        settings.is_ball_selected = True
                        settings.index_current_ball = index
                        if settings.index_current_ball != settings.index_prev_ball:
                            prev_ball = balls.sprites()[settings.index_prev_ball]
                            prev_ball.is_rotated = False
                        settings.index_prev_ball = index
  
            else:                           # область предметов, игровая поверхность
                radius = ball.radius
                if radius < round(sqrt((pos_center_ball[0] - mouse_x)*(pos_center_ball[0] - mouse_x)+(pos_center_ball[1] - mouse_y)*(pos_center_ball[1] - mouse_y))):  # растояние от центра шара до мыши
                    settings.is_draw_line = True                 # курсор мыши находится за границей выбранного шара, рисуем линию
                    
                    if not ball.isRolling:      # задаем направление движения мяча (a, b) в декартовой системе координат
                        settings.pos_center_ball = pos_center_ball
                        settings.a, settings.b = get_new_coordinates(pos_center_ball[0], pos_center_ball[1], mouse_x, mouse_y)
                settings.is_ball_selected = False
                ball.is_rotated = False
                    
            if settings.is_ball_down and mouse_y >= settings.screen_height and \
                                    not ball.isRolling and not settings.is_points_erasing:  #  шар возвращается обратно на панель шаров
                ball.move_balls_panel()
                settings.reset()  # сброс параметров

        if event.type == pygame.KEYDOWN: # при рисовании траектории движения можно поьзоваться стрелками
            if settings.is_draw_line:
                if event.key == pygame.K_SPACE:
                    launch_ball()      
                if event.key == pygame.K_RIGHT:
                    mouse_x +=1
                elif event.key == pygame.K_LEFT:
                    mouse_x -=1
                elif event.key == pygame.K_UP:
                    mouse_y -= 1
                elif event.key == pygame.K_DOWN:
                    mouse_y +=1
                pygame.mouse.set_pos(mouse_x, mouse_y)
                    
    sc.blit(background_image,(0, 0))

    pygame.draw.rect(sc, settings.bg_color, (0, 0, settings.screen_width, settings.screen_height), 2)
    pygame.draw.rect(sc, settings.bg_color, (0, settings.screen_height, settings.screen_width, settings.screen_height + settings.height_bottom_panel), 2)
   
    if settings.is_ball_selected and not settings.is_ball_pressed: # Выбор любого одного мяча на нижней панели
        ball = balls.sprites()[settings.index_current_ball]
        if not settings.is_draw_line and not settings.is_points_erasing: #  Во время движения мячи на панели выбрать нельзя
            ball.is_rotated = True

    if settings.is_ball_down:  # Мяч на игровой поверхности
        if settings.is_draw_line and not ball.isRolling and not settings.is_points_erasing: # Момент прицеливания
            build_path(ball.radius, ball.distance) # строим путь (ломаная кривая) и собираем информацию о движении мяча
            draw_path_and_tips(pos_center_ball)
            
        elif ball.isRolling:   # продолжаем рисовать траекторию движения мяча и крайние точки этой линии 
            draw_path_and_tips(settings.pos_center_ball)
            get_things_hit()

    if settings.is_points_erasing: # Мяч проделал весь путь, но не исчезнул. Ломаная линия исчезает
        if settings.is_deleted_ball: 
            deleted_balls.add(Deleted_thing(ball.x1, ball.y1, ball.image, ball.angle)) # Создание исчезающего вращающегося мяча
            balls.remove(ball)
            settings.is_deleted_ball = False
            settings.reset() 
            settings.edges.pop(0)  # Траектория мяча начинается не с позиции мыши, а с точки на окружности шара
            
        get_disappearing_path()
        draw_disappearing_path()
                
    draw_text(sc, get_hints(), settings.white, 20, (130, settings.screen_height+ 5))
    
    draw_text(sc, settings.text2, settings.white, 20, (30, settings.screen_height+ 5))
    draw_text(sc, settings.text1, settings.white, 20, (230, settings.screen_height+ 5))
    draw_text(sc, settings.text3, settings.white, 20, (330, settings.screen_height+ 15))

    next_level_button.draw(sc, settings)
    ruler_button.draw(sc, settings)

    things.update(things)
    things.draw(sc)

    balls.update(settings, sc)
    balls.draw(sc)
    
    deleted_balls.draw(sc)
    deleted_balls.update(settings)

    display_last_path_point() 

    pygame.display.update()
    pygame.time.delay(20)
   
    # settings.text1 = str(len(balls))
    # settings.text2 = str(len(things))
    # settings.text1 = "mouse " + str((mouse_x, mouse_y))
    # settings.text2 = str(settings.pos_center_ball)
    # settings.text1 = str(settings.index_current_ball)
    # settings.text2 = str(len(things))
    # settings.text1 = str(settings.is_draw_line)
    # settings.text2 = "ball_down " + str(settings.is_ball_down)

pygame.quit()


