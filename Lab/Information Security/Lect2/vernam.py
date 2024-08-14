def shuffleTwo(cipher):
    cipher = list(cipher)
    for i in range(0, len(cipher), 2):
        if i + 1 < len(cipher):
            cipher[i], cipher[i + 1] = cipher[i + 1], cipher[i]
    return "".join(cipher)

print(shuffleTwo("EHLLO"))