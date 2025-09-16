import math, random, pygame, pydub, pytweening, scipy, pymunk, pathfinding
import importlib.util
from PIL import Image
from pygame import mixer as mx
from pymunk import shapes
# main python script

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
    'screen_w': 1080, 'screen_h': 750, 'screen': pygame.display.set_mode((1080, 750)), 'player_size': 32, 'tile_size': 50, 'musics': ["track1.mp3", "track2.mp3"],
    'currently_playing_index': -1, 'hurt_sound': mx.Sound("assets/audio/sfx/hurt.mp3"), 'font': pygame.font.SysFont(None, 36), 
    'player_health_images': [pygame.Surface((50, 50)) for _ in range(3)], 'vignette': pygame.Surface((1080, 750), pygame.SRCALPHA), 'menu_background': pygame.Surface((200, 200)),
    'menu_bg_x': 0, 'menu_bg_can_animate': True, 'flash_active': False, 'flash_alpha': 0, 'flash_speed': 10, 'play_button': pygame.Rect(100, 100, 100, 50), 'settings_button': pygame.Rect(100, 200, 100, 50),
    'dragging_music_slider': False, 'music_slider': pygame.Rect(100, 300, 200, 20), 'to_menu': pygame.Rect(50, 50, 100, 50), 'camera_x': 0, 'camera_y': 0, 'camera_speed': 0.1,
    'current_frame': 0, 'frame_timer': 0, 'frame_delay': 5, 'frames': [pygame.Surface((32, 32))], 'game_stage': "menu", 'facing_left': False, 'mouse_pos': pygame.mouse.get_pos(),
    'mouse_pressed': pygame.mouse.get_pressed()[0], 'moving_up': False, 'moving_down': False, 'moving_left': False, 'moving_right': False, 'developer_tools': True, 'player': None,
    'musicswitcher': None
}

loading1 = load_into_globals("loader1.py")
print("loader 1 loading")
loading2 = load_into_globals("loader2.py")
print("loader 2 loading") # loads some files
loading3 = load_into_globals("loader3.py")
print("loader 3 loading")

loading1.loader1(main_globals)
print("loader1 loaded")
loading2.loader2(main_globals)
print("loader2 loaded") # actually loads some files
loading3.loader3(main_globals)
print("loader3 loaded")

main = DictNamespace(main_globals) # converts some globals
# dont use main_globals['🤖'] but instead use main.🤖
# stupar ce to vidite me je res prevec motilo da je vse bilo v neumni barvi vsega drugega "" texta in nisem hotel kopirati main_globals[''] cisto povsod


# i should probably burn this somewhere in loader 3 some time soon
# animates player with the gif
player_gif = Image.open("assets/models/player/playergif.gif")
try:
    while True:
        frame = player_gif.convert("RGBA")
        mode = frame.mode
        size = frame.size
        data = frame.tobytes()
        py_image = pygame.image.fromstring(data, size, mode).convert_alpha()            # this entire block was from google 
        main.frames.append(py_image)
        player_gif.seek(player_gif.tell() + 1)
except EOFError:
    pass

# loop setup
clock = pygame.time.Clock() # makes some clocks and sets the title
pygame.display.set_caption('Game')

# makes some game loops
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # key pressed
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_w: main.moving_up = True
            if event.key == pygame.K_s: main.moving_down = True
            if event.key == pygame.K_a: 
                main.moving_left = True
                main.facing_left = True
            if event.key == pygame.K_d: 
                main.moving_right = True
                main.facing_left = False
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
                    if event.key == pygame.K_p: main.game_stage = "dead"

        # key released
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_w: main.moving_up = False
            if event.key == pygame.K_s: main.moving_down = False
            if event.key == pygame.K_a: main.moving_left = False
            if event.key == pygame.K_d: main.moving_right = False

        # mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                main.mouse_pos = pygame.mouse.get_pos()
                if main.game_stage == "in menu":
                    if main.play_button.collidepoint(main.mouse_pos):
                        main.player.respawn()
                        main.musicswitcher(main_globals, 0)
                        main.game_stage = "in dungeon"
                        mx.music.unpause()
                    if main.settings_button.collidepoint(main.mouse_pos):
                        main.game_stage = "in settings"
                if main.game_stage == "in settings":
                    if main.music_slider.collidepoint(main.mouse_pos):
                        main.dragging_music_slider = True
                    if main.to_menu.collidepoint(main.mouse_pos):
                        main.game_stage = "in menu"
                if main.game_stage == "dead":
                    if main.to_menu.collidepoint(main.mouse_pos):
                        main.game_stage = "in menu"
                        mx.music.pause()

        # mouse button up
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                main.dragging_music_slider = False

        main.mouse_pos = pygame.mouse.get_pos()
        main.mouse_pressed = pygame.mouse.get_pressed()[0]

    screen.fill((0, 0, 0))  # background

    if main.game_stage == "in dungeon": 
        main.draw_dungeon(main_globals, main.player, main.moving_up, main.moving_down, main.moving_left, main.moving_right, main.is_paused, main.mouse_pos, main.facing_left)
        # to je prevec za 1 linijo prosim ne sprement 💖

    elif main.game_stage == "in menu":
        main.draw_menu(main_globals, main.mouse_pos)

    elif main.game_stage == "in settings":
        main.draw_settings(main_globals, main.mouse_pos)

    elif main.game_stage == "dead":
        main.draw_dead(main_globals, main.mouse_pos)

    if main.developer_tools == True:
        fps = int(clock.get_fps())
        pygame.display.set_caption(f"FPS: {fps}") # re changes the caption for testings of framings


    clock.tick(240)
    pygame.display.update()

pygame.quit()