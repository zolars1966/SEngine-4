import pygame as pg
import sys
import time
from sengine import *
from globals import *


# Perspective
def get_projections(translated_vec):
    return ((translated_vec @ perspective_matrix + [0.0, 0.0, -1.0]) / translated_vec[:, :, 2, np.newaxis] + 1.0) * [H_WIDTH, H_HEIGHT, 1.]


# Ortogonal
def get_projection_x(translated_vec):
    return (translated_vec + [WIDTH / HEIGHT, 1.0, 1.0]) * H_HEIGHT


# Polygon cliping (in case of "out of bounds" drawing)
def cliping(translated_vecs, normals):
    to = np.sum(translated_vecs, axis=1) - camera_position * 3
    tol = np.linalg.norm(to, axis=1)

    return np.where((np.dot(to / tol[:, np.newaxis], camera_direction) > cos(FOV / 720 * HEIGHT / H_WIDTH * pi)) &
                    (tol >= 1) & (tol <= 21000) & (np.dot(normals, camera_direction) <= 0))[0]


# Left mouse click check
def left_click(event):
    global l_press, l_press_el
    
    if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 1:
            l_press = True
    
    elif event.type == pg.MOUSEBUTTONUP and l_press:
        if event.button == 1:
            l_press = False
            l_press_dt = pg.time.get_ticks() - l_press_el
            l_press_el = pg.time.get_ticks()
            out = l_press_dt <= 200
            return out
    
    l_press_el = pg.time.get_ticks()
    
    return False


# Right mouse click check
def right_click(event):
    global r_press, r_press_el
    
    if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 3:
            r_press = True
    
    elif event.type == pg.MOUSEBUTTONUP and r_press:
        if event.button == 3:
            r_press = False
            r_press_dt = pg.time.get_ticks() - r_press_el
            r_press_el = pg.time.get_ticks()
            out = r_press_dt <= 200
            return out
    
    r_press_el = pg.time.get_ticks()
    
    return False


# Keyboard keys
def check_pressed():
    global camera_position, lightning_model

    keys = pg.key.get_pressed()

    if True in keys:
        speed = 2 * elapsed_ticks / 10

        if keys[pg.K_LSHIFT]:
            speed = 10 * elapsed_ticks / 10
        if keys[pg.K_LCTRL]:
            speed = 5 * elapsed_ticks / 100

        if keys[pg.K_w]:
            camera_position += forwardvector * speed
        elif keys[pg.K_s]:
            camera_position -= forwardvector * speed

        speed /= 2

        if keys[pg.K_e]:
            camera_position[1] -= speed
        elif keys[pg.K_q]:
            camera_position[1] += speed

        if keys[pg.K_a]:
            camera_position += rotate_y(pi / 2, forwardvector * speed)
        elif keys[pg.K_d]:
            camera_position -= rotate_y(pi / 2, forwardvector * speed)

        if keys[pg.K_0]:
            lightning_model = "carcass"
        elif keys[pg.K_1]:
            lightning_model = light_diff
        elif keys[pg.K_2]:
            lightning_model = lambert
        elif keys[pg.K_3]:
            lightning_model = wrap
        elif keys[pg.K_4]:
            lightning_model = phong
        elif keys[pg.K_5]:
            lightning_model = blinn
        elif keys[pg.K_6]:
            lightning_model = highlight
        elif keys[pg.K_7]:
            lightning_model = blinn_highlight
        elif keys[pg.K_8]:
            lightning_model = metal
        elif keys[pg.K_9]:
            lightning_model = light_reflect


if __name__ == "__main__":
    # creating a pygame window
    screen = pg.display.set_mode(SIZE, pg.SCALED)
    
    cursor_free = False
    pg.mouse.set_visible(cursor_free)
    clock = pg.time.Clock()
    title = "$~ SEngine 4.0"
  
    upd_ticks, vert_ticks, start_time, upd_time = pg.time.get_ticks(), pg.time.get_ticks(), pg.time.get_ticks(), time.perf_counter_ns()
    delta_ticks, delta_time = 1, 1
    pause = False

    fix_cam_dist_scale = 0.2

    obj, obj_colors = open_model("/Users/zolars/Documents/Projects/miph/obj/OLC/axis.obj")
  
    # creating environment
    # env = Environment(...)

    for _ in range(2):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        pg.mouse.set_pos((H_WIDTH, H_HEIGHT))
        pg.mouse.set_visible(False)
        pg.display.flip()

    # main cycle
    while True:
        # game environment updating (with vertical synchronization)
        if (N_DELTA_TIME <= time.perf_counter_ns() - upd_time) and not pause:
            delta_time = -upd_time
            upd_time = time.perf_counter_ns()
            delta_time += upd_time

            delta_ticks = -upd_ticks
            upd_ticks = pg.time.get_ticks()
            delta_ticks += upd_ticks

            # calling for game environment to update
            # env.update()

        # game Assets/UI/elements drawing
        if FPS_DT <= pg.time.get_ticks() - vert_ticks:
            # checking for keyboard, window, mouse inputs or events
            for event in pg.event.get():
                if event.type == pg.QUIT: 
                    exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.mouse.set_pos(H_SIZE)
                        cursor_free ^= 1
                        pg.mouse.set_visible(cursor_free)

                if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
                    if left_click(event):
                        # do something
                        pass
                
                    if right_click(event):
                        # do something
                        pass

            elapsed_ticks = pg.time.get_ticks() - vert_ticks
            vert_ticks = pg.time.get_ticks()

            screen.fill((255, 255, 255))
            
            check_pressed()

            if pg.mouse.get_focused() and not cursor_free:
                differenceX = pg.mouse.get_pos()[0] - H_WIDTH
                differenceY = pg.mouse.get_pos()[1] - H_HEIGHT
                pg.mouse.set_pos(H_SIZE)
                fYaw -= differenceX / 32400 * W_SCALE * FOV
                fXaw -= differenceY / 32400 * W_SCALE * FOV
                fXaw = max(-pi / 2 + 0.001, min(pi / 2 - 0.001, fXaw))

            upvector = [0.0, 1.0, 0.0]
            camera_direction = rotate_y(fYaw, rotate_x(fXaw, [0.0, 0.0, 1.0]))
            # light = rotate_y(fYaw, rotate_x(fXaw, [0.57735027, 0.57735027, 0.57735027]))
            forwardvector[...] = [camera_direction[0], 0.0, camera_direction[2]]
            forwardvector /= np.linalg.norm(forwardvector)

            camera_matrix = quick_inverse(camera_position, camera_direction, upvector)
            
            translated_vecs = obj
            normals = get_normals(translated_vecs)
            viewed = matrix_multiply(translated_vecs, camera_matrix)
            indexes = cliping(translated_vecs, normals)

            if len(indexes) != 0:
                viewed = viewed[indexes]
                colors = obj_colors[indexes]

                normals = normals[indexes]
                projection_vecs = get_projections(viewed)

                if lightning_model != "carcass":
                    dps = lightning_model(normals)
                    dps[dps > 1] = 1

                    indexes = np.argsort(-projection_vecs[:, :, 2].max(axis=1))

                    if lightning_model == light_reflect:
                        dps[dps < 0] = 0
                        dps *= 255

                        for i in indexes: pg.draw.polygon(screen, dps[i], projection_vecs[i, :, :2])
                    else:
                        dps = colors * dps[:, None] * 255

                        for i in indexes: pg.draw.polygon(screen, dps[i], projection_vecs[i, :, :2])
                else:                    
                    for polygon in projection_vecs: pg.draw.polygon(screen, (110, 110, 110), polygon[:, :2], 1)

            obj = rotate_y(pi / 180, obj)
            obj = rotate_z(pi / 180, obj)

            pg.display.set_caption(title + " ~fps: " + str(round(clock.get_fps(), 2)))

            pg.display.flip()
            clock.tick()
