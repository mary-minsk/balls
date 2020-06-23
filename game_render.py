
from random import randint
import os, random
import pygame
from thing import Thing
# from info import Info

def render(n, m, W, H, settings, color, shift): # игровое поле разбивается на m равных частей по вертикале в n столбцах. 
                            #    по одной точке в каждом прямоугольнике
    points = []
    step_x = W//n
    step_y = H//m
    lines = []
    for i in range(n):
        for j in range(m):

            x = randint(step_x*i, step_x*i+step_x)
            y = randint(step_y*j, step_y*j+step_y)
            points.append(((x, y), color))
          
            if settings.is_displayed_lines:
                rect = (step_x*i + settings.left_margin + shift, step_y*j + settings.up_margin + shift, step_x - 2*shift, step_y - 2*shift)
                lines.append((rect, color))

    return points, lines

def render_m(m, W, H, settings, color, shift = 0):# игровое поле разбивается на m равных частей по вертикале. В каждом прямоугольнике по одной точке
    points = []
    lines = []
    step_y = H/m
    for j in range(m):
        x = randint(0, W)
        y = randint(int(step_y*j), int(step_y*(j+1)))
        # points.append((x, y))
        points.append(((x, y), color))
        if settings.is_displayed_lines:
            rect = (settings.left_margin + shift, int(step_y*j) + shift+ settings.up_margin, W - 2*shift, int(step_y) - 2*shift)
            lines.append((rect, color))
    
    return points, lines

def get_points_list(W, H, settings):
    points_2_3, settings.lines_2_3 = render(2, 3, W, H, settings,settings.lime, 2) 
    points_2_2, settings.lines_2_2 = render(2, 2, W, H, settings, settings.yellow, 0)  

    points_1_5, settings.lines_1_5 = render_m(5, W, H, settings, settings.blue, 1)   
    list = points_2_3 + points_2_2 + points_1_5    # 5+4+6 = 15
    return list

def get_images(n, path):
    path_f = []
    path = os.path.dirname(os.path.abspath(__file__)) + path
    icons = [f for f in os.listdir(path) if f.endswith('.png')]
    index = 0
    if n<=len(icons):
        while len(path_f)<n:
            index = random.randint(0, len(icons)-1)
            full_path = os.path.join(path,icons[index]) # формирование адреса
            icons.pop(index)
            path_f.append(full_path) # добавление адреса в список
    return path_f   

def get_acceleration(n, speed):     # равномерное замедление/ускорение шара на финише или старте для
                                    # просеивания ненужных точек при изменении скорости шара
                                    # settings.path_acceleration = 0.2 означ. что не менее 20% траектории займет #  ускорение и торможение
                                    # Например, цыфра 5 в списке означает, что- в списке точек траектории остается каждая пятая точка, 2 - каждая вторая, 1 - точка не удаляется
    sifted_points = []
    sum = speed * (speed+1) 
    remainder = n//sum
    for i in range(speed):
        for _ in range(remainder+1):
            sifted_points.append(i+1)
    # print(sifted_points)
    return sifted_points, sifted_points[::-1]  # на финише и старте одинаковое изменение (ускорение/замедление    скорости

def get_image(path):
   return os.path.dirname(os.path.abspath(__file__)) + path

def get_things(sc, settings, things, THINGS_SURF, game_panel, info): # генерация settings.number_things
                                        # непересекающихся спрайтов с изображениями предметов  на игровай панели
    index_things = 0
    attempt = 0
    offset = 30
    n = settings.number_things
    
    points_list = get_points_list(game_panel.w, game_panel.h, settings)
    settings.deleted_things_rect = []
    new_thing = None
   
    while index_things < n and attempt < n*3:
        if len(points_list)>0: # заранее подготовленный список точек в разных частях поля
            objects = points_list.pop(0)
            point = objects[0]
            color = objects[1]
            new_thing = Thing(point[0] + settings.left_margin, point[1] + settings.up_margin, THINGS_SURF[index_things])
        
        if settings.is_displayed_lines:
            new_thing.rect_color = color
        # else:
        #     new_thing = Thing(randint(offset, settings.screen_width - offset), randint(offset, settings.screen_height +
        #                                              settings.height_bottom_panel - settings.height_bottom_panel - offset), THINGS_SURF[index_things])
        blocks_hit_list = pygame.sprite.spritecollide(new_thing, things, False, pygame.sprite.collide_circle)
        if len(blocks_hit_list) == 0:
            things.add(new_thing)
            index_things += 1
        else:
            # print(current_thing_rect)
            # pygame.draw.circle(sc, settings.red, current_thing.rect.center, current_thing.radius, 1)
            settings.deleted_things_rect.append(new_thing.rect)
            # pygame.draw.rect(sc, settings.bg_color, new_thing.rect, 1)
            # print(new_thing)
        attempt += 1
     
    info.display_things_attempts(attempt)
    return things
   
    