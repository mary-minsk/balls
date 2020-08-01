
from random import randint
import pygame
import random
from math import sqrt, hypot, sin, cos, atan2

from settings import Settings
from info import Info
import game_render, func
from ball import Ball
from thing import Thing
from deleted_things import Deleted_thing
from button import Button

def create_balls(): # создание трех шаров, определени6 их скорости движения (settings.balls_speed[i]) и растояния (settings.balls_distance[i])
    BALLS = game_render.get_images(settings.number_balls, settings.path_spirals)
    BALLS_SURF = []

    balls = pygame.sprite.Group()  # создание группы шаров
    shift = settings.left_offset
    list = []
    balls_space = []
    w1 = 0
    h1 = settings.screen_height - settings.bottom_margin_center_ball
    for i in range(settings.number_balls):
        BALLS_SURF.append(pygame.image.load(BALLS[i]).convert_alpha()) # добавление изображения
        w  = BALLS_SURF[i].get_rect()[2] # ширина изображения
        balls.add(Ball(settings, shift + settings.balls_offset*i + w//2, BALLS_SURF[i],i)) # добавляем в группу три шара
        shift = shift + w 
        # print(shift + settings.balls_offset*i + w//2)
        list.append((w, i)) 
        
        if i == settings.number_balls - 1:
            # print(shift + settings.balls_offset*i + w)
            w1 = shift + settings.balls_offset*i + settings.left_offset
            

    list = sorted(list)  #сортируем по размеру изображения шара
    distance_dictionary = {}   # маленький шар имеет самую большую скорость и прокатится на самое 
    speed_dictionary = {}      # большое растояние
    additional_info = {}

    
    for i in range(settings.number_balls):
        distance_dictionary[list[i][1]] = settings.balls_distance[i]
        speed_dictionary[list[i][1]] = settings.balls_speed[i]
        additional_info[list[i][1]] = settings.balls_info[i]
    
    for i in range(settings.number_balls):  # большой шар катится растояние - H, средний - 2*H, самый маленикий - 3*H                  
        balls.sprites()[i].distance = distance_dictionary.get(i)*settings.unit  # длина пути последующего движения шара 
        balls.sprites()[i].speed = speed_dictionary.get(i) 
        balls.sprites()[i].info = additional_info.get(i)
        # print(balls.sprites()[i].distance)
    max_h = (max(ball.radius for ball in balls))
    balls_space = [0, h1 - max_h,  w1, max_h * 2]
    
    return balls

def create_things(): # создание n предметов
    
    # генерация n непересекающихся предметов на поверхности
  
    things = game_render.get_things(sc, settings, info)
    
    return things

def get_things_hit(): # Мяч сталкивается с предметами. Создается группа удаленных с игровой поверхности предметов
                         # которые поле непродолжительного вращения и уменьшения быстро исчезнут м экрана

    things_set = set(things)
    hit_list_things = pygame.sprite.spritecollide(settings.ball_in_game, things, True, pygame.sprite.collide_circle)
    
    for thing in hit_list_things:
        if thing in things_set:
            deleted_balls.add(Deleted_thing((thing.x, thing.y), thing.image))
            things.remove(thing)
    
def create_groups(balls, things, deleted_balls, setting):  # Создание групп вещей и мячей вначале кажного нового уровня
    balls.empty()
    things.empty()
    deleted_balls.empty()
    setting.reset()
    
    if settings.current_level <= settings.last_level:
        settings.current_number_things += 1
        setting.current_level += 1
        setting.set_text_level()

    things = create_things()
    balls = create_balls()
    deleted_balls = pygame.sprite.Group()
    
    return balls, things, deleted_balls


def early_completion():
    settings.is_early_completion = True  # флаг досрочного завершения

    for point in settings.all_path_points:
        settings.ball_in_game.set_xy(point)
        get_things_hit()
        

    balls.remove(settings.ball_in_game)
    func.set_balls_index(balls)
    settings.reset()
    settings.is_early_completion = False


pygame.init()

settings = Settings()
info = Info(settings)

sc = func.get_screen(settings, info)
sc.fill(settings.black)

pygame.display.update()
func.set_caption(settings)
clock = pygame.time.Clock()
settings.background_image = pygame.image.load(game_render.get_image(settings.background_image_path))

next_level_button = Button(sc, settings.button_level, settings.button_level_text, settings.white, settings.bg_color, 22)
# ruler_button = Button(settings.button_ruler, settings.button_ruler_text)

things = create_things()
balls = create_balls()
deleted_balls = pygame.sprite.Group()
     
done = False

while not done:
    for event in pygame.event.get():
        info.reset_event_info()

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                if not func.is_ball_rolling(settings):
                    settings.selected_ball = func.get_ball(event.pos, balls)
                    func.rotation_balls_off(balls)
                    
                    if settings.selected_ball is not None:
                    
                    
                        if settings.prev_selected_ball != settings.selected_ball:
                            if settings.prev_selected_ball is not None:
                                settings.prev_selected_ball.go_home()
                                settings.ball_in_game = None

                                info.set_text_not_equal_balls()
                            settings.prev_selected_ball = settings.selected_ball
            
                        selected_offset_x = settings.selected_ball.x - event.pos[0]
                        selected_offset_y = settings.selected_ball.y - event.pos[1]

                # else:
                if next_level_button.isOver(settings.mouse_xy):
                    print("qq")
                    balls, things, deleted_balls = create_groups(balls, things, deleted_balls, settings)
                
                if info.check_click(): # Перегенерируются все объекты, если для них не было получено доп. информации
                    settings.current_number_things -=  1    # Только если активна доп. панель информации 
                    balls, things, deleted_balls = create_groups(balls, things, deleted_balls, settings)

                info.set_text_mousebuttondown(event.pos)

            elif event.button == 3:  # шарик начинает катиться по столу, собирая все предметы на своем пути
                func.launch_ball(settings)
                  
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if not func.is_ball_rolling(settings):
                    if settings.selected_ball is not None:
                        
                        settings.ball_in_game = settings.selected_ball
                        settings.ball_in_game.isJump = True
                        func.check_correct_bottom_border(settings) # Если мяч находится прямо на нижней линии, то корректируем его положение

                        settings.prev_selected_ball = settings.selected_ball
                        settings.selected_ball = None
                        settings.prev_selected_ball.is_rotated = True  # После отпускания мышки шарик на панели шаров вновь вращается
                    
            info.set_text_mousebuttonup(event.pos)

        elif event.type == pygame.MOUSEMOTION:
            if not func.is_ball_rolling(settings):
                if settings.selected_ball is not None:
                    settings.selected_ball.isJump = False
                    settings.selected_ball.x = event.pos[0] + selected_offset_x
                    settings.selected_ball.y = event.pos[1] + selected_offset_y
                    func.check_correct_up_left_right_border(settings.selected_ball, settings)
                
            info.set_text_mousemotion(event.pos)

        elif event.type == pygame.KEYDOWN:  # При нажатии  стрелок или Табуляции меняем на игровом поле мячи                 
            if settings.ball_in_game is not None:
                if not settings.is_points_erasing and not func.is_ball_rolling(settings):
                    if event.key == pygame.K_TAB:
                        func.check_tab(settings, balls)

                    elif event.key == pygame.K_SPACE:
                        func.launch_ball(settings)

                    else:        
                        func.check_keydown(event, settings)  # Можно одновременно нажимать несколько клавиш

                elif event.key == pygame.K_SPACE: # При повторном нажатии пробела удаляются все пересекающие траекторию предметы
                   early_completion()               # settings.is_early_completion = True 

            elif settings.is_points_erasing and event.key == pygame.K_SPACE: # Мяч проделал весь путь. Происходит стирание траектории
                early_completion()
                settings.is_points_erasing = False # Траектория, начальная и конечные точки пути не будут отображаться

        elif event.type == pygame.KEYUP:  # Отключение движения при отпускании клавиши
            func.check_keyup(event, settings)
        
        else:
            info.set_text_other_events()

        settings.is_draw_line = False
        settings.mouse_xy = pygame.mouse.get_pos()

        if not func.is_ball_rolling(settings):  # мяч катится и выбрать новый мяч нельзя
            if  settings.selected_ball is None:
                settings.rotated_ball = None
                
                if not pygame.Rect(settings.game_panel_add_3_margins).collidepoint(settings.mouse_xy):
                    settings.rotated_ball = func.get_ball(settings.mouse_xy, balls)
                    
                func.check_rotation(settings, balls)
            
                settings.is_draw_line = func.mouse_inside_ball_in_game(settings) # рисование траектории, если мышка за пределами шара
                if settings.is_draw_line:
                    settings.a, settings.b = func.get_cartesian_mouse_xy_coordinates(settings)

    info.set_text_events()   
    sc.blit(settings.background_image, (0, 0))
    func.check_holding_arrow_keys(settings) # При нажатии/удерживании клавиш стрелок, вычисляем направление движения мяча
   
    if settings.is_draw_line:  # Мяч на игровой поверхности. Момент прицеливания. Cтроим путь (ломаная кривая)
        func.build_path(settings)
        pygame.draw.aalines(sc, settings.bg_color, False, settings.edges)
        func.draw_tips(sc, settings, settings.ball_in_game.center())

    if not settings.is_early_completion:  # Если не досрочное завершение движения мяча (второй пробел)
        if func.is_ball_rolling(settings):    # Мяч катится по своей ттаектории
            pygame.draw.aalines(sc, settings.bg_color, False, settings.edges)
            func.draw_tips(sc, settings, settings.pos_center_ball)
            get_things_hit()             # Проверяем столкновение с предметами

        if settings.is_points_erasing: # Мяч проделал весь путь, но не исчезнул. Ломаная линия исчезает
            if settings.is_deleted_ball: 
                func.del_ball(settings, balls, deleted_balls)  # Удаляется мяч с поверхности. Он вращается и уменьшается
            
            func.get_disappearing_path(settings)  # Стирание траектории
            func.draw_disappearing_path(sc, settings)
            # print(settings.is_early_completion)
                
    
    func.display_info(sc, settings, info)
    next_level_button.draw()
    # ruler_button.draw(sc, settings)
    
    things.update(sc, settings, info, things)
    things.draw(sc)

    balls.update(settings, sc)
    balls.draw(sc)

    deleted_balls.draw(sc)
    deleted_balls.update(settings)

    func.display_last_path_point(sc, settings)
    func.display_game_borders(sc, settings)

    pygame.display.update()
    clock.tick(25)

pygame.quit()

# draw_tips(settings.a, settings.b, pos_center_ball)

