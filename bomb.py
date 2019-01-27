
import constants

class Bomb(object):
    # Bomb states
    PLANNED = 5
    QUEUED = 10
    ARMED = 20
    PLACED = 30
    EXPLODED = 40

    def __init__(self):
        self.state = Bomb.PLANNED
        self.kind = constants.CLASS_RED
        self.color = constants.CLASS_COLORS[self.kind]
        self.location = None
        self.max_time = constants.BOMB_MAX_TIMES[self.kind]
        self.time_to_explosion = 3.5
        self.blast_radius = constants.BOMB_BLAST_RADII[self.kind]
