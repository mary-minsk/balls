
from random import randint
import os, random
import pygame
from thing import Thing

def render(n, m, W, H):
    points = []
    step_x = W//n
    step_y = H//m
    for i in range(n):
        for j in range(m):
            x = randint(step_x*i, step_x*i+step_x)
            y = randint(step_y*j, step_y*j+step_y)
            points.append((x, y))
    return points

def render_m(m, W, H):
    points = []
    step_y = H//m
    for j in range(m):
        x = randint(0, W)
        y = randint(step_y*j, step_y*j+step_y)
        points.append((x, y))
    return points

def get_points_list(W, H):
    points_2_3 = render(2, 3, W, H) 
    points_2_2 = render(2, 2, W, H)  
    points_1_4 = render_m(5, W, H)   
    list = points_1_4 + points_2_2 + points_2_3  
    return (list)

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

def get_things(settings, things, THINGS_SURF): # генерация settings.number_things
                                        # непересекающихся спрайтов с изображениями предметов  на игровай панели
    index_things = 0
    attempt = 0
    offset = 30
    n = settings.number_things
    points_list = get_points_list(settings.screen_width - 2 * offset, settings.screen_height- 2 * offset)
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
    return things

    