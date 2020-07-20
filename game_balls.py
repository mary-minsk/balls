
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


def point_to_str(point): # строковое представление точки
    return "(" + str(point[0])+ ", " + str(point[1]) + ")"

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
    
    if settings.current_level <= settings.last_level:
        settings.current_number_things += 1
        setting.current_level += 1
        setting.set_text_level()

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
x_change = 0
num = 0
prev = 0
fl = False
     
done = False

while not done:
    for event in pygame.event.get():

        info.reset_event_info()
        settings.is_draw_line = False

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

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

                else:
                    if next_level_button.isOver(settings.mouse_xy):
                        balls, things, deleted_balls = create_groups(balls, things, deleted_balls, settings)
                    
                    if info.check_click(): # Перегенерируются все объекты, если для них не было получено доп. информации
                        settings.current_number_things -=  1    # Только если активна доп. панель информации 
                        balls, things, deleted_balls = create_groups(balls, things, deleted_balls, settings)

                info.set_text_mousebuttondown(event.pos)
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:

                if settings.selected_ball is not None:
                    
                    settings.ball_in_game = settings.selected_ball
                    settings.ball_in_game.isJump = True
                    func.check_correct_bottom_border(settings) # Если мяч находится прямо на нижней линии, то корректируем его положение

                    settings.prev_selected_ball = settings.selected_ball
                    settings.selected_ball = None
                    settings.prev_selected_ball.is_rotated = True  # После отпускания мышки шарик на панели шаров вновь вращается
                    # if settings.ball_in_game is not None:
                    # if settings.ball_in_game is not None:
                        # settings.ball_in_game.isJump = True
            info.set_text_mousebuttonup(event.pos)

        elif event.type == pygame.MOUSEMOTION:
            
            if settings.selected_ball is not None:
                settings.selected_ball.isJump = False
                settings.selected_ball.x = event.pos[0] + selected_offset_x
                settings.selected_ball.y = event.pos[1] + selected_offset_y
                func.check_correct_up_left_right_border(settings.selected_ball, settings)
                
            info.set_text_mousemotion(event.pos)

        elif event.type == pygame.KEYDOWN:  # При нажатии Табуляции меняем на игровом поле мячи                 
            if settings.ball_in_game is not None:
                if event.key == pygame.K_TAB:
                    settings.next_ball = func.get_next_ball(settings.ball_in_game, balls)

                    if settings.next_ball is not None:
                        center = settings.ball_in_game.rect.center
                        # включить нужный мувин
                        func.continue_ball_moving(settings.ball_in_game, settings.next_ball)
                        settings.ball_in_game.stop_moving()
                        # settings.ball_in_game.go_home()  # При нажатии Таб, settings.ball_in_game не измениется в None
                        # settings.ball_in_game.isJump = True
                        settings.next_ball.set_ball_xy((center))
                        # func.jump_ball_on(settings, balls, settings.next_ball)
                        
                        # Если при нажатии Таб следующий по счету мяч выходит за границы игрового поля, то корректируем его центр
                        func.check_ball_border(settings)
                        func.jump_ball_on(balls, settings.next_ball)
                        settings.ball_in_game = settings.next_ball
                        # settings.ball_in_game.isJump = True
                        # func.jump_ball_on(settings, balls)
                        settings.prev_selected_ball = settings.next_ball

                elif event.key == pygame.K_SPACE:
                    if settings.is_draw_line:
                        func.launch_ball(settings)

                elif event.key == pygame.K_RIGHT:
                    settings.ball_in_game.moving_right = True

                elif event.key == pygame.K_LEFT:
                    settings.ball_in_game.moving_left = True
                
                elif event.key == pygame.K_UP:
                    settings.ball_in_game.moving_up = True

                elif event.key == pygame.K_DOWN:
                    settings.ball_in_game.moving_down = True

        elif event.type == pygame.KEYUP:
            if settings.ball_in_game is not None:
                if event.key == pygame.K_LEFT:
                    settings.ball_in_game.moving_left = False

                if event.key == pygame.K_RIGHT:
                    settings.ball_in_game.moving_right = False

                if event.key == pygame.K_UP:
                    settings.ball_in_game.moving_up = False

                if event.key == pygame.K_DOWN:
                    settings.ball_in_game.moving_down = False
        
        else:
            info.set_text_other_events()

        if  settings.selected_ball is None:
            
            settings.mouse_xy = pygame.mouse.get_pos()
            settings.rotated_ball = None
            
            if not pygame.Rect(settings.game_panel_add_3_margins).collidepoint(settings.mouse_xy):
                settings.rotated_ball = func.get_ball(settings.mouse_xy, balls)

            if settings.rotated_ball is None:        # курсор мыши не над мячиками
                func.rotation_balls_off(balls)
            else:                           # над мячиком мышка
                func.rotation_ball_on(balls, settings.rotated_ball)  # Мяч вращается, его можно перетаскивать

        
            settings.is_draw_line = func.mouse_inside_ball_in_game(settings)
            if settings.is_draw_line:
                settings.a, settings.b = func.get_cartesian_mouse_xy_coordinates(settings)
    info.set_text_events()
        
    sc.blit(settings.background_image, (0, 0))

    func.check_holding_arrow_keys(settings)
   
    if settings.is_draw_line:  # Мяч на игровой поверхности
        # # if settings.is_draw_line and not ball.isRolling and not settings.is_points_erasing: # Момент прицеливания
        #     # строим путь (ломаная кривая) и собираем информацию о движении мяча
        func.build_path(settings)
        pygame.draw.aalines(sc, settings.bg_color, False, settings.edges)
        func.draw_tips(sc, settings)
        # draw_path_and_tips(settings.ball_in_game.rect.center)

    pygame.draw.rect(sc, settings.bg_color, settings.game_panel, 2)
    pygame.draw.rect(sc, settings.bg_color, settings.border_game_panel, 2) 
    # pygame.draw.rect(sc, settings.blue, settings.ticker_rect, 1)
    
      
     
    # if settings.is_ball_selected and not settings.is_ball_pressed: # Выбор любого одного мяча на нижней панели
    #     ball = balls.sprites()[settings.index_current_ball]
    #     if not settings.is_draw_line and not settings.is_points_erasing: #  Во время движения мячи на панели выбрать нельзя
    #         ball.is_rotated = True

    # if settings.is_ball_down:  # Мяч на игровой поверхности
    #     if settings.is_draw_line and not ball.isRolling and not settings.is_points_erasing: # Момент прицеливания
    #         build_path(ball.radius, ball.distance) # строим путь (ломаная кривая) и собираем информацию о движении мяча
    #         draw_path_and_tips(pos_center_ball)
            
    #     elif ball.isRolling:   # продолжаем рисовать траекторию движения мяча и крайние точки этой линии 
    #         draw_path_and_tips(settings.pos_center_ball)
    #         get_things_hit()

    # if settings.is_points_erasing: # Мяч проделал весь путь, но не исчезнул. Ломаная линия исчезает
    #     if settings.is_deleted_ball: 
    #         deleted_balls.add(Deleted_thing(ball.x1, ball.y1, ball.image, ball.angle)) # Создание исчезающего вращающегося мяча
    #         balls.remove(ball)
    #         settings.is_deleted_ball = False
    #         settings.reset() 
    #         settings.edges.pop(0)  # Траектория мяча начинается не с позиции мыши, а с точки на окружности шара
            
    #     get_disappearing_path()
    #     draw_disappearing_path()
                
    
    func.display_info(sc, settings, info)
    next_level_button.draw()
    # ruler_button.draw(sc, settings)
    
    things.update(sc, settings, info, things)
    things.draw(sc)

    balls.update(settings, sc)
    balls.draw(sc)

    # deleted_balls.draw(sc)
    # deleted_balls.update(settings)

    # display_last_path_point() 

    pygame.display.update()
    clock.tick(25)

pygame.quit()


