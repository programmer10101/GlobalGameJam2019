
import constants
import random
from bomb import Bomb
from enemy import Enemy
from path import Path

SCREEN_W, SCREEN_H = constants.SCREEN_SIZE

# kind, sprite
enemy_kinds = (
    (constants.CLASS_YELLOW, constants.ENEMY_YELLOW_IMG),
    (constants.CLASS_BLUE, constants.ENEMY_BLUE_IMG),
    (constants.CLASS_GREEN, constants.ENEMY_GREEN_IMG),
    (constants.CLASS_RED, constants.ENEMY_RED_IMG)
)

enemy_sizes = (
    (128, 128),
    (100, 100),
    (90, 90),
    (80, 90)
)


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
        bombs.append(b)
    return bombs

class World(object):
    def __init__(self, screen_width=SCREEN_W, screen_height=SCREEN_H):
        self.size = screen_width, screen_height
        self.paths = [Path()]    # Paths enemies follow
        self.paths[0].read_from_file(constants.ENEMY_PATH)
        self.enemies = create_enemies(140)
        self.bombs = create_bombs()

    def __str__(self):
        return "World size:{}".format(self.size)

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



if __name__ == '__main__':
    world = World()
    print(world)
