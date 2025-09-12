# this file is for images and audio
# loader 2

import math, random, pygame, pydub, pytweening, scipy, pymunk, pathfinding
from PIL import Image
from pygame import mixer as mx
from pymunk import shapes

def loader2(main_globals):
    main_globals['player_ded'] = pygame.image.load("assets/models/player/ded.png").convert_alpha()
    main_globals['tile_images'] = [
        pygame.image.load("assets/useful images/tiles/tile600x600.png").convert_alpha()
    ]
    main_globals['vignette'] = pygame.image.load("assets/useful images/redvignette.png").convert_alpha()
    main_globals['vignette'] = pygame.transform.scale(main_globals['vignette'], (main_globals['screen_w'], main_globals['screen_h']))
    main_globals['menu_background'] = pygame.image.load("assets/useful images/aimenubg.png").convert_alpha()
    main_globals['menu_background'] = pygame.transform.scale(main_globals['menu_background'], (750, 750))
    player_health_images = []
    for i in range(1, 4):
        img = pygame.image.load(f"assets/models/player/playerhealth{i}.png").convert_alpha()
        w, h = img.get_size()
        img = pygame.transform.scale(img, (w * 4, h * 4))
        player_health_images.append(img)
    main_globals['player_health_images'] = player_health_images
    main_globals['death_sound'] = mx.Sound("assets/audio/sfx/vineboom.mp3")
    main_globals['hurt_sound'] = mx.Sound("assets/audio/sfx/hurt.mp3")
    main_globals['musics'] = ["assets/audio/music/testdroga.mp3", "assets/audio/music/game_over_loop.mp3"]
    mx.music.load(main_globals['musics'][0])
    mx.music.play(-1)
    mx.music.pause()
    mx.music.set_volume(1)
    print("loader2 file loaded")
