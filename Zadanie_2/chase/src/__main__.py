from src import wolfs_and_sheeps as was

if __name__ == "__main__":
    simulate = was.Simulate()
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
    was.close_logger()  # bez tego nie działa usuwanie pliku

    # do przemyślenia tutaj to całe
    if was.logging_type == 0:
        try:
            was.os.remove("chase.log")
        except PermissionError:
            print("Nie udało się usunąć pliku chase.log!")
            was.logger.critical("Nie udało się usunąć pliku chase.log")
