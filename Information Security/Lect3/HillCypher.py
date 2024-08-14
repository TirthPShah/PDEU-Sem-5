# Hill Cipher

import math
import numpy as np
# print("\nHill Cypher Encryption/Decryption\n")
# input_message = input("\nEnter the message you want to encrypt: ")
# key = input("\nEnter the encryption key (4 letter or 9 letter) you want to use: ")

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

        if n != int(n):
            print("Invalid key length")
            return None

        n = int(n)

        for i in range(0, n):
            row = []
            for j in range(0, n):
                row.append(keyList[i * n + j])
            keyMat.append(row)

        return keyMat

    def getMessageMatrixList(self, key, message):

        lenOfMessage = len(message)
        n = math.sqrt(len(key))

        if n != int(n):
            print("Invalid key length")
            return None

        n = int(n)

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

    def encrypt(self, input_message, key):
        
        keyMat = self.getKeyMatrix(key)
        messageMatList = self.getMessageMatrixList(key, input_message)

        encryptedMessage = ""

        for messageMat in messageMatList:

            encryptedMat = matMult(keyMat, messageMat)

            n = int(math.sqrt(len(key)))
            for i in range(0, n):
                encryptedMessage += chr(encryptedMat[i][0] + ord('A'))

        return encryptedMessage

    def decrypt(self, input_message, key):
        pass

class ImprovedHillCypher:

    def getKeyMatrix(self, key):

        lenOfKey = len(key)

        keyMat = []

        key = key.upper()
        key = key.replace(" ", "")

        keyList = list(key)
        keyList = [ord(i) - ord('A') for i in keyList]

        n = math.sqrt(lenOfKey)

        if n != int(n):
            print("Invalid key length")
            return None

        n = int(n)

        for i in range(0, n):
            row = []
            for j in range(0, n):
                row.append(keyList[i * n + j])
            keyMat.append(row)

        return keyMat

    def getMessageMatrixList(self, key, message):
            
        lenOfMessage = len(message)
        n = math.sqrt(len(key))

        if n != int(n):
            print("Invalid key length")
            return None

        n = int(n)

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

hill = HillCypher()

print(hill.encrypt("EXAM", "HILL"))
