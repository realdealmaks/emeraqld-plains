# for bobbers
import pygame, math

def enemy(main_globals):

    class Enemy():
        def __init__(self, main_globals, x, y, type):
            self.main_globals = main_globals
            self.x = x
            self.y = y
            self.size = main_globals['enemy_size']
            self.health = 50
            self.alive = True
            self.speed = 0.8
            self.type = type
            self.active = False
            self.images = [
                pygame.transform.scale2x(main_globals['enemy_test_0'].convert_alpha()),
                pygame.transform.scale2x(main_globals['enemy_test_1'].convert_alpha())
            ]
            self.rect = self.images[0].get_rect()

        def damaged(self, damage):
            self.health -= damage
            if self.health <= 0:
                self.alive = False
                self.die()
            else:
                pass # here is damage animation
                # which will probably just tint red

        def detect(self, player):
            distance = math.dist((self.x, self.y), (player.x, player.y))
            if distance <= 150:
                self.active = True
            return self.active

        def move(self, player): # ookay?
            if self.active:
                # find vector between the two
                dx, dy = player.x - self.rect.x, player.y - self.rect.y
                dist = math.hypot(dx, dy)
                dx, dy = dx / dist, dy / dist  # idk what this does
                # actually move
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed

        def draw(self, type):
            if self.alive:
                screen = main_globals['screen']
                screen.blit(self.images[type], (self.x - main_globals['camera_x'], self.y - main_globals['camera_y']))
                self.rect.topleft = (self.x - main_globals['camera_x'], self.y - main_globals['camera_y'])
            elif not self.alive:
                # death animation and break loop
                # why the fuck does every enemy have a death animation
                pass

        def die(self):
            if self in self.main_globals['enemy_list']:
                self.main_globals['enemy_list'].remove(self)

    enemy = Enemy(main_globals, main_globals['spawn_x'], main_globals['spawn_y'], main_globals['enemy_type'])

    main_globals['enemy'] = enemy
    main_globals['Enemy'] = Enemy

    print("enemy file loaded")
