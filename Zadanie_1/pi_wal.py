def pi(n: int):
    if n < 1:
        return 0
    result = 1
    for part in range(1, n + 1):
        upper = (2 * part) ** 2  # górna część ułamka
        lower = (2 * part - 1) * (2 * part + 1)  # dolna część ułamka
        result *= upper / lower  # wynik jednej iteracji
    return result * 2  # wzór wallisa zwraca pi/2, dlatego wynik mnożymy przez 2


#  wyświetlenie pierwszych 10 przybliżeń dziesiętnych
for i in range(1, 11):
    print(i, ": ", pi(i))
