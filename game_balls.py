
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

def create_balls(): # создание трех шаров, определени6 их скорости движения (settings.balls_speed[i]) и растояния (settings.balls_distance[i])

    balls = pygame.sprite.Group()  # создание группы шаров
    shift = settings.left_offset
    list = []
    ball_images = game_render.random_balls_images(settings)
    for i in range(settings.number_balls):
        surf = ball_images[i]
        w = surf.get_rect()[2]
        if settings.balls_size_reduction[settings.current_difficulty] != 100:
            if surf.get_width() >= settings.min_ball_size:
                new_size = surf.get_width() * settings.balls_size_reduction[settings.current_difficulty] // 100, \
                    surf.get_height() * settings.balls_size_reduction[settings.current_difficulty] // 100
            
                surf = pygame.transform.scale(surf, new_size)
       
        balls.add(Ball(settings, shift + settings.balls_offset*i + w//2, surf, i))  # добавляем в группу три шара
        shift = shift + w 
        list.append((w, i)) 
            
    list = sorted(list)  # сортируем по размеру изображения шара
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
       
    # max_h = (max(ball.radius for ball in balls))
    
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
            settings.level_score *= 2
            settings.score += settings.level_score
            deleted_balls.add(Deleted_thing((thing.x, thing.y), thing.image, 0, settings.level_score, False))
            things.remove(thing)
            settings.set_text_score()

def create_groups(balls, things, deleted_balls, setting, isRestart):  # Создание групп вещей и мячей вначале кажного нового уровня
    balls.empty()
    things.empty()
    deleted_balls.empty()
    setting.reset()
    # settings.attempts = 3  # Три попытки, три мяча на уровень
    settings.is_level_win = False
    settings.is_level_defeat = False

    if not isRestart:
        if settings.current_level <= settings.last_level:
            settings.current_number_things += 1
            setting.current_level += 1
            setting.set_text_level()

    things = create_things()
    balls = create_balls()
    deleted_balls = pygame.sprite.Group()
    settings.set_level_time()
    
    return balls, things, deleted_balls

def change_difficulty():

    settings.current_difficulty += 1
    if settings.current_difficulty >= len(settings.difficulty_level):
        settings.current_difficulty = 0
    settings.difficulty_button.text = settings.difficulty_level[settings.current_difficulty]

def early_completion():
    settings.is_early_completion = True #  Проверка, не завершен ли уровень

    for point in settings.all_path_points:
        settings.ball_in_game.set_xy(point)
        get_things_hit()

    balls.remove(settings.ball_in_game)
    func.set_balls_index(balls)
    settings.reset()

def restart_level(pballs, pthings, pdeleted_balls, psettings):
    global balls, things, deleted_balls, settings
    balls, things, deleted_balls = create_groups(pballs, pthings, pdeleted_balls, psettings, True)

def start_next_level(pballs, pthings, pdeleted_balls, psettings):
    global balls, things, deleted_balls, settings
    balls, things, deleted_balls = create_groups(pballs, pthings, pdeleted_balls, psettings, False)

def init_images_buttons():
    settings.background_image = pygame.image.load(game_render.get_image(settings.background_image_path))
    settings.game_settings_image = pygame.image.load(game_render.get_image(settings.system_image_path))
    settings.options_icon = settings.game_settings_image.get_rect(center=(390, 22))
    settings.set_original_balls_surf()  # settings.balls_surf получаем изображения шаров
    settings.create_buttons(sc)
    settings.game_settings(sc)

def check_info_restart_level(balls, things, deleted_balls, settings, info):
    if info.is_restart_level or settings.is_restart_level:
        if not settings.is_show_finish:
            restart_level(balls, things, deleted_balls, settings)
            info.is_restart_level = False
            settings.is_restart_level = False

    if settings.is_start_next_level:
        if not settings.is_show_finish:
            start_next_level(balls, things, deleted_balls, settings)
            settings.is_start_next_level = False
        

def get_level_result():

    if settings.ball_in_game is None:
        if not settings.is_level_defeat and not settings.is_level_win:
            if len(things) == 0:
                settings.is_level_win = True
                # print("win")
                settings.text_result_level = "Win!"
                return True
            else:
                if len(balls) == 0:
                    settings.is_level_defeat = True
                    settings.text_result_level = "Defeat"
                    # print("defeat")
                    return True
    return False

def check_finish_level():

    is_level_result = get_level_result()
    if is_level_result:
        if settings.is_early_completion:  # Завершение уровня при нажатии пробел
            settings.set_finish_time()  # Запуск таймера
            settings.is_early_completion = False

    if settings.is_show_finish or (settings.is_points_erasing and is_level_result):
        settings.level_box(settings.text_result_level)
        sc.blit(settings.text_level_box_surf, settings.text_level_box_rect)

    if settings.is_show_level:
        settings.level_box("Level " + str(settings.current_level))
        sc.blit(settings.text_level_box_surf, settings.text_level_box_rect)
    
pygame.init()

settings = Settings()
info = Info(settings)

sc = func.get_screen(settings, info)
sc.fill(settings.black)

pygame.display.update()
func.set_caption(settings)
init_images_buttons()

things = create_things()
balls = create_balls()
deleted_balls = pygame.sprite.Group()

settings.set_level_time()
     
done = False

while not done:
    func.check_level_timer(settings)  # Вывод уровня игры
    func.check_finish_timer(settings)  # Вывод "Win!"
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

                if settings.next_level_button.isOver(settings.mouse_xy):
                    start_next_level(balls, things, deleted_balls, settings)
                
                if info.check_click(): # Перегенерируются все объекты, если для них не было получено доп. информации
                                          # Только если активна доп. панель информации. Для тестирования и отладки
                    restart_level(balls, things, deleted_balls, settings)

                func.check_options(settings, event.pos)

                if settings.is_show_options_menu:
                    if settings.difficulty_button.isOver(event.pos):
                        change_difficulty()

                    elif settings.restart_game_button.isOver(event.pos):
                        settings.is_show_options_menu = False
                        restart_level(balls, things, deleted_balls, settings)


                info.set_text_mousebuttondown(event.pos)

            elif event.button == 3:  # шарик начинает катиться по столу, собирая все предметы на своем пути
                if settings.is_draw_line and not func.is_ball_rolling(settings) and not settings.is_points_erasing:
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
                        if settings.is_draw_line:
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

    if settings.is_points_erasing and settings.selected_ball is None:  # После удалении мяча с поля след. мяч начинает вращаться
                                                            #  если над ним находится мышка и траектория предыдущего мяча еще не удалена
        settings.rotated_ball = func.get_ball(settings.mouse_xy, balls)
        func.rotation_ball_on(balls, settings.rotated_ball)

    info.set_text_events()
    
    sc.blit(settings.background_image, (0, 0))
    sc.blit(settings.game_settings_image, settings.options_icon)
    
    func.check_holding_arrow_keys(settings) # При нажатии/удерживании клавиш стрелок, вычисляем направление движения мяча
   
    if settings.is_draw_line:  # Мяч на игровой поверхности. Момент прицеливания. Cтроим путь (ломаная кривая)
        func.build_path(settings)
        pygame.draw.aalines(sc, settings.bg_color, False, settings.edges)
        func.draw_tips(sc, settings, settings.ball_in_game.center())

    if func.is_ball_rolling(settings):    # Мяч катится по своей траектории. При досрочном завершении произойдет сброс параметров
        pygame.draw.aalines(sc, settings.bg_color, False, settings.edges)
        func.draw_tips(sc, settings, settings.pos_center_ball)
        get_things_hit()             # Проверяем столкновение с предметами

    if settings.is_points_erasing: # Мяч проделал весь путь, но не исчезнул. Ломаная линия исчезает
        if settings.is_deleted_ball: 
            func.del_ball(settings, balls, deleted_balls)  # Удаляется мяч с поверхности. Он вращается и уменьшается
        
        func.get_disappearing_path(settings)  # Стирание траектории
        func.draw_disappearing_path(sc, settings)
                
    func.display_info(sc, settings, info, balls)
    
    settings.next_level_button.draw()
    
    if not settings.is_show_level:
        things.update(sc, settings, info, things)
        things.draw(sc)

    balls.update(settings, sc)
    balls.draw(sc)

    deleted_balls.draw(sc)
    deleted_balls.update(sc, settings)

    func.display_last_path_point(sc, settings)
    func.display_game_borders(sc, settings)
    func.game_options(sc, settings)

    check_info_restart_level(balls, things, deleted_balls, settings, info)
    check_finish_level()

    pygame.display.update()
    settings.clock.tick(25)

pygame.quit()



