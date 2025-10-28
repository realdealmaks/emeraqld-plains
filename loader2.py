# this file is for images and audio
# loader 2

import pygame
from PIL import Image
from pygame import mixer as mx

def loader2(main_globals):
    main_globals['player_ded'] = pygame.image.load("assets/models/player/ded.png").convert_alpha()
    main_globals['tile_images'] = pygame.image.load("assets/useful images/tiles/tile600x600.png").convert_alpha()
    main_globals['vignette'] = pygame.image.load("assets/useful images/redvignette.png").convert_alpha()
    main_globals['vignette'] = pygame.transform.scale(main_globals['vignette'], (main_globals['screen_w'], main_globals['screen_h']))
    main_globals['menu_background'] = pygame.image.load("assets/useful images/aimenubg.png").convert_alpha()
    main_globals['menu_background'] = pygame.transform.scale(main_globals['menu_background'], (750, 750))
    main_globals['enemy_test_0'] = pygame.image.load("assets/models/enemies/bobber0.png").convert_alpha()
    main_globals['enemy_test_1'] = pygame.image.load("assets/models/enemies/bobber1.png").convert_alpha()
    main_globals['thx'] = pygame.image.load("assets/useful images/thx.png")
    main_globals['save_image'] = pygame.image.load("assets/useful images/save.png")
    main_globals['save_image'] = pygame.transform.scale2x(main_globals['save_image'])
    main_globals['floorboard'] = pygame.image.load('assets/useful images/tiles/image.png')
    main_globals['playergif'] = Image.open("assets/models/player/playergif.gif")

    player_health_images = []
    for i in range(1, 4):
        img = pygame.image.load(f"assets/models/player/playerhealth{i}.png").convert_alpha()
        w, h = img.get_size()
        img = pygame.transform.scale(img, (w * 4, h * 4))
        player_health_images.append(img)
    main_globals['player_health_images'] = player_health_images
    main_globals['death_sound'] = mx.Sound("assets/audio/sfx/vineboom.mp3")
    main_globals['hurt_sound'] = mx.Sound("assets/audio/sfx/new_hurt.ogg") # FUCK
    main_globals['musics'] = ["assets/audio/music/testdroga.mp3", "assets/audio/music/game_over_loop.mp3"]
    mx.music.load(main_globals['musics'][0])
    mx.music.play(-1)
    mx.music.pause()
    mx.music.set_volume(1)

    main_globals['interact_image'] = pygame.image.load("assets/useful images/interact.png").convert_alpha()
    main_globals['interact_image'] = pygame.transform.scale(main_globals['interact_image'], (50, 50))

    main_globals['new_mutation_image'] = pygame.image.load("assets/useful images/mutation.png").convert_alpha()

    main_globals['key_a_hint'] = pygame.image.load("assets/keys/key_A.png").convert_alpha()
    main_globals['key_a_hint'] = pygame.transform.scale2x(main_globals['key_a_hint'])
    main_globals['key_s_hint'] = pygame.image.load("assets/keys/key_S.png").convert_alpha()
    main_globals['key_s_hint'] = pygame.transform.scale2x(main_globals['key_s_hint'])
    main_globals['key_d_hint'] = pygame.image.load("assets/keys/key_D.png").convert_alpha()
    main_globals['key_d_hint'] = pygame.transform.scale2x(main_globals['key_d_hint'])
    main_globals['key_w_hint'] = pygame.image.load("assets/keys/key_W.png").convert_alpha()
    main_globals['key_w_hint'] = pygame.transform.scale2x(main_globals['key_w_hint'])
    main_globals['key_e_hint'] = pygame.image.load("assets/keys/key_E.png").convert_alpha()
    main_globals['key_e_hint'] = pygame.transform.scale2x(main_globals['key_e_hint'])
    main_globals['mouse_blank_hint'] = pygame.image.load("assets/keys/normal_mouse.png").convert_alpha()
    mouse_w = main_globals['mouse_blank_hint'].get_width()
    mouse_h = main_globals['mouse_blank_hint'].get_height()
    main_globals['mouse_blank_hint'] = pygame.transform.scale(main_globals['mouse_blank_hint'], (mouse_w * 3.5, mouse_h * 3.5))
    main_globals['mouse_left_hint'] = pygame.image.load("assets/keys/left_mouse.png").convert_alpha()
    main_globals['mouse_left_hint'] = pygame.transform.scale(main_globals['mouse_left_hint'], (mouse_w * 3.5, mouse_h * 3.5))
    main_globals['mouse_right_hint'] = pygame.image.load("assets/keys/right_mouse.png").convert_alpha()
    main_globals['mouse_right_hint'] = pygame.transform.scale(main_globals['mouse_right_hint'], (mouse_w * 3.5, mouse_h * 3.5))

    main_globals['pedistal_image'] = pygame.image.load("assets/useful images/pedestal.png").convert_alpha()
    main_globals['pedistal_image'] = pygame.transform.scale2x(main_globals['pedistal_image'])

    main_globals['shop_holder'] = pygame.image.load("assets/useful images/shop_holder.png").convert_alpha()

    # weapone sectione
    sword_image = pygame.image.load("assets/models/weapons/sword.png").convert_alpha()
    w, h = sword_image.get_size()
    sword_image = pygame.transform.scale(sword_image, (int(w * 1.2), int(h * 1.2)))
    axe_image = pygame.image.load("assets/models/weapons/axe.png").convert_alpha()
    w, h = axe_image.get_size()
    axe_image = pygame.transform.scale(axe_image, (int(w * 1.2), int(h * 1.2)))

    main_globals['slash_image'] = pygame.image.load("assets/useful images/slash.png").convert_alpha()
    main_globals['slash_image'] = pygame.transform.scale(main_globals['slash_image'], (50, 50))

    main_globals['active_slash'] = None

    main_globals['weapon_images'] = {
        "sword": sword_image,
        "axe": axe_image,
    }

    main_globals['weapon_stats'] = {
        "sword": {"damage": 10, "range": 50, "cooldown": 0.6},
        "axe": {"damage": 15, "range": 75, "cooldown": 1},
    }

    print("loader2 file loaded")
