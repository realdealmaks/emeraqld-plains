import math, random, pygame, pydub, pytweening, scipy, pymunk, pathfinding
import importlib.util
from PIL import Image
from pygame import mixer as mx
from pymunk import shapes

# main

# initiate things
pygame.init()
mx.init(frequency=44100, size=-16, channels=16, buffer=8192)
screen_h, screen_w = 750, 1080
screen = pygame.display.set_mode((screen_w, screen_h))

def load_into_globals(filepath):
    spec = importlib.util.spec_from_file_location("module_name", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    globals().update(module.__dict__)
    return module


main_globals = {
    'screen_w': 1080,
    'screen_h': 750,
    'screen': pygame.display.set_mode((1080, 750)),
    'player_size': 32,
    'tile_size': 50,
    'musics': ["track1.mp3", "track2.mp3"],
    'currently_playing_index': -1,
    'hurt_sound': mx.Sound("assets/audio/sfx/hurt.mp3"),
    'font': pygame.font.SysFont(None, 36),
    'player_health_images': [pygame.Surface((50, 50)) for _ in range(3)],
    'vignette': pygame.Surface((1080, 750), pygame.SRCALPHA),
    'menu_background': pygame.Surface((200, 200)),
    'menu_bg_x': 0,
    'menu_bg_can_animate': True,
    'flash_active': False,
    'flash_alpha': 0,
    'flash_speed': 10,
    'play_button': pygame.Rect(100, 100, 100, 50),
    'settings_button': pygame.Rect(100, 200, 100, 50),
    'dragging_music_slider': False,
    'music_slider': pygame.Rect(100, 300, 200, 20),
    'to_menu': pygame.Rect(50, 50, 100, 50),
    'camera_x': 0,
    'camera_y': 0,
    'camera_speed': 0.1,
    'current_frame': 0,
    'frame_timer': 0,
    'frame_delay': 5,
    'frames': [pygame.Surface((32, 32))],
    'game_stage': 'menu',
    'facing_left': False,
    'mouse_pos': pygame.mouse.get_pos(),
    'mouse_pressed': pygame.mouse.get_pressed()[0],
    'moving_up': False,
    'moving_down': False,
    'moving_left': False,
    'moving_right': False,
    'developer_tools': True,
    'player': None,
    'musicswitcher': None
}

loading1 = load_into_globals("loader1.py")
print("loader 1 loading")
loading2 = load_into_globals("loader2.py")
print("loader 2 loading")
loading3 = load_into_globals("loader3.py")
print("loader 3 loading")

loading1.loader1(main_globals)
print("loader1 loaded")
loading2.loader2(main_globals)
print("loader2 loaded")
loading3.loader3(main_globals)
print("loader3 loaded")

# i used a tutorial for this ^ , if it doesnt work: ask the indian on youtube

# animate player with the gif
player_gif = Image.open("assets/models/player/playergif.gif")
try:
    while True:
        frame = player_gif.convert("RGBA")
        mode = frame.mode
        size = frame.size
        data = frame.tobytes()
        py_image = pygame.image.fromstring(data, size, mode).convert_alpha()            # this entire block was from google 
        main_globals['frames'].append(py_image)
        player_gif.seek(player_gif.tell() + 1)
except EOFError:
    pass


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
            if event.key == pygame.K_w: main_globals['moving_up'] = True
            if event.key == pygame.K_s: main_globals['moving_down'] = True
            if event.key == pygame.K_a: 
                main_globals['moving_left'] = True
                main_globals['facing_left'] = True
            if event.key == pygame.K_d: 
                main_globals['moving_right'] = True
                main_globals['facing_left'] = False
            if event.key == pygame.K_ESCAPE:
                if main_globals['is_paused'] == False: main_globals['is_paused'] = True
                else: main_globals['is_paused'] = False
            if main_globals['developer_tools'] == True:
                if event.key == pygame.K_m:
                    if main_globals['game_stage'] == "in dungeon":
                        mx.music.pause()
                        main_globals['game_stage'] = "in menu"
                if main_globals['game_stage'] == "in dungeon":
                    if event.key == pygame.K_h:
                        main_globals['player'].damaged(10)
                    if event.key == pygame.K_p: main_globals['game_stage'] = "dead"

        # key released
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_w: main_globals['moving_up'] = False
            if event.key == pygame.K_s: main_globals['moving_down'] = False
            if event.key == pygame.K_a: main_globals['moving_left'] = False
            if event.key == pygame.K_d: main_globals['moving_right'] = False

        # mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                main_globals['mouse_pos'] = pygame.mouse.get_pos()
                if main_globals['game_stage'] == "in menu":
                    if main_globals['play_button'].collidepoint(main_globals['mouse_pos']):
                        main_globals['player'].respawn()
                        main_globals['musicswitcher'](main_globals, 0)
                        main_globals['game_stage'] = "in dungeon"
                        mx.music.unpause()
                    if main_globals['settings_button'].collidepoint(main_globals['mouse_pos']):
                        main_globals['game_stage'] = "in settings"
                if main_globals['game_stage'] == "in settings":
                    if main_globals['music_slider'].collidepoint(main_globals['mouse_pos']):
                        main_globals['dragging_music_slider'] = True
                    if main_globals['to_menu'].collidepoint(main_globals['mouse_pos']):
                        main_globals['game_stage'] = "in menu"
                if main_globals['game_stage'] == "dead":
                    if main_globals['to_menu'].collidepoint(main_globals['mouse_pos']):
                        main_globals['game_stage'] = "in menu"
                        mx.music.pause()

        # mouse button up
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                main_globals['dragging_music_slider'] = False

        main_globals['mouse_pos'] = pygame.mouse.get_pos()
        main_globals['mouse_pressed'] = pygame.mouse.get_pressed()[0]

    screen.fill((0, 0, 0))  # background

    if main_globals['game_stage'] == "in dungeon": 
        main_globals['draw_dungeon'](main_globals, main_globals['player'], main_globals.get('moving_up', False), main_globals.get('moving_down', False), main_globals.get('moving_left', False), main_globals.get('moving_right', False), main_globals.get('is_paused', False), main_globals['mouse_pos'], main_globals['facing_left'])

    elif main_globals['game_stage'] == "in menu":
        main_globals['draw_menu'](main_globals, main_globals['mouse_pos'])

    elif main_globals['game_stage'] == "in settings":
        main_globals['draw_settings'](main_globals, main_globals['mouse_pos'])

    elif main_globals['game_stage'] == "dead":
        main_globals['draw_dead'](main_globals, main_globals['mouse_pos'])

    fps = int(clock.get_fps())
    pygame.display.set_caption(f"FPS: {fps}")


    clock.tick(240)
    pygame.display.update()

pygame.quit()