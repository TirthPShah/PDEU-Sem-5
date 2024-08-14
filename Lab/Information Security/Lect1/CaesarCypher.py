print("\nCaesar Cypher Encryption/Decryption\n")
choice = input("Enter the operation you want to perform: Encryption(1)/Decryption(0): ")

# Populating the alphabet table before hand without loop to avoid any overhead
alphabetTable = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
reverseAlphabetTable = {v: k for k, v in alphabetTable.items()}

if choice == "1":
    input_message = input("\nEnter the message you want to encrypt: ")
    key = int(input("\nEnter the encryption key you want to use: "))
    encrypted_message = ""

    for c in input_message:
        if (65 <= ord(c) <= 90):
            encrypted_message += reverseAlphabetTable[(alphabetTable[c] + key) % 26]
        elif (97 <= ord(c) <= 122):
            temp = ord(c) - 32
            encrypted_message += reverseAlphabetTable[(alphabetTable[chr(temp)] + key) % 26].lower()
        else:
            encrypted_message += c

    print("\nEncrypted message: ", encrypted_message, end="\n\n")

elif choice == "0":
    input_message = input("\nEnter the message you want to decrypt: ")
    key = int(input("\nEnter the decryption key you want to use: "))
    decrypted_message = ""

    for c in input_message:
        if (65 <= ord(c) <= 90):
            decrypted_message += reverseAlphabetTable[(alphabetTable[c] - key) % 26]
        elif (97 <= ord(c) <= 122):
            temp = ord(c) - 32
            decrypted_message += reverseAlphabetTable[(alphabetTable[chr(temp)] - key) % 26].lower()
        else:
            decrypted_message += c

    print("\nDecrypted message: ", decrypted_message, end="\n\n")

else:
    print("\nInvalid choice! Please enter 1 for encryption or 0 for decryption.")