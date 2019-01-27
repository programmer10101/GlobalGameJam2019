
import constants
import math
import pygame
import pygame.gfxdraw

def draw_sector(screen, cx, cy, r, color, start, end, n_pts=50):
    pts = [(cx,cy)]
    if abs(end - start) > 360:
        return
    delta = (end - start) / n_pts
    if delta < .001: delta = .01
    angle = start
    while angle < end:
        x = cx + int(r*math.cos(angle*math.pi/180))
        y = cy + int(r*math.sin(angle*math.pi/180))
        pts.append((x,y))
        angle += delta
    pts.append((cx, cy))
    if len(pts) > 2:
        pygame.draw.polygon(screen, (200,200,200), pts)


class Graphics(object):
    def __init__(self, world):
        self.init(world)

    def init(self, world):
        self.world = world
        self.screen = pygame.display.set_mode(self.world.get_screen_size(), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        pygame.display.set_caption("Time Bomb Home Defense")
        self.background = pygame.image.load(constants.BACKGROUND_IMG).convert()
        self.background = pygame.transform.scale(self.background, self.world.get_screen_size())
        self.font = pygame.font.Font(None, 20)
        self.enemy_sprites = {}
        self.enemy_sprites[constants.ENEMY_YELLOW_IMG] = {}
        self.enemy_sprites[constants.ENEMY_BLUE_IMG] = {}
        self.enemy_sprites[constants.ENEMY_GREEN_IMG] = {}
        self.enemy_sprites[constants.ENEMY_RED_IMG] = {}

        enemy_yellow = pygame.image.load(constants.ENEMY_YELLOW_IMG).convert_alpha()
        enemy_blue =  pygame.image.load(constants.ENEMY_BLUE_IMG).convert_alpha()
        enemy_green = pygame.image.load(constants.ENEMY_GREEN_IMG).convert_alpha()
        enemy_red = pygame.image.load(constants.ENEMY_RED_IMG).convert_alpha()

        self.enemy_sprites[constants.ENEMY_YELLOW_IMG][constants.LEFT] = enemy_yellow
        self.enemy_sprites[constants.ENEMY_BLUE_IMG][constants.LEFT] = enemy_blue
        self.enemy_sprites[constants.ENEMY_GREEN_IMG][constants.LEFT] = enemy_green
        self.enemy_sprites[constants.ENEMY_RED_IMG][constants.LEFT] = enemy_red

        self.enemy_sprites[constants.ENEMY_YELLOW_IMG][constants.RIGHT] = pygame.transform.flip(enemy_yellow, True, False)
        self.enemy_sprites[constants.ENEMY_BLUE_IMG][constants.RIGHT] = pygame.transform.flip(enemy_blue, True, False)
        self.enemy_sprites[constants.ENEMY_GREEN_IMG][constants.RIGHT] = pygame.transform.flip(enemy_green, True, False)
        self.enemy_sprites[constants.ENEMY_RED_IMG][constants.RIGHT] = pygame.transform.flip(enemy_red, True, False)

        self.bomb_explosion = pygame.image.load(constants.BOMB_BLAST).convert_alpha()
        self.bomb_sprites = [[] for x in range(len(constants.BOMBS))]
        self.bomb_frag_tops = [[] for x in range(len(constants.BOMB_FRAG_TOPS))]
        self.bomb_frag_bottoms = [[] for x in range(len(constants.BOMB_FRAG_BOTTOMS))]
        self.bomb_frag_lefts = [[] for x in range(len(constants.BOMB_FRAG_LEFTS))]
        self.bomb_frag_rights = [[] for x in range(len(constants.BOMB_FRAG_RIGHTS))]

        for i, filename in enumerate(constants.BOMBS):
            self.bomb_sprites[i] = pygame.image.load(filename).convert_alpha()

        for i, filename in enumerate(constants.BOMB_FRAG_TOPS):
            self.bomb_frag_tops[i] = pygame.image.load(filename).convert_alpha()

        for i, filename in enumerate(constants.BOMB_FRAG_BOTTOMS):
            self.bomb_frag_bottoms[i] = pygame.image.load(filename).convert_alpha()

        for i, filename in enumerate(constants.BOMB_FRAG_LEFTS):
            self.bomb_frag_lefts[i] = pygame.image.load(filename).convert_alpha()

        for i, filename in enumerate(constants.BOMB_FRAG_RIGHTS):
            self.bomb_frag_rights[i]   = pygame.image.load(filename).convert_alpha()



    def set_screen(self, screen):
        self.screen = screen

    def get_enemy_surface(self, sprite_name, direction):
        """ Returned cached enemy sprite surface or None """
        if sprite_name and direction:
            return self.enemy_sprites[sprite_name][direction]
        return None

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_path(self, path, color=(0, 222, 0)):
        points = path.get_points()
        step_count = path.get_step_count()
        # print("printing", step_count, "steps")
        for i in range(1, step_count + 1):
            ptA, ptB = path.get_step(i)
            # print("   pts:",ptA,ptB)
            pygame.draw.line(self.screen, color, ptA, ptB)

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, constants.BROWN)
        self.screen.blit(text_surface, (x, y))

    def draw_enemy(self, enemy):
        img = self.get_enemy_surface(enemy.sprite, enemy.direction)
        if img and enemy.location:
            loc = [int(val) for val in enemy.location]
            scaled_img = pygame.transform.scale(img, enemy.size)
            loc[1] -= enemy.size[1] // 2  # move sprite up half its height
            self.screen.blit(scaled_img, loc)

    def draw_enemy_timeline(self, left, top, width, height, bgcolor=constants.BLACK):
        """ Represent enemies along straight line to anticipate their entry to screen and path """
        pygame.draw.rect(self.screen, bgcolor, (left, top, width, height), 2)   # border
        start_left = int(width * .1) + left
        pygame.draw.line(self.screen, constants.ORANGE, (start_left, top+2), (start_left, top + height -2))
        cy = top + height // 2
        r = max(height // 4, 2)
        for e in self.world.get_enemies():
            a = (e.distance_from_path + 10) / 100.0
            if a > 0 and a < 1:
                cx = int(a * width) + left
                pygame.draw.circle(self.screen, e.color, (cx, cy), r)

    def draw_enemies(self):
        enemies = self.world.get_enemies()
        for enemy in enemies:
            self.draw_enemy(enemy)

    def draw_bomb_queued_slots(self, color=constants.ORANGE):
        bomb_queued_areas = [slot.area for slot in self.world.bomb_queued_slots]
        for rect in bomb_queued_areas:
            pygame.draw.rect(self.screen, color, rect)

    def draw_bomb_armed_slots(self, color=constants.GREEN):
        bomb_armed_areas = [slot.area for slot in self.world.bomb_armed_slots]
        for rect in bomb_armed_areas:
            pygame.draw.rect(self.screen, color, rect)

    def draw_bomb(self, bomb, location, size=(64, 64)):
        img = self.bomb_sprites[bomb.kind]
        img = pygame.transform.scale(img, size)
        self.screen.blit(img, location)

    def draw_queued_bombs(self):
        for slot in self.world.bomb_queued_slots:
            if not slot.bomb is None:
                x, y, w, h = slot.area
                self.draw_bomb(slot.bomb, (x, y), constants.BOMB_QUEUE_SIZE)

    def draw_armed_bombs(self):
        for slot in self.world.bomb_armed_slots:
            if not slot.bomb is None:
                x, y, w, h = slot.area
                self.draw_bomb(slot.bomb, (x, y), constants.BOMB_ARMED_SIZE)


    def update(self):
        pygame.display.update()
