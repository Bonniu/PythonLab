import random

import Simulate


class Sheep:
    def __init__(self):
        Simulate.logger.debug('Wywołana metoda __init__ z klasy Sheep')
        self.x = random.randint(-Simulate.init_pos_limit * 100, Simulate.init_pos_limit * 100) / 100
        self.y = random.randint(-Simulate.init_pos_limit * 100, Simulate.init_pos_limit * 100) / 100
        self.is_alive = True
        Simulate.logger.info('Ustawienie pozycji owcy oraz flagi is_alive: ' + self.__repr__())
        Simulate.logger.debug('Wyjście z metody __init__ z klasy Sheep')

    def move_sheep(self):
        Simulate.logger.debug('Wywołana metoda move_sheep z argumentem typu Sheep - ' + self.__repr__())
        Simulate.logger.info('Wylosowanie kierunku, w którym pójdzie owca')
        direction = random.randint(1, 4)
        if direction == 1:
            Simulate.logger.info('Kierunek: do góry, początkowa pozycja ' + self.__repr__())
            self.y += Simulate.sheep_move_dist
            Simulate.logger.info('Kierunek: do góry, końcowa pozycja ' + self.__repr__())
        elif direction == 2:
            Simulate.logger.info('Kierunek: w prawo, początkowa pozycja ' + self.__repr__())
            self.x += Simulate.sheep_move_dist
            Simulate.logger.info('Kierunek: w prawo, końcowa pozycja ' + self.__repr__())
        elif direction == 3:
            Simulate.logger.info('Kierunek: w dół, początkowa pozycja ' + self.__repr__())
            self.y -= Simulate.sheep_move_dist
            Simulate.logger.info('Kierunek: w dół, końcowa pozycja ' + self.__repr__())
        else:
            Simulate.logger.info('Kierunek: w lewo, początkowa pozycja ' + self.__repr__())
            self.x -= Simulate.sheep_move_dist
            Simulate.logger.info('Kierunek: w lewo, końcowa pozycja ' + self.__repr__())
        Simulate.logger.debug('Wyjście z metody move_sheep')

    def kill_sheep(self):
        Simulate.logger.debug('Wywołana metoda kill_sheep z klasy Sheep na obiekcie ' + self.__repr__())
        self.is_alive = False
        Simulate.logger.debug('Wyjście z metody kill_sheep, końcowy stan obiektu: ' + self.__repr__())

    def __repr__(self):
        return "Sheep[x=" + str(self.x) + ", y=" + str(self.y) + ", is_alive=" + str(self.is_alive) + "]"
