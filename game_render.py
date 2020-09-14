
from random import randint
import os, random
import pygame
from thing import Thing

def del_elements(info, things, max_len, color):
    while len(things) > max_len:
        ind = random.randint(0, len(things)-1)
        elem = things.sprites()[ind]
        info.random_deleted_things_rect.append((elem.rect, color)) 
        # print("%d elem killed" % (ind))
        elem.kill()
   
def get_things(sc, settings, info): # генерация n = settings.current_number_things
                                    # непересекающихся спрайтов с изображениями предметов  на игровай панели
    THINGS = get_images(settings.max_things_images, settings.path_things) # 30 случайных изображений и максимум 20 предметов на игровом поле
    THINGS_SURF = []
   
    for i in range(len(THINGS)):  # изображения вещей
        surf = pygame.image.load(THINGS[i]).convert_alpha()
        if settings.balls_size_reduction[settings.current_difficulty] != 100:
            new_size = surf.get_width() * settings.balls_size_reduction[settings.current_difficulty] // 100, \
                surf.get_height() * settings.balls_size_reduction[settings.current_difficulty] // 100
            surf = pygame.transform.scale(surf, (new_size))
        THINGS_SURF.append(surf)

    main_things = pygame.sprite.Group()
    things = pygame.sprite.Group()
   
    info.reset_things_text()

    info.generated_things_lines = False #  Флаг, сгенерированы ли все рамки у предметов, текст за кнопкой на    доп. панели. Если нет, то после нажатия кнопки все предметы будут перегенерированы
    if info.is_displayed_lines:
        info.generated_things_lines = True

    # Решетка 2*3 = 6. Игровое поле делится на 6 частей (ячеек) и в каждой прямоугольной части находится центр с изображением предмета
    # в группу предметов things  -  может вхдить три различных разбиений игрового поля (2*3, 2*2, 1*5) и еще случайно сгенерированные предметы
    # things нужна для предотвращения наложения предметов и их выхода за пределы поля. Лишние предметы удаляются
    # Если элементов не хватает (в какой-то ячейке было сделано 3 неудачных попытки разместить предмет), то 
    # случайным образом генерируется еще один предмет, уже без каких-либо ограничений (решеток). Например когда 4+6 =10 предметов и одна ячейка оказалась пустой
    # main_things - окончательный список. Формируется путем последовательного объединения всех ячеек (2*3, 2*2, 1*5) и зависит от заданного числа settings.current_number_things 

    things, additional_things_2_3, info.lines_2_3, unsuitable_things_2_3 = render(2, 3, THINGS_SURF, settings, things, settings.green, 2, info) 

    info.set_text_len_things_2_3(len(additional_things_2_3))
    info.set_text_unsuitable_things_2_3(unsuitable_things_2_3)
    # print(" len(additional_things_2_3) = %d elem" % (len(additional_things_2_3)))
    # print(" settings.current_number_things = %d elem" % settings.current_number_things)
    
    if settings.current_number_things <= 5:  # 2*3 -1 = 5 elements
        number_del_elements = len(things) - settings.current_number_things
        max_len = len(additional_things_2_3) - number_del_elements

        if number_del_elements > 0:
            del_elements(info, additional_things_2_3, max_len, settings.green)
            info.set_text_del_things(number_del_elements, "2 x 3", settings.green)
        main_things = additional_things_2_3

    elif settings.current_number_things == 6: # 2*3 = 6 elements. Возможно, все 6 элементов уже сгенерированы
        main_things = additional_things_2_3

    elif settings.current_number_things in range(7,11):  # 2*3 + 2*2 = 10 elements
        # Вторая решетка 2*2 = 4. Накладывается еще одна решетка. Максимум еще 4 предмета. Не более трех попыток разместить предмет в одну ячейку
        things, additional_things_2_2, info.lines_2_2, unsuitable_things_2_2 = render(2, 2, THINGS_SURF, settings, things, settings.yellow, 0, info)  
        
        info.set_text_len_things_2_2(len(additional_things_2_2))
        info.set_text_unsuitable_things_2_2(unsuitable_things_2_2)

        number_del_elements = len(things) - settings.current_number_things  
        max_len = len(additional_things_2_2) - number_del_elements
       
        if number_del_elements > 0:  # Лишние предметы удаляются из группы
            del_elements(info, additional_things_2_2, max_len, settings.yellow)
            info.set_text_del_things(number_del_elements, "2 x 2", settings.yellow)

        for thing in additional_things_2_2:   # Объединяем 2 группы
            additional_things_2_3.add(thing)

        main_things = additional_things_2_3
   
    # elif settings.current_number_things in range(11,16): # 2*3 + 2*2 + 1*5  = 15 elements
    elif settings.current_number_things >=11: # 2*3 + 2*2 + 1*5  = 15 elements
        # Вторая решетка 2*2 = 4.
        things, additional_things_2_2, info.lines_2_2, unsuitable_things_2_2 = render(2, 2, THINGS_SURF, settings, things, settings.yellow, 0, info)  
        # Третья решетка 1*5 = 5. Максимум 5 предметов
        things, additional_things_1_5, info.lines_1_5, unsuitable_things_1_5 = render_m(5, THINGS_SURF, settings, things, settings.blue, 1, info)  
        
        info.set_text_unsuitable_things_2_2(unsuitable_things_2_2)
        info.set_text_unsuitable_things_1_5(unsuitable_things_1_5)
        
        number_del_elements = len(things) - settings.current_number_things  
        max_len = len(additional_things_1_5) - number_del_elements
        
        info.set_text_len_things_2_2(len(additional_things_2_2))
        info.set_text_len_things_1_5(len(additional_things_1_5))
       
        if number_del_elements > 0:
            del_elements(info, additional_things_1_5, max_len, settings.blue)
            info.set_text_del_things(number_del_elements, "1 x 5", settings.blue)
        
        for thing in additional_things_2_2:
            additional_things_2_3.add(thing)

        for thing in additional_things_1_5:
            additional_things_2_3.add(thing)

        main_things = additional_things_2_3
                            # settings.finish_things - мах количество предметов одновременно на игровом поле
        settings.current_number_things = min(20, settings.current_number_things) # <20 вещей  ограничение

    if len(main_things) < settings.current_number_things:
        delta = settings.current_number_things - len(main_things)

        for i in range(delta):  # если не хватает предметов, то суже лучайным образом генерием нужное число
            main_things = render_thing(settings, info, main_things, THINGS_SURF, 10)

        if settings.current_number_things == len(main_things):
            info.set_text_number_random_lines(delta)
            info.display_random_unfit()
    
    return main_things

def render_thing(settings, info, main_things, THINGS_SURF, max_attemps): # Случайное размещение предметов
    is_point_found = False
    W, H = settings.game_panel.w, settings.game_panel.h
    current_attempt = 0
    
    if len(THINGS_SURF) == 0:
        print("There will be no new generated images! They are over.") # settings.max_things_images = 35
        return  main_things
    else:
        serf = THINGS_SURF.pop(0)
       
    while not is_point_found and current_attempt < max_attemps: 
                
        possible_point = randint(0, W), randint(0, H)
        thing = check_possible_place(settings, info, main_things, serf, possible_point, settings.fuchsia)
        info.all_attempts +=1
        if thing is not None:
            main_things.add(thing)  
            is_point_found = True
            info.number_random_lines +=1
        else:
            info.random_unfit +=1

        current_attempt +=1
    return main_things


def check_possible_place(settings, info, things, thing_surf, possible_point, rect_color):
    
    new_thing = Thing(possible_point[0] + settings.left_margin, possible_point[1] + settings.up_margin, thing_surf)
     
    if info.is_displayed_lines:
        new_thing.rect_color = rect_color

    blocks_hit_list = pygame.sprite.spritecollide(new_thing, things, False, pygame.sprite.collide_circle)

    if len(blocks_hit_list) == 0:
        if pygame.Rect(settings.game_panel).contains(new_thing.rect):
            return new_thing
        else: 
            info.deleted_things_rect.append((new_thing.rect, rect_color))
    else:
        info.deleted_things_rect.append((new_thing.rect, rect_color))
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
                thing = check_possible_place(settings, info, things, serf, possible_point, color)
                
                if thing is not None:
                    things.add(thing)
                    is_point_found = True
                    additional_things.add(thing)
                else:
                    unsuitable_things +=1 
            
                if info.is_displayed_lines and current_attempt==0:
                    rect = (step_x*i + settings.left_margin + shift, step_y*j + settings.up_margin + shift, step_x - 2*shift, step_y - 2*shift)
                    lines.append((rect, color))
                current_attempt += 1
            info.all_attempts += current_attempt
    
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
            thing = check_possible_place(settings, info, things, serf, possible_point, color)
            current_attempt +=1
            info.all_attempts += 1

            if thing is not None:
                things.add(thing)
                additional_things.add(thing)
                is_point_found = True
            else:
                unsuitable_things +=1
        
            if info.is_displayed_lines:
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
    return sifted_points, sifted_points[::-1]  # на финише и старте одинаковое изменение (ускорение/замедление    скорости

def get_image(path):
   return os.path.dirname(os.path.abspath(__file__)) + path


def random_balls_images(settings):
    balls_images = settings.initial_balls_surf.copy()
    random_balls_images = []
    while len(balls_images) > 0:
        ind = random.randint(0, len(balls_images)-1)
        random_balls_images.append(balls_images.pop(ind))
    return random_balls_images



