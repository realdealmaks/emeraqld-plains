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

        for row_idx, row in enumerate(main_globals['tilemap']):
            for col_idx, tile_type in enumerate(row):

                if tile_type == 99: # makes player spawn here 
                    if main_globals['spawn_set'] == False:
                        ts = main_globals['tile_size'] + main_globals['tile_offset']
                        main_globals['spawn_x'] = col_idx * ts + (main_globals['tile_size'] - player_size) // 2
                        main_globals['spawn_y'] = row_idx * ts + (main_globals['tile_size'] - player_size) // 2
                        if main_globals.get('player') is None:
                            main_globals['player'] = main_globals['Player'](main_globals, main_globals['spawn_x'], main_globals['spawn_y'])
                        else:
                            main_globals['player'].x = main_globals['spawn_x']
                            main_globals['player'].y = main_globals['spawn_y']
                        main_globals['spawn_set'] = True

                elif tile_type == 2:
                    # fixed position because why would it not be
                    screen.blit(main_globals['pedistal_image'], (col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_width() // 2, row_idx * ts - camera_y + main_globals['tile_size'] // 2 - main_globals['pedistal_image'].get_height() // 2 + 50))

                elif tile_type == 3: # okay...
                    ts = main_globals['tile_size'] + main_globals['tile_offset']
                    if main_globals['groups_spawned'] >= sum(i.count(3) for i in tilemap): # not dIh
                        pass
                    else:
                        tile_center_x = col_idx * ts + main_globals['tile_size'] // 2
                        tile_center_y = row_idx * ts + main_globals['tile_size'] // 2
                        # i dont know what this is for and im not going to question it \/
                        '''upper limit :D'''
                        # actually i will question it, stop calling random every damn frame
                        upper = random.randrange(2, 10)
                        previous_coords = []
                        min_distance = 100
                        for i in range(1, upper): # adds x through y
                            attempts = 0
                            max_attempts = 500 # give him some tries
                            while attempts < max_attempts:    
                                deviation = random.randrange(50, 200)
                                enemy_x = tile_center_x - enemy_size // 2 + random.choice((deviation, -deviation))
                                enemy_y = tile_center_y - enemy_size // 2 + random.choice((deviation, -deviation))

                                # check from the previous cocks
                                # on_walkable = rect_touches_color(main_globals['walkable_mask'], temporary_rect, (0, 255, 0))
                                too_close = False
                                for (px, py) in previous_coords:
                                    if math.isclose(enemy_x, px, abs_tol=min_distance) and math.isclose(enemy_y, py, abs_tol=min_distance):
                                        too_close = True
                                        break
                                if not too_close:
                                    new_enemy = main_globals['Enemy'](main_globals, enemy_x, enemy_y, random.choice([0, 1]))
                                    enemy_list.append(new_enemy)
                                    previous_coords.append((enemy_x, enemy_y))
                                    break  # valid position found
                                attempts += 1
                        print(f"spawned enemy group {main_globals['groups_spawned']} on tile with x {row_idx} and y {col_idx}")
                        print(previous_coords)
                        main_globals['groups_spawned'] += 1

                elif tile_type == 88:
                    main_globals['shop'].stand_x = col_idx * ts - camera_x + main_globals['tile_size'] // 2 - main_globals['shop_holder'].get_width() // 2
                    main_globals['shop'].stand_y = row_idx * ts - camera_y + main_globals['tile_size'] // 2 - main_globals['shop_holder'].get_height() // 2 + 50
                    screen.blit(main_globals['shop_holder'], (main_globals['shop'].stand_x, main_globals['shop'].stand_y))

                    # interact with shop
                    if main_globals['distance_to'](player, (main_globals['shop'].stand_x, main_globals['shop'].stand_y)) < main_globals['interact_distance']:
                        screen.blit(main_globals['interact_image'], (main_globals['shop'].stand_x, main_globals['shop'].stand_y + 50))
                    if main_globals['pressed_f'] and main_globals['distance_to'](player, (main_globals['shop'].stand_x, main_globals['shop'].stand_y)) < main_globals['interact_distance']:
                        main_globals['game_stage'] = "shopping"

        # draw weapons
        for weapon in main_globals['weapons_on_map'][:]:
            weapon_image = main_globals['weapon_images'][weapon.name]
            draw_x = weapon.x - weapon_image.get_width() // 2 - camera_x + 15
            draw_y = weapon.y - weapon_image.get_height() // 2 - camera_y
            weapon.draw(screen, draw_x, draw_y)

            # interact image
            if main_globals['distance_to'](player, weapon) < main_globals['interact_distance']:
                screen.blit(main_globals['interact_image'], (draw_x, draw_y + weapon_image.get_height()))

                # pick up weapon
                main_globals['interact'](main_globals, player, weapon.x, weapon.y, lambda w=weapon: w.pickup(player))

        # gets bobbers moving
        # hopefully this fits here
        # it did actually fit here, but i moved it because i wanted to draw slashes over bobbers
        for enemy in enemy_list:
            enemy.move()

        if 'active_slashes' in main_globals and main_globals['active_slashes']:
            active_slashes = main_globals['active_slashes']
            for enemy in enemy_list:
                if not enemy.alive:
                    continue
                for slash in active_slashes:
                    if pygame.Rect.colliderect(enemy.rect, slash['rect']):
                        if enemy not in slash['hit_enemies']:
                            enemy.damaged(20) # or use weapon damage eh?
                            slash['hit_enemies'].add(enemy)

        for enemy in enemy_list:
            enemy.draw(enemy.type)

        if 'active_slashes' in main_globals:
            now = pygame.time.get_ticks() # current time in ms
            still_active = []
            for slash in main_globals['active_slashes']:
                if now < slash['expiry']:
                    screen.blit(slash['image'], slash['rect'])
                    still_active.append(slash)
            main_globals['active_slashes'] = still_active

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

        player_frame = pygame.transform.scale(frames[current_frame], (player_size * 3, player_size * 3))
        if main_globals['facing_left']:
            player_frame = pygame.transform.flip(player_frame, True, False)

        offset_x = (player_size * 3 - player_size) // 2
        offset_y = (player_size * 3 - player_size) // 2
        shake_x, shake_y = player.shake()
        draw_x = player.x - camera_x - offset_x + shake_x
        draw_y = player.y - camera_y - offset_y + shake_y
        if facing_left:
            draw_x += 30
        else:
            draw_x -= 30

        # draw weapon to player
        screen.blit(player_frame, (draw_x, draw_y))
        if len(player.weapons) > 0:
            weapon = player.weapons[0]
            weapon_image = main_globals['weapon_images'][weapon.name]
            scale_fraction = 1.8
            weapon_image = pygame.transform.scale(weapon_image, ((main_globals['player_size'] // 2) * scale_fraction, (main_globals['player_size'] // 2) * scale_fraction))
            weapon_image = pygame.transform.rotate(weapon_image, 65)
            weapon_image = pygame.transform.flip(weapon_image, True, False)

            weapon_x = draw_x + player_size + 40 # x offset
            weapon_y = draw_y + player_size // 2 + 36  # y offset

            if facing_left:
                weapon_image = pygame.transform.flip(weapon_image, True, False)
                weapon_x -= 90

            screen.blit(weapon_image, (weapon_x, weapon_y))

        # draw bloodes
        # this has to be here because player draws before
        new_particles = []
        for body, shape, color, lifetime, max_lifetime in main_globals['blood_particles']:
            # stop at landing y
            if body.position.y > body.landing_y:
                body.position = (body.position.x, body.landing_y)
                body.velocity = (0, 0)

            # fade out
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
                # remove
                main_globals['space'].remove(body, shape)

        main_globals['blood_particles'] = new_particles

        if is_paused == False:
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
        else:
            main_globals['draw_pause_menu'](main_globals)

    main_globals['draw_dungeon'] = draw_dungeon

    print("dungeon file loaded")