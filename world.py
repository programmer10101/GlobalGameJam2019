
import constants
import pygame
import random
from bomb import Bomb
from enemy import Enemy
from path import Path

SCREEN_W, SCREEN_H = constants.SCREEN_SIZE

# kind, sprite
enemy_kinds = (
    (constants.CLASS_RED, constants.ENEMY_RED_IMG),
    (constants.CLASS_GREEN, constants.ENEMY_GREEN_IMG),
    (constants.CLASS_BLUE, constants.ENEMY_BLUE_IMG),
    (constants.CLASS_YELLOW, constants.ENEMY_YELLOW_IMG)
)

enemy_sizes = (
    (128, 128),
    (100, 100),
    (90, 90),
    (80, 90)
)

# bomb_queue_size = (84, 84)
# bomb_armed_size = (64, 64)


def create_enemies(n=20):
    enemies = []
    for i in range(n):
        e = Enemy()
        e.distance_from_path = 3 + (i * 122)
        # x = 80 + random.randint(0, 600)
        # y = 100 + random.randint(5, 500)
        # e.location = (x,y)
        if random.randint(0, 100) < 50:
            e.direction = constants.LEFT
        else:
            e.direction = constants.RIGHT
        e.speed = random.randint(15, 245)
        e.kind, e.sprite = random.choice(enemy_kinds)
        e.color = constants.CLASS_COLORS[e.kind]
        e.size = random.choice(enemy_sizes)
        enemies.append(e)
    return enemies

def create_bombs(n=40):
    bombs = []
    for i in range(n):
        b = Bomb()
        b.kind, _ = random.choice(enemy_kinds)
        b.color = constants.CLASS_COLORS[b.kind]
        b.max_time = constants.BOMB_MAX_TIMES[b.kind]
        b.time_to_explosion = max(random.randint(25, 100) / 100.0 * b.max_time, 2.0)
        bombs.append(b)
    return bombs

class BombSlot(object):
    def __init__(self):
        self.area = None
        self.bomb = None

class World(object):
    def __init__(self, screen_width=SCREEN_W, screen_height=SCREEN_H):
        self.size = screen_width, screen_height
        self.paths = [Path()]    # Paths enemies follow
        self.paths[0].read_from_file(constants.ENEMY_PATH)
        self.enemies = create_enemies(140)
        self.bombs = create_bombs()
        self.bomb_queued_slots = []   # location of next bombs to come preview
        self.bomb_armed_slots = []    # locations of bombs to drag-n-drop on path

        self.init_bomb_queued_slots()
        self.init_bomb_armed_slots()

    def __str__(self):
        return "World size:{}".format(self.size)

    def init_bomb_queued_slots(self):
        self.bomb_queued_slots = []
        x = 30
        w, h = constants.BOMB_QUEUE_SIZE
        bombs = create_bombs(constants.QUEUED_BOMB_SLOTS_COUNT)
        for i in range(constants.QUEUED_BOMB_SLOTS_COUNT):
            y = 280 + (100 * i)
            area = pygame.Rect(x, y, w, h)
            slot = BombSlot()
            slot.area = area
            slot.bomb = bombs[i]
            self.bomb_queued_slots.append(slot)

    def init_bomb_armed_slots(self):
        self.bomb_armed_slots = []
        y = 600
        w, h = constants.BOMB_ARMED_SIZE
        bombs = create_bombs(constants.ARMED_BOMB_SLOTS_COUNT)
        for i in range(constants.ARMED_BOMB_SLOTS_COUNT):
            x = 300 + (150 * i)
            area = pygame.Rect(x, y, w, h)
            slot = BombSlot()
            slot.area = area
            slot.bomb = bombs[i]
            self.bomb_armed_slots.append(slot)

    def print_enemies(self):
        i = 0
        for e in self.enemies:
            i += 1
            print("enemy",i, " at ",e.location)

    def get_screen_size(self):
        return self.size

    def get_paths(self):
        return self.paths

    def get_path(self, index):
        if index >= 0 and index < len(self.paths):
            return self.paths[index]
        else:
            return Path()

    def get_enemies(self):
        return self.enemies

    def get_bombs(self):
        return self.bombs

    def move_enemies(self, timedelta_millis):
        timedelta_secs = timedelta_millis / 1000.0
        for enemy in self.enemies:
            self.move_enemy(enemy, timedelta_secs)

    def move_enemy(self, enemy, timedelta_secs):
        d = enemy.speed * timedelta_secs
        enemy.distance_from_path -= d
        path = self.get_path(enemy.path_index)
        if enemy.distance_from_path <= 0:  # enemy reached path
            abs_dist = abs(enemy.distance_from_path)
            if abs_dist > path.get_total_length():   # enemy reached your base
                self.enemies.remove(enemy)
                # do player damage
            else:   # enemy on path
                if not enemy.location:  # just reached path
                    enemy.current_step_distance = 0
                    enemy.current_step = 1
                    enemy.current_step, enemy.current_step_distance = path.get_position(enemy.current_step, enemy.current_step_distance, abs_dist)
                    enemy.location = path.get_location(enemy.current_step, enemy.current_step_distance)
                else:
                    enemy.current_step, enemy.current_step_distance = path.get_position(enemy.current_step, enemy.current_step_distance, d)
                    enemy.location = path.get_location(enemy.current_step, enemy.current_step_distance)

    def update_bomb_slots(self):
        """ Make sure slots are full.
            Create more bombs if needed.
        """
        # If get low on bombs, create more
        if len(self.bombs) < 10:
            self.bombs.extend(self.create_bombs(20))

        # Check for any empty slots in armed area. Fill empty slot with next from queue.
        is_armed_slot_empty = False
        empty_slot_index = 0
        for index, slot in enumerate(self.bomb_armed_slots):
            if slot.bomb is None:
                is_armed_slot_empty = True
                empty_slot_index = index
                break
        if is_armed_slot_empty:
            self.bomb_armed_slots[empty_slot_index].bomb = self.bomb_queued_slots[constants.QUEUED_BOMB_SLOTS_COUNT - 1].bomb
            self.bomb_queued_slots[constants.QUEUED_BOMB_SLOTS_COUNT - 1].bomb = None

        # If last queued slot is empty, shift bombs and add another
        if self.bomb_queued_slots[constants.QUEUED_BOMB_SLOTS_COUNT - 1].bomb is None:
            for i in range(constants.QUEUED_BOMB_SLOTS_COUNT - 2, -1, -1):
                self.bomb_queued_slots[i+1].bomb = self.bomb_queued_slots[i].bomb
            self.bomb_queued_slots[0].bomb = self.bombs.pop(0)





if __name__ == '__main__':
    world = World()
    print(world)
