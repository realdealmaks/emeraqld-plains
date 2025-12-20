# this file is for images and audio

try:
    import pygame
    from PIL import Image
    from pygame import mixer as mx
except ImportError as e:
    print(f"missing module {e}")

def loader2(main_globals):
    # player images
    main_globals['player_ded'] = pygame.image.load("assets/models/player/ded.png").convert_alpha()
    main_globals['playergif'] = Image.open("assets/models/player/playergif.gif")

    # player hud health images
    player_health_images = []
    for i in range(1, 4):
        img = pygame.image.load(f"assets/models/player/playerhealth{i}.png").convert_alpha()
        w, h = img.get_size()
        img = pygame.transform.scale(img, (w * 4, h * 4))
        player_health_images.append(img)
    main_globals['player_health_images'] = player_health_images

    #shop images
    main_globals['shopbase'] = pygame.image.load("assets/useful images/shop/shop_holder.png").convert_alpha()

    # sfx
    main_globals['death_sound'] = mx.Sound("assets/audio/sfx/vineboom.mp3")
    main_globals['hurt_sound'] = mx.Sound("assets/audio/sfx/new_hurt.ogg")

    # enemy images
    main_globals['enemy_test_0'] = pygame.image.load("assets/models/enemies/bobber0.png").convert_alpha()
    main_globals['enemy_test_1'] = pygame.image.load("assets/models/enemies/bobber1.png").convert_alpha()

    # menu images
    menu_bg = pygame.image.load("assets/useful images/aimenubg.png").convert_alpha()
    main_globals['menu_background'] = pygame.transform.scale(menu_bg, (750, 750))

    main_globals['tile_images'] = pygame.image.load("assets/useful images/tiles/tile600x600.png").convert_alpha()

    vignette = pygame.image.load("assets/useful images/redvignette.png").convert_alpha()
    main_globals['vignette'] = pygame.transform.scale(vignette, (main_globals['screen_w'], main_globals['screen_h']))

    return_img = pygame.image.load("assets/useful images/return.png").convert_alpha()
    w, h = return_img.get_size()
    main_globals['return_image'] = pygame.transform.scale(return_img, (int(w * 1.6), int(h * 1.6)))

    main_globals['thx'] = pygame.image.load("assets/useful images/thx.png") # credits
    save_img = pygame.image.load("assets/useful images/save.png").convert_alpha()
    main_globals['save_image'] = pygame.transform.scale2x(save_img)

    # battle pass image
    battlepass_img = pygame.image.load("assets/random images/battle_pass.png").convert_alpha()
    main_globals['battlepass_image'] = pygame.transform.scale(battlepass_img, main_globals['resolution'])

    # mode selection images
    mode1_img = pygame.image.load("assets/useful images/mode1.png").convert_alpha() # background
    mode2_img = pygame.image.load("assets/useful images/mode2.png").convert_alpha() # make some real ones soon
    w, h = main_globals['screen_w'] // 2, main_globals['screen_h']
    main_globals['mode1img'] = pygame.transform.scale(mode1_img, (w, int(h * 1.2)))
    main_globals['mode2img'] = pygame.transform.scale(mode2_img, (w, int(h * 1.2)))

    # dungeon assets
    pedestal = pygame.image.load("assets/useful images/pedestal.png").convert_alpha()
    main_globals['pedistal_image'] = pygame.transform.scale2x(pedestal) # pedestal
    main_globals['shop_item_info_box'] = pygame.image.load("assets/useful images/shop_item_info_box.png").convert_alpha()
    main_globals['shop_item_info_box_rect'] = main_globals['shop_item_info_box'].get_rect()
    main_globals['floorboard'] = pygame.image.load("assets/useful images/tiles/image.png")
    main_globals['shop_holder'] = pygame.image.load("assets/useful images/shop/shop_holder.png").convert_alpha()
    stairs = pygame.image.load("assets/useful images/stairs.png").convert_alpha() # thing to rebuild tilemap
    main_globals['stairs_image'] = pygame.transform.scale2x(stairs)
    main_globals['tile_texture'] = pygame.image.load("assets/useful images/tiles/tile600x600.png")
    # main_globals['tile_texture'] = pygame.image.load("assets/random images/porco.png")
    # main_globals['tile_texture'] = pygame.image.load("assets/random images/tony.png")
    # main_globals['tile_texture'] = pygame.image.load("assets/random images/negro hitler bot.jpg")

    # background music
    main_globals['musics'] = ["assets/audio/music/testdroga.mp3", "assets/audio/music/game_over_loop.mp3", "assets/audio/music/bakus funk trim.mp3"]
    mx.music.load(main_globals['musics'][0])
    mx.music.play(-1)
    mx.music.pause()
    mx.music.set_volume(1)

    # interaction image
    interact = pygame.image.load("assets/useful images/interact.png").convert_alpha()
    main_globals['interact_image'] = pygame.transform.scale(interact, (50, 50))
    main_globals['new_mutation_image'] = pygame.image.load("assets/useful images/mutation.png").convert_alpha()

    # hint images - keys
    key_hints = ["a", "s", "d", "w", "e"]
    for key in key_hints:
        img = pygame.image.load(f"assets/keys/key_{key}.png").convert_alpha()
        main_globals[f"key_{key}_hint"] = pygame.transform.scale(img, (int(img.get_width() * 1.6), int(img.get_height() * 1.6)))

    # hint images - mouse
    mouse_w, mouse_h = pygame.image.load("assets/keys/mouse_left.png").convert_alpha().get_size()
    mouse_hints = ["blank", "left", "right"]
    for hint in mouse_hints:
        img = pygame.image.load(f"assets/keys/mouse_{hint}.png").convert_alpha()
        main_globals[f"mouse_{hint}_hint"] = pygame.transform.scale(img, (int(mouse_w * 3.5), int(mouse_h * 3.5)))

    # pause menu
    screen_w, screen_h = main_globals['screen_w'], main_globals['screen_h']
    background_mult = 0.72
    size_mult = 2.9
    background = pygame.image.load("assets/pause/pause_background.png").convert_alpha()
    background = pygame.transform.scale(background, (screen_w * background_mult, screen_h * background_mult))
    buttons = pygame.image.load("assets/pause/pause_buttons.png").convert_alpha()
    buttons = pygame.transform.scale(buttons, (buttons.get_width() * size_mult, buttons.get_height() * size_mult))
    stats = pygame.image.load("assets/pause/pause_player.png").convert_alpha()
    stats = pygame.transform.scale(stats, (stats.get_width() * size_mult, stats.get_height() * size_mult))
    inventory = pygame.image.load("assets/pause/pause_inventory.png").convert_alpha()
    inventory = pygame.transform.scale(inventory, (inventory.get_width() * size_mult, inventory.get_height() * size_mult))
    main_globals['pause_tabs_images'] = {
        'background': background,
        'buttons': buttons,
        'inventory': inventory,
        'player_stats': stats
    }
    main_globals['pause_buttons'] = { # in order
        'resume': pygame.Rect(0, 0, 200, 50),
        'inventory': pygame.Rect(0, 0, 200, 50),
        'weapon': pygame.Rect(0, 0, 200, 50),
        'quit': pygame.Rect(0, 0, 200, 50)
    }

    # weapon stat frame
    weapon_frame = pygame.image.load("assets/models/weapons/stats/weaponFrame.png").convert_alpha()
    weapon_frame = pygame.transform.scale2x(weapon_frame)
    weapon_frame = pygame.transform.scale2x(weapon_frame)
    main_globals['weapon_frame'] = weapon_frame

    # weapon stats images
    damage_stat = pygame.image.load("assets/models/weapons/stats/damage.png").convert_alpha()
    damage_stat = pygame.transform.scale(damage_stat, (int(damage_stat.get_width() * 1.2), int(damage_stat.get_height() * 1.2)))
    range_stat = pygame.image.load("assets/models/weapons/stats/reach.png").convert_alpha()
    range_stat = pygame.transform.scale(range_stat, (int(range_stat.get_width() * 1.2), int(range_stat.get_height() * 1.2)))
    cooldown_stat = pygame.image.load("assets/models/weapons/stats/cooldown.png").convert_alpha()
    main_globals['weapon_stat_images'] = [damage_stat, range_stat, cooldown_stat]

    # stat light
    weapon_light = pygame.image.load("assets/models/weapons/stats/light.png").convert_alpha()
    weapon_light.set_alpha(70) # light behind the weapon while in stats
    weapon_light = pygame.transform.scale(weapon_light, (int(weapon_light.get_width() * 2.2), int(weapon_light.get_height() * 2.2)))
    main_globals['weapon_light'] = weapon_light

    # weapon images
    sword = pygame.image.load("assets/models/weapons/sword.png").convert_alpha()
    w, h = sword.get_size()
    sword = pygame.transform.scale(sword, (int(w * 1.2), int(h * 1.2)))

    axe = pygame.image.load("assets/models/weapons/axe.png").convert_alpha()
    w, h = axe.get_size()
    axe = pygame.transform.scale(axe, (int(w * 1.2), int(h * 1.2)))

    book = pygame.image.load("assets/models/weapons/burningbook.png").convert_alpha()
    w, h = book.get_size()
    book = pygame.transform.scale(book, (int(w * 2.2), int(h * 2.2)))

    katana = pygame.image.load("assets/models/weapons/katana.png").convert_alpha()
    w, h = katana.get_size()
    katana = pygame.transform.scale(katana, (int(w * 0.7), int(h * 0.7)))

    # reg atk
    main_globals['slash_image'] = pygame.image.load("assets/useful images/slash.png").convert_alpha()
    main_globals['slash_image'] = pygame.transform.scale(main_globals['slash_image'], (50, 50))

    # active atks
    main_globals['active_slash'] = None
    main_globals['active_special_attacks'] = []

    main_globals['weapon_images'] = {
        "sword": sword,
        "axe": axe,
        "book": book,
        "katana": katana
    }

    # special weapons attack image
    katana_attack = pygame.image.load("assets/useful images/katanaslash.png").convert_alpha()

    main_globals['special_attack_images'] = {
        "katana": katana_attack
    }

    damage_mult = main_globals['damage_mult']
    cooldown_mult = main_globals['cooldown_mult']

    main_globals['weapon_stats'] = {
        "sword": {"damage": 15 * damage_mult, "range": 50, "cooldown": 0.6 * cooldown_mult, 'chance': 0.4},
        "axe": {"damage": 20 * damage_mult, "range": 75, "cooldown": 1 * cooldown_mult, 'chance': 0.4},
        "book": {"damage": 25 * damage_mult, "range": 100, "cooldown": 2 * cooldown_mult, 'chance': 0.0},
        "katana": {"damage": 5 * damage_mult, "range": 60, "cooldown": 0.8 * cooldown_mult, 'chance': 0.2}
    }

    # crystals
    crystal_ui_bg = pygame.image.load("assets/models/items/consumables/crystal/crystal_ui_bg.png").convert_alpha()
    main_globals['crystal_ui_bg'] = pygame.transform.scale(crystal_ui_bg, (screen_w, screen_h))

    base = pygame.image.load("assets/models/items/consumables/crystal/crystal_reg.png").convert_alpha()
    base = pygame.transform.scale2x(base)

    green = base.copy()
    green.fill((0,255,0,0), special_flags=pygame.BLEND_RGBA_ADD)

    red = base.copy()
    red.fill((255,0,0,0), special_flags=pygame.BLEND_RGBA_ADD)

    blue = base.copy()
    blue.fill((0,0,255,0), special_flags=pygame.BLEND_RGBA_ADD)

    main_globals['crystal_ui_buttons'] = [green, red, blue]

    print("loader2, ", end="")
