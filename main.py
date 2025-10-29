# main python script
try:
    import random, pygame, pymunk, time, importlib.util
    from pygame import mixer as mx
except ModuleNotFoundError as e:
    print(f"you are missing module {e.name} man")

# initiate things
pygame.init()
mx.init(frequency=44100, size=-16, channels=16, buffer=8192)
screen_h, screen_w = 750, 1080
screen = pygame.display.set_mode((screen_w, screen_h))
resolution = screen_w, screen_h

virtual_fps = 0
vfps_max = 175
virtual_dt = 1 / vfps_max
virtual_accumulator = 0
virtual_prev_time = pygame.time.get_ticks() / 1000
virtual_clock = pygame.time.Clock()
virtual_w = 1080
virtual_h = 750
virtual_screen = pygame.Surface((virtual_w, virtual_h))
dt = dt = virtual_clock.tick(vfps_max) / 1000
prev_time = pygame.time.get_ticks() / 1000
max_fps = 60

space = pymunk.Space()
space.gravity = (0, 0)

def load_into_globals(filepath):
    spec = importlib.util.spec_from_file_location("module_name", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    globals().update(module.__dict__)
    return module

# this turns all of the main_globals[''] slop into actually non eye burning variables
class DictNamespace:
    def __init__(self, d):
        self._d = d
    def __getattr__(self, k):
        return self._d[k]
    def __setattr__(self, k, v):
        if k == "_d":
            super().__setattr__(k, v)
        else:
            self._d[k] = v
    def __getitem__(self, k):
        return self._d[k]
    def __setitem__(self, k, v):
        self._d[k] = v

# pre defines some variables
main_globals = {
    'screen_w': 1080, 'screen_h': 750, 'screen': pygame.display.set_mode((1080, 750)), 'player_size': 32, 'tile_size': 600, 'musics': ["track1.mp3", "track2.mp3"],
    'currently_playing_index': -1, 'hurt_sound': mx.Sound("assets/audio/sfx/hurt.mp3"), 
    'player_health_images': [pygame.Surface((50, 50)) for i in range(3)], 'vignette': pygame.Surface((1080, 750), pygame.SRCALPHA), 'menu_background': pygame.Surface((200, 200)),
    'menu_bg_x': 0, 'menu_bg_can_animate': True, 'flash_active': False, 'flash_alpha': 0, 'flash_speed': 10, 'play_button': pygame.Rect(100, 100, 100, 50), 'settings_button': pygame.Rect(100, 200, 100, 50),
    'dragging_music_slider': False, 'music_slider': pygame.Rect(100, 300, 200, 20), 'to_menu': pygame.Rect(50, 50, 100, 50), 'camera_x': 0, 'camera_y': 0, 'camera_speed': 0.1,
    'current_frame': 0, 'frame_timer': 0, 'frame_delay': 5, 'frames': [pygame.Surface((32, 32))], 'game_stage': "", 'facing_left': False,
    'moving_up': False, 'moving_down': False, 'moving_left': False, 'moving_right': False, 'developer_tools': True, 'player': None,
    'musicswitcher': None, 'faded_in': False
}

last_context = None
loading_step = 0
loading_steps = 11
bar_risen = False
bar_h = 0
splash_alpha = 0
text_alpha = 0
text_faded = False
bar_color = (0, 170, 0)
fade_out = False
fade_speed = 5
splash_image = pygame.image.load("assets/useful images/splashimage.jpg").convert_alpha()
loading_icon = pygame.image.load("assets/useful images/save.png")
loading_icon = pygame.transform.scale2x(loading_icon)

def draw_loading_screen(step, total, context):
    global bar_risen, bar_h, splash_alpha, bar_color, last_context, text_alpha, text_faded, fade_out

    if context is not None:
        last_context = context
    else:
        context = last_context

    screen.fill((0, 0, 0))
    splash_image.set_alpha(splash_alpha)
    screen.blit(splash_image, (screen_w // 2 - splash_image.get_width() // 2, screen_h // 2 - splash_image.get_height() // 2))

    if not fade_out and splash_alpha < 255:
        splash_alpha += 5
        if splash_alpha > 255:
            splash_alpha = 255

    if fade_out and splash_alpha > 0:
        splash_alpha -= fade_speed
        if splash_alpha < 0:
            splash_alpha = 0

    bar_w = screen_w
    target_bar_h = 20

    if not fade_out and not bar_risen and bar_h < target_bar_h:
        bar_h += 2
        if bar_h >= target_bar_h:
            bar_h = target_bar_h
            bar_risen = True

    if fade_out and bar_h > 0:
        bar_h -= 2
        if bar_h < 0:
            bar_h = 0

    if not fade_out and bar_risen and not text_faded:
        text_alpha += 5
        if text_alpha >= 255:
            text_alpha = 255
            text_faded = True

    if fade_out:
        if text_alpha > 0:
            text_alpha -= fade_speed
            if text_alpha < 0:
                text_alpha = 0

    # straight bars yo
    pygame.draw.rect(screen, (80, 80, 80), (0, screen_h - bar_h, bar_w, target_bar_h))
    pygame.draw.rect(screen, bar_color, (0, screen_h - bar_h, (bar_w / total) * step if total else 0, target_bar_h))

    angle = (pygame.time.get_ticks() // 5) % 360
    rotated_icon = pygame.transform.rotate(loading_icon, angle)
    rotated_rect = rotated_icon.get_rect(center=(50, screen_h - 70))
    rotated_icon.set_alpha(text_alpha)
    screen.blit(rotated_icon, rotated_rect.topleft)

    # temp_font = pygame.font.SysFont(None, 34)
    temp_font = pygame.font.Font("assets/font/editundo.ttf", 34)
    if context == "finalizing":
        display_text = "finalizing"
    elif context == "preparing":
        display_text = "preparing"
    else:
        display_text = f"loading {context}..."
    text = temp_font.render(display_text, True, (255, 255, 255))
    text_rect = text.get_rect(topleft=(loading_icon.get_width() + 20, screen_h - 60))
    text.set_alpha(text_alpha)
    screen.blit(text, text_rect)

    if not fade_out and bar_risen and not text_faded:
        text_alpha += 5
        if text_alpha >= 255:
            text_alpha = 255
            text_faded = True

    pygame.display.flip()

def loading_bar_flicker(duration=0.5, steps=10, force_full=False):
    global bar_color, loading_step
    normal = (0, 170, 0)
    bright = (0, 255, 0)
    white = (255, 255, 255)

    for i in range(steps):
        t = i / steps
        bar_color = tuple(int(white[j] + t * (bright[j] - white[j])) for j in range(3))
        draw_loading_screen(loading_steps if force_full else loading_step, loading_steps, last_context)
        pygame.time.wait(int((duration / (2 * steps)) * 1000))

    for i in range(steps):
        t = i / steps
        bar_color = tuple(int(bright[j] + t * (normal[j] - bright[j])) for j in range(3))
        draw_loading_screen(loading_steps if force_full else loading_step, loading_steps, last_context)
        pygame.time.wait(int((duration / (2 * steps)) * 1000))

    bar_color = normal

start_time = time.time()
modules_to_load = [
    ("stsw", "stager"),
    ("loader1", "variables"),
    ("connector", "data"),
    ("loader2", "assets"),
    ("weapons", "logic"),
    ("loader3", "logic"),
    ("dungeon", "logic"),
    ("player", "logic"),
    ("enemy", "logic")
]

# prep
last_context = "preparing"
bar_risen = False
text_faded = False
fade_out = False

while not bar_risen or text_alpha < 255:
    draw_loading_screen(0, loading_steps, "preparing")
    pygame.event.pump()
    pygame.time.wait(30)

# initial
draw_loading_screen(loading_step, loading_steps, "starting")
loaded_modules = []

for idx, (mod_name, context) in enumerate(modules_to_load, start=1):
    loading_step = idx
    draw_loading_screen(idx, len(modules_to_load), context)
    loading_bar_flicker()
    if mod_name is not None:
        mod = load_into_globals(f"{mod_name}.py")
        loaded_modules.append((mod, mod_name))
        loader_func = getattr(mod, mod_name, None)
        try:
            loader_func(main_globals)
        except Exception as e:
            print(f"error loading {mod_name}: {e}")

# finalize
loading_step = len(loaded_modules) + 1
fade_out = True
while splash_alpha > 0:
    draw_loading_screen(loading_step, len(loaded_modules) + 1, "finalizing")
    pygame.time.wait(20)

main_globals['game_stage'] = "in menu"
total_time = time.time() - start_time
print(f"took {total_time:.2f} seconds to load")

saved_data = main_globals['connector_instance'].get_data()
for key, value in saved_data.items():
    if key in main_globals:
        main_globals[key] = value
print(f"loaded saved data: {saved_data}")

main = DictNamespace(main_globals) # converts some globals
print("converted main_globals to mains, get ready to tish!")
# dont use main_globals['🤖'] but instead use main.🤖
# stupar ce to vidite me je res prevec motilo da je vse bilo v neumni barvi vsega drugega "" texta in nisem hotel kopirati main_globals[''] cisto povsod

frame_caps = main.frame_caps
main.frame_cap = main_globals.get('max_fps', 60)
main.frame_cap_index = min(range(len(frame_caps)), key=lambda i: abs(frame_caps[i] - main.frame_cap))
main.frame_cap = frame_caps[main.frame_cap_index]

resolutions = main.resolutions
main.resolution = main_globals.get('resolution', (1080, 750))
main.resolution_index = min(range(len(resolutions)), key=lambda i: abs(resolutions[i][0] - main.resolution[0]))
main.resolution = resolutions[main.resolution_index]

music_volume = saved_data.get("music", 1)
main.music_volume = music_volume
mx.music.set_volume(music_volume)

current_time = pygame.time.get_ticks() / 1000
main.dt = current_time - main.prev_time
main.prev_time = current_time
main.screen = virtual_screen
main.resolution = resolutions[main.resolution_index]

main.player_gif(main_globals) # loads the player gif

main.space = space
space.gravity = (0, 500)

time.sleep(0.3)

print("started")
# loop setup
clock = pygame.time.Clock() # makes some clocks and sets the titles
pygame.display.set_caption(' naganou :)))') # change to naganou? :))) # sure man

main.walkable_mask = main.make_initial_walkable_surface(main.tilemap, main_globals) # makes the initial walkable surface
# makes some game loops
running = True
while running:
    main.space.step(main.dt)
    main.virtual_screen.fill((0, 0, 0))
    real_mx, real_my = pygame.mouse.get_pos()
    mouse_pos = pygame.mouse.get_pos()
    main.mouse_pos = (
        real_mx * virtual_w / screen.get_width(),
        real_my * virtual_h / screen.get_height()
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: 
                main.moving_up = True
            if event.key == pygame.K_s: 
                main.moving_down = True
            if event.key == pygame.K_a:
                main.moving_left = True
                main.facing_left = True
            if event.key == pygame.K_d: 
                main.moving_right = True
                main.facing_left = False
            if event.key == pygame.K_e:
                main.pressed_e = True
            else:
                main.pressed_e = False
            if event.key == pygame.K_f:
                main.pressed_f = True
            else:
                main.pressed_f = False
            if event.key == pygame.K_ESCAPE:
                if main.is_paused == False: main.is_paused = True
                else: main.is_paused = False
            if main.developer_tools == True:
                if event.key == pygame.K_m:
                    if main.game_stage == "in dungeon":
                        mx.music.pause()
                        main.game_stage = "in menu"
                if main.game_stage == "in dungeon":
                    if event.key == pygame.K_h:
                        main.player.damaged(10)
                    if event.key == pygame.K_p:
                        main.game_stage = "dead"
                    if event.key == pygame.K_y:
                        rand1 = random.randint(0, 9)
                        rand2 = random.randint(0, 9)
                        main.update_tile(main_globals, rand1, rand2, 99)
                        main.update_tile(main_globals, rand1 + 1, rand2, 2)
                        main.camera_x, main.camera_y = main.get_camera_offset(main_globals, main.player, main.tile_size)
                        main.spawn_weapons(main_globals)
                    if event.key == pygame.K_r:
                        main.player.respawn()
                    if event.key == pygame.K_o:
                        main.player.locked = not main.player.locked
                        print(f"is locked {main.player.locked}")
                    if event.key == pygame.K_b:
                        if not main.in_shop:
                            main.in_shop = True # just now for debugging use match state when actually doing the thing
                            main.game_stage = "shopping"
                            print("in shop")
                        else:
                            main.in_shop = False
                            main.game_stage = "in dungeon"
                            print("dih")
        # key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w: main.moving_up = False
            if event.key == pygame.K_s: main.moving_down = False
            if event.key == pygame.K_a: main.moving_left = False
            if event.key == pygame.K_d: main.moving_right = False

        # mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if main.game_stage == "in menu": # IF IN MENU
                    if main.play_button.collidepoint(main.mouse_pos):
                        main.player.respawn()
                        main.player.effect("healfull", 0) # resets player health
                        main.musicswitcher(main_globals, 0)
                        main.game_stage = "in dungeon"
                        mx.music.unpause()
                    if main.settings_button.collidepoint(main.mouse_pos):
                        main.game_stage = "in settings"
                    if main.credits_button.collidepoint(main.mouse_pos):
                        main.game_stage = "in credits"
                if main.game_stage == "in credits": # IF IN CREDITS
                    if main.to_menu.collidepoint(main.mouse_pos):
                        main.game_stage = "in menu"
                if main.game_stage == "in settings": # IF IN SETTINGS
                    if main.frame_slider.collidepoint(main.mouse_pos):
                        main.dragging_frame_slider = True
                    elif main.music_slider.collidepoint(main.mouse_pos):
                        main.dragging_music_slider = True
                    elif main.resolution_slider.collidepoint(main.mouse_pos):
                        main.dragging_resolution_slider = True
                    if main.hints_button.collidepoint(main.mouse_pos):
                        if main.hints_text == "True":
                            main.hints_text = "False"
                            print("hints disabled")
                        else: 
                            main.hints_text = "True"
                            print("hints reenabled")
                    if main.to_menu.collidepoint(main.mouse_pos):
                        main.game_stage = "in menu"
                if main.game_stage == "dead": # IF DEAD
                    if main.to_menu.collidepoint(main.mouse_pos):
                        main.game_stage = "in menu"
                        mx.music.pause()
                if main.player is not None:
                    if main.game_stage == "in dungeon":
                        if main.player.weapons != []:
                            main.player.attack(main_globals)
                            # print("player attacked") annoys me that it says it even if its on cd so i moved it

        main.mouse_pressed = pygame.mouse.get_pressed()[0]

        # mouse button up
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                main.dragging_frame_slider = False
                main.dragging_music_slider = False
                main.dragging_resolution_slider = False

    if main.game_stage == "in dungeon":
        keys = pygame.key.get_pressed()
        if any(keys): # any key
            main_globals['last_input_time'] = pygame.time.get_ticks() / 1000 # ms to s

        mouse_buttons = pygame.mouse.get_pressed()
        if any(mouse_buttons): # any mouse press
            main_globals['last_input_time'] = pygame.time.get_ticks() / 1000

        current_time = pygame.time.get_ticks() / 1000
        main_globals['idle_time'] = current_time - main_globals['last_input_time']

    else: main_globals['last_input_time'] = 0

    # update main screen with virtual screen
    current_time = pygame.time.get_ticks() / 1000
    frame_time = current_time - virtual_prev_time
    virtual_prev_time = current_time

    frame_time = min(frame_time, 0.1)
    virtual_accumulator += frame_time
    max_virtual_steps = 5
    steps = 0
    while virtual_accumulator >= virtual_dt and steps < max_virtual_steps:
        main.dt = virtual_dt
        main.match_state(main_globals, main.game_stage)
        virtual_accumulator -= virtual_dt
        steps += 1

    if main.resolution != resolution:
        resolution = main.resolution
        screen = pygame.display.set_mode(resolution)

    screen.blit(pygame.transform.scale(main.screen, resolution), (0, 0))

    loop_fps = clock.tick(main.max_fps)
    pygame.display.flip()

    if main.developer_tools:
        vfps = int(1 / virtual_dt)
        pygame.display.set_caption(f"fps: {int(clock.get_fps())} / {main.max_fps}, vfps: {vfps}, mouse pos: {pygame.mouse.get_pos()}, vmouse pos: {int(main.mouse_pos[0]), int(main.mouse_pos[1])}, player pos: {main_globals['player'].x, main_globals['player'].y}")

pygame.quit()