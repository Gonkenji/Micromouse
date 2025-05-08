lista = [1,2,3,4,5,6,-3]

l = []

ob = 0

for i in range(3):
    l.append(lista[ob + i])

print(l)

for r in range(10):
    ob += 1
    for i in range(3):
        if ob == len(lista) - i:
            ob = -i
        l[i] = lista[ob + i]
    print(l)