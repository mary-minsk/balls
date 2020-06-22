
from random import randint
import os, random
import pygame
from thing import Thing
# from info import Info

def render(n, m, W, H, settings, point_shift = 0): # игровое поле разбивается на m равных частей по вертикале в n столбцах. 
                            #    по одной точке в каждом прямоугольнике
    points = []
    step_x = W//n
    step_y = H//m
    print("step_y")
    print(step_y)
    lines = []
    lines_last = []
    m +=1
    for i in range(n):
        if settings.is_displayed_lines:
            lines.append([])
            print(i)
        for j in range(m):

            x = randint(step_x*i, step_x*i+step_x)
            y = randint(step_y*j, step_y*j+step_y)
            if j!=m-1:
                points.append((x, y))
          
            if settings.is_displayed_lines:
                point_a = (step_x*i + settings.left_margin + 4 , step_y*j + settings.up_margin + point_shift)
                point_b = (step_x*i+step_x+ settings.left_margin - 4, step_y*j + settings.up_margin + point_shift)
                lines[i].append((point_a, point_b))

    
    # print((n, m))
    # print(lines)
    # lines.append(lines_last)      
    # print(lines)
    
    
    # print(lines_last)
    # print("*****")
    return points, lines

def render_m(m, W, H, settings):# игровое поле разбивается на m равных частей по вертикале. В каждом прямоугольнике по одной точке
    points = []
    lines = []
    step_y = H//m
    m +=1
    for j in range(m):
        x = randint(0, W)
        y = randint(step_y*j, step_y*j+step_y)
        if j != m-1:
            points.append((x, y))

        if settings.is_displayed_lines:
            point_a = (0 + settings.left_margin, step_y*j + settings.up_margin)
            point_b = (W + settings.left_margin, step_y*j + settings.up_margin)
            lines.append((point_a, point_b))
            # if j == m-1:
            #     # point_a = (0 + settings.left_margin, step_y*j + step_y + settings.up_margin)
            #     # point_b = (W + settings.left_margin, step_y*j + step_y + settings.up_margin)
            #     lines.append((point_a, point_b))
                

    # print(m_lines)
    return points, lines

def get_points_list(W, H, settings):
    points_2_3, settings.lines_2_3 = render(2, 3, W, H, settings, -1) 
    points_2_2, settings.lines_2_2 = render(2, 2, W, H, settings, 1)  
    points_1_5, settings.lines_1_5 = render_m(5, W, H, settings)   
    list = points_1_5 + points_2_2 + points_2_3  
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
    
    # print(game_panel.w)
    # print(game_panel.w)
    
    # //points_list = get_points_list(settings.screen_width - 2 * offset, settings.screen_height- 2 * offset)
    points_list = get_points_list(game_panel.w, game_panel.h, settings)
    
        # settings.screen_height- 2 * offset)
    
    while index_things < n and attempt < n*3:
        if len(points_list)>0: # заранее подготовленный список точек в разных частях поля
            point = points_list.pop()
            new_thing = Thing(point[0] + offset, point[1] + offset, THINGS_SURF[index_things])
        else:
            new_thing = Thing(randint(offset, settings.screen_width - offset), randint(offset, settings.screen_height +
                                                     settings.height_bottom_panel - settings.height_bottom_panel - offset), THINGS_SURF[index_things])
        blocks_hit_list = pygame.sprite.spritecollide(new_thing, things, False, pygame.sprite.collide_circle)
        if len(blocks_hit_list) == 0:
            things.add(new_thing)
            index_things += 1
        attempt += 1
    # print(attempt)    
    info.display_things_attempts(attempt)
    return things
   
    