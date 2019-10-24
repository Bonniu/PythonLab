import random
from math import sqrt
import json
import csv
import argparse
import os
import logging
import configparser

logger: logging
init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0
directory = "."
logging_type = 0
logging_choices = {'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'CRITICAL': 50}
logging.basicConfig(filename='chase.log', filemode='w', format='%(name)s:%(levelname)s:%(message)s')


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


def calc_distance(w: Wolf, s: Sheep):
    return sqrt((w.x - s.x) ** 2 + (w.y - s.y) ** 2)


def close_logger():
    logger.debug('Wywołana metoda close_logger')
    logger.info('Zamykanie loggera metodą logging.shutdown()')
    logging.shutdown()


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
            self.sheeps.append(Sheep())

    def init_wolf(self):
        self.wolf = Wolf()

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
                _.append(None)
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
                print("Creation of the directory %s failed" % directory)

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
                print("Creation of the directory %s failed" % directory)
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

    def load_from_ini_file(self, file_name: str):
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

    def add_args_to_parser(self, parser_):
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

    def handle_parser_args(self):
        parser = argparse.ArgumentParser(description='Symulacja wilka i owiec')
        self.add_args_to_parser(parser)
        args: dict = vars(parser.parse_args())

        if args['config'] is not None:
            self.load_from_ini_file(args['config'])

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
            self.nr_of_rounds = args['rounds']

        if args['sheep'] is not None:
            if args['sheep'] <= 0:
                raise Exception('Liczba owiec musi być większa od 0')
            self.nr_of_sheeps = args['sheep']

        if args['wait'] is not None:
            self.wait_flag = args['wait']

    def simulate(self):
        self.init_sheeps()
        self.print_sheeps()
        self.init_wolf()
        round_ = 0
        while round_ != self.nr_of_rounds and self.alive_sheeps() > 0:
            #  ruch owiec
            for i in self.sheeps:
                i.move_sheep()

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
            else:
                self.wolf.move_wolf(self.sheeps[closest_sheep_index])

            #  informacje o turze
            print("Tura", round_, "/", self.nr_of_rounds - 1, " Pozycja wilka: (", str(self.wolf.x), ",",
                  str(self.wolf.y), ")", " Ilość żywych owiec: ", self.alive_sheeps(), "\n")
            if self.wait_flag:
                input("Press Enter to continue...")
            self.add_to_json_list(round_)
            self.add_to_csv(round_)
            #  licznik tury
            round_ += 1
        # za pętlą
        self.save_json_to_file('pos.json')
        self.save_csv_to_file('alive.csv')

        self.print_sheeps(only_alive=True)
        close_logger()  # bez tego nie działa usuwanie pliku


if __name__ == "__main__":
    simulate = Simulate()
    simulate.handle_parser_args()
    simulate.simulate()
    # do przemyślenia tutaj to całe
    if logging_type == 0:
        try:
            os.remove("chase.log")
        except PermissionError:
            print("Nie udało się usunąć pliku chase.log!")
            logger.critical("Nie udało się usunąć pliku chase.log")
