# Hill Cipher

import math
import numpy as np
# print("\nHill Cypher Encryption/Decryption\n")
# input_message = input("\nEnter the message you want to encrypt: ")
# key = input("\nEnter the encryption key (4 letter or 9 letter) you want to use: ")

def copyMatrix(A):
    return [row[:] for row in A]

def detRec(A, total=0):
    indices = list(range(len(A)))

    if len(A) == 1 and len(A[0]) == 1:
        return A[0][0]
    
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return val

    for fc in indices:
        ASubForFocCol = copyMatrix(A)
        ASubForFocCol = ASubForFocCol[1:]
        height = len(ASubForFocCol)

        for i in range(height):
            a = ASubForFocCol[i][0:fc]
            b = ASubForFocCol[i][fc+1:]
            ASubForFocCol[i] = ASubForFocCol[i][0:fc] + ASubForFocCol[i][fc+1:]

        sign = (-1) ** (fc)
        sub_det = detRec(ASubForFocCol)
        total += sign * A[0][fc] * sub_det

    return total

def getAdjointMatrix(mat):

    n = len(mat)
    adjointMat = []

    for i in range(0, n):
        row = []
        for j in range(0, n):
            subMat = []
            for k in range(0, n):
                if k == i:
                    continue
                temp = []
                for l in range(0, n):
                    if l == j:
                        continue
                    temp.append(mat[k][l])
                subMat.append(temp)
            row.append(detRec(subMat))
        adjointMat.append(row)

    for i in range(0, n):
        for j in range(0, n):
            adjointMat[i][j] = ((-1) ** (i + j)) * adjointMat[i][j]

    for i in range(0, n):
        for j in range(i, n):
            temp = adjointMat[i][j]
            adjointMat[i][j] = adjointMat[j][i]
            adjointMat[j][i] = temp

    return adjointMat

def getModularInverse(n):

    for i in range(26):
        if (n * i) % 26 == 1:
            return i
    return -1

def printMatrix(mat):

    n = len(mat)

    for i in range(0, n):
        for j in range(0, n):
            print(mat[i][j], end = " ")
        print()

def matMult(keyMat, messageMat):

    result = []

    n = len(keyMat)

    one = 0

    for i in range(0, n):
        temp = []
        one = 0
        for j in range(0, n):
            one += keyMat[i][j] * messageMat[j][0]
        temp.append(one % 26)
        result.append(temp)
        
    return result

class HillCypher:

    n = 0

    def getKeyMatrix(self, key):

        lenOfKey = len(key)

        keyMat = []

        key = key.upper()
        key = key.replace(" ", "")

        keyList = list(key)
        keyList = [ord(i) - ord('A') for i in keyList]

        self.n = math.sqrt(lenOfKey)
        n = self.n

        nextSq = math.ceil(n) ** 2

        paddingValue = ord('X') - ord('A')

        if len(keyList) < nextSq:
            keyList += [paddingValue] * (nextSq - len(keyList))

        n = int(math.sqrt(len(keyList)))

        for i in range(0, n):
            row = []
            for j in range(0, n):
                row.append(keyList[i * n + j])
            keyMat.append(row)

        return keyMat

    def getInverseKeyMatrix(self, key):
        
        keyMat = self.getKeyMatrix(key)
        det = detRec(keyMat)

        if det == 0:
            return None

        adjointMat = getAdjointMatrix(keyMat)

        detInv = getModularInverse(det)

        if detInv == -1:
            return None

        n = len(adjointMat)

        for i in range(0, n):
            for j in range(0, n):
                adjointMat[i][j] = (((adjointMat[i][j]) % 26) * detInv) % 26

        return adjointMat

    def getMessageMatrixList(self, key, message):

        lenOfMessage = len(message)
        n = int(math.sqrt(math.ceil(math.sqrt(len(key))) ** 2))

        if lenOfMessage % n != 0:
            message = message.upper().replace(" ", "") 
            message += "X" * (n - (lenOfMessage % n))

        messageMatList = []

        messageList = list(message)
        messageList = [ord(i) - ord('A') for i in messageList]

        for i in range(0, len(messageList), n):
            mat = []
            for j in range(0, n):
                listInt = [messageList[i + j]]
                mat.append(listInt)
            messageMatList.append(mat)

        
        return messageMatList

    def encrypt(self, key, input_message):
        
        keyMat = self.getKeyMatrix(key)
        
        messageMatList = self.getMessageMatrixList(key, input_message)

        encryptedMessage = ""
        encryptedMessageList = []

        for messageMat in messageMatList:

            encryptedMat = matMult(keyMat, messageMat)

            n = int(math.sqrt(math.ceil(math.sqrt(len(key))) ** 2))

            encryptedMessageList.append(encryptedMat)

            for i in range(0, n):
                encryptedMessage += chr(encryptedMat[i][0] + ord('A'))


        return encryptedMessageList, encryptedMessage

    def decrypt(self, key, input_message):
        
        keyInv = self.getInverseKeyMatrix(key)

        if keyInv == None:
            return None

        messageMatList = self.getMessageMatrixList(key, input_message)

        decryptedMessage = ""

        for messageMat in messageMatList:

            decryptedMat = matMult(keyInv, messageMat)

            n = int(math.sqrt(math.ceil(math.sqrt(len(key))) ** 2))

            for i in range(0, n):
                decryptedMessage += chr(decryptedMat[i][0] + ord('A'))

        # Remove the trailing 'X' characters without using library function or prebuilt function

        while decryptedMessage[-1] == 'X':
            decryptedMessage = decryptedMessage[:-1]



        return decryptedMessage

class ImprovedHillCypher:

    def getKeyMatrix(self, key):

        lenOfKey = len(key)

        keyMat = []

        key = key.upper()
        key = key.replace(" ", "")

        keyList = list(key)
        keyList = [ord(i) - ord('A') for i in keyList]

        self.n = math.sqrt(lenOfKey)
        n = self.n

        nextSq = math.ceil(n) ** 2

        paddingValue = ord('X') - ord('A')

        if len(keyList) < nextSq:
            keyList += [paddingValue] * (nextSq - len(keyList))

        n = int(math.sqrt(len(keyList)))

        for i in range(0, n):
            row = []
            for j in range(0, n):
                row.append(keyList[i * n + j])
            keyMat.append(row)

        return keyMat

    def getInverseKeyMatrix(self, key):

        keyMat = self.getKeyMatrix(key)
        keyMat = self.rotateMatrix(keyMat)
        keyMat = self.shiftColsRight(keyMat, key)
        det = detRec(keyMat)

        if det == 0:
            return None

        adjointMat = getAdjointMatrix(keyMat)

        detInv = getModularInverse(det)

        if detInv == -1:
            return None

        n = len(adjointMat)

        for i in range(0, n):
            for j in range(0, n):
                adjointMat[i][j] = (((adjointMat[i][j]) % 26) * detInv) % 26

        return adjointMat

    def rotateMatrix(self, matr):

        n = len(matr[0])

        for i in range(0, n):
            for j in range(i, n):
                temp = matr[i][j]
                matr[i][j] = matr[j][i]
                matr[j][i] = temp

        # Reverse each row without using library function or prebuilt function

        for i in range(0, n):
            for j in range(0, n // 2):
                temp = matr[i][j]
                matr[i][j] = matr[i][n - j - 1]
                matr[i][n - j - 1] = temp

        return matr
    
    def shiftColsRight(self, matr, key):

        n = len(matr[0])

        sumOfKey = 0

        for i in key:
            sumOfKey += ord(i)

        shift = sumOfKey % n

        shifted_matrix = [[0] * n for _ in range(n)]

        for i in range(0, n):
            for j in range(0, n):
                shifted_matrix[i][(j + shift) % n] = matr[i][j]

        return shifted_matrix

    def getMessageMatrixList(self, key, message):
            
        lenOfMessage = len(message)
        n = int(math.sqrt(math.ceil(math.sqrt(len(key))) ** 2))

        if lenOfMessage % n != 0:
            message = message.upper().replace(" ", "") 
            message += "X" * (n - (lenOfMessage % n))

        messageMatList = []

        messageList = list(message)
        messageList = [ord(i) - ord('A') for i in messageList]

        for i in range(0, len(messageList), n):
            mat = []
            for j in range(0, n):
                listInt = [messageList[i + j]]
                mat.append(listInt)
            messageMatList.append(mat)

        
        return messageMatList

    def encrypt(self, key, input_message):
            
        keyMat = self.getKeyMatrix(key)
        keyMat = self.rotateMatrix(keyMat)
        keyMat = self.shiftColsRight(keyMat, key)
        
        messageMatList = self.getMessageMatrixList(key, input_message)

        encryptedMessage = ""
        encryptedMessageList = []

        for messageMat in messageMatList:

            encryptedMat = matMult(keyMat, messageMat)

            n = int(math.sqrt(math.ceil(math.sqrt(len(key))) ** 2))

            encryptedMessageList.append(encryptedMat)

            for i in range(0, n):
                encryptedMessage += chr(encryptedMat[i][0] + ord('A'))


        return encryptedMessageList, encryptedMessage

    def decrypt(self, key, input_message):
                
        keyInv = self.getInverseKeyMatrix(key)

        if keyInv == None:
            return None

        messageMatList = self.getMessageMatrixList(key, input_message)

        decryptedMessage = ""

        for messageMat in messageMatList:

            decryptedMat = matMult(keyInv, messageMat)

            n = int(math.sqrt(math.ceil(math.sqrt(len(key))) ** 2))

            for i in range(0, n):
                decryptedMessage += chr(decryptedMat[i][0] + ord('A'))

        # Remove the trailing 'X' characters without using library function or prebuilt function

        while decryptedMessage[-1] == 'X':
            decryptedMessage = decryptedMessage[:-1]

        return decryptedMessage

# Testing encryption of Both HillCypher and ImprovedHillCypher

# hill = HillCypher()
# improvedHill = ImprovedHillCypher()

# print("\nHill Cypher Encryption: ", end="")
# print(hill.encrypt("HILL", "HELLO")[1])

# print("\nImproved Hill Cypher Encryption: ", end="")
# print(improvedHill.encrypt("HILL", "HELLO")[1])

hill = HillCypher()

print("\nHill Cypher Encryption: ", end="")

enc = hill.encrypt("HILL", "HELLO")[1]

print(enc)

print("\nHill Cypher Decryption: ", end="")

dec = hill.decrypt("HILL", enc)

print(dec)

improvedHill = ImprovedHillCypher()

print("\nImproved Hill Cypher Encryption: ", end="")

enc = improvedHill.encrypt("HILL", "HELLO")[1]

print(enc)

print("\nImproved Hill Cypher Decryption: ", end="")

dec = improvedHill.decrypt("HILL", enc)

print(dec)