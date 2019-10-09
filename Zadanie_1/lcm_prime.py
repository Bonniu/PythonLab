def lcm(a: [], b: []):
    index_b = 0
    result = []
    for i in range(len(a)):
        print("index: ", index_b)
        if index_b == len(b):
            break
        if a[i] == b[index_b]:
            b[index_b] = 0
            result.append(a[i])
            index_b += 1
    return iloczyn(result)


def iloczyn(tab: []) -> int:
    tmp = 1
    for i in tab:
        tmp *= i
    return tmp


tab1 = [1, 2, 3, 5, 2, 3, 2, 3, 2]
tab2 = [1, 2, 3, 2, 17, 17, 17]
print(lcm(tab1, tab2))
