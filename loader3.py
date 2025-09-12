# this file is for classes and definitions
# loader 3

import math, random, pygame, pydub, pytweening, scipy, pymunk, pathfinding
from PIL import Image
from pygame import mixer as mx
from pymunk import shapes

def loader3(main_globals):
    # screen = None
    def musicswitcher(main_globals, indexhere):
        if main_globals['currently_playing_index'] != indexhere:
            mx.music.load(main_globals['musics'][indexhere])
            mx.music.play(-1)
            main_globals['currently_playing_index'] = indexhere


    def get_camera_offset(main_globals, player, tile_size):
        center_x = player.x + main_globals['player_size'] // 2
        center_y = player.y + main_globals['player_size'] // 2

        tile_x = int(center_x // tile_size)
        tile_y = int(center_y // tile_size)

        offset_x = tile_x * tile_size - (main_globals['screen_w'] - tile_size) // 2
        offset_y = tile_y * tile_size - (main_globals['screen_h'] - tile_size) // 2

        return offset_x, offset_y

    class Player:
        def __init__(self, main_globals, x, y):
            self.x = x
            self.y = y
            self.speed = 2
            self.health = 100
            self.alive = True
            self.shake_timer = 0
            self.main_globals = main_globals

        def move(self, dx, dy):
            new_x, new_y = self.x, self.y
            if dx != 0:
                new_x = self.x + dx * self.speed
            if dy != 0:
                new_y = self.y + dy * self.speed

            self.x, self.y = new_x, new_y

        def shake(self):
            if self.shake_timer > 0:
                self.shake_timer -= 1
                return random.randint(-5, 5), random.randint(-5, 5)
            return 0, 0

        def damaged(self, amount):
            self.health -= amount
            self.shake_timer = 10
            if self.health <= 0:
                self.die()
            else:
                self.main_globals['hurt_sound'].play()

        def die(self):
            self.main_globals['game_stage'] = "dead"
            print("player died")

        def respawn(self):
            self.health = 100
            self.alive = True
            self.x = main_globals['screen_w'] // 2
            self.y = main_globals['screen_h'] // 2
            mx.music.rewind()

    player = Player(main_globals, 0, 0)


    class Tile:
        def __init__(self, main_globals, x, y):
            self.main_globals = main_globals
            self.size = main_globals['tile_size']
            self.color = (0, 255, 0)
            self.x = x
            self.y = y
            self.tile_offset = 15
            self.old_x = x
            self.old_y = y
            self.layout = [False, False, False]

        def draw_tile(self):
            pygame.draw.rect(self.main_globals['screen'], self.color, (self.x, self.y, self.size, self.size))

        def tile_images(self):
            self.main_globals['screen'].blit(self.main_globals['tile_images'][0], (self.x, self.y))

        def connect_tile(self):
            screen = self.main_globals['screen']
            if self.layout[0]:
                pygame.draw.rect(screen, self.color, (self.old_x + self.tile_offset + self.size, self.old_y, self.size, self.size))
            if self.layout[1]:
                pygame.draw.rect(screen, self.color, (self.old_x, self.old_y + self.tile_offset + self.size, self.size, self.size))
            if self.layout[2]:
                pygame.draw.rect(screen, self.color, (self.old_x - self.tile_offset - self.size, self.old_y, self.size, self.size))

    tile = Tile(main_globals, 0, 0)

    def draw_hud(main_globals, player):
        if player.alive:
            shake_x, shake_y = player.shake()
            screen = main_globals['screen']
            pygame.draw.circle(screen, (20, 20, 20), (100, main_globals['screen_h'] - 100), 80)
            screen.blit(main_globals['font'].render(str(player.health), True, (255, 255, 255)),
                        (120, main_globals['screen_h'] - 220))
            if player.health > 66:
                screen.blit(main_globals['player_health_images'][0], (-50 + shake_x, main_globals['screen_h'] - 260 + shake_y))
            elif player.health > 33:
                screen.blit(main_globals['player_health_images'][1], (-50 + shake_x, main_globals['screen_h'] - 260 + shake_y))
            else:
                screen.blit(main_globals['player_health_images'][2], (-50 + shake_x, main_globals['screen_h'] - 260 + shake_y))

    def draw_vignette(main_globals, player):
        if player.alive:
            max_alpha = 180
            vignette_alpha = max_alpha * (1 - player.health / 100)
            main_globals['vignette'].set_alpha(vignette_alpha)
            main_globals['screen'].blit(main_globals['vignette'], (0, 0))

    def draw_pause_menu(main_globals):
        screen = main_globals['screen']
        pygame.draw.rect(screen, (20, 20, 20), (main_globals['screen_w'] // 2 - main_globals['screen_w'] // 4, main_globals['screen_h'] // 2 - main_globals['screen_h'] // 4, main_globals['screen_w'] // 2, main_globals['screen_h'] // 2), 0)
        screen.blit(main_globals['font'].render("paused", True, (255, 255, 255)), (main_globals['screen_w'] // 2 - 60, main_globals['screen_h'] // 2 - 22))
        mx.music.pause()

    def draw_menu(main_globals, mouse_pos):
        screen = main_globals['screen']
        if main_globals['menu_bg_can_animate']:
            target_x = main_globals['screen_w'] - main_globals['menu_background'].get_width()
            if main_globals['menu_bg_x'] > target_x:
                main_globals['menu_bg_x'] -= 10
            else:
                main_globals['menu_bg_x'] = target_x
                main_globals['menu_bg_can_animate'] = False
                main_globals['flash_active'] = True

        screen.blit(main_globals['menu_background'], (main_globals['menu_bg_x'], 0))

        if main_globals['flash_active'] and main_globals['flash_alpha'] < 255:
            main_globals['flash_alpha'] += main_globals['flash_speed']
            if main_globals['flash_alpha'] > 255:
                main_globals['flash_alpha'] = 255
            flash_surface = pygame.Surface((main_globals['screen_w'], main_globals['screen_h']))
            flash_surface.fill((255, 255, 255))
            flash_surface.set_alpha(255 - main_globals['flash_alpha'])
            screen.blit(flash_surface, (0, 0))
        else:
            main_globals['flash_active'] = False

        if not main_globals['menu_bg_can_animate'] and not main_globals['flash_active']:
            # play button
            play_color = (70, 70, 70) if main_globals['play_button'].collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.rect(screen, play_color, main_globals['play_button'])
            text_surf = main_globals['font'].render("Play", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=main_globals['play_button'].center)
            screen.blit(text_surf, text_rect.topleft)
            # settings button
            settings_color = (70, 70, 70) if main_globals['settings_button'].collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.rect(screen, settings_color, main_globals['settings_button'])
            text_surf = main_globals['font'].render("Settings", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=main_globals['settings_button'].center)
            screen.blit(text_surf, text_rect.topleft)


    def draw_settings(main_globals, mouse_pos):
        screen = main_globals['screen']
        dragging_music_slider = main_globals['dragging_music_slider']
        music_slider = main_globals['music_slider']
        to_menu = main_globals['to_menu']
        font = main_globals['font']

        setting_font = pygame.font.SysFont(None, 34)
        screen.blit(font.render("settings", True, (255, 255, 255)), (20, 20))

        # music slider
        pygame.draw.rect(screen, (120, 120, 120), music_slider)
        volume = mx.music.get_volume()
        filled_width = int(music_slider.width * volume)
        filled_rect = pygame.Rect(music_slider.x, music_slider.y, filled_width, music_slider.height)
        pygame.draw.rect(screen, (180, 180, 180), filled_rect)

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] and dragging_music_slider:
            relative_x = mouse_pos[0] - music_slider.x
            volume = max(0.0, min(1.0, relative_x / music_slider.width))
            mx.music.set_volume(volume)

        screen.blit(setting_font.render("music volume", True, (255, 255, 255)), (100, 100))
        screen.blit(setting_font.render(f"{int(volume * 100)}%", True, (255, 255, 255)), (main_globals['screen_w'] // 2 + 20, 110))

        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        text_surf = font.render("To menu", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=main_globals['to_menu'].center)
        screen.blit(text_surf, text_rect.topleft)


    def draw_dead(main_globals, mouse_pos):
        screen = main_globals['screen']
        font = main_globals['font']
        to_menu = main_globals['to_menu']

        screen.blit(font.render("ded", True, (255, 255, 255)), (20, 20))
        main_globals['musicswitcher'](main_globals, 1)

        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        text_surf = font.render("To menu", True, (255, 255, 255))
        screen.blit(text_surf, to_menu.topleft)

    def draw_dungeon(main_globals, player, moving_up, moving_down, moving_left, moving_right, is_paused, mouse_pos, facing_left):
        screen = main_globals['screen']
        camera_x = main_globals['camera_x']
        camera_y = main_globals['camera_y']
        camera_speed = main_globals['camera_speed']
        current_frame = main_globals['current_frame']
        frame_timer = main_globals['frame_timer']
        frame_delay = main_globals['frame_delay']
        frames = main_globals['frames']
        player_size = main_globals['player_size']

        target_x, target_y = get_camera_offset(main_globals, player, main_globals['tile'].size)
        camera_x += (target_x - camera_x) * camera_speed
        camera_y += (target_y - camera_y) * camera_speed
        main_globals['camera_x'] = camera_x
        main_globals['camera_y'] = camera_y

        # animate player
        frame_timer += 1
        if frame_timer >= frame_delay:
            frame_timer = 0
            current_frame = (current_frame + 1) % len(frames)
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

        screen.blit(player_frame, (draw_x, draw_y))

        if not is_paused:
            draw_vignette(main_globals, player)
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
            draw_hud(main_globals, player)
        else:
            draw_pause_menu(main_globals)


    main_globals['draw_menu'] = draw_menu
    main_globals['draw_dungeon'] = draw_dungeon
    main_globals['draw_hud'] = draw_hud
    main_globals['draw_pause_menu'] = draw_pause_menu
    main_globals['draw_settings'] = draw_settings
    main_globals['draw_dead'] = draw_dead
    main_globals['musicswitcher'] = musicswitcher
    main_globals['get_camera_offset'] = get_camera_offset
    main_globals['draw_vignette'] = draw_vignette
    main_globals['Tile'] = Tile
    main_globals['player'] = player
    main_globals['Player'] = Player
    main_globals['tile'] = tile


    print("loader3 file loaded")