# this file is for loading the dungeon
try:
    import pygame, random, math, types, threading, time
    from pygame import mixer as mx
except ImportError as e:
    print(f"missing module{e}")

def dungeon(main_globals):
    smallfont = pygame.font.Font("assets/font/editundo.ttf", 22)

    def draw_dungeon(main_globals, player, is_paused, facing_left):
        screen = main_globals['screen']
        screen.fill((0, 0, 0))
        main_globals['draw_tiles'](main_globals) # moved up for faster prio
        camera_x = main_globals['camera_x']
        camera_y = main_globals['camera_y']
        camera_speed = main_globals['camera_speed']
        current_frame = main_globals['current_frame'] # gif frame
        frame_timer = main_globals['frame_timer'] # time since last gif frame change
        frame_delay = main_globals['frame_delay'] # time between gif frames
        frames = main_globals['frames'] # player gif frames
        player_size = main_globals['player_size']
        enemy_size = main_globals['enemy_size']
        enemy_list = main_globals['enemy_list']
        tilemap = main_globals['tilemap']

        target_x, target_y = main_globals['get_camera_offset'](main_globals, player, main_globals['tile_size'])
        camera_x += (target_x - camera_x) * camera_speed
        camera_y += (target_y - camera_y) * camera_speed
        main_globals['camera_x'] = camera_x
        main_globals['camera_y'] = camera_y
        ts = main_globals['tile_size'] + main_globals['tile_offset']

        if 'enemy_groups' not in main_globals:
            main_globals['enemy_groups'] = []

        # activate tiles
        ts = main_globals['tile_size'] + main_globals['tile_offset']

        left = int((player.x + player_size // 2) // ts)
        right = int((player.x + player_size // 2 + player_size - 1) // ts)
        top = int((player.y + player_size // 2) // ts)
        bottom = int((player.y + player_size // 2 + player_size - 1) // ts)

        for tx in range(left, right + 1):
            for ty in range(top, bottom + 1):
                tile = (tx, ty)
                if tile not in main_globals['active_tiles']:
                    main_globals['active_tiles'].append(tile)
                    print(f"added active tile {tile}, ", end="")

        # tile checking systems
        for row_idx, row in enumerate(main_globals['tilemap']):
            for col_idx, tile_type in enumerate(row):

                if tile_type == 99: # makes player spawn here
                    if main_globals['spawn_set'] == False:
                        ts = main_globals['tile_size'] + main_globals['tile_offset']
                        main_globals['spawn_x'] = col_idx * ts + (main_globals['tile_size'] - player_size) // 2
                        main_globals['spawn_y'] = row_idx * ts + (main_globals['tile_size'] - player_size) // 2

                        if main_globals.get('player') is None: # for new player
                            main_globals['player'] = main_globals['Player'](main_globals, main_globals['spawn_x'], main_globals['spawn_y'])
                        else: # for existing player
                            main_globals['player'].x = main_globals['spawn_x']
                            main_globals['player'].y = main_globals['spawn_y']
                        main_globals['spawn_set'] = True
                    print(main_globals['shop_initialised'])

                elif tile_type == 2:
                    screen.blit(main_globals['pedistal_image'], (col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_width() // 2, row_idx * ts - camera_y + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_height() // 2 + 50))

                elif tile_type == 3: # enemy spawn tile
                    ts = main_globals['tile_size'] + main_globals['tile_offset']
                    if main_globals['groups_spawned'] >= sum(i.count(3) for i in tilemap): # not dIh
                        pass
                    else:
                        tile_center_x = col_idx * ts + main_globals['tile_size'] // 2
                        tile_center_y = row_idx * ts + main_globals['tile_size'] // 2
                        # i dont know what this is for and im not going to question it \/
                        '''upper limit :D''' # ookay?
                        upper = random.randrange(2, 10)
                        previous_coords = []
                        min_distance = 100
                        hemorrhoids_in_tile = []
                        for i in range(1, upper): # adds x through y
                            attempts = 0
                            max_attempts = 500 # give him some tries
                            while attempts < max_attempts: # to get a valid pos
                                deviation = random.randrange(50, 200)
                                enemy_x = tile_center_x - enemy_size // 2 + random.choice((deviation, -deviation))
                                enemy_y = tile_center_y - enemy_size // 2 + random.choice((deviation, -deviation))

                                # check distance to the previous cocks
                                too_close = False
                                for (px, py) in previous_coords:
                                    if math.isclose(enemy_x, px, abs_tol=min_distance) and math.isclose(enemy_y, py, abs_tol=min_distance):
                                        too_close = True
                                        break # too close to another cock

                                if not too_close: # wow he did it
                                    new_enemy = main_globals['Enemy'](main_globals, enemy_x, enemy_y, random.choice([0, 1]))
                                    enemy_list.append(new_enemy)
                                    hemorrhoids_in_tile.append(new_enemy)
                                    previous_coords.append((enemy_x, enemy_y))
                                    break  # valid position found
                                attempts += 1

                        main_globals['enemy_groups'].append({
                            'tile_pos': (row_idx, col_idx),
                            'enemies': hemorrhoids_in_tile,
                            'active': True
                        })
                        print(f"spawned group {main_globals['groups_spawned']} on ({row_idx}, {col_idx}), ", end="")
                        main_globals['groups_spawned'] += 1

                elif tile_type == 88: # shop tile with literal yanderedev code # dont worry makus im here
                    shops_x = col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['shop_item_info_box'].get_width() // 2
                    shops_y = row_idx * ts - camera_y + main_globals['tile_size'] // 2 - main_globals['shop_item_info_box'].get_height() // 2 + 50

                    offset = 200
                    pedestal_x_left = col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_width() // 2 - offset
                    pedestal_x_right = col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_width() // 2 + offset
                    pedestal_x_center = col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_width() // 2
                    pedestal_y = row_idx * ts - camera_y + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_height() // 2 + offset
                    
                    #screen.blit(main_globals['shop_holder'], (shops_x, shops_y))
                    screen.blit(main_globals['pedistal_image'], (pedestal_x_center, pedestal_y))
                    screen.blit(main_globals['pedistal_image'], (pedestal_x_left, pedestal_y))
                    screen.blit(main_globals['pedistal_image'], (pedestal_x_right, pedestal_y))

                    # rcon_name, rcon_desc, rcon_func, rcon_img = random.choice(list(main_globals['items'].items()))
                    excluded_c = ['fuck', 'crystal', 'crystal_fragments'] # excluded items from shop pool
                    available_c = [key for key in main_globals['items'].keys() if key not in excluded_c] # items allowed in shop

                    # create items you can purchase
                    if not main_globals['shop_initialised']:
                        main_globals['article1'], main_globals['article2'], main_globals['article3'] = None, None, None
                        print('articles reset')
                        for article_key in ['article1', 'article2', 'article3']:
                            random_c = random.choice(available_c) # select it
                            main_globals[article_key] = random_c
                            article = main_globals[article_key] # get it
                            print(f"article: {article}, random item: {random_c}")
                        main_globals['shop_initialised'] = True
                        print(main_globals['article1'], main_globals['article2'], main_globals['article3'])
                    else:
                        print('shop already init')

                    # and blit them too
                    if main_globals['article2']: screen.blit(main_globals['items'][main_globals['article2']]['image'], (col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['items'][main_globals['article2']]['image'].get_width() // 2, pedestal_y - 20))
                    if main_globals['article1']: screen.blit(main_globals['items'][main_globals['article1']]['image'], (col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['items'][main_globals['article1']]['image'].get_width() // 2 - 200, pedestal_y - 20))
                    if main_globals['article3']: screen.blit(main_globals['items'][main_globals['article3']]['image'], (col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['items'][main_globals['article3']]['image'].get_width() // 2 + 200, pedestal_y - 20))

                    screen.blit(main_globals['shop_item_info_box'], (shops_x, shops_y))

                    info_box_width, info_box_height = main_globals['shop_item_info_box'].get_size()
                    info_box_center_y = shops_y + info_box_height // 2

                    # check pedestals

                    pedestals = [
                        {'key': 'article1', 'x': pedestal_x_left},
                        {'key': 'article2', 'x': pedestal_x_center},
                        {'key': 'article3', 'x': pedestal_x_right}
                    ]

                    positions = {
                        'potion_x': col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['small_potion_big'].get_width() // 2,
                        'potion_y': #row_idx * ts - camera_y + main_globals['tile_size'] // 2 - main_globals['shop_item_info_box'].get_height() // 2
                        info_box_center_y,
                        'offset': info_box_width // 4
                    }
                    
                    for pedestal in pedestals:
                        article_key = pedestal['key']
                        article_x = pedestal['x']

                        if main_globals[article_key] is not None:
                            pedestal_pos = (
                                col_idx * ts + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_width() // 2 + (article_x - pedestal_x_center),
                                row_idx * ts + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_height() // 2 + 200
                            )

                            if main_globals['distance_to'](player, pedestal_pos) < main_globals['interact_distance']:
                                screen.blit(
                                    main_globals['interact_image'],
                                    (
                                        article_x + main_globals['pedistal_image'].get_width() // 2 - main_globals['interact_image'].get_width() // 2,
                                        pedestal_y - main_globals['interact_image'].get_height() - 10
                                    )
                                )

                                # main_globals['items'][main_globals[article_key]]['image']
                                screen.blit(main_globals[f'{main_globals[article_key]}_big'], (positions['potion_x'] - positions['offset'], positions['potion_y'] - 10))

                                if main_globals['pressed_e']:
                                    item = main_globals['items'][main_globals[article_key]]
                                    if item['price'] <= main_globals['player'].wealth:
                                        main_globals['add_to_inventory'](main_globals, main_globals[article_key])
                                        main_globals['player'].wealth -= item['price']
                                        main_globals[article_key] = None
                                        main_globals['pressed_e'] = False

                    #screen.blit(main_globals['shop_item_info_box'], (row_idx * ts - camera_y + main_globals['tile_size'] // 2 - main_globals['shop_item_info_box'].get_height() // 2, row_idx * ts - camera_y + main_globals['tile_size'] // 2 - main_globals['shop_item_info_box'].get_height() // 2 - 200))

                    # interact with shop
                    #if main_globals['distance_to'](player, (main_globals['shop'].stand_x, main_globals['shop'].stand_y)) < main_globals['interact_distance']:
                    #    screen.blit(main_globals['interact_image'], (main_globals['shop'].stand_x, main_globals['shop'].stand_y + 50))
                    #    if main_globals['pressed_e']:
                    #        main_globals['game_stage'] = "shopping"

                elif tile_type == 98: # end tile
                    tile_center = type('', (), {
                        'x': col_idx * ts + main_globals['tile_size'] // 2,
                        'y': row_idx * ts + main_globals['tile_size'] // 2
                    })()
                    screen.blit(main_globals['stairs_image'], (tile_center.x - camera_x - main_globals['stairs_image'].get_width() // 2, tile_center.y - camera_y - main_globals['stairs_image'].get_height() // 2))
                    if main_globals['distance_to'](player, tile_center) < main_globals['interact_distance']:
                        screen.blit(main_globals['interact_image'],
                            (tile_center.x - camera_x - main_globals['interact_image'].get_width() // 2, tile_center.y - camera_y - main_globals['interact_image'].get_height() // 2))
                        if main_globals['pressed_e']:
                            if main_globals['check_floor'](main_globals, main_globals['current_floor']) and main_globals['current_floor'] != 1 or 0 and main_globals['in_shop']:
                                main_globals['remake_floor']()
                                main_globals['shop_initialised'] = False
                                # print(main_globals['in_shop'])
                            elif main_globals['in_shop']:
                                main_globals['remake_floor']()
                                main_globals['in_shop'] = False
                                main_globals['article1'], main_globals['article2'], main_globals['article3'] = None, None, None
                                main_globals['shop_initialised'] = False
                            else:
                                for call in main_globals['shop_tilemap_calls']:
                                    eval(call)
                                rebuild_walkable_mask(main_globals)
                                main_globals['in_shop'] = True
                                # print(main_globals['in_shop'])
                        # print(tile_center)

        # drawing things on tiles

        for weapon in main_globals['weapons_on_map'][:]:

            if not main_globals['is_on_active_tile'](main_globals, weapon.x, weapon.y):
                continue # skip if not active

            weapon_image = main_globals['weapon_images'][weapon.name]
            draw_x = weapon.x - weapon_image.get_width() // 2 - camera_x + 15
            draw_y = weapon.y - weapon_image.get_height() // 2 - camera_y
            weapon.draw(screen, draw_x, draw_y)

            if main_globals['distance_to'](player, weapon) < main_globals['interact_distance']: # interact
                screen.blit(main_globals['interact_image'], (draw_x, draw_y + weapon_image.get_height()))
                main_globals['interact'](main_globals, player, weapon.x, weapon.y, lambda w=weapon: w.pickup(player))

        # enemy groups
        for group in main_globals['enemy_groups']:

            gx, gy = group['tile_pos']
            if (gy, gx) not in main_globals['active_tiles']: # skip if not in active tile
                continue

            # check if ANY enemy in the group detects the player
            group_should_activate = False
            for enemy in group['enemies']:

                # draw !
                if enemy.active and enemy.active_counter > 0:
                    enemy.active_counter -= main_globals['dt'] * 60
                    text_surface = main_globals['font'].render("!", True, (255, 70, 70))
                    main_globals['screen'].blit(text_surface, (enemy.x - main_globals['camera_x'], enemy.y - main_globals['camera_y'] - enemy.size // 2 - 8))

                if not enemy.active and enemy.detect(player):
                    for e in group['enemies']:
                        e.active = True
                    group_should_activate = True
                    break

            # if any enemy detects the player, activate the entire group
            if group_should_activate:
                for enemy in group['enemies']:
                    enemy.active = True
                player.locked = True

        # check if all enemies in a group are dead, and unlock player if so
        for group in main_globals['enemy_groups']:
            # if every enemy in this group is dead
            if all(not enemy.alive for enemy in group['enemies']):
                if group['active']:
                    group['active'] = False
                    main_globals['groups_cleared'] += 1
                    if main_globals['groups_cleared'] > main_globals['most_groups_cleared']:
                        main_globals['most_groups_cleared'] = main_globals['groups_cleared']
                        main_globals['save'](main_globals, most_groups_cleared=main_globals['most_groups_cleared'])
                    print(f"group at {group['tile_pos']} cleared, ", end="")
                    player.locked = False # unlock player once group is cleared

        # check if slash hits enemy
        if 'active_slashes' in main_globals and main_globals['active_slashes']:
            active_slashes = main_globals['active_slashes']
            for enemy in enemy_list:
                if not enemy.alive: # skip if dead
                    continue
                for slash in active_slashes: # check if slash hits enemy ( for real ts time )
                    if pygame.Rect.colliderect(enemy.rect, slash['rect']):
                        if enemy not in slash['hit_enemies']:
                            current_weapon = player.weapons
                            damage = main_globals['weapon_stats'][current_weapon[0].name]['damage'] # or use weapon damage eh? # YES YES I KNOW!!
                            enemy.damaged(damage)
                            slash['hit_enemies'].add(enemy) # add to list that the slash hit ( so it doesnt spam )

        # draw slashes
        if 'active_slashes' in main_globals:
            now = pygame.time.get_ticks() # current time in ms
            still_active = []
            for slash in main_globals['active_slashes']:
                if now < slash['expiry']: # if expired :(
                    screen.blit(slash['image'], slash['rect'])
                    still_active.append(slash)
            main_globals['active_slashes'] = still_active

        player_frame = pygame.transform.scale(frames[current_frame], (player_size * 3, player_size * 3))
        if main_globals['facing_left']:
            player_frame = pygame.transform.flip(player_frame, True, False)

        # draw bob
        for enemy in enemy_list:
            enemy.draw(enemy.type)

        # draw special attacks
        if 'active_special_attacks' in main_globals or 'active_special_children' in main_globals:
            now = pygame.time.get_ticks()

            # update parents
            still_parents = []
            for special_attack in main_globals.get('active_special_attacks', []):

                # draw if visible
                if special_attack.get('draw', True) and (special_attack['expiry'] == -1 or now < special_attack['expiry']):
                    screen.blit(special_attack['image'], special_attack['rect'])

                # spawn next child
                if special_attack.get('hits', 0) > 0 and now >= special_attack.get('next_spawn', 0):
                    if special_attack.get('flip_next', True):
                        child_image = special_attack.get('flipimage', special_attack['image'])
                        child_rect = special_attack.get('fliprect', special_attack['rect']).copy()
                    else:
                        child_image = special_attack['image']
                        child_rect = special_attack['rect'].copy()

                    # create child attack
                    child_attack = {
                        'image': child_image,
                        'rect': child_rect.copy(),
                        'expiry': now + special_attack.get('child_lifetime', 150),
                        'hit_enemies': set(),
                        'draw': True,
                        'effect': special_attack.get('effect', None)
                    }
                    main_globals.setdefault('active_special_children', []).append(child_attack)

                    # toggle for next spawn
                    special_attack['flip_next'] = not special_attack.get('flip_next', True)
                    special_attack['hits'] -= 1
                    special_attack['next_spawn'] = now + special_attack.get('delay', 250)

                # keep parent alive
                if special_attack['expiry'] == -1 or now < special_attack['expiry']:
                    still_parents.append(special_attack)

            main_globals['active_special_attacks'] = still_parents

            # update children
            still_children = []
            for child in main_globals.get('active_special_children', []):
                if now < child['expiry']:
                    if child.get('draw', True):
                        screen.blit(child['image'], child['rect'])
                    still_children.append(child)

            main_globals['active_special_children'] = still_children

            # check if special attack hits enemy
            for attack in main_globals.get('active_special_children', []):
                for enemy in enemy_list:
                    if not enemy.alive: # skip if dead
                        continue
                    if pygame.Rect.colliderect(enemy.rect, attack['rect']):
                        if enemy not in attack['hit_enemies']:
                            current_weapon = player.weapons
                            damage = main_globals['weapon_stats'][current_weapon[0].name]['damage']
                            enemy.damaged(damage)
                            attack['hit_enemies'].add(enemy)

        # change player orientation? is it orientation? just change the way he is looking
        offset_x = (player_size * 3 - player_size) // 2
        offset_y = (player_size * 3 - player_size) // 2
        shake_x, shake_y = player.shake()
        draw_x = player.x - camera_x - offset_x + shake_x
        draw_y = player.y - camera_y - offset_y + shake_y
        if facing_left: # offset because the image is not centered
            draw_x += 30
        else:
            draw_x -= 30

        # draw weapon to player
        screen.blit(player_frame, (draw_x, draw_y))
        if len(player.weapons) > 0:
            weapon = player.weapons[0]
            weapon_image = main_globals['weapon_images'][weapon.name]
            scale_fraction = 1.8 # scale by this much ( 1.0 is original )
            weapon_image = pygame.transform.scale(weapon_image, ((main_globals['player_size'] // 2) * scale_fraction, (main_globals['player_size'] // 2) * scale_fraction))
            weapon_image = pygame.transform.rotate(weapon_image, 65)
            weapon_image = pygame.transform.flip(weapon_image, True, False)

            weapon_x = draw_x + player_size + 40 # x offset
            weapon_y = draw_y + player_size // 2 + 36 # y offset

            if facing_left: # offset because of player offset
                weapon_image = pygame.transform.flip(weapon_image, True, False)
                weapon_x -= int(weapon_image.get_width()*1.24) if weapon.name in main_globals['dual_wields'] else int(weapon_image.get_width()*1.46) # most probably will break

            if weapon.name in main_globals['dual_wields']:
                screen.blit(weapon_image, (weapon_x - weapon_image.get_width() // 2.7, weapon_y))

            screen.blit(weapon_image, (weapon_x, weapon_y))

        # draw blood particles
        new_particles = []
        for body, shape, color, lifetime, max_lifetime in main_globals['blood_particles']:
            # stop at landing y
            if body.position.y > body.landing_y:
                body.position = (body.position.x, body.landing_y)
                body.velocity = (0, 0)

            # particle fade out
            alpha = max(0, min(255, int(255 * (lifetime / max_lifetime))))
            draw_color = (*color, alpha)
            pos = int(body.position.x - main_globals['camera_x']), int(body.position.y - main_globals['camera_y'])
            surf = pygame.Surface((int(shape.radius*2), int(shape.radius*2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, draw_color, (int(shape.radius), int(shape.radius)), int(shape.radius))
            screen.blit(surf, (pos[0]-shape.radius, pos[1]-shape.radius))

            lifetime -= main_globals['dt']
            if lifetime > 0:
                new_particles.append((body, shape, color, lifetime, max_lifetime))
            else:
                # remove particle
                main_globals['space'].remove(body, shape)

        main_globals['blood_particles'] = new_particles

        # pausing of the game
        if not is_paused: # not paused
            main_globals['draw_minimap'](main_globals, main_globals['tilemap'], player)

            # enemy attack
            for enemy in enemy_list:
                enemy.attack(player)

            # animate player
            frame_timer += 1
            if frame_timer >= frame_delay:
                frame_timer = 0
                if main_globals['moving_up'] or main_globals['moving_down'] or main_globals['moving_left'] or main_globals['moving_right']:
                    current_frame = (current_frame + 1) % len(frames)
                else:
                    current_frame = 1
            main_globals['frame_timer'] = frame_timer
            main_globals['current_frame'] = current_frame

            # move enemies if they are active
            for enemy in enemy_list: 
                if enemy.active: enemy.move(player)

            # + money
            for item in main_globals['money_texts']:
                screen.blit(item['text'], (130, 300))
                item['timer'] -= main_globals['dt']
                if item['timer'] <= 0:
                    main_globals['money_texts'].remove(item)
                    player.effect("money", item['amount'])
                    print(f"player got {item['amount']} moneys, ", end="")
                    if player.wealth > main_globals['richest_player']:
                        main_globals['richest_player'] = player.wealth
                        main_globals['save'](main_globals, richest_player=main_globals['richest_player'])

            # + items image
            offset = 25 # from bottom right
            padding = 5 # between items
            for index, item in enumerate(main_globals['inventory_texts'][:]):
                img = item['image']
                text = item['text']

                x = screen.get_width() - img.get_width() - offset
                y = screen.get_height() - img.get_height() - offset - index * (img.get_height() + padding)

                text_y = y + (img.get_height() - text.get_height()) // 2
                text_x = x - text.get_width() - 5

                background = pygame.Surface((img.get_width() + text.get_width() + 10, img.get_height()), pygame.SRCALPHA)
                background.fill((50, 50, 50, 150))
                screen.blit(background, (text_x - 5, y))

                screen.blit(text, (text_x, text_y))
                screen.blit(img, (x, y))

                item['timer'] -= main_globals['dt']
                if item['timer'] <= 0:
                    main_globals['inventory_texts'].remove(item)

            # draw damage numbers (enemy)
            new_damages = []

            for dmg in main_globals['damages_takens']:
                enemy_ref = dmg['enemy_ref']

                if enemy_ref.alive:
                    x = enemy_ref.x - main_globals['camera_x']
                    y = enemy_ref.y - main_globals['camera_y'] - 20 # 20 px above

                    # rise
                    lifetime = dmg.get('lifetime', 1.0) # seconds to expire
                    dmg.setdefault('lifetime', lifetime)
                    progress = 1.0 - dmg['timer'] / lifetime
                    y -= progress * 30 # rise 30 px

                    # fade
                    alpha = max(0, min(255, int((dmg['timer'] / lifetime) * 255)))

                    # text
                    text_surface = smallfont.render(dmg['value'], True, (255, 40, 40))
                    text_surface.set_alpha(alpha)
                    main_globals['screen'].blit(text_surface, (x, y))

                # decrease timer
                dmg['timer'] -= main_globals['dt']
                if dmg['timer'] > 0:
                    new_damages.append(dmg)

            main_globals['damages_takens'] = new_damages

            main_globals['draw_vignette'](main_globals, player)
            mx.music.unpause()
            dx = dy = 0
            if main_globals['moving_up']: dy -= 1
            if main_globals['moving_down']: dy += 1
            if main_globals['moving_left']:
                dx -= 1
                main_globals['facing_left'] = True
            if main_globals['moving_right']:
                dx += 1
                main_globals['facing_left'] = False
            player.move(dx, dy)
            main_globals['draw_hud'](main_globals, player)

            if main_globals['tutorial_floor']:
                main_globals['tutorial_text'](main_globals)

        else: # if paused
            main_globals['pause_menu'](main_globals)

        if main_globals['choosing']: # if he is in some menu
            if main_globals['choosing_crystal']: # if he is choosing a crystal effect
                main_globals['crystal_ui'](main_globals)

    def remake_floor(): # remakes the floor
        tilemap = main_globals['tilemap']
        rows = len(tilemap)
        cols = len(tilemap[0])
        min_distance = 5 # minimum distance between start and end
        min_straight = 1 # minimum distance before turning again
        tile_choices = [1, 2, 3] # tiles the path can be filled with
        tile_probs = [0.6, 0.1, 0.3] # in order of ^ # *100 in %

        main_globals['tutorial_floor'] = False # dont show tutorial text

        # pick start and end far enough apart
        while True:
            start_r = random.randint(0, rows - 1)
            start_c = random.randint(0, cols - 1)
            end_r = random.randint(0, rows - 1)
            end_c = random.randint(0, cols - 1)
            distance = abs(start_r - end_r) + abs(start_c - end_c)
            if distance >= min_distance:
                break

        # mark start and end
        main_globals['update_tile'](main_globals, start_c, start_r, 99)
        main_globals['update_tile'](main_globals, end_c, end_r, 98)

        # r = hoRizontal c = vertiCal
        current_r, current_c = start_r, start_c
        current_dir = 'r' if random.random() < 0.5 else 'c'
        straight_count = 0

        path_tiles = [] # tiles between start and end

        turn_chance = 0.3

        while (current_r, current_c) != (end_r, end_c):
            dr = end_r - current_r
            dc = end_c - current_c

            # random turn
            if straight_count >= min_straight and random.random() < turn_chance:
                # flip direction
                current_dir = 'c' if current_dir == 'r' else 'r'
                straight_count = 0

                # move exactly 1 tile in the new direction
                if current_dir == 'r':
                    current_c += 1 if dc > 0 else -1
                else:
                    current_r += 1 if dr > 0 else -1

                # clamp
                current_r = max(0, min(rows - 1, current_r))
                current_c = max(0, min(cols - 1, current_c))

                # write tile
                tile_value = random.choices(tile_choices, weights=tile_probs)[0]
                path_tiles.append((current_r, current_c, tile_value))
                continue

            can_turn = straight_count >= min_straight

            if current_dir == 'r' and dc != 0:
                step = 1 if dc > 0 else -1
                current_c += step
                straight_count += 1
            elif current_dir == 'c' and dr != 0:
                step = 1 if dr > 0 else -1
                current_r += step
                straight_count += 1
            elif can_turn:
                if current_dir == 'r' and dr != 0:
                    step = 1 if dr > 0 else -1
                    current_r += step
                    current_dir = 'c'
                    straight_count = 1
                elif current_dir == 'c' and dc != 0:
                    step = 1 if dc > 0 else -1
                    current_c += step
                    current_dir = 'r'
                    straight_count = 1
            else:
                if current_dir == 'r' and dc == 0 and dr != 0:
                    step = 1 if dr > 0 else -1
                    current_r += step
                    current_dir = 'c'
                    straight_count = 1
                elif current_dir == 'c' and dr == 0 and dc != 0:
                    step = 1 if dc > 0 else -1
                    current_c += step
                    current_dir = 'r'
                    straight_count = 1

            # clamp again
            current_r = max(0, min(len(tilemap) - 1, current_r))
            current_c = max(0, min(len(tilemap[0]) - 1, current_c))

            # append tile if not start or end
            if (current_r, current_c) not in [(start_r, start_c), (end_r, end_c)]:
                tile_value = random.choices(tile_choices, weights=tile_probs)[0]
                path_tiles.append((current_r, current_c, tile_value))

        # add branches
        num_branches = random.randint(0, 2) # how many
        branch_length_range = (1, 4) # how long

        for _ in range(num_branches):
            if not path_tiles:
                break
            # pick a random tile in the path as branch start
            br, bc, _ = random.choice(path_tiles)
            branch_dir = random.choice(['r', 'c'])
            branch_length = random.randint(*branch_length_range)
            straight_count = 0

            for _ in range(branch_length):
                if branch_dir == 'r':
                    step = random.choice([-1, 1])
                    bc += step
                else:
                    step = random.choice([-1, 1])
                    br += step

                # clamp as always
                br = max(0, min(rows - 1, br))
                bc = max(0, min(cols - 1, bc))

                # dont overlap start and end
                if (br, bc) in [(start_r, start_c), (end_r, end_c)]:
                    break

                # make tile only if not already in path
                if not any(t[0] == br and t[1] == bc for t in path_tiles):
                    tile_value = random.choices(tile_choices, weights=tile_probs)[0]
                    path_tiles.append((br, bc, tile_value))

                straight_count += 1
                # only turn after min straight
                if straight_count >= min_straight and random.random() < 0.3:
                    branch_dir = 'c' if branch_dir == 'r' else 'r'
                    straight_count = 0

        # force at least 1 tile 2 or 3
        if not any(tile[2] in (2, 3) for tile in path_tiles):
            idx = random.randint(0, len(path_tiles) - 1)
            r, c, _ = path_tiles[idx]
            path_tiles[idx] = (r, c, random.choice([2, 3]))

        # ts shit gets overwritten
        main_globals['update_tile'](main_globals, end_c, end_r, 98)

        # update tilemap
        for r, c, val in path_tiles:
            main_globals['update_tile'](main_globals, c, r, val)

        print("new tilemap is:")
        main_globals['current_floor'] += 1 # save floors
        if main_globals['current_floor'] > main_globals['best_floor']:
            main_globals['best_floor'] = main_globals['current_floor']
            main_globals['save'](main_globals, best_floor=main_globals['best_floor'])
        for i in range(len(main_globals['tilemap'])):
            print(main_globals['tilemap'][i])
        main_globals['rebuild_walkable_mask'](main_globals)

    def update_tile(main_globals, col_idx, row_idx, new_tile_type): # updates a specific tile
        # ex. update_tilemap(main_globals, 0, 0, 99)
        # update tilemap ( glogales, column index, row index, tile type )

        ts = main_globals['tile_size'] + main_globals['tile_offset']
        center_x = col_idx * ts + main_globals['tile_size'] // 2
        center_y = row_idx * ts + main_globals['tile_size'] // 2

        if new_tile_type == 99: # clears other tiles if new tile is a spawn tile
            print("clearing tiles")
            for i in range(len(main_globals['tilemap'])):
                for j in range(len(main_globals['tilemap'][0])):
                    main_globals['tilemap'][i][j] = 0
            main_globals['player'].respawn()

        main_globals['weapons_on_map'] = [ # remove all weapons that are not on the new tiles
        w for w in main_globals['weapons_on_map']
            if not (math.isclose(w.x, center_x, abs_tol=1) and math.isclose(w.y, center_y, abs_tol=1))
        ]

        print(f"updating tilemap with {col_idx, row_idx} as type {new_tile_type}, ", end="")
        main_globals['tilemap'][row_idx][col_idx] = new_tile_type # actually updates the tile
        if 'groups_spawned' in main_globals:
            main_globals['groups_spawned'] = 0

    def get_camera_offset(main_globals, player, tile_size): # offset of the camera depending on tile with player
        player_center_x = player.x + main_globals['player_size'] // 2
        player_center_y = player.y + main_globals['player_size'] // 2

        tile_x = player_center_x // (tile_size + main_globals['tile_offset'])
        tile_y = player_center_y // (tile_size + main_globals['tile_offset'])
        # camera moves to the center of the tile
        offset_x = tile_x * (tile_size + main_globals['tile_offset']) + tile_size // 2 - main_globals['screen'].get_width() // 2
        offset_y = tile_y * (tile_size + main_globals['tile_offset']) + tile_size // 2 - main_globals['screen'].get_height() // 2
        return offset_x, offset_y

    def tile_texturer(main_globals, mask, store_key='textured_tiles'):
        texture = main_globals['tile_texture']
        main_globals['textures_ready'] = False
        tex_w, tex_h = texture.get_size() # texture image size
        map_w, map_h = mask.get_size() # map size
        ts = main_globals['tile_size'] + main_globals['tile_offset']

        texture_surface = pygame.Surface((map_w, map_h), pygame.SRCALPHA)

        # progress
        main_globals['texturing_progress'] = {'rows_done': 0, 'total_rows': map_h}

        for y in range(0, map_h, tex_h):
            for x in range(0, map_w, tex_w):
                texture_surface.blit(texture, (x, y))
            main_globals['texturing_progress']['rows_done'] = y + tex_h

        mask_array = pygame.surfarray.pixels3d(mask).copy()
        mask_copy = mask.copy()

        # check tilemap
        tilemap = main_globals['tilemap']
        for row_index, row in enumerate(tilemap):
            for col_index, tile in enumerate(row):
                if tile == 0:
                    continue  # skip empty tile

                x0 = col_index * ts
                y0 = row_index * ts
                x1 = min(x0 + ts, map_w)
                y1 = min(y0 + ts, map_h)

                if x1 <= x0 or y1 <= y0:
                    continue

                tile_region = mask_array[x0:x1, y0:y1]

                green_mask = tile_region[:, :, 1] > 0 # get green
                tile_region[green_mask] = [255, 255, 255] # set it to white

                # apply
                pygame.surfarray.blit_array(mask_copy.subsurface((x0, y0, x1 - x0, y1 - y0)), tile_region)

        del mask_array

        # apply texture
        texture_surface.blit(mask_copy, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        main_globals[store_key] = texture_surface

        if store_key != 'textured_tiles':
            main_globals['textures_ready'] = True

        # remove progress
        if 'texturing_progress' in main_globals:
            del main_globals['texturing_progress']

    def tt_thread(main_globals, mask, store_key='textured_tiles'): # tile texturers thread
        thread = threading.Thread(target=main_globals['tile_texturer'], args=(main_globals, mask, store_key))
        thread.start()
        return thread

    def draw_texturing_progress(main_globals):
        screen = main_globals['screen']
        screen.fill((0, 0, 0))
        font = pygame.font.Font("assets/font/editundo.ttf", 20) # between small and smaller font
        if 'texturing_progress' in main_globals:
            screen = main_globals['screen']
            progress = main_globals['texturing_progress']
            total = progress['total_rows']
            done = progress['rows_done']
            screen_w, screen_h = screen.get_size()

            if 'current_bar_width' not in progress:
                progress['current_bar_width'] = 0
                progress['start_time'] = time.time()

            target_width = int(screen_w * done / total)
            progress['current_bar_width'] += (target_width - progress['current_bar_width']) * 0.1
            bar_width = int(progress['current_bar_width'])

            # draw bar
            bar_height = 20
            bar_y = screen_h - bar_height
            pygame.draw.rect(screen, (0, 255, 0), (0, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 0, 0), (0, bar_y, screen_w, bar_height), 2)

            # % done
            percent = int(done / total * 100)
            if percent > 100: # it goes to 103 btw
                percent = 100
            percent_text = font.render(f"{percent}%", True, (255, 255, 255))
            percent_rect = percent_text.get_rect(center=(screen_w // 2, bar_y - 10))
            screen.blit(percent_text, percent_rect)

            # time left
            elapsed = time.time() - progress['start_time']
            if done > 0:
                time_left = elapsed / done * (total - done)
                approx_text = font.render(f"{int(time_left)} seconds left", True, (255, 255, 255))
                screen.blit(approx_text, (5, percent_rect.y))

            pygame.display.flip()

    def draw_tiles(main_globals):
        screen = main_globals['screen']
        camera_x = int(main_globals['camera_x'])
        camera_y = int(main_globals['camera_y'])
        screen_w, screen_h = screen.get_size()

        # locked or unlocked player
        texture = main_globals['textured_tiles'] if not main_globals['player'].locked else main_globals['locked_textured_tiles']

        tex_w, tex_h = texture.get_size()

        # clamp camera to bounds
        cam_x = max(0, min(camera_x, tex_w - screen_w))
        cam_y = max(0, min(camera_y, tex_h - screen_h))

        # how much the camera was clamped
        offset_x = camera_x - cam_x
        offset_y = camera_y - cam_y

        subsurf = texture.subsurface((cam_x, cam_y, min(screen_w, tex_w), min(screen_h, tex_h)))

        # blit what you can see
        screen.blit(subsurf, (-offset_x, -offset_y))

    def make_initial_walkable_surface(tilemap, main_globals, bridging=True, counter=0): # make the initial walkable mask as its own surface
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        tile_size = main_globals['tile_size']
        mask = pygame.Surface((len(tilemap[0]) * ts, len(tilemap) * ts))
        mask.fill((0, 0, 0)) # black is not walkable

        bridge_fraction = 0.25 # *100 in % of tile size
        bridge_size = int(tile_size * bridge_fraction)

        for row_idx, row in enumerate(tilemap):
            for col_idx, tile_type in enumerate(row):
                if tile_type in main_globals['walkable_tiles']:
                    tx = col_idx * ts
                    ty = row_idx * ts
                    # draw main tile in mask
                    pygame.draw.rect(mask, (0, 255, 0), (tx, ty, tile_size, tile_size))

                    if bridging == True: # for enabling bridges/pathing between tiles
                        # horizontal bridge
                        if col_idx + 1 < len(row) and tilemap[row_idx][col_idx + 1] in main_globals['walkable_tiles']:
                            pygame.draw.rect(mask, (0, 255, 0), (tx + tile_size, ty + tile_size//2 - bridge_size//2,bridge_size, bridge_size))

                        # vertical bridge
                        if row_idx + 1 < len(tilemap) and tilemap[row_idx + 1][col_idx] in main_globals['walkable_tiles']:
                            pygame.draw.rect(mask, (0, 255, 0), (tx + tile_size//2 - bridge_size//2, ty + tile_size, bridge_size, bridge_size))

        main_globals['spawn_weapons'](main_globals)
        if counter == 0:
            # cba to make a seperate mask so calls itself with a counter for looping
            main_globals['locked_mask'] = main_globals['make_initial_walkable_surface'](tilemap, main_globals, False, counter + 1)
            print(f"previous active tiles: {main_globals['active_tiles']}")
            thread_reg = main_globals['tt_thread'](main_globals, mask)
            thread_lock = main_globals['tt_thread'](main_globals, main_globals['locked_mask'], 'locked_textured_tiles')
        main_globals['active_tiles'] = []
        return mask

    def rebuild_walkable_mask(main_globals): # rebuilds the mask if something changed

        print("rebuilding walkable mask")
        tilemap = main_globals['tilemap']
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        mask_width = len(tilemap[0]) * ts
        mask_height = len(tilemap) * ts

        new_mask = pygame.Surface((mask_width, mask_height))
        new_mask.fill((0, 0, 0)) # clear mask

        main_globals['walkable_mask'] = new_mask

        # remake the mask
        main_globals['walkable_mask'] = main_globals['make_initial_walkable_surface'](tilemap, main_globals)

    def is_on_active_tile(main_globals, x, y): # is something on a tile the player walked on?
        ts = main_globals['tile_size'] + main_globals['tile_offset']
        tile_x = (x + main_globals['player_size'] // 2) // ts
        tile_y = (y + main_globals['player_size'] // 2) // ts
        tile = (tile_x, tile_y)

        return tile in main_globals['active_tiles']

    # define functions and classes into main globals
    for name, obj in locals().items():
        if isinstance(obj, (types.FunctionType, type)):
            main_globals[name] = obj

    print("dungeon, ", end = "")