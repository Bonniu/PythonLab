# szukamy liczb pierwszych
import math


def primes(num: int):
    tablica = []
    wynik = []
    for i in range(0, num + 1):
        tablica.append(True)  # wypelniamy tablice wartosciami True

    for i in range(2, int(math.sqrt(num)) + 1):  # z przedzialu (2)-(sqrt(n))
        if tablica[i]:  # jesli jakas wartosc jest True to
            for j in range(2 * i, num + 1, i):  # wszystkie tablice gdzie indeks jest wielokrotnoscia "i"
                # ustawiamy na false
                tablica[j] = False

    for i in range(2, num + 1):  # wartosci ktore maja wartosc True to l.pierwsze
        if tablica[i]:
            wynik.append(i)
    return wynik


if __name__ == "__main__":
    print("***Algorytm wyznaczania liczb pierwszych z zadanego przedziału[2,n]***")
    n = 100
    # szukać liczb pierwszych
    print(primes(n))
