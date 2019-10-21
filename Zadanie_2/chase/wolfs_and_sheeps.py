import random
from math import sqrt
import json
import csv
import argparse
import os
import logging
import configparser


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
        tmp_x = vector[0] * wolf_move_dist / calc_distance(self, sheep)
        tmp_y = vector[1] * wolf_move_dist / calc_distance(self, sheep)
        self.x += tmp_x
        self.y += tmp_y
        # print("Wilk ruszyl sie o :", sqrt(tmp_x ** 2 + tmp_y ** 2))

    def __repr__(self):
        return "Wolf[x=" + str(self.x) + ", y=" + str(self.y) + "]"


nr_of_rounds = 50
nr_of_sheeps = 15
init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0
sheeps = []
wolf = Wolf()
data_json = []
data_csv = []
directory = "."
wait_flag = True
logging_type = 0
logging_choices = {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}


def init_sheeps():
    for i in range(nr_of_sheeps):
        sheeps.append(Sheep())


def calc_distance(w: Wolf, s: Sheep):
    return sqrt((w.x - s.x) ** 2 + (w.y - s.y) ** 2)


def print_sheeps(only_alive: bool = False):
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
    if directory != ".":
        try:
            os.mkdir(directory)
        except OSError:
            print("Creation of the directory %s failed" % directory)

    with open(str(directory + "\\" + file_name), 'w') as outfile:
        json.dump(data_json, outfile, indent=4)


def add_to_csv(_round: int):
    data_csv.append([_round, alive_sheeps()])


def save_csv_to_file(file_name: str):
    logging.debug('Wywołana metoda save_csv_to_file z parametrem file_name=' + file_name)
    if directory != ".":
        try:
            os.mkdir(directory)
        except OSError:
            print("Creation of the directory %s failed" % directory)
    with open(str(directory + "\\" + file_name), 'w', newline='') as csv_file:
        print(data_csv)
        csv_file.write("sep=,\n")
        csv_writer = csv.writer(csv_file, delimiter=',')
        for i in data_csv:
            csv_writer.writerow([i[0], i[1]])
    if csv_file.closed:
        return
    else:
        raise Exception("Error while saving")


def load_from_ini_file(file_name: str):
    config = configparser.ConfigParser()
    config.read(file_name)
    if float(config['Terrain']['InitPosLimit']) <= 0:
        raise Exception("InitPosLimit musi być liczbą większą od 0")
    else:
        global init_pos_limit
        init_pos_limit = float(config['Terrain']['InitPosLimit'])

    if float(config['Movement']['SheepMoveDist']) <= 0:
        raise Exception("SheepMoveDist musi być liczbą większą od 0")
    else:
        global sheep_move_dist
        sheep_move_dist = float(config['Movement']['SheepMoveDist'])

    if float(config['Movement']['WolfMoveDist']) <= 0:
        raise Exception("WolfMoveDist musi być liczbą większą od 0")
    else:
        global wolf_move_dist
        wolf_move_dist = float(config['Movement']['WolfMoveDist'])


def add_args_to_parser(_parser):
    _parser.add_argument('-c', '--config', metavar='FILE',
                         help='dodatkowy plik konfiguracyjny, gdzie FILE - nazwa pliku')
    _parser.add_argument('-d', '--dir', metavar='DIR',
                         help='podkatalog, w którym mają zostać zapisane pliki pos.json, alive.csv oraz - opcjonalnie '
                              '- chase.log, gdzie DIR - nazwa podkatalogu')
    _parser.add_argument('-l', '--log', choices=logging_choices.keys(), metavar='LEVEL',
                         help='zapis zdarzeń do dziennika, gdzie '
                              'LEVEL - poziom zdarzeń  (DEBUG, INFO, WARNING, ERROR lub CRITICAL)')
    _parser.add_argument('-r', '--rounds', metavar='NUM', type=int,
                         help='liczba tur')
    _parser.add_argument('-s', '--sheep', metavar='NUM', type=int,
                         help='liczba owiec')
    _parser.add_argument('-w', '--wait', action='store_true',
                         help='flaga oczekiwania na naciśnięcie klawisza po wyświetlaniu podstawowych '
                              'informacji o stanie symulacji na zakończenie każdej tury.')


def handle_parser_args():
    parser = argparse.ArgumentParser(description='Symulacja wilka i owiec')
    add_args_to_parser(parser)
    args: dict = vars(parser.parse_args())

    if args['config'] is not None:
        load_from_ini_file(args['config'])

    if args['dir'] is not None:
        global directory
        directory = args['dir']

    if args['log'] is not None:
        global logging_type
        logging_type = logging_choices[args['log']]
        logging.basicConfig(filename='chase.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                            level=logging_type)

    if args['rounds'] is not None:
        if args['rounds'] <= 0:
            raise Exception('Liczba tur musi być większa od 0')
        global nr_of_rounds
        nr_of_rounds = args['rounds']

    if args['sheep'] is not None:
        if args['sheep'] <= 0:
            raise Exception('Liczba owiec musi być większa od 0')
        global nr_of_sheeps
        nr_of_sheeps = args['sheep']

    if args['wait'] is not None:
        global wait_flag
        wait_flag = args['wait']


def simulate():
    init_sheeps()
    print_sheeps()
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
        if wait_flag:
            input("Press Enter to continue...")
        add_to_json_list(round)
        add_to_csv(round)
        #  licznik tury
        round += 1
    # za pętlą
    save_json_to_file('pos.json')
    save_csv_to_file('alive.csv')

    print_sheeps(only_alive=True)


if __name__ == "__main__":
    handle_parser_args()
    simulate()
