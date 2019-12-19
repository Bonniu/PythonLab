import Simulate
from Sheep import Sheep


class Wolf:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def move_wolf(self, sheep: Sheep):
        vector = (sheep.x - self.x, sheep.y - self.y)
        tmp_x = vector[0] * Simulate.wolf_move_dist / Simulate.calc_distance(self, sheep)
        tmp_y = vector[1] * Simulate.wolf_move_dist / Simulate.calc_distance(self, sheep)
        self.x += tmp_x
        self.y += tmp_y
        self.x = round(self.x, 3)
        self.y = round(self.y, 3)

    def __repr__(self):
        return "Wolf[x=" + str(self.x) + ", y=" + str(self.y) + "]"
