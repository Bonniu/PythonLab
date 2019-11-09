from math import sqrt
import json
import csv
import argparse
import os
import logging
import configparser
import Sheep
import Wolf

init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0
logger: logging
directory = "."
logging_type = 0
logging_choices = {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}
logging.basicConfig(filename=directory + "\\" + 'chase.log', filemode='w', format='%(name)s:%(levelname)s:%(message)s')


def calc_distance(w: Wolf.Wolf, s: Sheep.Sheep):
    return sqrt((w.x - s.x) ** 2 + (w.y - s.y) ** 2)


def close_logger():
    logger.debug('Wywołana metoda close_logger')
    logger.info('Zamykanie loggera metodą logging.shutdown()')
    logging.shutdown()


def load_from_ini_file(file_name: str):
    logger.debug('Wywołana metoda load_from_ini_file z parametrem file_name=' + file_name)
    config = configparser.ConfigParser()
    logger.info('Czytanie z pliku .ini')
    config.read(file_name)

    if float(config['Terrain']['InitPosLimit']) <= 0:
        logger.critical('InitPosLimit musi być liczbą większą od 0')
        raise Exception("InitPosLimit musi być liczbą większą od 0")
    else:
        global init_pos_limit
        init_pos_limit = float(config['Terrain']['InitPosLimit'])

    if float(config['Movement']['SheepMoveDist']) <= 0:
        logger.critical('SheepMoveDist musi być liczbą większą od 0')
        raise Exception("SheepMoveDist musi być liczbą większą od 0")
    else:
        global sheep_move_dist
        sheep_move_dist = float(config['Movement']['SheepMoveDist'])

    if float(config['Movement']['WolfMoveDist']) <= 0:
        logger.critical('WolfMoveDist musi być liczbą większą od 0')
        raise Exception("WolfMoveDist musi być liczbą większą od 0")
    else:
        global wolf_move_dist
        wolf_move_dist = float(config['Movement']['WolfMoveDist'])

    logging.debug('Wyjście z metody load_from_ini_file')


def add_args_to_parser(parser_):
    parser_.add_argument('-c', '--config', metavar='FILE',
                         help='dodatkowy plik konfiguracyjny, gdzie FILE - nazwa pliku')
    parser_.add_argument('-d', '--dir', metavar='DIR',
                         help='podkatalog, w którym mają zostać zapisane pliki pos.json, alive.csv oraz '
                              'opcjonalnie chase.log, gdzie DIR - nazwa podkatalogu')
    parser_.add_argument('-l', '--log', choices=logging_choices.keys(), metavar='LEVEL',
                         help='zapis zdarzeń do dziennika, gdzie '
                              'LEVEL - poziom zdarzeń  (DEBUG, INFO, WARNING, ERROR lub CRITICAL)')
    parser_.add_argument('-r', '--rounds', metavar='NUM', type=int,
                         help='liczba tur')
    parser_.add_argument('-s', '--sheep', metavar='NUM', type=int,
                         help='liczba owiec')
    parser_.add_argument('-w', '--wait', action='store_true',
                         help='flaga oczekiwania na naciśnięcie klawisza po wyświetlaniu podstawowych '
                              'informacji o stanie symulacji na zakończenie każdej tury.')


class Simulate:
    # zmienne globalne
    def __init__(self):
        self.nr_of_rounds = 50
        self.nr_of_sheeps = 15
        self.sheeps = []
        self.wolf: Wolf
        self.data_json = []
        self.data_csv = []
        self.wait_flag = True

    def init_sheeps(self):
        for i in range(self.nr_of_sheeps):
            self.sheeps.append(Sheep.Sheep())

    def init_wolf(self):
        self.wolf = Wolf.Wolf()

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

    def add_to_json_list(self, round_nr: int):
        _ = []
        for i in self.sheeps:
            if i.is_alive:
                _.append((i.x, i.y))
            else:
                _.append("None")
        self.data_json.append({
            'round_no': round_nr,
            'wolf_pos': (self.wolf.x, self.wolf.y),
            'sheep_pos': _
        })

    def save_json_to_file(self, file_name: str):
        if directory != ".":
            try:
                os.mkdir(directory)
            except OSError:
                pass
        with open(str(directory + "\\" + file_name), 'w') as outfile:
            json.dump(self.data_json, outfile, indent=4)

    def add_to_csv(self, round_: int):
        self.data_csv.append([round_, self.alive_sheeps()])

    def save_csv_to_file(self, file_name: str):
        logger.debug('Wywołana metoda save_csv_to_file z parametrem file_name=' + file_name)
        if directory != ".":
            try:
                os.mkdir(directory)
            except OSError:
                pass
        with open(str(directory + "\\" + file_name), 'w', newline='') as csv_file:
            csv_file.write("sep=,\n")
            csv_writer = csv.writer(csv_file, delimiter=',')
            for i in self.data_csv:
                csv_writer.writerow([i[0], i[1]])
        if csv_file.closed:
            logger.debug('Wyjście z metody save_csv_to_file')
            return
        else:
            logger.error('Błąd zamknięcia pliku .csv do pliku!')
            raise Exception("Błąd zapisu")

    def handle_parser_args(self):
        parser = argparse.ArgumentParser(description='Symulacja wilka i owiec')
        add_args_to_parser(parser)
        args: dict = vars(parser.parse_args())

        global logger
        logger = logging.getLogger(__name__)
        if args['log'] is not None:
            global logging_type
            logging_type = logging_choices[args['log']]
            logger.setLevel(logging_type)

        if args['config'] is not None:
            load_from_ini_file(args['config'])

        if args['dir'] is not None:
            global directory
            directory = args['dir']

        if args['rounds'] is not None:
            if args['rounds'] <= 0:
                raise Exception('Liczba tur musi być większa od 0')
            self.nr_of_rounds = args['rounds']

        if args['sheep'] is not None:
            if args['sheep'] <= 0:
                raise Exception('Liczba owiec musi być większa od 0')
            self.nr_of_sheeps = args['sheep']

        self.wait_flag = args['wait']

    def move_wolf(self):
        #  ruch wilka
        closest_sheep_index = 0
        closest_sheep_dist = 1000000

        for i in range(len(self.sheeps)):
            if calc_distance(self.wolf, self.sheeps[i]) < closest_sheep_dist and self.sheeps[i].is_alive:
                closest_sheep_index = i
                closest_sheep_dist = calc_distance(self.wolf, self.sheeps[i])

        #  zjedzenie lub ruch wilka
        if closest_sheep_dist < wolf_move_dist:
            self.sheeps[closest_sheep_index].kill_sheep()
            print("Zjedzona owca nr", closest_sheep_index)
            logger.info("Zjedzona owca nr " + str(closest_sheep_index))
        else:
            self.wolf.move_wolf(self.sheeps[closest_sheep_index])

    def move_sheeps(self):
        for i in self.sheeps:
            if i.is_alive:
                i.move_sheep()
