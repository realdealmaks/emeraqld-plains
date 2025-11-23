# user interface
try:
    import pygame, time, types
    from pygame import mixer as mx
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")

def ui(main_globals):
    font = pygame.font.Font("assets/font/editundo.ttf", 24)
    bigfont = pygame.font.Font("assets/font/editundo.ttf", 48)
    setting_font = credits_font = pygame.font.Font("assets/font/editundo.ttf", 28)
    smallfont = pygame.font.Font("assets/font/editundo.ttf", 22)
    smallerfont = pygame.font.Font("assets/font/editundo.ttf", 16)

    def draw_hud(main_globals, player): # top left images for symboling his health
        if player.alive: # IS HE????????
            shake_x, shake_y = player.shake() # reuse player shake for the hud
            screen = main_globals['screen']
            pygame.draw.circle(screen, (20, 20, 20), (100, 100), 80) # i think we should remove the text
            screen.blit(bigfont.render(str(player.health), True, (255, 255, 255)), (120, 200))
            screen.blit(bigfont.render(str(player.wealth), True, (255, 215, 0)), (120, 250)) # just realised man good job!!!!! wealth health
            if main_globals['blood_text'] == "True":
                if player.health > 66: # jebo vam siks seven 🤖
                    screen.blit(main_globals['player_health_images'][0], (-50 + shake_x, -50 + shake_y))
                elif player.health > 33:
                    screen.blit(main_globals['player_health_images'][1], (-50 + shake_x, -50 + shake_y))
                else:
                    screen.blit(main_globals['player_health_images'][2], (-50 + shake_x, -50 + shake_y))
            else:
                screen.blit(main_globals['player_health_images'][0], (-50 + shake_x, -50 + shake_y))

    def draw_minimap(main_globals, tilemap, player):
        screen = main_globals['screen']

        background_rect_surf = pygame.Surface((75, 75), pygame.SRCALPHA)
        background_rect_surf.fill((50, 50, 50, 128)) # color and alpha

        tl_size = 10
        tl_spacing = 2 # spacing between tiles
        padding = 18 # offset from top right corner

        rows = len(tilemap)
        cols = len(tilemap[0])

        # player tile
        player_tile_x = (player.x + main_globals['player_size'] // 2) // (main_globals['tile_size'] + main_globals['tile_offset'])
        player_tile_y = (player.y + main_globals['player_size'] // 2) // (main_globals['tile_size'] + main_globals['tile_offset'])

        # view around player
        view_radius = 2
        start_x = max(player_tile_x - view_radius, 0)
        start_y = max(player_tile_y - view_radius, 0)
        end_x = min(player_tile_x + view_radius, cols - 1)
        end_y = min(player_tile_y + view_radius, rows - 1)

        offset_x = screen.get_width() - background_rect_surf.get_width() - padding
        offset_y = padding

        center_x = offset_x + background_rect_surf.get_width() // 2
        center_y = offset_y + background_rect_surf.get_height() // 2

        screen.blit(background_rect_surf, (offset_x, offset_y))

        # draw tiles
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                if tilemap[y][x] in main_globals['walkable_tiles']:
                    tile_color = (90, 90, 90) # default
                    if (x, y) == (player_tile_x, player_tile_y): # for tile with player
                        tile_color = (140, 140, 240)
                    elif (x, y) in main_globals['active_tiles']: # for explored tiles
                        tile_color = (170, 170, 170)

                    rel_x = (x - player_tile_x) * (tl_size + tl_spacing)
                    rel_y = (y - player_tile_y) * (tl_size + tl_spacing)

                    rect = pygame.Rect(
                        center_x + rel_x - tl_size // 2,
                        center_y + rel_y - tl_size // 2,
                        tl_size,
                        tl_size
                    )
                    pygame.draw.rect(screen, tile_color, rect)

    def pause_menu(main_globals):
        mx.music.pause()
        screen = main_globals['screen']
        tabs = main_globals['tabs']
        background = main_globals['pause_tabs_images']['background']

        current_tab = main_globals.get('current_tab', 'weapon')
        main_globals['current_tab'] = current_tab

        screen.blit(background, (screen.get_width() // 2 - background.get_width() // 2, screen.get_height() // 2 - background.get_height() // 2))

        paused_surf = main_globals['font'].render("paused", True, (255, 255, 255))
        paused_rect = paused_surf.get_rect()
        paused_rect.center = (main_globals['screen'].get_width() // 2, main_globals['screen'].get_height() // 4 - 45)
        screen.blit(paused_surf, paused_rect.topleft)

        text = current_tab.replace("_", " ")
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect()
        text_rect.center = (main_globals['screen'].get_width() // 2, main_globals['screen'].get_height() - 130)
        screen.blit(text_surf, text_rect.topleft)

        main_globals['draw_pause_buttons'](main_globals)
        main_globals['draw_pause_stats'](main_globals)
        if current_tab in tabs:
            func_name = tabs[current_tab]
            main_globals[func_name](main_globals)

    def draw_hints(main_globals): # not really hints, just like keybinds but with a timer
        if main_globals['hints_text'] == "False":
            return
        dt = main_globals['dt']
        screen = main_globals['screen']
        alpha = main_globals['hint_alpha']
        main_globals['hint_alpha'] = alpha
        block_size = main_globals['key_w_hint'].get_width()

        if main_globals['idle_time'] >= main_globals['idle_threshold'] or main_globals['is_paused']: # if player is idle for long enough
            alpha = main_globals.get('hint_alpha', 0)
            alpha += dt * 255 / main_globals['hint_fade_duration']
            if alpha > 255:
                alpha = 255

            # really shoulda made a for loop for ts
            # i did
            main_globals['hint_alpha'] = alpha
            hints = {
                'key_w_hint': (10 + block_size, main_globals['screen'].get_height() - block_size*2 - 10),
                'key_a_hint': (10, main_globals['screen'].get_height() - block_size - 10),
                'key_s_hint': (10 + block_size, main_globals['screen'].get_height() - block_size - 10),
                'key_d_hint': (10 + block_size*2, main_globals['screen'].get_height() - block_size - 10),
                'key_e_hint': (10 + block_size*2, main_globals['screen'].get_height() - block_size*2 - 10),
            }

            for key, pos in hints.items():
                main_globals[key].set_alpha(alpha)
                screen.blit(main_globals[key], pos)

            # swap mouse image
            ticks = pygame.time.get_ticks() # ms
            if (ticks // 1000) % 2 == 0: # s
                main_globals['mouse_blank_hint'].set_alpha(alpha)
                screen.blit(main_globals['mouse_blank_hint'], (main_globals['screen'].get_width() - main_globals['mouse_blank_hint'].get_width() - 10, main_globals['screen'].get_height() - main_globals['mouse_blank_hint'].get_height() - 10))
            else:
                main_globals['mouse_left_hint'].set_alpha(alpha)
                screen.blit(main_globals['mouse_left_hint'], (main_globals['screen'].get_width() - main_globals['mouse_left_hint'].get_width() - 10, main_globals['screen'].get_height() - main_globals['mouse_left_hint'].get_height() - 10))
        else:
            main_globals['hint_alpha'] = 0

    def draw_inventory(main_globals):
        screen = main_globals['screen']
        inventory = main_globals['player'].inventory
        panel_image = main_globals['pause_tabs_images']['inventory']
        items_data = main_globals['items'] # data for items

        mouse_pos = main_globals['mouse_pos']

        # position of the panel
        panel_x = screen.get_width() // 2 - panel_image.get_width() // 2
        panel_y = screen.get_height() // 2 - panel_image.get_height() // 2
        screen.blit(panel_image, (panel_x, panel_y))

        # offsets inside panel
        offset_top = 20
        offset_bottom = 20
        offset_left = 20
        offset_right = 20

        # available space
        inner_width = panel_image.get_width() - offset_left - offset_right
        inner_height = panel_image.get_height() - offset_top - offset_bottom

        # item layout
        item_size = 50
        spacing_x = item_size + 10
        spacing_y = item_size + 10
        items_per_row = max(1, inner_width // spacing_x)

        # boxes
        item_rects = {}
        for idx, (name, count) in enumerate(inventory.items()):
            if name not in items_data:
                continue # skip if unknown

            row = idx // items_per_row
            col = idx % items_per_row

            # center position for this item
            x = panel_x + offset_left + col * spacing_x + item_size // 2
            y = panel_y + offset_top + row * spacing_y + item_size // 2

            border_rect = pygame.Rect(0, 0, item_size, item_size)
            border_rect.center = (x, y)
            pygame.draw.rect(screen, (50, 50, 50), border_rect, 2)

            img = items_data[name]['image']
            img_rect = img.get_rect(center=border_rect.center)
            screen.blit(img, img_rect)

            # hover overlay
            if border_rect.collidepoint(mouse_pos):
                overlay = pygame.Surface((border_rect.width, border_rect.height), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 60))
                screen.blit(overlay, border_rect.topleft)
            if main_globals['selected_item'] == name:
                overlay = pygame.Surface((border_rect.width, border_rect.height), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 130))
                screen.blit(overlay, border_rect.topleft)

            count_text = smallerfont.render(str(count), True, (255, 255, 255))
            count_pos = (border_rect.right - count_text.get_width() - 3, border_rect.bottom - count_text.get_height() - 3)
            screen.blit(count_text, count_pos)

            item_rects[name] = border_rect

        main_globals['inventory_items_rects'] = item_rects

        # description box

        # offsets
        offset_top = 300
        offset_bottom = 20
        offset_left = 20
        offset_right = 20

        # available space
        inner_width = panel_image.get_width() - offset_left - offset_right
        inner_height = panel_image.get_height() - offset_top - offset_bottom

        # description text
        if main_globals['selected_item'] is not None:
            item_name = main_globals['selected_item']
            if item_name in items_data and item_name in main_globals['player'].inventory:
                description = items_data[item_name]['description']
                desc_lines = description.split('\n')

                desc_x = panel_x + offset_left
                desc_y = panel_y + offset_top

                for line in desc_lines:
                    desc_text = smallerfont.render(line, True, (255, 255, 255))
                    screen.blit(desc_text, (desc_x, desc_y))
                    desc_y += desc_text.get_height() + 5

                if main_globals['items'][item_name]['function'] is not None:
                    use_text = smallerfont.render("use", True, (255, 255, 255))
                    use_rect = use_text.get_rect()
                    use_rect.topright = (panel_x + panel_image.get_width() - offset_right, desc_y + 10)
                    screen.blit(use_text, use_rect.topleft)
                    border_rect = use_rect.inflate(10, 10)
                    pygame.draw.rect(screen, (200, 200, 200), border_rect, 2)
                    if border_rect.collidepoint(mouse_pos):
                        overlay = pygame.Surface((border_rect.width, border_rect.height), pygame.SRCALPHA)
                        overlay.fill((255, 255, 255, 60))
                        screen.blit(overlay, border_rect.topleft)

                    if main_globals['mouse_pressed'] and border_rect.collidepoint(mouse_pos) and not main_globals['mouse_clicked']:
                        main_globals['items'][item_name]['function'](main_globals)
                        if main_globals['player'].inventory[item_name] > 1:
                            main_globals['player'].inventory[item_name] -= 1
                        else:
                            del main_globals['player'].inventory[item_name]
                        main_globals['mouse_clicked'] = True

        if not main_globals['mouse_pressed']: # it spammed :(
            main_globals['mouse_clicked'] = False

    def draw_pause_buttons(main_globals):
        screen = main_globals['screen']
        screen_w, screen_h = screen.get_size()

        image = main_globals['pause_tabs_images']['buttons']
        image_x = screen.get_width() // 2 + main_globals['pause_tabs_images']['background'].get_width() // 2 - image.get_width()
        image_y = screen_h // 2 - image.get_height() // 2
        screen.blit(image, (image_x, image_y))

        buttons_dict = main_globals['pause_buttons']
        mouse_pos = pygame.mouse.get_pos()

        num_buttons = len(buttons_dict)

        # scale to fit
        button_width = int(image.get_width() * 0.8) # 80% of background
        button_height = int(image.get_height() / (num_buttons + 1) * 0.8) # fit vert

        spacing = image.get_height() / (num_buttons + 1)
        center_x = image_x + image.get_width() // 2 # hor center

        for i, (name, rect) in enumerate(buttons_dict.items(), start=1):
            # resize
            rect.width = button_width
            rect.height = button_height

            # position
            rect.center = (center_x, image_y + i * spacing)
            buttons_dict[name] = rect

            # hover
            color = (110, 110, 110) if rect.collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.line(screen, color, (rect.right, rect.top), (rect.right, rect.bottom), 3)

            name = name.replace("_", " ")
            text_surf = smallfont.render(name, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

            if name == main_globals['current_tab']:
                indicator_surf = smallfont.render(">", True, (255, 255, 255))
                indicator_rect = indicator_surf.get_rect(midleft=(rect.left - 4, rect.centery))
                screen.blit(indicator_surf, indicator_rect)

    def draw_pause_stats(main_globals):
        screen = main_globals['screen']
        image = main_globals['pause_tabs_images']['player_stats']
        bg = main_globals['pause_tabs_images']['background']
        image_x = screen.get_width() // 2 - bg.get_width() // 2 + 4
        image_y = screen.get_height() // 2 - image.get_height() // 2

        screen.blit(image, (image_x, image_y))

        # position
        start_y_offset = 40 # y offset for the first stat
        inner_padding_x = 15
        spacing = 20 # space between label and value
        line_spacing = 45 # space between stats

        base_x = image_x + inner_padding_x
        base_y = image_y + start_y_offset

        stats = {
            "Health": main_globals['player'].health,
            "Wealth": main_globals['player'].wealth,
            "Enemies killed": main_globals['enemies_killed'],
            "Floor": main_globals['current_floor']
        }

        y = base_y
        for label, value in stats.items():
            label_surf = smallerfont.render(f"{label}:", True, (255, 255, 255))
            value_surf = smallerfont.render(str(value), True, (255, 255, 255))

            screen.blit(label_surf, (base_x, y))
            screen.blit(value_surf, (base_x, y + spacing))

            y += line_spacing

    def weapon_info(main_globals):
        screen = main_globals['screen']
        weapons = main_globals['player'].weapons
        screen_w = main_globals['screen'].get_width()
        screen_h = main_globals['screen'].get_height()
        image_x = screen_w // 2 - main_globals['weapon_frame'].get_width() // 2 + 0
        image_y = screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 0
        screen.blit(main_globals['weapon_frame'], (screen_w // 2 - main_globals['weapon_frame'].get_width() // 2, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2))

        if not weapons or weapons[0] is None:
            # draw some hands or something
            return

        weapon = main_globals['player'].weapons[0]
        weapon_image = main_globals['weapon_images'][weapon.name]
        screen.blit(main_globals['weapon_light'], (screen_w // 2 - main_globals['weapon_frame'].get_width() // 2 + 35, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 30))
        screen.blit(weapon_image, (screen_w // 2 - main_globals['weapon_frame'].get_width() // 2 + 35, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 30))

        # stats
        text = smallfont.render(weapon.name, True, (255, 255, 255))
        screen.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 20))

        text = smallfont.render(str(weapon.damage), True, (255, 255, 255))
        screen.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 50))

        text = smallfont.render(str(weapon.range), True, (255, 255, 255))
        screen.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 80))

        text = smallfont.render(str(weapon.cooldown), True, (255, 255, 255))
        screen.blit(text, (screen_w // 2 - text.get_width() // 2, screen_h // 2 - main_globals['weapon_frame'].get_height() // 2 + 110))

    def new_mutation(main_globals, effect, number): # remake this shit
        screen = main_globals['screen']
        mutation_alpha = 0
        while mutation_alpha < 255:
            mutation_alpha += 20
            if mutation_alpha > 255:
                mutation_alpha = 255
            screen.fill((0, 0, 0))
            main_globals['mutation_image'].set_alpha(mutation_alpha)
            screen.blit(main_globals['mutation_image'], (0, 0))
            time.sleep(0.01)
            pygame.display.flip()
        main_globals['player'].effect(effect, number)
        time.sleep(1)
        while mutation_alpha > 0:
            mutation_alpha -= 25
            if mutation_alpha < 0:
                mutation_alpha = 0
            screen.fill((0, 0, 0))
            main_globals['mutation_image'].set_alpha(mutation_alpha)
            screen.blit(main_globals['mutation_image'], (0, 0))
            time.sleep(0.01)
            pygame.display.flip()
        main_globals['mutation_image'].set_alpha(255)

    def draw_vignette(main_globals, player): # if you dont know what 'vignette' means go away!
        if main_globals['blood_text'] == "False":
            return
        if player.alive: # you filthy hog
            max_alpha = 180
            try:
                if main_globals['vignette'].get_alpha() != max_alpha * (1 - player.health / 100):
                    vignette_alpha = max_alpha * (1 - player.health / 100)
                    main_globals['vignette'].set_alpha(vignette_alpha)
            except UnboundLocalError: # if it dont exists yet
                vignette_alpha = max_alpha
            main_globals['screen'].blit(main_globals['vignette'], (0, 0))

    def draw_menu(main_globals, mouse_pos): # main menu
        screen = main_globals['screen']
        screen.fill((0, 0, 0))

        if main_globals['menu_bg_can_animate']: # roll in on first launch
            target_x = main_globals['screen'].get_width() - main_globals['menu_background'].get_width()
            if main_globals['menu_bg_x'] > target_x:
                main_globals['menu_bg_x'] -= 10
            else:
                main_globals['menu_bg_x'] = target_x
                main_globals['menu_bg_can_animate'] = False
                main_globals['flash_active'] = True

        screen.blit(main_globals['menu_background'], (main_globals['menu_bg_x'], 0))

        # flash at the first launch
        if main_globals['flash_active'] and main_globals['flash_alpha'] < 255:
            main_globals['flash_alpha'] += main_globals['flash_speed']
            if main_globals['flash_alpha'] > 255:
                main_globals['flash_alpha'] = 255
            flash_surface = pygame.Surface((main_globals['screen'].get_width(), main_globals['screen'].get_height()))
            flash_surface.fill((255, 255, 255))
            flash_surface.set_alpha(255 - main_globals['flash_alpha'])
            screen.blit(flash_surface, (0, 0))
        else:
            main_globals['flash_active'] = False

        # if i finished showing off my skills ( animation )
        if main_globals['menu_bg_can_animate']== False and main_globals['flash_active'] == False:

            # title
            title_text = main_globals['font'].render("Title", True, (255, 255, 255))
            title_rect = title_text.get_rect(topleft=(10, 5)) # for some reason top looks way bigger even if its same number
            screen.blit(title_text, title_rect)

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

            # kredits batten :robot:
            credits_color = (70, 70, 70) if main_globals['credits_button'].collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.rect(screen, credits_color, main_globals['credits_button'])
            text_surf = main_globals['font'].render("Credits", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=main_globals['credits_button'].center)
            screen.blit(text_surf, text_rect.topleft)

            # battle pass button :kekw:
            bp_color = (70, 70, 70) if main_globals['bp_button'].collidepoint(mouse_pos) else (40, 40, 40)
            pygame.draw.rect(screen, bp_color, main_globals['bp_button'])
            text_surf = font.render("Battle Pass", True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=main_globals['bp_button'].center)
            screen.blit(text_surf, text_rect.topleft)
            # uncomment if you dare
            # i dared and its staying this way ;)

    def draw_credits(main_globals, mouse_pos): # cursed with 1% total fps
        screen = main_globals['screen']
        to_menu = main_globals['to_menu']
        font = main_globals['font']
        screen.fill((0, 0, 0))

        screen.blit(font.render("credits", True, (255, 255, 255)), (20, 20))
        # screen.blit(main_globals['thx'], (540, 0)) # i got the coordinates right first try btw
        # show off

        # no problem man
        screen.blit(main_globals['thx'], (main_globals['screen'].get_width() // 2, 0))

        # return
        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        img_rect = main_globals['return_image'].get_rect(center=main_globals['to_menu'].center)
        screen.blit(main_globals['return_image'], img_rect.topleft)

        # credits text
        screen.blit(credits_font.render("shmuby ones", True, (255, 255, 255)), (50, 100))
        screen.blit(credits_font.render("made some code and pixel art", True, (255, 255, 255)), (50, 150))

        screen.blit(credits_font.render("deal bedal maks", True, (255, 255, 255)), (50, 250))
        screen.blit(credits_font.render("some more code and the sfx", True, (255, 255, 255)), (50, 300))

        screen.blit(credits_font.render("SPECIAL THANKS!!!:", True, (255, 255, 255)), (50, 400))

        screen.blit(credits_font.render("you", True, (255, 255, 255)), (50, 500))
        screen.blit(credits_font.render("for playing, my boy", True, (255, 255, 255)), (50, 550))

        # liners (credits edition)
        liner_y = 85
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 100
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 100
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        liner_y += 50
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)
        liner_y += 100
        liner = pygame.Rect(50, liner_y, main_globals['screen'].get_width() / 2 - 100, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

    def draw_settings(main_globals, mouse_pos):
        screen = main_globals['screen']
        music_slider = main_globals['music_slider']
        to_menu = main_globals['to_menu']
        font = main_globals['font']
        screen.fill((0, 0, 0))

        # title
        screen.blit(font.render("settings", True, (255, 255, 255)), (20, 20))

        # line
        liner_y = 85
        liner = pygame.Rect(100, liner_y, main_globals['screen'].get_width() - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        # music volume
        pygame.draw.rect(screen, (120, 120, 120), music_slider)
        volume = main_globals.get('volume_preview', main_globals.get('music_volume', mx.music.get_volume()))
        filled_width = int(music_slider.width * volume)
        filled_rect = pygame.Rect(music_slider.x, music_slider.y, filled_width, music_slider.height)
        pygame.draw.rect(screen, (180, 180, 180), filled_rect)

        if main_globals['dragging_music_slider']:
            relative_x = mouse_pos[0] - music_slider.x
            volume = max(0.0, min(1.0, relative_x / music_slider.width))
            main_globals['volume_preview'] = volume

        if 'volume_preview' in main_globals and main_globals['volume_preview'] != main_globals.get('music_volume', mx.music.get_volume()):
            main_globals['draw_apply_button'](main_globals, main_globals['screen'].get_width() // 2 - 120, 90, "music")

        screen.blit(setting_font.render("music volume", True, (255, 255, 255)), (100, 100))
        screen.blit(setting_font.render(f"{int(volume * 100)}%", True, (255, 255, 255)), (main_globals['screen'].get_width() // 2 + 20, 100))

        # line
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen'].get_width() - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        # hints
        screen.blit(setting_font.render("hints", True, (255, 255, 255)), (100, 150))
        hints_color = (70, 70, 70) if main_globals['hints_button'].collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, hints_color, main_globals['hints_button'])
        text_surf = setting_font.render(main_globals['hints_text'], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=main_globals['hints_button'].center)
        screen.blit(text_surf, text_rect.topleft)

        # line
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen'].get_width() - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        # resolution
        resolution_index = main_globals['resolution_index']
        step = main_globals['resolution_slider_base'].width / (len(main_globals['resolutions']) - 1)

        if main_globals['dragging_resolution_slider']:
            relative_x = mouse_pos[0] - main_globals['resolution_slider_base'].x
            resolution_index = round(relative_x / step)
            resolution_index = max(0, min(resolution_index, len(main_globals['resolutions']) - 1))
            main_globals['resolution_index'] = resolution_index

        handle_width = 15
        handle_height = main_globals['resolution_slider_base'].height + 15
        handle_x = main_globals['resolution_slider_base'].x + resolution_index * step - handle_width // 2
        handle_y = main_globals['resolution_slider_base'].y - 7
        handle_rect = pygame.Rect(handle_x, handle_y, handle_width, handle_height)

        screen.blit(setting_font.render("resolution", True, (255, 255, 255)), (100, 200))
        resolution_color = (120, 120, 120) if handle_rect.collidepoint(mouse_pos) else (70, 70, 70)
        pygame.draw.rect(screen, (40, 40, 40), main_globals['resolution_slider_base'])
        res = main_globals['resolutions'][resolution_index]
        res_text = f"{res[0]}x{res[1]}"
        screen.blit(setting_font.render(res_text, True, (255, 255, 255)), (main_globals['screen'].get_width() // 2 + 20, 200))
        pygame.draw.rect(screen, resolution_color, handle_rect)
        main_globals['resolution_slider'] = handle_rect
        if main_globals['resolution'] != res:
            main_globals['draw_apply_button'](main_globals, main_globals['screen'].get_width() // 2 - 120, 190, "resolution")

        # line
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen'].get_width() - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        # framerate cap slider
        frame_cap_index = main_globals['frame_cap_index']
        step = main_globals['frame_slider_base'].width / (len(main_globals['frame_caps'])-1)

        if main_globals['dragging_frame_slider']:
            relative_x = mouse_pos[0] - main_globals['frame_slider_base'].x
            frame_cap_index = round(relative_x / step)
            frame_cap_index = max(0, min(frame_cap_index, len(main_globals['frame_caps'])-1))
            main_globals['frame_cap_index'] = frame_cap_index

        handle_width = 15
        handle_height = main_globals['frame_slider_base'].height + 15
        handle_x = main_globals['frame_slider_base'].x + frame_cap_index * step - handle_width // 2
        handle_y = main_globals['frame_slider_base'].y - 7
        handle_rect = pygame.Rect(handle_x, handle_y, handle_width, handle_height)

        screen.blit(setting_font.render("framerate cap", True, (255, 255, 255)), (100, 250))
        framerate_color = (120, 120, 120) if handle_rect.collidepoint(mouse_pos) else (70, 70, 70)
        pygame.draw.rect(screen, (40, 40, 40), main_globals['frame_slider_base'])
        frame = main_globals['frame_caps'][frame_cap_index]
        frame_text = f"{frame} fps"
        screen.blit(setting_font.render(frame_text, True, (255, 255, 255)), (main_globals['screen'].get_width() // 2 + 20, 250))
        pygame.draw.rect(screen, framerate_color, handle_rect)
        main_globals['frame_slider'] = handle_rect
        if frame != main_globals['max_fps']:
            main_globals['draw_apply_button'](main_globals, main_globals['screen'].get_width() // 2 - 120, 242, "framerate")

        # line
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen'].get_width() - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        # blood toggle
        screen.blit(setting_font.render("blood", True, (255, 255, 255)), (100, 300))
        blood_color = (70, 70, 70) if main_globals['blood_button'].collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, blood_color, main_globals['blood_button'])
        text_surf = setting_font.render(main_globals['blood_text'], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=main_globals['blood_button'].center)
        screen.blit(text_surf, text_rect.topleft)

        # line
        liner_y += 50
        liner = pygame.Rect(100, liner_y, main_globals['screen'].get_width() - 150, 2)
        pygame.draw.rect(screen, (40, 40, 40), liner)

        # return button
        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        img_rect = main_globals['return_image'].get_rect(center=main_globals['to_menu'].center)
        screen.blit(main_globals['return_image'], img_rect.topleft)

    def draw_dead(main_globals, mouse_pos):
        screen = main_globals['screen']
        font = main_globals['font']
        to_menu = main_globals['to_menu']
        screen.fill((0, 0, 0))

        screen.blit(font.render("ded", True, (255, 255, 255)), (20, 20))
        main_globals['musicswitcher'](main_globals, 1)

        # return
        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        img_rect = main_globals['return_image'].get_rect(center=main_globals['to_menu'].center)
        screen.blit(main_globals['return_image'], img_rect.topleft)

    def draw_battle_pass(main_globals, mouse_pos):
        screen = main_globals['screen']
        font = main_globals['font']
        buy_button = main_globals['buy_button']
        to_menu = main_globals['to_menu']
        buy_button_color = (70, 70, 70) if buy_button.collidepoint(mouse_pos) else (40, 40, 40)
        text_surf = font.render("14.99$", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=main_globals['buy_button'].center)

        screen.fill((0, 0, 0))
        screen.blit(main_globals['battlepass_image'], (0, 0))
        pygame.draw.rect(screen, buy_button_color, buy_button)
        screen.blit(text_surf, text_rect.topleft)
        
        # return
        to_menu_color = (70, 70, 70) if to_menu.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, to_menu_color, to_menu)
        img_rect = main_globals['return_image'].get_rect(center=main_globals['to_menu'].center)
        screen.blit(main_globals['return_image'], img_rect.topleft)

    # define functions and classes into main globals
    for name, obj in locals().items():
        if isinstance(obj, (types.FunctionType, type)):
            main_globals[name] = obj

    print("ui, ", end="")