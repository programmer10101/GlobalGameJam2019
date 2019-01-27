import constants
import random

class Enemy(object):
    def __init__(self):
        self.sprite = constants.ENEMY_RED_IMG
        self.size = (128, 128)
        self.distance_from_path = 20
        self.speed = 20    # pixels per second
        self.location = None
        self.direction = constants.LEFT
        self.path_index = 0
        self.current_step = 0
        self.current_step_distance = 0
        self.kind = constants.CLASS_YELLOW  # enemy type
        self.color = constants.CLASS_COLORS[self.kind]
        self.max_health = 100
        self.health = self.max_health
