import Simulate

if __name__ == "__main__":
    simulate = Simulate.Simulate()
    simulate.init_sheeps()
    simulate.print_sheeps()
    round_ = 0
    while round_ != simulate.nr_of_rounds and simulate.alive_sheeps() > 0:
        #  ruch owiec
        simulate.move_sheeps()
        #  ruch wilka
        simulate.move_wolf()
        #  informacje o turze (później zakomentować)
        print("Tura", round_, "/", simulate.nr_of_rounds - 1, " Pozycja wilka: (", str(simulate.wolf.x), ",",
              str(simulate.wolf.y), ")", " Ilość żywych owiec: ", simulate.alive_sheeps(), "\n")
        #  licznik tury
        round_ += 1
    # za pętlą
    simulate.print_sheeps(only_alive=True)
