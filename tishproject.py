import math, random, pygame, pydub, pytweening, scipy, pymunk, pathfinding
from PIL import Image
from pygame import mixer as mx
from pymunk import shapes
from time import sleep

developert_tools = True

pygame.init()
screen_h, screen_w = 750, 1080
screen = pygame.display.set_mode((screen_w, screen_h))

# audio and whatnot

mx.init()
musics = ["testdroga.mp3", "game_over_loop.mp3"]
currently_playing_index = 0 # 0 being the first track so it's insta loaded

def musicswitcher(indexhere):
    global currently_playing_index
    if currently_playing_index != indexhere:
        mx.music.load(musics[indexhere])
        mx.music.play(-1) # -1 to loop forever, important because the game over theme is like 40 seconds long
        currently_playing_index = indexhere
    else:
        pass
mx.music.load("testdroga.mp3")
mx.music.play(-1) # this makes it play forever, apparently
mx.music.pause() # also me btw
mx.music.set_volume(1) # me btw
# sybau

death_sound = mx.Sound("vineboom.mp3")
hurt_sound = mx.Sound("hurt.mp3")

def deathsound():
    pass # ignore this

# images
tile_images = [
    pygame.image.load("image (1).png").convert_alpha(), # if we want to spice it up add more
]

menu_background = pygame.image.load("aimenubg.png").convert_alpha()
menu_background = pygame.transform.scale(menu_background, (750, 750))
blood_vignette = pygame.image.load("redvignette.png").convert_alpha()
player_ded = pygame.image.load("ded.png").convert_alpha()

player_health_images = []
for i in range(1, 4):
    img = pygame.image.load(f"playerhealth{i}.png").convert_alpha()
    w, h = img.get_size()
    img = pygame.transform.scale(img, (w * 4, h * 4))
    player_health_images.append(img)

player_gif = Image.open("playergif.gif")
frames = []
try:
    while True:
        frame = player_gif.convert("RGBA")
        mode = frame.mode
        size = frame.size
        data = frame.tobytes()
        py_image = pygame.image.fromstring(data, size, mode).convert_alpha()            # this was from google 
        frames.append(py_image)
        player_gif.seek(player_gif.tell() + 1)
except EOFError:
    pass
current_frame = 0
frame_timer = 0
frame_delay = 50
facing_left = False

# classes and functions

class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2  #  speed
        self.health = 100 # health
        self.alive = True # not dead yet
        self.shake_timer = 0

    def move(self, dx, dy, tile_grid, tile_size):
        grid_height = len(tile_grid)
        grid_width = len(tile_grid[0])

    # horizontal
        if dx != 0:
            new_x = self.x + dx * self.speed
            corners_x = [
                (new_x, self.y),
                (new_x + player_size - 1, self.y),
                (new_x, self.y + player_size - 1),
                (new_x + player_size - 1, self.y + player_size - 1)
            ]
            can_move_x = True
            for cx, cy in corners_x:
                tile_x = max(0, min(int(cx // tile_size), grid_width - 1))
                tile_y = max(0, min(int(cy // tile_size), grid_height - 1))
                if tile_grid[tile_y][tile_x] == 0:
                    can_move_x = False
                    break
            if can_move_x:
                self.x = new_x

        # vertical
        if dy != 0:
            new_y = self.y + dy * self.speed
            corners_y = [
                (self.x, new_y),
                (self.x + player_size - 1, new_y),
                (self.x, new_y + player_size - 1),
                (self.x + player_size - 1, new_y + player_size - 1)
            ]
            can_move_y = True
            for cx, cy in corners_y:
                tile_x = max(0, min(int(cx // tile_size), grid_width - 1))
                tile_y = max(0, min(int(cy // tile_size), grid_height - 1))
                if tile_grid[tile_y][tile_x] == 0:
                    can_move_y = False
                    break
            if can_move_y:
                self.y = new_y

    def shake(self):
        if self.shake_timer > 0:
            self.shake_timer -= 1
            return random.randint(-5, 5), random.randint(-5, 5)
        return 0, 0

    def damaged(self, amount):
        global die
        self.health -= amount
        self.shake_timer = 10  # frames of shake
        if self.health <= 0:
            self.die()
        else:
            hurt_sound.play()

    def die(self):
        global game_stage
        game_stage = "dead"
        print("player died")

    def respawn(self):
        self.health = 100
        self.alive = True
        self.x = start_x
        self.y = start_y
        mx.music.rewind()

player_size = 50

class tile:
    def __init__(self):
        self.sprite = pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 50, 50))
tile_size = 600  # size of a tile

# tile structure
tilestructure = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

# tile grid
tile_grid = [ 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 99, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
# dictionary:
# 0 = empty
# 1 = wall
# 99 = spawn

# find tile 99 to set player there
for row_idx, row in enumerate(tile_grid):
    for col_idx, tile_type in enumerate(row):
        if tile_type == 99:
            start_x = col_idx * tile_size + (tile_size - player_size) // 2
            start_y = row_idx * tile_size + (tile_size - player_size) // 2
            player = player(start_x, start_y)
            break

# camera variables
camera_x, camera_y = 0, 0
camera_speed = 0.1  # lower = slower

def get_camera_offset(player, tile_size):
    center_x = player.x + player_size // 2
    center_y = player.y + player_size // 2

    tile_x = int(center_x // tile_size)
    tile_y = int(center_y // tile_size)

    offset_x = tile_x * tile_size - (screen_w - tile_size) // 2
    offset_y = tile_y * tile_size - (screen_h - tile_size) // 2

    return offset_x, offset_y

# tile decor
tile_decorations = {}
for row_idx, row in enumerate(tile_grid):
    for col_idx, tile_type in enumerate(row):
        if tile_type != 0:
            images_for_tile = []
            x = 0
            while x < tile_size:
                y = 0
                while y < tile_size:
                    img = random.choice(tile_images)
                    rotation = random.choice([0, 90])
                    img_rotated = pygame.transform.rotate(img, rotation)
                    w, h = img_rotated.get_size()
                    images_for_tile.append((img_rotated, x, y))
                    y += h
                x += w
            tile_decorations[(row_idx, col_idx)] = images_for_tile

# some variables
moving_up = moving_down = moving_left = moving_right = False
game_stage = "in menu"
font = pygame.font.SysFont(None, 48)
is_paused = False
dragging_music_slider = False
menu_bg_can_animate = True
menu_bg_x = screen_w
flash_alpha = 0
flash_active = False
flash_speed = 1

# button variables
music_slider = pygame.Rect(screen_w - 400, 110, 300, 20)
play_button = pygame.Rect(50, screen_h - 150, 200, 100)
settings_button = pygame.Rect(50, screen_h - 300, 200, 100)
to_menu = pygame.Rect(screen_w - 250, screen_h - 150, 200, 100)

# loop setup
clock = pygame.time.Clock()
pygame.display.set_caption('Game')

# loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # key pressed
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_w: moving_up = True
            if event.key == pygame.K_s: moving_down = True
            if event.key == pygame.K_a: moving_left = True
            if event.key == pygame.K_d: moving_right = True
            if event.key == pygame.K_ESCAPE: 
                if is_paused == False: is_paused = True
                else: is_paused = False
            if developert_tools == True:
                if event.key == pygame.K_m:
                    if game_stage == "in menu":
                        mx.music.unpause()
                        game_stage = "in dungeon"
                    else:
                        game_stage = "in menu"
                        mx.music.pause()
                if event.key == pygame.K_h:
                    player.damaged(10)
                if event.key == pygame.K_p: game_stage = "dead"

        # key released
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_w: moving_up = False
            if event.key == pygame.K_s: moving_down = False
            if event.key == pygame.K_a: moving_left = False
            if event.key == pygame.K_d: moving_right = False

        # bouse mutton own
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if game_stage == "in menu":
                    if play_button.collidepoint(mouse_pos):
                        player.respawn()
                        musicswitcher(0) # ni problema maks tihur # ?????????
                        game_stage = "in dungeon"
                        mx.music.unpause()
                    if settings_button.collidepoint(mouse_pos):
                        game_stage="in settings"
                if game_stage == "in settings":
                    if music_slider.collidepoint(mouse_pos):
                        dragging_music_slider = True
                if game_stage == "dead":
                    if to_menu.collidepoint(mouse_pos):
                        game_stage = "in menu"
                        mx.music.pause()

        # bouse mutton op
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_music_slider = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

    # drawing
    screen.fill((0, 0, 0))  # background

    if game_stage == "in dungeon":
    # tile camera transition
        target_x, target_y = get_camera_offset(player, tile_size)
        camera_x += (target_x - camera_x) * camera_speed
        camera_y += (target_y - camera_y) * camera_speed
        for row_idx, row in enumerate(tile_grid):
            for col_idx, tile_type in enumerate(row):

                if tile_type != 0:
                    tile_x = col_idx * tile_size
                    tile_y = row_idx * tile_size
                    pygame.draw.rect(screen, (0, 0, 0), (tile_x - camera_x, tile_y - camera_y, tile_size, tile_size))
                    for img, img_x, img_y in tile_decorations[(row_idx, col_idx)]:
                        screen.blit(img, (tile_x + img_x - camera_x, tile_y + img_y - camera_y))

        # animate player
        frame_timer += 1
        if frame_timer >= frame_delay:
            frame_timer = 0
            current_frame = (current_frame + 1) % len(frames)

        player_frame = pygame.transform.scale(frames[current_frame], (player_size * 3, player_size * 3))

        if facing_left:
            player_frame = pygame.transform.flip(player_frame, True, False)
        offset_x = (player_size * 3 - player_size) // 2
        offset_y = (player_size * 3 - player_size) // 2
        shake_x, shake_y = player.shake()
        draw_x = player.x - camera_x - offset_x + shake_x
        draw_y = player.y - camera_y - offset_y + shake_y
        if facing_left:
            draw_x +=30 # offset because i didnt center the gif 😁
        else:
            draw_x -=30

        screen.blit(player_frame, (draw_x, draw_y))

        # while not paused
        if is_paused != True:
            mx.music.unpause()
            dx = dy = 0
            if moving_up: dy -= 1
            if moving_down: dy += 1
            if moving_left:
                dx -= 1
                facing_left = True
            if moving_right:
                dx += 1
                facing_left = False

            player.move(dx, dy, tile_grid, tile_size)

            # character image
            hud_shake_x, hud_shake_y = player.shake()

            pygame.draw.circle(screen, (20, 20, 20), (100, screen_h - 100), 80)
            screen.blit(font.render(str(player.health), True, (255, 255, 255)), (120, screen_h - 220))

            if player.health > 66:
                screen.blit(player_health_images[0], (-50 + hud_shake_x, screen_h - 260 + hud_shake_y))
            elif player.health > 33:
                screen.blit(player_health_images[1], (-50 + hud_shake_x, screen_h - 260 + hud_shake_y))
            else:
                screen.blit(player_health_images[2], (-50 + hud_shake_x, screen_h - 260 + hud_shake_y))


        # while paused
        elif is_paused == True:
            pygame.draw.rect(screen, (20, 20, 20), (screen_w // 2 - screen_w // 4, screen_h // 2 - screen_h // 4, screen_w // 2, screen_h // 2), 0)
            screen.blit(font.render("paused", True, (255, 255, 255)), (screen_w // 2 - 60, screen_h //2 - 22))
            mx.music.pause()

    elif game_stage == "in menu":
        if menu_bg_can_animate:
            target_x = screen_w - menu_background.get_width() # stop at right edge
            if menu_bg_x > target_x:
                menu_bg_x -= 10
                
            else:
                menu_bg_x = target_x
                menu_bg_can_animate = False
                flash_active = True
        screen.blit(menu_background, (menu_bg_x, 0))
        if flash_active and flash_alpha < 255:
            flash_alpha += flash_speed
            if flash_alpha > 255:
                flash_alpha = 255

            flash_surface = pygame.Surface((screen_w, screen_h))
            flash_surface.fill((255, 255, 255))
            flash_surface.set_alpha(255 - flash_alpha)  # fade out effect
            screen.blit(flash_surface, (0, 0))
        else:
            flash_active = False

        screen.blit(font.render("game title", True, (255, 255, 255)), (20, 20))
        # play button
        if play_button.collidepoint(mouse_pos):
            play_button_color = (70, 70, 70)   # lighter when hovered over
        else:
            play_button_color = (40, 40, 40)
        pygame.draw.rect(screen, (play_button_color), play_button)
        text_surf = font.render("Play", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=play_button.center)
        screen.blit(text_surf, text_rect)
        # settings button
        if settings_button.collidepoint(mouse_pos):
            settings_button_color = (70, 70, 70)   # lighter when hovered over
        else:
            settings_button_color = (40, 40, 40)
        pygame.draw.rect(screen, (settings_button_color), settings_button)
        text_surf = font.render("Settings", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=settings_button.center)
        screen.blit(text_surf, text_rect)

    elif game_stage == "in settings":
        setting_font = pygame.font.SysFont(None, 34) # new font for settings cause small
        screen.blit(font.render("settings", True, (255, 255, 255)), (20, 20))
        # music slider
        pygame.draw.rect(screen, (120, 120, 120), music_slider)
        volume = mx.music.get_volume()
        filled_width = int(music_slider.width * volume)
        filled_rect = pygame.Rect(music_slider.x, music_slider.y, filled_width, music_slider.height)
        pygame.draw.rect(screen, (180, 180, 180), filled_rect)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            # set volume
            if dragging_music_slider == True:
                relative_x = mouse_pos[0] - music_slider.x
                volume = max(0.0, min(1.0, relative_x / music_slider.width))
                mx.music.set_volume(volume)
        screen.blit(setting_font.render("music volume", True, (255, 255, 255)), (100, 100))
        screen.blit(setting_font.render(f"{int(volume * 100)}%", True, (255, 255, 255)), (screen_w // 2 + 20, 110))

    elif game_stage == "dead":
        screen.blit(font.render("ded", True, (255, 255, 255)), (20, 20))
        musicswitcher(1) # it worked because i'm a fucking genius from mars # but it doesnt switch back genious # SYFM
        if to_menu.collidepoint(mouse_pos):
            to_menu_color = (70, 70, 70)
        else:
            to_menu_color = (40, 40, 40)
        screen.blit(font.render("ded", True, (255, 255, 255)), (20, 20))
        pygame.draw.rect(screen, (to_menu_color), to_menu)
        text_surf = font.render("To menu", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=to_menu.center)
        screen.blit(text_surf, text_rect)

    clock.tick(240) 
    pygame.display.update()

pygame.quit()