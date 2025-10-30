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
            self.speed = 0.9
            self.type = type
            self.active = False
            self.cooldown = 1500 # ms, 1 1/2 seconds
            self.damage = 10 # why not right?
            self.last_attack_time = 0
            self.images = [
                pygame.transform.scale2x(main_globals['enemy_test_0'].convert_alpha()),
                pygame.transform.scale2x(main_globals['enemy_test_1'].convert_alpha())
            ]
            self.rect = self.images[0].get_rect()
            self.stagger_duration = 500  # ms, 1/2 seconds
            self.stagger_end_time = 0    # when stagger ends
            self.is_staggered = False

        def damaged(self, damage):
            self.health -= damage
            if self.health <= 0:
                self.alive = False
                self.die()
            else:
                self.is_staggered = True
                self.stagger_end_time = pygame.time.get_ticks() + self.stagger_duration

        def detect(self, player):
            distance = math.dist((self.x, self.y), (player.x, player.y))
            if distance <= 150:
                self.active = True
            return self.active
        
        def attack(self, player):
            now = pygame.time.get_ticks()
            distance = math.dist((self.x, self.y), (player.x, player.y))
            if distance <= 40 and now - self.last_attack_time >= self.cooldown:
                player.damaged(self.damage)
                self.last_attack_time = now

        def move(self, player): # ookay?
            if not self.active or not self.alive:
                return
            else:
                if self.is_staggered:
                    # check if stagger has ended
                    if pygame.time.get_ticks() >= self.stagger_end_time:
                        self.is_staggered = False
                    else:
                        return
                target_x = player.x
                target_y = player.y

                dx = target_x - self.x
                dy = target_y - self.y

                # normalise some shit apparently this is important
                distance = math.hypot(dx, dy)
                if distance == 25:
                    return  # bro is already here

                dx /= distance
                dy /= distance

                # move
                self.x += dx * self.speed
                self.y += dy * self.speed

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
