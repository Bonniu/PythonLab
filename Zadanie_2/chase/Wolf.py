import Simulate
from Sheep import Sheep


class Wolf:
    def __init__(self):
        Simulate.logger.debug('Wywołana metoda __init__ z klasy Wolf')
        self.x = 0.0
        self.y = 0.0
        Simulate.logger.debug('Wyjście z metody __init__, utworzono obiekt ' + self.__repr__())

    def move_wolf(self, sheep: Sheep):
        Simulate.logger.debug(
            'Wywołana metoda move_wolf z klasy Wolf z parametrami: self=' + self.__repr__() + ', sheep=' +
            sheep.__repr__())
        vector = (sheep.x - self.x, sheep.y - self.y)
        tmp_x = vector[0] * Simulate.wolf_move_dist / Simulate.calc_distance(self, sheep)
        tmp_y = vector[1] * Simulate.wolf_move_dist / Simulate.calc_distance(self, sheep)
        Simulate.logger.info('Ustawienie pozycji wilka: początkowa pozycja: ' + self.__repr__())
        self.x += tmp_x
        self.y += tmp_y
        Simulate.logger.info('Ustawienie pozycji wilka: końcowa pozycja: ' + self.__repr__())
        Simulate.logger.debug('Wyjście z metody move_wolf z klasy Wolf')

    def __repr__(self):
        return "Wolf[x=" + str(self.x) + ", y=" + str(self.y) + "]"
