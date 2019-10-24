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
        logger.debug('Wywołana metoda __init__ z klasy Sheep')
        self.x = random.randint(-init_pos_limit * 100, init_pos_limit * 100) / 100
        self.y = random.randint(-init_pos_limit * 100, init_pos_limit * 100) / 100
        self.is_alive = True
        logger.info('Ustawienie pozycji owcy oraz flagi is_alive: ' + self.__repr__())
        logger.debug('Wyjście z metody __init__ z klasy Sheep')

    def move_sheep(self):
        logger.debug('Wywołana metoda move_sheep z argumentem typu Sheep - ' + self.__repr__())
        logger.info('Wylosowanie kierunku, w którym pójdzie owca')
        direction = random.randint(1, 4)
        if direction == 1:
            logger.info('Kierunek: do góry, początkowa pozycja ' + self.__repr__())
            self.y += sheep_move_dist
            logger.info('Kierunek: do góry, końcowa pozycja ' + self.__repr__())
        elif direction == 2:
            logger.info('Kierunek: w prawo, początkowa pozycja ' + self.__repr__())
            self.x += sheep_move_dist
            logger.info('Kierunek: w prawo, końcowa pozycja ' + self.__repr__())
        elif direction == 3:
            logger.info('Kierunek: w dół, początkowa pozycja ' + self.__repr__())
            self.y -= sheep_move_dist
            logger.info('Kierunek: w dół, końcowa pozycja ' + self.__repr__())
        else:
            logger.info('Kierunek: w lewo, początkowa pozycja ' + self.__repr__())
            self.x -= sheep_move_dist
            logger.info('Kierunek: w lewo, końcowa pozycja ' + self.__repr__())
        logger.debug('Wyjście z metody move_sheep')

    def kill_sheep(self):
        logger.debug('Wywołana metoda kill_sheep z klasy Sheep na obiekcie ' + self.__repr__())
        self.is_alive = False
        logger.debug('Wyjście z metody kill_sheep, końcowy stan obiektu: ' + self.__repr__())

    def __repr__(self):
        return "Sheep[x=" + str(self.x) + ", y=" + str(self.y) + ", is_alive=" + str(self.is_alive) + "]"


class Wolf:
    def __init__(self):
        logger.debug('Wywołana metoda __init__ z klasy Wolf')
        self.x = 0.0
        self.y = 0.0
        logger.debug('Wyjście z metody __init__, utworzono obiekt ' + self.__repr__())

    def move_wolf(self, sheep: Sheep):
        logger.debug('Wywołana metoda move_wolf z klasy Wolf z parametrami: self=' + self.__repr__() + ', sheep=' +
                     sheep.__repr__())
        vector = (sheep.x - self.x, sheep.y - self.y)
        tmp_x = vector[0] * wolf_move_dist / calc_distance(self, sheep)
        tmp_y = vector[1] * wolf_move_dist / calc_distance(self, sheep)
        logger.info('Ustawienie pozycji wilka: początkowa pozycja: ' + self.__repr__())
        self.x += tmp_x
        self.y += tmp_y
        logger.info('Ustawienie pozycji wilka: końcowa pozycja: ' + self.__repr__())
        logger.debug('Wyjście z metody move_wolf z klasy Wolf')

    def __repr__(self):
        return "Wolf[x=" + str(self.x) + ", y=" + str(self.y) + "]"


# zmienne globalne
nr_of_rounds = 50
nr_of_sheeps = 15
init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0
sheeps = []
wolf: Wolf
data_json = []
data_csv = []
directory = "."
wait_flag = True
logging_type = 0
logging_choices = {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}
logger: logging
logging.basicConfig(filename='chase.log', filemode='w', format='%(name)s:%(levelname)s:%(message)s')


def init_sheeps():
    for i in range(nr_of_sheeps):
        sheeps.append(Sheep())


def init_wolf():
    global wolf
    wolf = Wolf()


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


def add_to_csv(round_: int):
    data_csv.append([round_, alive_sheeps()])


def save_csv_to_file(file_name: str):
    logger.debug('Wywołana metoda save_csv_to_file z parametrem file_name=' + file_name)
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
        logger.debug('Wyjście z metody save_csv_to_file')
        return
    else:
        logger.error('Błąd zamknięcia pliku .csv do pliku!')
        raise Exception("Błąd zapisu")


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


def close_logger():
    logger.debug('Wywołana metoda close_logger')
    logger.info('Zamykanie loggera metodą logging.shutdown()')
    logging.shutdown()


def add_args_to_parser(parser_):
    parser_.add_argument('-c', '--config', metavar='FILE',
                         help='dodatkowy plik konfiguracyjny, gdzie FILE - nazwa pliku')
    parser_.add_argument('-d', '--dir', metavar='DIR',
                         help='podkatalog, w którym mają zostać zapisane pliki pos.json, alive.csv oraz - opcjonalnie '
                              '- chase.log, gdzie DIR - nazwa podkatalogu')
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


def handle_parser_args():
    parser = argparse.ArgumentParser(description='Symulacja wilka i owiec')
    add_args_to_parser(parser)
    args: dict = vars(parser.parse_args())

    if args['config'] is not None:
        load_from_ini_file(args['config'])

    if args['dir'] is not None:
        global directory
        directory = args['dir']

    global logger
    logger = logging.getLogger(__name__)
    if args['log'] is not None:
        global logging_type
        logging_type = logging_choices[args['log']]
        logger.setLevel(logging_type)

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
    init_wolf()
    print_sheeps()
    round_ = 0
    while round_ != nr_of_rounds and alive_sheeps() > 0:
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
        print("Tura", round_, "/", nr_of_rounds - 1, " Pozycja wilka: (", str(wolf.x), ",",
              str(wolf.y), ")", " Ilość żywych owiec: ", alive_sheeps(), "\n")
        if wait_flag:
            input("Press Enter to continue...")
        add_to_json_list(round_)
        add_to_csv(round_)
        #  licznik tury
        round_ += 1
    # za pętlą
    save_json_to_file('pos.json')
    save_csv_to_file('alive.csv')

    print_sheeps(only_alive=True)
    close_logger()  # bez tego nie działa usuwanie pliku


if __name__ == "__main__":
    handle_parser_args()
    simulate()
    # do przemyślenia tutaj to całe
    if logging_type == 0:
        try:
            os.remove("chase.log")
        except PermissionError:
            print("Nie udało się usunąć pliku chase.log!")
            logger.critical("Nie udało się usunąć pliku chase.log")
