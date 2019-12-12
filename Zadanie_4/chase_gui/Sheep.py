import random

import Simulate


class Sheep:
    def __init__(self):
        self.x = random.randint(-Simulate.init_pos_limit * 100, Simulate.init_pos_limit * 100) / 100
        self.y = random.randint(-Simulate.init_pos_limit * 100, Simulate.init_pos_limit * 100) / 100
        self.is_alive = True

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def move_sheep(self):
        direction = random.randint(1, 4)
        if direction == 1:
            self.y += Simulate.sheep_move_dist
        elif direction == 2:
            self.x += Simulate.sheep_move_dist
        elif direction == 3:
            self.y -= Simulate.sheep_move_dist
        else:
            self.x -= Simulate.sheep_move_dist
        self.x = round(self.x, 3)
        self.y = round(self.y, 3)

    def kill_sheep(self):
        self.is_alive = False

    def __repr__(self):
        return "Sheep[x=" + str(self.x) + ", y=" + str(self.y) + ", is_alive=" + str(self.is_alive) + "]"
