# this file is for loading the dungeon
import pygame, random, math
from pygame import mixer as mx

def dungeon(main_globals):

    def draw_dungeon(main_globals, player, is_paused, facing_left):
        screen = main_globals['screen']
        camera_x = main_globals['camera_x']
        camera_y = main_globals['camera_y']
        camera_speed = main_globals['camera_speed']
        current_frame = main_globals['current_frame']
        frame_timer = main_globals['frame_timer']
        frame_delay = main_globals['frame_delay']
        frames = main_globals['frames']
        player_size = main_globals['player_size']
        enemy_size = main_globals['enemy_size']
        enemy_list = main_globals['enemy_list']
        screen.fill((0, 0, 0))

        target_x, target_y = main_globals['get_camera_offset'](main_globals, player, main_globals['tile_size'])
        camera_x += (target_x - camera_x) * camera_speed
        camera_y += (target_y - camera_y) * camera_speed
        main_globals['camera_x'] = camera_x
        main_globals['camera_y'] = camera_y
        ts = main_globals['tile_size'] + main_globals['tile_offset']

        mask_width, mask_height = main_globals['walkable_mask'].get_size()
        tile_surface = main_globals['tile_images']
        tilemap = main_globals['tilemap']
        for y in range(0, mask_height, ts):
            for x in range(0, mask_width, ts):
                if main_globals['walkable_mask'].get_at((x, y))[:3] == (0, 255, 0):
                    screen.blit(tile_surface, (x - camera_x, y - camera_y))
        
        if 'enemy_groups' not in main_globals:
            main_globals['enemy_groups'] = []

        # tile checking systems
        for row_idx, row in enumerate(main_globals['tilemap']):
            for col_idx, tile_type in enumerate(row):

                if tile_type == 99: # makes player spawn here, its a spawn tile obviously
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

                elif tile_type == 2: # weapon tile
                    # fixed position because why would it not be
                    # it shouldnt have been fixed
                    # i dont think its even centered
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
                        # actually i will question it, stop calling random every damn frame
                        upper = random.randrange(2, 10)
                        previous_coords = []
                        min_distance = 100
                        hemorrhoids_in_tile = []
                        for i in range(1, upper): # adds x through y
                            attempts = 0
                            max_attempts = 500 # give him some tries
                            while attempts < max_attempts:    
                                deviation = random.randrange(50, 200)
                                enemy_x = tile_center_x - enemy_size // 2 + random.choice((deviation, -deviation))
                                enemy_y = tile_center_y - enemy_size // 2 + random.choice((deviation, -deviation))

                                # check from the previous cocks # the previous WHAT
                                # on_walkable = rect_touches_color(main_globals['walkable_mask'], temporary_rect, (0, 255, 0))
                                too_close = False
                                for (px, py) in previous_coords:
                                    if math.isclose(enemy_x, px, abs_tol=min_distance) and math.isclose(enemy_y, py, abs_tol=min_distance):
                                        too_close = True
                                        break # too close to another guy

                                if not too_close:
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

                elif tile_type == 88: # shop tile
                    main_globals['shop'].stand_x = col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['shop_holder'].get_width() // 2
                    main_globals['shop'].stand_y = row_idx * ts - camera_y + main_globals['tile_size'] // 2 - main_globals['shop_holder'].get_height() // 2 + 50
                    screen.blit(main_globals['shop_holder'], (main_globals['shop'].stand_x, main_globals['shop'].stand_y))

                    # interact with shop
                    if main_globals['distance_to'](player, (main_globals['shop'].stand_x, main_globals['shop'].stand_y)) < main_globals['interact_distance']:
                        screen.blit(main_globals['interact_image'], (main_globals['shop'].stand_x, main_globals['shop'].stand_y + 50))
                        if main_globals['pressed_e']:
                            main_globals['game_stage'] = "shopping"

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
                            main_globals['remake_floor']()


        # drawing things on tiles

        # draw weapons
        for weapon in main_globals['weapons_on_map'][:]:
            weapon_image = main_globals['weapon_images'][weapon.name]
            draw_x = weapon.x - weapon_image.get_width() // 2 - camera_x + 15
            draw_y = weapon.y - weapon_image.get_height() // 2 - camera_y
            weapon.draw(screen, draw_x, draw_y)

            # interact image for said weapon
            if main_globals['distance_to'](player, weapon) < main_globals['interact_distance']:
                screen.blit(main_globals['interact_image'], (draw_x, draw_y + weapon_image.get_height()))

                # pick up weapon
                main_globals['interact'](main_globals, player, weapon.x, weapon.y, lambda w=weapon: w.pickup(player))

        # enemy groups
        for group in main_globals['enemy_groups']:

            # check if ANY enemy in the group detects the player
            group_should_activate = False
            for enemy in group['enemies']:
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

        # check if all enemies in a group are dead, and unlock player if so
        for group in main_globals['enemy_groups']:
            # if every enemy in this group is dead
            if all(not enemy.alive for enemy in group['enemies']):
                if group['active']:
                    group['active'] = False
                    print(f"group at {group['tile_pos']} cleared, ", end="")
                    player.locked = False  # unlock player once group is cleared

        # draw bob
        for enemy in enemy_list:
            enemy.draw(enemy.type)

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
            weapon_y = draw_y + player_size // 2 + 36  # y offset

            if facing_left: # offset because of player offset
                weapon_image = pygame.transform.flip(weapon_image, True, False)
                weapon_x -= 90

            screen.blit(weapon_image, (weapon_x, weapon_y))

        # draw blood particles
        # this is here because we need to draw them over the player
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
        if not is_paused:

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

            for item in main_globals['money_texts']:
                screen.blit(item['text'], (130, 300))
                item['timer'] -= main_globals['dt']
                if item['timer'] <= 0 or player.locked == False:
                    main_globals['money_texts'].remove(item)
                    player.effect("money", item['amount'])
                    print(f"player got {item['amount']} moneys, ", end="")

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

        else: # if paused
            main_globals['draw_pause_menu'](main_globals)

    main_globals['draw_dungeon'] = draw_dungeon

    print("dungeon, ", end = "")