import math, random, pygame, PIL, pydub, pytweening, scipy, dearpygui

pygame.init()
screen_h, screen_w = 750, 1080
screen = pygame.display.set_mode((screen_w, screen_h))

# classes and functions

class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5  #  speed
        self.health = 100

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

    def die(self):
        pass

player_size = 50

class tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 50, 50))
    
    def destroy(self):
        pass

tile_size = 600  # size of a tile

# tile structure
tilestrucure = [
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
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

# movement variables
moving_up = moving_down = moving_left = moving_right = False
game_stage = ""

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

        # Key pressed
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_w: moving_up = True
            if event.key == pygame.K_s: moving_down = True
            if event.key == pygame.K_a: moving_left = True
            if event.key == pygame.K_d: moving_right = True

        # key released
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_w: moving_up = False
            if event.key == pygame.K_s: moving_down = False
            if event.key == pygame.K_a: moving_left = False
            if event.key == pygame.K_d: moving_right = False

    # movement
    dx = dy = 0
    if moving_up: dy -= 1
    if moving_down: dy += 1
    if moving_left: dx -= 1
    if moving_right: dx += 1

    player.move(dx, dy, tile_grid, tile_size)

    # tile camera transition
    target_x, target_y = get_camera_offset(player, tile_size)
    camera_x += (target_x - camera_x) * camera_speed
    camera_y += (target_y - camera_y) * camera_speed

    # drawing
    screen.fill((0, 0, 0))  # background

    for row_idx, row in enumerate(tile_grid):
        for col_idx, tile_type in enumerate(row):
            if tile_type != 0:
                pygame.draw.rect(screen, (0, 255, 0), (col_idx*tile_size - camera_x, row_idx*tile_size - camera_y, tile_size, tile_size))

    pygame.draw.rect(screen, (255, 0, 0), (player.x - camera_x,player.y - camera_y, player_size, player_size))

    clock.tick(240)
    pygame.display.update()

pygame.quit()
