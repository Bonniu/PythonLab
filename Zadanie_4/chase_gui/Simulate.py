from math import sqrt
import Sheep
import Wolf

init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0
directory = "."


def calc_distance(w: Wolf.Wolf, s: Sheep.Sheep):
    return sqrt((w.x - s.x) ** 2 + (w.y - s.y) ** 2)


class Simulate:
    def __init__(self):
        self.nr_of_rounds = 50
        self.nr_of_sheeps = 15
        self.sheeps = []
        self.data_json = []
        self.data_csv = []
        self.wait_flag = False
        self.wolf = Wolf.Wolf()

    def init_sheeps(self):
        for i in range(self.nr_of_sheeps):
            self.sheeps.append(Sheep.Sheep())

    def print_sheeps(self, only_alive: bool = False):
        for i in range(len(self.sheeps)):
            if only_alive:
                if self.sheeps[i].is_alive:
                    print(i, " - ", self.sheeps[i])
            else:
                print(i, " - ", self.sheeps[i])

    def alive_sheeps(self) -> int:
        counter = 0
        for i in self.sheeps:
            if i.is_alive:
                counter += 1
        return counter

    def move_wolf(self):
        closest_sheep_index = 0
        closest_sheep_dist = 1000000
        # ustalenie która owca jest najbliżej i jej odległość
        for i in range(len(self.sheeps)):
            _ = calc_distance(self.wolf, self.sheeps[i])
            if _ < closest_sheep_dist and self.sheeps[i].is_alive:
                closest_sheep_index = i
                closest_sheep_dist = _
        #  zjedzenie lub ruch wilka
        if closest_sheep_dist < wolf_move_dist:
            self.sheeps[closest_sheep_index].kill_sheep()
            print("Zjedzona owca nr", closest_sheep_index)
        else:
            self.wolf.move_wolf(self.sheeps[closest_sheep_index])

    def move_sheeps(self):
        for i in self.sheeps:
            if i.is_alive:
                i.move_sheep()
