def lcm(a: [], b: []):
    index_b = 0
    result = []
    for i in range(len(a)):
        if index_b == len(b):
            break
        if a[i] == b[index_b]:
            b[index_b] = 1
            result.append(a[i])
            index_b += 1
    return iloczyn(a) * iloczyn(b)


def iloczyn(tab: []) -> int:
    tmp = 1
    for i in tab:
        tmp *= i
    return tmp



def dzielniki_liczby(x: int):
    i=2
    lista = []

    while x != 1:
        if x % i == 0:
            lista.append(i)
            x = x / i
            i = 2

        else: i=i+1

    return lista



tablica1 = dzielniki_liczby(192)
tablica2 = dzielniki_liczby(348)
print(lcm(tablica1,tablica2))
print(tablica2)
print(tablica1)





