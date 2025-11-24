# for bobbers

import pygame, math, random

def enemy(main_globals):

    class Enemy():
        def __init__(self, main_globals, x, y, type):
            self.main_globals = main_globals
            self.x = x
            self.y = y
            self.size = main_globals['enemy_size']
            if type == 0:
                self.health = 40
            elif type == 1:
                self.health = 60
            self.alive = True
            self.speed = 0.9
            self.type = type
            self.active = False
            self.facing_left = False
            self.cooldown = 1500 # ms, 1 1/2 seconds
            self.damage = 10 # why not right?
            self.active_counter = 10 # frames until ! disappears
            self.last_attack_time = 0
            self.images = [
                pygame.transform.scale2x(main_globals['enemy_test_0'].convert_alpha()),
                pygame.transform.scale2x(main_globals['enemy_test_1'].convert_alpha())
            ]
            self.rect = self.images[0].get_rect()
            self.stagger_duration = 500 # ms, 1/2 seconds
            self.stagger_end_time = 0 # when stagger ends
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

            if not main_globals['is_on_active_tile'](self.main_globals, self.x, self.y):
                return False

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
                    return # bro is already here

                dx /= distance
                dy /= distance

                if distance > 40: # so he doesnt spam >:(
                    if dx < 0:
                        self.facing_left = True
                    else:
                        self.facing_left = False

                # move
                self.x += dx * self.speed
                self.y += dy * self.speed

            # collision with other naganous
            for other in self.main_globals['enemy_list']:
                if other is self:
                    continue

                dx2 = self.x - other.x
                dy2 = self.y - other.y
                dist = math.hypot(dx2, dy2)
                min_dist = self.size // 1.6 # space between them

                if dist < min_dist and dist > 0:
                    overlap = min_dist - dist
                    dx2 /= dist
                    dy2 /= dist

                    # push both
                    self.x += dx2 * overlap * 0.5
                    self.y += dy2 * overlap * 0.5
                    other.x -= dx2 * overlap * 0.5
                    other.y -= dy2 * overlap * 0.5

        def draw(self, type):
            if not main_globals['is_on_active_tile'](self.main_globals, self.x, self.y):
                return

            if self.alive:
                screen = main_globals['screen']
                img = self.images[type]
                if self.facing_left:
                    img = pygame.transform.flip(img, True, False)

                screen.blit(img, (self.x - main_globals['camera_x'], self.y - main_globals['camera_y']))
                self.rect.topleft = (self.x - main_globals['camera_x'], self.y - main_globals['camera_y'])

            elif not self.alive:
                # death animation and break loop
                # why the fuck does every enemy have a death animation
                pass

        def die(self):
            if self in self.main_globals['enemy_list']:
                self.main_globals['enemy_list'].remove(self)

                # give money to super jew
                ammount = 0
                if self.type == 0:
                    ammount = 10
                elif self.type == 1:
                    ammount = 15
                main_globals['give_money'](ammount)

                main_globals['enemies_killed'] += 1
                if main_globals['most_enemies_killed'] < main_globals['enemies_killed']:
                    main_globals['most_enemies_killed'] = main_globals['enemies_killed']
                    main_globals['save'](main_globals, most_enemies_killed=main_globals['most_enemies_killed'])

                if random.random() < 0.9: # *100 in %
                    main_globals['add_to_inventory'](main_globals, "crystal_fragments", 1)

    enemy = Enemy(main_globals, main_globals['spawn_x'], main_globals['spawn_y'], main_globals['enemy_type'])

    main_globals['enemy'] = enemy
    main_globals['Enemy'] = Enemy

    print("enemy, ", end = "")
