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

        # Random order of columns:
        self.order = list(range(len(self.key)))
        random.shuffle(self.order)
        
    # Rotate the rows based on key
    def rotateRows(self, mat):
        for i, row in enumerate(mat):
            shift = sum(ord(char) for char in self.key) % len(row)
            mat[i] = row[shift:] + row[:shift]
        return mat

    # Reverse the row rotation during decryption
    def reverseRotateRows(self, mat):
        for i, row in enumerate(mat):
            shift = sum(ord(char) for char in self.key) % len(row)
            mat[i] = row[-shift:] + row[:-shift]
        return mat

    # Create the columnar matrix for the given plaintext
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
            tempList = []
            for j in range(len(self.key)):
                tempList.append(plaintext[look])
                look += 1
            mat.append(tempList)

        return mat

    # Encrypt the plaintext
    def encrypt(self, plaintext):
        mat = self.getColumnarMatrix(plaintext)
        
        # Rotate the rows
        mat = self.rotateRows(mat)
        
        orderEnu = list(enumerate(self.order))
        sortedEnuList = sorted(orderEnu, key=lambda x: x[1])

        cipher = ''

        # If column is even, go from top to bottom, otherwise bottom to top
        for index, _ in orderEnu:
            if index % 2 == 0:
                for row in range(len(mat)):
                    cipher += mat[row][index]
            else:
                for row in range(len(mat) - 1, -1, -1):
                    cipher += mat[row][index]

        return cipher

    # Decrypt the ciphertext
    def decrypt(self, cipher):
        totalRow = math.ceil(len(cipher) / len(self.key))
        mat = [['' for _ in range(len(self.key))] for _ in range(totalRow)]

        look = 0

        orderEnu = list(enumerate(self.order))
        sortedEnuList = sorted(orderEnu, key=lambda x: x[1])

        # If column is even, go top-down, otherwise bottom-up to fill the matrix
        for index, _ in orderEnu:
            if index % 2 == 0:
                for row in range(len(mat)):
                    mat[row][index] = cipher[look]
                    look += 1
            else:
                for row in range(len(mat) - 1, -1, -1):
                    mat[row][index] = cipher[look]
                    look += 1

        # Reverse the row rotation
        mat = self.reverseRotateRows(mat)

        plainText = ''.join(''.join(row) for row in mat)
        
        return plainText.rstrip('X')




col = ColumnarTransposition('keys')
cipher = col.encrypt('hellohowareyouiamfine'.upper())
print(f"Cipher: {cipher}")
print(f"Decrypted: {col.decrypt(cipher)}")

impro = ImprovedCol('keys')
cipher = impro.encrypt('hellohowareyouiamfine'.upper())
print(f"Cipher: {cipher}")
print(f"Decrypted: {impro.decrypt(cipher)}")