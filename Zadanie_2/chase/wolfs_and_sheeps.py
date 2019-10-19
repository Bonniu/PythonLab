import random
from math import sqrt
import json


class Sheep:
    def __init__(self):
        self.x = random.randint(-init_pos_limit * 100, init_pos_limit * 100) / 100
        self.y = random.randint(-init_pos_limit * 100, init_pos_limit * 100) / 100
        self.is_alive = True

    def move_sheep(self):
        direction = random.randint(1, 4)
        if direction == 1:
            self.y += sheep_move_dist
        elif direction == 2:
            self.x += sheep_move_dist
        elif direction == 3:
            self.y -= sheep_move_dist
        else:
            self.x -= sheep_move_dist

    def kill_sheep(self):
        self.is_alive = False

    def __repr__(self):
        return "Sheep[x=" + str(self.x) + ", y=" + str(self.y) + ", is_alive=" + str(self.is_alive) + "]"


class Wolf:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def move_wolf(self, sheep: Sheep):
        vector = (sheep.x - self.x, sheep.y - self.y)
        self.x += vector[0] * wolf_move_dist / calc_distance(self, sheep)
        self.y += vector[1] * wolf_move_dist / calc_distance(self, sheep)

    def __repr__(self):
        return "Wolf[x=" + str(self.x) + ", y=" + str(self.y) + "]"


nr_of_rounds = 50
nr_of_sheeps = 15
init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0
sheeps: list = []
wolf = Wolf()
data_json = []


def init_sheeps():
    for i in range(nr_of_sheeps):
        sheeps.append(Sheep())


def calc_distance(w: Wolf, s: Sheep):
    return sqrt((w.x - s.x) ** 2 + (w.y - s.y) ** 2)


def print_sheeps(only_alive: bool):
    for i in range(len(sheeps)):
        if only_alive:
            if sheeps[i].is_alive:
                print(i, " - ", sheeps[i])
        else:
            print(i, " - ", sheeps[i])


def alive_sheeps() -> int:
    counter = 0
    for i in sheeps:
        if i.is_alive:
            counter += 1
    return counter


def add_to_json_list(round_nr: int):
    _ = []
    for i in sheeps:
        if i.is_alive:
            _.append((i.x, i.y))
        else:
            _.append(None)
    data_json.append({
        'round_no': round_nr,
        'wolf_pos': (wolf.x, wolf.y),
        'sheep_pos': _
    })


def save_json_to_file(file_name: str):
    with open(file_name, 'w') as outfile:
        json.dump(data_json, outfile, indent=4)


def simulate():
    init_sheeps()
    print_sheeps(only_alive=False)
    round = 0
    while round != nr_of_rounds and alive_sheeps() > 0:
        #  ruch owiec
        for i in sheeps:
            i.move_sheep()

        #  ruch wilka
        closest_sheep_index = 0
        closest_sheep_dist = 1000000

        for i in range(len(sheeps)):
            if calc_distance(wolf, sheeps[i]) < closest_sheep_dist and sheeps[i].is_alive:
                closest_sheep_index = i
                closest_sheep_dist = calc_distance(wolf, sheeps[i])

        #  zjedzenie lub ruch wilka
        if closest_sheep_dist < wolf_move_dist:
            sheeps[closest_sheep_index].kill_sheep()
            print("Zjedzona owca nr", closest_sheep_index)
        else:
            wolf.move_wolf(sheeps[closest_sheep_index])

        #  informacje o turze
        print("Tura", round, "/", nr_of_rounds - 1, " Pozycja wilka: (", str(wolf.x), ",",
              str(wolf.y), ")", " Ilość żywych owiec: ", alive_sheeps(), "\n")

        #  dodanie do pliku json
        add_to_json_list(round)
        #  licznik tury
        round += 1
        # za pętlą
    save_json_to_file('pos.json')
    print_sheeps(only_alive=True)


if __name__ == "__main__":
    simulate()
