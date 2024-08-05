#Playfair Cypher

print("\PlayFair Cypher Encryption/Decryption\n")
choice = input("Enter the operation you want to perform: Encryption(1)/Decryption(0): ")



def getMat(key):

    usedAlphas = set()
    matList = []
    skipped = False
    mat = []

    key = key.upper()
    encrypted_message = ""

    for k in key:
        if k not in usedAlphas:
            usedAlphas.add(k)
            matList.append(k)

    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    for a in alphabets:
        if a not in usedAlphas:
            if len(matList) >= 12 and not skipped:
                skipped = True
                continue
            usedAlphas.add(a)
            matList.append(a)
    
    for i in range(5):
        l = []
        for j in range(5):
            index = 5 * i
            index = index + j
            l.append(matList[index])
        mat.append(l)

    return mat

def modifyInput(input_message):

    input_message = input_message.upper()
    formatted_message = ""

    i = 0
    while i < len(input_message):
        formatted_message += input_message[i]
        if i + 1 < len(input_message):
            if input_message[i] == input_message[i + 1]:
                formatted_message += 'X'
                i += 1
                continue
            else:
                formatted_message += input_message[i + 1]
            i += 2
        else:
            formatted_message += 'X'
            i += 1

    return formatted_message

def findPosition(a, mat):
    for i, row in enumerate(mat):
        if a in row:
            return i, row.index(a)
    return None

def displayMat(mat):
    print("\nMatrix: \n")
    for i in range(5):
        for j in range(5):
            print(mat[i][j], end = "   ")
        print()
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
    modified_input = modifyInput(input_message)

    plain = ""
    i = 0

    while i < len(modified_input):
        a = modified_input[i]
        b = modified_input[i + 1]

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

    formattedPlain = ""

    for ch in plain:
        if ch == 'X':
            continue
        formattedPlain += ch

    return formattedPlain   


if choice == '1':
    input_message = input("\nEnter the message you want to encrypt: ")
    key = input("\nEnter the encryption key you want to use: ")
    encrypted_message = playFairEncrypt(input_message, key)
    print("\nEncrypted Message: ", encrypted_message)

elif choice == '0':
    input_message = input("\nEnter the message you want to decrypt: ")
    key = input("\nEnter the decryption key you want to use: ")
    decrypted_message = playFairDecrypt(input_message, key)
    print("\nDecrypted Message: ", decrypted_message, "\n")

else:
    print("\nInvalid option chosen. Run the code again with  valid options.\n")