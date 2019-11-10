import Simulate

if __name__ == "__main__":
    simulate = Simulate.Simulate()
    simulate.handle_parser_args()

    simulate.init_sheeps()
    simulate.print_sheeps()
    simulate.init_wolf()
    round_ = 0
    while round_ != simulate.nr_of_rounds and simulate.alive_sheeps() > 0:
        #  ruch owiec
        simulate.move_sheeps()

        #  ruch wilka
        simulate.move_wolf()

        #  informacje o turze
        print("Tura", round_, "/", simulate.nr_of_rounds - 1, " Pozycja wilka: (", str(simulate.wolf.x), ",",
              str(simulate.wolf.y), ")", " Ilość żywych owiec: ", simulate.alive_sheeps(), "\n")
        if simulate.wait_flag:
            input("Press Enter to continue...")
        simulate.add_to_json_list(round_)
        simulate.add_to_csv(round_)
        #  licznik tury
        round_ += 1
    # za pętlą
    simulate.save_json_to_file('pos.json')
    simulate.save_csv_to_file('alive.csv')

    simulate.print_sheeps(only_alive=True)
    # Simulate.close_logger()
