import math
print("***Algorytm wyznaczania liczb pierwszych z zadanego przedziału[2,n]***")
print("Podaj liczbe calkowita n>1:")
n = int(input())  # wczytujemy koniec zakresu liczb w ktorym bedziemy szukać
# liczb pierwszych

tablica = []

for i in range(0, n + 1):
    tablica.append(bool(1))  # wypelniamy tablice wartosciami True

for i in range(2, int(math.sqrt(n))):  # z przedzialu (2)-(sqrt(n))
    if tablica[i]:  # jesli jakas wartosc jest True to
        for j in range(2 * i, n + 1, i):  # wszystkie tablice gdzie indeks jest wielokrotnoscia "i"
            # ustawiamy na false
            tablica[j] = False

for i in range(2, n + 1):  # wartosci ktore maja wartosc True to l.pierwsze
    if tablica[i]:
        print(i)
