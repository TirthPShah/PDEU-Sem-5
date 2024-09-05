import math
import random

class ColumnarTransposition:

    # Constructor to initialize with the provided key
    def __init__(self, key):
        self.key = key

    # Function to update the key if needed
    def setKey(self, key):
        self.key = key
    
    # Function to create the columnar matrix for encryption and decryption
    def getColumnarMatrix(self, plaintext):
        # Calculate the target length by rounding up to fill the grid
        targetLength = math.ceil(len(plaintext) / len(self.key)) * len(self.key)
        plainList = list(plaintext)
        # Pad the plaintext with 'X' if necessary to complete the matrix
        plainList += ['X' for _ in range(targetLength - len(plaintext))]
        plaintext = ''.join(plainList)

        mat = []

        totalRow = int(len(plaintext) / len(self.key))
        look = 0

        # Populate the matrix row by row
        for i in range(totalRow):
            tempString = ''
            tempList = []
            for j in range(len(self.key)):
                tempList.append(plaintext[look])
                look += 1
            mat.append(tempList)

        return mat

    # Encryption function using the key to rearrange the matrix columns
    def encrypt(self, plaintext):
        mat = self.getColumnarMatrix(plaintext)

        enuList = list(enumerate(self.key))

        # Sort the key to get the new column order
        sortedEnuList = sorted(enuList, key= lambda x : x[1])

        cipher = ''

        totalRow = int(len(plaintext) / len(self.key))

        # Read the columns in sorted key order to generate the ciphertext
        for index, _ in sortedEnuList:
            for row in range(totalRow + 1):
                cipher += mat[row][index]

        return cipher

    # Decryption function that reverses the encryption process
    def decrypt(self, cipher):
        totalRow = math.ceil(len(cipher) / len(self.key))  # Number of rows in the matrix

        # Create a matrix with empty strings to store the reordered columns
        mat = [['' for _ in range(len(self.key))] for _ in range(totalRow)]
        
        # Sort the key to find the column order
        enuList = list(enumerate(self.key))
        sortedEnuList = sorted(enuList, key=lambda x: x[1])

        look = 0

        # Refill the matrix columns in the sorted order
        for index, _ in sortedEnuList:
            for row in range(totalRow):
                mat[row][index] = cipher[look]
                look += 1

        plainText = ''
        
        # Rebuild the plaintext by reading the matrix row by row
        for row in mat:
            plainText += ''.join(row)

        return plainText.rstrip('X')  # Remove padding (X) if any

class ImprovedCol:

    # Constructor to initialize with the provided key
    def __init__(self, key):
        self.key = key

        # Seed the random module using the sum of ASCII values of characters in the key
        seed_value = sum(ord(char) for char in self.key)
        random.seed(seed_value)

        # Generate a random number (0 or 1) to decide the mode of writing/reading
        self.mode = random.randint(0, 1)

    # Function to generate the matrix based on the given mode
    def getColumnarMatrix(self, text, is_encrypt=True):
        # Calculate the target length to fill the matrix with extra padding if necessary
        targetLength = math.ceil(len(text) / len(self.key)) * len(self.key)
        textList = list(text)
        # Pad the text with 'X' to fill up the matrix if needed
        textList += ['X' for _ in range(targetLength - len(text))]

        mat = []
        look = 0
        totalRow = len(textList) // len(self.key)

        # Create the matrix row by row
        for i in range(totalRow):
            tempList = []
            for j in range(len(self.key)):
                tempList.append(textList[look])
                look += 1
            mat.append(tempList)

        return mat

    # Function to encrypt the text based on the randomly chosen mode
    def encrypt(self, plaintext):
        mat = self.getColumnarMatrix(plaintext)

        # Get the list of key indices in sorted order based on the key's characters
        enuList = list(enumerate(self.key))
        sortedEnuList = sorted(enuList, key=lambda x: x[1])

        cipher = ''

        totalRow = len(mat)

        # If mode is 0, write by row and read by column (standard transposition)
        if self.mode == 0:
            for index, _ in sortedEnuList:
                for row in range(totalRow):
                    cipher += mat[row][index]

        # If mode is 1, write by column and read by row
        else:
            for row in mat:
                for col in row:
                    cipher += col

        return cipher

    # Function to decrypt the cipher based on the chosen mode
    def decrypt(self, cipher):
        totalRow = math.ceil(len(cipher) / len(self.key))

        # Create an empty matrix for decryption
        mat = [['' for _ in range(len(self.key))] for _ in range(totalRow)]

        # Get the list of key indices in sorted order based on the key's characters
        enuList = list(enumerate(self.key))
        sortedEnuList = sorted(enuList, key=lambda x: x[1])

        look = 0

        # If mode is 0, read by column and write by row
        if self.mode == 0:
            for index, _ in sortedEnuList:
                for row in range(totalRow):
                    mat[row][index] = cipher[look]
                    look += 1

        # If mode is 1, read by row and write by column
        else:
            for row in range(totalRow):
                for col in range(len(self.key)):
                    mat[row][col] = cipher[look]
                    look += 1

        plainText = ''

        # Rebuild the plaintext by reading row by row from the matrix
        for row in mat:
            plainText += ''.join(row)

        return plainText.rstrip('X')  # Remove padding (X) if any


col = ColumnarTransposition('keys')
cipher = col.encrypt('hello')
print(f"Cipher: {cipher}")
print(f"Decrypted: {col.decrypt(cipher)}")

impro = ImprovedCol('keys')
cipher = impro.encrypt('hfllo')
print(f"Cipher: {cipher}")
print(f"Decrypted: {impro.decrypt(cipher)}")