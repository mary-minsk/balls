
from random import randint
import os, random
import pygame
from thing import Thing

def get_things(n, sc, settings, things, info): # генерация n
                                        # непересекающихся спрайтов с изображениями предметов  на игровай панели
    THINGS = get_images(30, settings.path_things)
    THINGS_SURF = []
    
    for i in range(len(THINGS)): # добавление изображения 10 вещей
        THINGS_SURF.append(pygame.image.load(THINGS[i]).convert_alpha())

    settings.deleted_things_rect = []
    settings.all_attempts = 0
    thing_2_3, settings.lines_2_3 = render(2, 3, THINGS_SURF, settings, things, settings.lime, 2, info) 
    thing_2_2, settings.lines_2_2 = render(2, 2, THINGS_SURF, settings, things, settings.yellow, 0, info)  
    thungs_1_5, settings.lines_1_5 = render_m(5, THINGS_SURF, settings, things, settings.blue, 1, info)   
    info.display_things_attempts(settings.all_attempts)

        #     new_thing = Thing(randint(offset, settings.screen_width - offset), randint(offset, settings.screen_height +
        #                                              settings.height_bottom_panel - settings.height_bottom_panel - offset), THINGS_SURF[index_things])
   
    return thungs_1_5

def check_possible_place(settings, things, thing_surf, possible_point, rect_color):
    
    new_thing = Thing(possible_point[0] + settings.left_margin, possible_point[1] + settings.up_margin, thing_surf)
     
    if settings.is_displayed_lines:
        new_thing.rect_color = rect_color

    blocks_hit_list = pygame.sprite.spritecollide(new_thing, things, False, pygame.sprite.collide_circle)

    if len(blocks_hit_list) == 0:
        if pygame.Rect(settings.game_panel).contains(new_thing.rect):
            return new_thing
        else: 
            settings.deleted_things_rect.append((new_thing.rect, rect_color))
    else:
        settings.deleted_things_rect.append((new_thing.rect, rect_color))
    return None
   
def render(n, m, THINGS_SURF, settings, things, color, shift, info): # игровое поле разбивается на m равных частей по вертикале в n столбцах. 
                            #    по одной точке в каждом прямоугольнике
    W, H = settings.game_panel.w, settings.game_panel.h
    step_x = W//n
    step_y = H//m
    lines = []
    
    for i in range(n):
        for j in range(m):
            current_attempt = 0
            is_point_found = False
            while not is_point_found and current_attempt < settings.attempts_place_thing: 
                possible_point = randint(step_x*i, step_x*i+step_x), randint(step_y*j, step_y*j+step_y)
                serf = THINGS_SURF.pop(0)
                thing = check_possible_place(settings, things, serf, possible_point, color)
                
                if thing is not None:
                    things.add(thing)
                    is_point_found = True
            
                if settings.is_displayed_lines:
                    rect = (step_x*i + settings.left_margin + shift, step_y*j + settings.up_margin + shift, step_x - 2*shift, step_y - 2*shift)
                    lines.append((rect, color))
                current_attempt += 1
            settings.all_attempts += current_attempt
    
    return things, lines

def render_m(m, THINGS_SURF, settings, things, color, shift, info):# игровое поле разбивается на m равных частей по вертикале. В каждом прямоугольнике по одной точке
    W, H = settings.game_panel.w, settings.game_panel.h
    lines = []
    step_y = H/m
    
    for j in range(m):
        
        is_point_found = False
        current_attempt = 0
        while not is_point_found and current_attempt < settings.attempts_place_thing: 

            possible_point = randint(0, W), randint(int(step_y*j), int(step_y*(j+1)))
            serf = THINGS_SURF.pop(0)
            thing = check_possible_place(settings, things, serf, possible_point, color)
            current_attempt +=1
            settings.all_attempts += 1

            if thing is not None:
                things.add(thing)
                is_point_found = True
        
            if settings.is_displayed_lines:
                rect = (settings.left_margin + shift, int(step_y*j) + shift+ settings.up_margin, W - 2*shift, int(step_y) - 2*shift)
                lines.append((rect, color))
                
            current_attempt += 1
    
    return things, lines

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


