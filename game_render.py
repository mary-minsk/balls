
from random import randint
import os, random
import pygame, func
from thing import Thing

def del_elements(settings, things, max_len):
    while len(things) > max_len:
        ind = random.randint(0, len(things)-1)
        elem = things.sprites()[ind]
        settings.deleted_things_rect.append((elem.rect, (255, 255, 255)))
        # print("%d elem killed" % (ind))
        elem.kill()
   
def get_things(sc, settings, info): # генерация n
                                        # непересекающихся спрайтов с изображениями предметов  на игровай панели
    THINGS = get_images(30, settings.path_things)
    THINGS_SURF = []
    
    for i in range(len(THINGS)): # изображения вещей
        THINGS_SURF.append(pygame.image.load(THINGS[i]).convert_alpha())

    main_things = pygame.sprite.Group()
    things = pygame.sprite.Group()
    settings.deleted_things_rect = []
    settings.all_attempts = 0

    settings.generated_things_lines = False
    if settings.is_displayed_lines:
        settings.generated_things_lines = True

    things, additional_things_2_3, settings.lines_2_3, unsuitable_things_2_3 = render(2, 3, THINGS_SURF, settings, things, settings.green, 2, info) 
    info.reset_len_things()
    info.display_len_things_2_3(len(additional_things_2_3))
    info.display_unsuitable_things_2_3(unsuitable_things_2_3)
   
    if settings.number_current_things == 5: # 2*3 -1 = 5 elements
    
        if  len(additional_things_2_3) == 6:
            del_elements(settings, additional_things_2_3, 5)
            info.display_del_things(1, "2 x 3", settings.green)
        main_things = additional_things_2_3

    elif settings.number_current_things == 6: # 2*3 = 6 elements
        main_things = additional_things_2_3

    elif settings.number_current_things in range(7,11):  # 2*3 + 2*2 = 10 elements
        
        things, additional_things_2_2, settings.lines_2_2, unsuitable_things_2_2 = render(2, 2, THINGS_SURF, settings, things, settings.yellow, 0, info)  
        info.display_unsuitable_things_2_2(unsuitable_things_2_2)
        number_del_elements = len(things) - settings.number_current_things  
        max_len = len(additional_things_2_2) - number_del_elements
        info.display_len_things_2_2(len(additional_things_2_2))
       
        if number_del_elements > 0:
            del_elements(settings, additional_things_2_2, max_len)
            info.display_del_things(number_del_elements, "2 x 2", settings.yellow)

        for thing in additional_things_2_2:
            additional_things_2_3.add(thing)

        main_things = additional_things_2_3
   
    elif settings.number_current_things in range(11,16): # 2*3 + 2*2 + 1*5  = 15 elements
        
        things, additional_things_2_2, settings.lines_2_2, unsuitable_things_2_2 = render(2, 2, THINGS_SURF, settings, things, settings.yellow, 0, info)  
        things, additional_things_1_5, settings.lines_1_5, unsuitable_things_1_5 = render_m(5, THINGS_SURF, settings, things, settings.blue, 1, info)  
        
        info.display_unsuitable_things_2_2(unsuitable_things_2_2)
        info.display_unsuitable_things_1_5(unsuitable_things_1_5)
        
        number_del_elements = len(things) - settings.number_current_things  
        max_len = len(additional_things_1_5) - number_del_elements
        
        info.display_len_things_2_2(len(additional_things_2_2))
        info.display_len_things_1_5(len(additional_things_1_5))
       
        if number_del_elements > 0:
            del_elements(settings, additional_things_1_5, max_len)
            info.display_del_things(number_del_elements, "1 x 5", settings.blue)
        
        for thing in additional_things_2_2:
            additional_things_2_3.add(thing)

        for thing in additional_things_1_5:
            additional_things_2_3.add(thing)

        main_things = additional_things_2_3
    else:
        things, additional_things_1_5, settings.lines_1_5, unsuitable_things = render_m(5, THINGS_SURF, settings, things, settings.blue, 2, info)  
        main_things = things
    
    # print(len(main_things))
    return main_things

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
    additional_things = pygame.sprite.Group()
    unsuitable_things = 0
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
                    additional_things.add(thing)
                else:
                    unsuitable_things +=1 
            
                if settings.is_displayed_lines:
                    rect = (step_x*i + settings.left_margin + shift, step_y*j + settings.up_margin + shift, step_x - 2*shift, step_y - 2*shift)
                    lines.append((rect, color))
                current_attempt += 1
            settings.all_attempts += current_attempt
    # print("unsuitable_things  = %d" % (unsuitable_things))
    return things, additional_things, lines, unsuitable_things

def render_m(m, THINGS_SURF, settings, things, color, shift, info):# игровое поле разбивается на m равных частей по вертикале. В каждом прямоугольнике по одной точке
    W, H = settings.game_panel.w, settings.game_panel.h
    lines = []
    step_y = H/m
    additional_things = pygame.sprite.Group()
    unsuitable_things = 0
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
                additional_things.add(thing)
                is_point_found = True
            else:
                unsuitable_things +=1
        
            if settings.is_displayed_lines:
                rect = (settings.left_margin + shift, int(step_y*j) + shift + settings.up_margin, W - 2*shift, int(step_y) - 2*shift)
                lines.append((rect, color))
                
            current_attempt += 1
    # print("unsuitable_things 1 5 = %d" % (unsuitable_things))
    return things, additional_things, lines, unsuitable_things

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


