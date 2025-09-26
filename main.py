import math, random, pygame, pydub, pytweening, scipy, pymunk, pathfinding
import importlib.util
from PIL import Image
from pygame import mixer as mx
from pymunk import shapes
import time
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
    'screen_w': 1080, 'screen_h': 750, 'screen': pygame.display.set_mode((1080, 750)), 'player_size': 32, 'tile_size': 600, 'musics': ["track1.mp3", "track2.mp3"],
    'currently_playing_index': -1, 'hurt_sound': mx.Sound("assets/audio/sfx/hurt.mp3"), 'font': pygame.font.SysFont(None, 36), 
    'player_health_images': [pygame.Surface((50, 50)) for _ in range(3)], 'vignette': pygame.Surface((1080, 750), pygame.SRCALPHA), 'menu_background': pygame.Surface((200, 200)),
    'menu_bg_x': 0, 'menu_bg_can_animate': True, 'flash_active': False, 'flash_alpha': 0, 'flash_speed': 10, 'play_button': pygame.Rect(100, 100, 100, 50), 'settings_button': pygame.Rect(100, 200, 100, 50),
    'dragging_music_slider': False, 'music_slider': pygame.Rect(100, 300, 200, 20), 'to_menu': pygame.Rect(50, 50, 100, 50), 'camera_x': 0, 'camera_y': 0, 'camera_speed': 0.1,
    'current_frame': 0, 'frame_timer': 0, 'frame_delay': 5, 'frames': [pygame.Surface((32, 32))], 'game_stage': "", 'facing_left': False, 'mouse_pos': pygame.mouse.get_pos(),
    'mouse_pressed': pygame.mouse.get_pressed()[0], 'moving_up': False, 'moving_down': False, 'moving_left': False, 'moving_right': False, 'developer_tools': True, 'player': None,
    'musicswitcher': None, 'faded_in': False
}

def draw_loading_screen(step, total):
    screen.fill((20, 20, 20))
    text = ""

    for i in range(step):
        if i%3 == 0:
            text = "."
        elif i%3 == 1:
            text = ".."
        elif i%3 == 2:
            text = "..."

    font = pygame.font.SysFont(None, 50)
    if step != total:
        label = font.render(f"Loading {text}", True, (200, 200, 200))
    else:
        label = font.render("Loading complete!", True, (200, 200, 200))
    rect = label.get_rect(center=(screen_w // 2, screen_h // 2 - 50))
    screen.blit(label, rect)
    label = font.render(f"{int((step / total) * 100)}%", True, (200, 200, 200))
    rect = label.get_rect(center=(screen_w // 2, screen_h // 2 + 80))
    screen.blit(label, rect)
    font = pygame.font.SysFont(None, 20)
    label = font.render("dont touch until in menu", True, (200, 20, 20))
    rect = label.get_rect(center=(screen_w // 2, screen_h - 80))
    screen.blit(label, rect)

    # Progress bar
    bar_w, bar_h = 400, 40
    bar_x = (screen_w - bar_w) // 2
    bar_y = (screen_h - bar_h) // 2 + 20
    pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_w, bar_h))
    pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, int(bar_w * (step / total)), bar_h))

    pygame.display.flip()

loading_step = 0
loading_steps = 1

draw_loading_screen(loading_step, loading_steps)
loading_step += 1
loading_steps += 1
loading1 = load_into_globals("loader1.py")
loading1.loader1(main_globals)
time.sleep(0.2)

draw_loading_screen(loading_step, loading_steps)
loading_step += 1
loading_steps += 1
loading2 = load_into_globals("loader2.py")
loading2.loader2(main_globals)
time.sleep(0.2)

draw_loading_screen(loading_step, loading_steps)
loading_step += 1
loading_steps += 1
loading3 = load_into_globals("loader3.py")
loading3.loader3(main_globals)
time.sleep(0.2)

draw_loading_screen(loading_step, loading_steps)
draw_loading_screen(loading_steps, loading_steps)
time.sleep(3)

pygame.display.quit()
print("restarting displayzers")

main = DictNamespace(main_globals) # converts some globals
print("converted main_globals to mains, get ready to tish!")
# dont use main_globals['🤖'] but instead use main.🤖
# stupar ce to vidite me je res prevec motilo da je vse bilo v neumni barvi vsega drugega "" texta in nisem hotel kopirati main_globals[''] cisto povsod

time.sleep(0.3)
pygame.init()
screen = pygame.display.set_mode((main.screen_w, main.screen_h)) # retish the balish
main.screen = screen # regalishes it to the main globas zalish
print("started some displayzers")
main.game_stage = "splash" # starts at splash screen

main.walkable_mask = main.make_initial_walkable_surface(main.tilemap, main_globals) # makes the initial walkable surface

# loop setup
clock = pygame.time.Clock() # makes some clocks and sets the titles
pygame.display.set_caption('Game')

main.player_gif(main_globals) # loads the player gif

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
                    if event.key == pygame.K_p:
                        main.game_stage = "dead"
                    if event.key == pygame.K_y:
                        rand1 = random.randint(0, 9)
                        rand2 = random.randint(0, 9)
                        main.update_tile(main_globals, rand1, rand2, 99)
                        main.camera_x, main.camera_y = main.get_camera_offset(main_globals, main.player, main.tile_size)

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
                        main.player.effect("healfull", 0) # resets player health
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

    if main.game_stage == "splash":
        main.draw_splash(main_globals) # makes shit look cool! 🤖
        time.sleep(2)
        main.game_stage = "in menu"

    if main.game_stage == "in dungeon":
        main.draw_dungeon(main_globals, main.player, main.is_paused, main.facing_left)
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