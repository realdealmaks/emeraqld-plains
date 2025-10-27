# for bobbers
import pygame

def enemy(main_globals):
    screen = main_globals['screen']

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
            self.img0 = pygame.transform.scale2x(main_globals['enemy_test_0'].convert_alpha())
            self.img1 = pygame.transform.scale2x(main_globals['enemy_test_1'].convert_alpha())
            self.rect = self.img0.get_rect()

        def spawn(self):
            pass

        def damaged(self, damage):
            self.health -= damage
            if self.health <= 0:
                self.alive = False

        def move(self):
            if self.alive:
                pass

        def draw(self, type):
            if self.alive:
                match type:
                    case 0:
                        screen.blit(self.img0, (self.x - main_globals['camera_x'], self.y - main_globals['camera_y']))
                        print(f"drew enemy type {type} at {self.x, self.y}")
                    case 1:
                        screen.blit(self.img1, (self.x - main_globals['camera_x'], self.y - main_globals['camera_y']))
                        print(f"drew enemy type {type} at {self.x, self.y}")
            elif not self.alive:
                # death animation and break loop
                pass
        
        def die(self):
            pass # heh

    enemy = Enemy(main_globals, main_globals['spawn_x'], main_globals['spawn_y'], main_globals['enemy_type'])

    main_globals['enemy'] = enemy
    main_globals['Enemy'] = Enemy

    print("enemy file loaded")
