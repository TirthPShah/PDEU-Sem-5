for i in range(1, 17):
    sete = set()
    for j in range(1, 17):
        print((i**j)%17, end=" ")
        sete.add((i**j) % 17)

    print(sete)
    if len(sete) == 16:
        print("Ands", i)

