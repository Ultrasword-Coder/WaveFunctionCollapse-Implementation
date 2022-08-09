import pygame
# from OpenGL.GL import *
# from OpenGL.GLU import *
# import numpy as np


from engine.singleton import *

from engine import clock, user_input, handler, animation
from engine import particle, chunk, tile, entity
from engine import statehandler, scenehandler

from engine import singleton as EGLOB

from engine.window import Window
from engine.filehandler import *

# --------- initialization -------------- #



WINDOW_CAPTION = "RPG Game"
WW = 1280
WINDOW_SIZE = [WW, int(WW/16*9)]
WW//=3
FB_SIZE = [WW, int(WW/16*9)]

FPS = 60

Window.create_window(WINDOW_CAPTION, WINDOW_SIZE[0], WINDOW_SIZE[1], pygame.RESIZABLE | pygame.DOUBLEBUF , 16)
# window.set_icon()
fb = Window.create_framebuffer(FB_SIZE[0], FB_SIZE[1], flags=0, bits=32).convert_alpha()

# print(EGLOB.FB_WIDTH)
# -------- external imports --------- #

from scripts import generate_level

# ----------------------------------- #

__scene = scenehandler.Scene()
scenehandler.SceneHandler.push_state(__scene)
STATE = __scene.handler

generate_level(__scene.world)


# ----------------------------- #

clock.start()
while Window.running:
    if scenehandler.SceneHandler.CURRENT:
        fb.fill((255, 255, 255))
        scenehandler.SceneHandler.CURRENT.handler.handle_entities(fb)
        scenehandler.SceneHandler.CURRENT.world.handle_chunks(fb)
    
    # rescale framebuffer to window
    Window.instance.blit(pygame.transform.scale(fb, (Window.WIDTH, Window.HEIGHT)), (0,0))

    user_input.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            Window.running = False
        elif e.type == pygame.KEYDOWN:
            # keyboard press
            user_input.key_press(e)
        elif e.type == pygame.KEYUP:
            # keyboard release
            user_input.key_release(e)
        elif e.type == pygame.MOUSEMOTION:
            # mouse movement
            user_input.mouse_move_update(e)
        elif e.type == pygame.MOUSEBUTTONDOWN:
            # mouse press
            user_input.mouse_button_press(e)
        elif e.type == pygame.MOUSEBUTTONUP:
            # mouse release
            user_input.mouse_button_release(e)
        elif e.type == pygame.WINDOWRESIZED:
            # window resized
            Window.handle_resize(e)
            fbsize = fb.get_size()
            user_input.update_ratio(Window.WIDTH, Window.HEIGHT, fbsize[0], fbsize[1])
    pygame.display.flip()
    clock.update()


pygame.quit()
