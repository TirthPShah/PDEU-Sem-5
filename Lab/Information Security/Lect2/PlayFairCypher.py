import string

def getMat(key): 
    key = key.upper().replace("J", "I")
    usedAlphas = set()
    matList = []

    # Add key characters to the matrix
    for k in key:
        if k not in usedAlphas and k in string.ascii_uppercase:
            usedAlphas.add(k)
            matList.append(k)

    # Add remaining characters to the matrix
    for a in string.ascii_uppercase:
        if a not in usedAlphas and a != "J":
            usedAlphas.add(a)
            matList.append(a)

    # Generate the 5x5 matrix
    mat = [matList[i:i + 5] for i in range(0, 25, 5)]

    return mat

def modifyInput(input_message):
    input_message = input_message.upper().replace(" ", "").replace("J", "I")
    formatted_message = ""
    
    i = 0
    while i < len(input_message):
        formatted_message += input_message[i]
        if i + 1 < len(input_message):
            if input_message[i] == input_message[i + 1]:
                formatted_message += 'X'
                i += 1
            else:
                formatted_message += input_message[i + 1]
                i += 2
        else:
            formatted_message += 'X'
            i += 1

    return formatted_message

def findPosition(char, mat):
    for i, row in enumerate(mat):
        if char in row:
            return i, row.index(char)
    return None

def displayMat(mat):
    print("\nMatrix: \n")
    for row in mat:
        print("   ".join(row))
    print()

def playFairEncrypt(input_message, key):
    mat = getMat(key)
    displayMat(mat)
    modified_input = modifyInput(input_message)

    encrypted = ""
    i = 0

    while i < len(modified_input):
        a = modified_input[i]
        b = modified_input[i + 1]

        row1, col1 = findPosition(a, mat)
        row2, col2 = findPosition(b, mat)

        if row1 == row2:
            encrypted += mat[row1][(col1 + 1) % 5]
            encrypted += mat[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted += mat[(row1 + 1) % 5][col1]
            encrypted += mat[(row2 + 1) % 5][col2]
        else:
            encrypted += mat[row1][col2]
            encrypted += mat[row2][col1]

        i += 2

    return encrypted

def playFairDecrypt(cypher, key):
    mat = getMat(key)
    displayMat(mat)

    plain = ""
    i = 0

    while i < len(cypher):
        a = cypher[i]
        b = cypher[i + 1]

        row1, col1 = findPosition(a, mat)
        row2, col2 = findPosition(b, mat)

        if row1 == row2:
            plain += mat[row1][(col1 - 1) % 5]
            plain += mat[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plain += mat[(row1 - 1) % 5][col1]
            plain += mat[(row2 - 1) % 5][col2]
        else:
            plain += mat[row1][col2]
            plain += mat[row2][col1]

        i += 2

    return plain

print("\nPlayFair Cypher Encryption/Decryption\n")

input_message = input("\nEnter the message you want to encrypt: ")
key = input("\nEnter the encryption key you want to use: ")
encrypted_message = playFairEncrypt(input_message, key)
print("\nEncrypted Message: ", encrypted_message)
decrypted_message = playFairDecrypt(encrypted_message, key).replace("X", "")
print("\nDecrypted Message: ", decrypted_message, "\n")