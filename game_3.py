import game_render, func
from math import hypot
# from game_render import get_a_b
# from func import get_dx_dy


def build_path(settings, center_ball_xy):  # определение траектории движения мяча

    #  accumulated_distance + current_distance = max_distance. Траектория нужной длины построена: is_path_passed = True
    accumulated_distance = 0
    current_distance = 0
    is_path_passed = False

    # center_ball_xy = point
    radius, max_distance = 20, 1000

    x, y = center_ball_xy    # Начало траектории от центра шара
    prev_point = center_ball_xy

    point2 = game_render.get_a_b() # направление линии
    dx, dy = func.get_dx_dy(settings, point2) # смещение за единицу по оси X или Y

    edges = []  # список крайних точек ломаной кривой (вершин) для рисования линии
    edges.append(center_ball_xy)
    # print(center_ball_xy, point2)

    while not is_path_passed:
        
        if accumulated_distance + current_distance <= max_distance:
            is_new_point = False
            if x + dx + settings.right_margin > settings.screen_width - radius or x + dx - settings.left_margin < radius:
                dx = -dx
                is_new_point = True

            if y + dy + settings.bottom_margin + settings.height_bottom_panel > settings.screen_height - radius or y + dy - settings.up_margin < radius:
                dy = -dy
                is_new_point = True

            if is_new_point:
                accumulated_distance += hypot(
                    prev_point[0]-x, prev_point[1]-y)
                edges.append((round(x), round(y)))
                prev_point = (x, y)
                current_distance = 0

            x += dx
            y += dy
            
            current_distance = hypot(prev_point[0]-x, prev_point[1]-y)
        else:
            is_path_passed = True

    edges.append((round(x), round(y)))
    # print(len(edges))
    return edges

def ball_set_values(settings, ball):         # один мяч на всю игру
    ball_name = settings.large_ball_png
    pos = ball_name.find(".")
    ball.info = ball_name[:pos]
    ball.distance = settings.ball_distance[settings.current_level - 1]
    ball.speed = settings.ball_speed[settings.current_level - 1]
    print((ball.distance, ball.speed))
