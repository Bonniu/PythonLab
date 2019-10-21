# najwiekszy wspolny dzielnik
def nwd(a: int, b: int):
    if a < 1 or b < 1:
        return None
    while b != 0:  # dopóki b nie jest 0 wykonuj
        c = a % b  # reszta z dzielenia a przez b
        a = b  # zastąpienie a liczbą b i b liczbą c
        b = c
    return a


#  wyświetlenie wyniku dla liczb 84 i 18
print("Wynik: ", nwd(84, 18))
