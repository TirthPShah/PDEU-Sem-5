print("\nCaesar Cypher Encryption/Decryption\n")
choice = input("Enter the operation you want to perform: Encryption(1)/Decryption(0): ")

# Populating the alphabet table before hand without loop to avoid any overhead
alphabetTable = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def adjustLength(keyword, input_message):

    diff = len(input_message) - len(keyword)
    newKeyword = ""
    if diff < 0:
        for i in range(len(input_message)):
            newKeyword += keyword[i]

    elif diff == 0:
        newKeyword = keyword

    else:
        for i in range(len(input_message)):
            newKeyword += keyword[i % len(keyword)]

    return newKeyword

def simpleHash(keyword, key):

    hashValue = 0
    for i in range(len(keyword)):
        hashValue += ord(keyword[i])

    key = key * 17
    return hashValue % key


def imporvedCaesarEncrypt(input_message, key, keyword, alphabetTable):

    sameLengthKeyword = adjustLength(keyword, input_message)
    shiftValue = simpleHash(sameLengthKeyword, key)
    encrypted_message = ""

    for c in input_message:

        if (65 <= ord(c) <= 90):
            encrypted_message += alphabetTable[(alphabetTable.index(c) + shiftValue) % 26]
        elif (97 <= ord(c) <= 122):
            temp = ord(c) - 32
            encrypted_message += alphabetTable[(alphabetTable.index(chr(temp)) + shiftValue) % 26].lower()
        else:
            encrypted_message += c
        
    return encrypted_message

def imporvedCaesarDecrypt(input_message, key, keyword, alphabetTable):

    sameLengthKeyword = adjustLength(keyword, input_message)
    shiftValue = simpleHash(sameLengthKeyword, key)
    decrypted_message = ""

    for c in input_message:

        if (65 <= ord(c) <= 90):
            decrypted_message += alphabetTable[(alphabetTable.index(c) - shiftValue) % 26]
        elif (97 <= ord(c) <= 122):
            temp = ord(c) - 32
            decrypted_message += alphabetTable[(alphabetTable.index(chr(temp)) - shiftValue) % 26].lower()
        else:
            decrypted_message += c
        
    return decrypted_message

if choice == "1":

    input_message = input("\nEnter the message you want to encrypt: ")
    key = int(input("\nEnter the encryption key you want to use: "))
    keyword = input("\nEnter the keyword you want to use: ")
    encrypted_message = imporvedCaesarEncrypt(input_message, key, keyword, alphabetTable)
    print("\nEncrypted message: ", encrypted_message, end="\n\n")

elif choice == "0":

    input_message = input("\nEnter the message you want to decrypt: ")
    key = int(input("\nEnter the decryption key you want to use: "))
    keyword = input("\nEnter the keyword you want to use: ")
    decrypted_message = imporvedCaesarDecrypt(input_message, key, keyword, alphabetTable)
    print("\nDecrypted message: ", decrypted_message, end="\n\n")