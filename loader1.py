# this file is for variables
# loader 1

import math, random, pygame, pydub, pytweening, scipy, pymunk, pathfinding
import importlib.util
from PIL import Image
from pygame import mixer as mx
from pymunk import shapes

def loader1(main_globals):
    # global tile_size, currently_playing_index, player_size, screen_h, screen_w, menu_bg_x, menu_background, moving_up, moving_down, moving_left, moving_right, game_stage, font, is_paused, dragging_music_slider, menu_bg_can_animate, flash_alpha, flash_active, flash_speed, camera_x, camera_y, camera_speed, music_slider, play_button, settings_button, to_menu, mouse_pos, mouse_pressed, current_frame, frame_timer, frame_delay, facing_left, frames, developert_tools
    main_globals['tile_size'] = 600
    main_globals['currently_playing_index'] = 0 # 0 being the first track so it's insta loaded
    main_globals['player_size'] = 50
    main_globals['screen_h'] = 750 
    main_globals['screen_w'] = 1080

    main_globals['menu_bg_x'] = main_globals['screen_w']
    main_globals['faded_in'] = False
    main_globals['faded_out'] = False
    main_globals['splash_alpha'] = 0

    main_globals['moving_up'] = False
    main_globals['moving_down'] = False
    main_globals['moving_left'] = False
    main_globals['moving_right'] = False
    main_globals['game_stage'] = ""
    main_globals['spawn_set'] = False
    main_globals['can_move_x'] = True
    main_globals['can_move_y'] = True

    main_globals['font'] = pygame.font.SysFont(None, 48)
    main_globals['is_paused'] = False

    main_globals['dragging_music_slider'] = False

    main_globals['menu_bg_can_animate'] = True
    main_globals['flash_alpha'] = 0
    main_globals['flash_active'] = False
    main_globals['flash_speed'] = 1

    main_globals['camera_x'] = 0
    main_globals['camera_y'] = 0
    main_globals['camera_speed'] = 0.1  # lower = slower

    main_globals['music_slider'] = pygame.Rect(main_globals['screen_w'] - 400, 110, 300, 20)
    main_globals['play_button'] = pygame.Rect(50, main_globals['screen_h'] - 150, 200, 100)
    main_globals['settings_button'] = pygame.Rect(50, main_globals['screen_h'] - 300, 200, 100)
    main_globals['to_menu'] = pygame.Rect(main_globals['screen_w'] - 250, main_globals['screen_h'] - 150, 200, 100)

    main_globals['mouse_pos'] = pygame.mouse.get_pos()
    main_globals['mouse_pressed'] = pygame.mouse.get_pressed()[0]

    main_globals['current_frame'] = 0
    main_globals['frame_timer'] = 0
    main_globals['frame_delay'] = 50
    main_globals['facing_left'] = False
    main_globals['frames'] = []

    main_globals['developer_tools'] = True

    main_globals['tilemap'] = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 99, 1, 1, 0, 0, 0, 0, 0, 0,],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
    ]

    main_globals['spawn_x'] = 0
    main_globals['spawn_y'] = 0

    main_globals['tile_offset'] = 50

    print("loader1 file loaded")
