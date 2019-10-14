def lcm(l1: int, l2: int):  # oblicza nww(l1,l2)
    a = get_dividers(l1)
    b = get_dividers(l2)
    result = a.copy()  # tworzy kopie a nie referencje do tablicy, potem są jeszcze potrzebne dzielniki pierwszej liczby
    # początkowym wynikiem są dzielniki pierwszej liczby, potem dodajemy pozostałe drugiej liczby
    for j in range(len(b)):  # przechodzimy po całej tablicy dzielników drugeij liczby
        if b[j] in a:  # i jeżeli liczba jest już w dzielnikach to nie dodajemy
            a.remove(b[j])
        else:  # w przeciwynym razie dodajemy ją do końcowego wyniku
            result.append(b[j])
    return product_of_elements(result)


def product_of_elements(tab: []) -> int:  # zwraca iloczyn wszystkich elementów w tablicy tab
    tmp = 1
    for i in tab:
        tmp *= i
    return tmp


def get_dividers(x: int):  # oblicza dzielniki podanej jako argument liczby
    i = 2
    lista = []
    while x != 1:
        if x % i == 0:
            lista.append(i)
            x = x / i
            i = 2
        else:
            i = i + 1
    return lista


if __name__ == "__main__":
    print(lcm(348, 192))
