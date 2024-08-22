class VignereCipher:

    def __init__(self, key):
        self.key = key  # Initialize the key for the cipher

    def setKey(self, key):
        self.key = key  # Method to set a new key for the cipher

    def encrypt(self, plaintext):
        ciphertext = ""  # Initialize the ciphertext as an empty string
        for i in range(len(plaintext)):
            chNum = ord(plaintext[i]) - ord('A')  # Convert plaintext character to 0-25 range
            chNum += ord(self.key[i % len(self.key)]) - ord('A')  # Add corresponding key character value
            chNum %= 26  # Wrap around if the sum exceeds 25
            ciphertext += chr(chNum + ord('A'))  # Convert back to a character and append to ciphertext
        return ciphertext  # Return the encrypted text

    def decrypt(self, ciphertext):
        plaintext = ""  # Initialize the plaintext as an empty string
        for i in range(len(ciphertext)):
            chNum = ord(ciphertext[i]) - ord('A')  # Convert ciphertext character to 0-25 range
            chNum -= ord(self.key[i % len(self.key)]) - ord('A')  # Subtract corresponding key character value
            chNum %= 26  # Wrap around if the result is negative
            plaintext += chr(chNum + ord('A'))  # Convert back to a character and append to plaintext
        return plaintext  # Return the decrypted text


class ImprovedVignereCipher:

    def __init__(self, key):
        self.key = key  # Initialize the key for the improved cipher

    def setKey(self, key):
        self.key = key  # Method to set a new key for the improved cipher

    def encrypt(self, plaintext):
        newKey = ""  # Initialize the new key as an empty string

        # Generate a new key that matches the length of the plaintext
        for i in range(len(plaintext)):
            newKey += self.key[i % len(self.key)]

        # Sort the new key in reverse order
        newKeyOne = ""
        for i in range(len(self.key)):
            j = i
            while j < len(newKey):
                newKeyOne += newKey[j]  # Rearrange the new key in reverse order
                j += len(self.key)

        newKey = ""
        for i in range(len(newKeyOne) - 1, -1, -1):
            newKey += newKeyOne[i]  # Reverse the newKeyOne to form the final newKey

        ciphertext = ""  # Initialize the ciphertext as an empty string

        # Encrypt using the modified key
        for i in range(len(plaintext)):
            chNum = ord(plaintext[i]) - ord('A')  # Convert plaintext character to 0-25 range
            chNum += ord(newKey[i % len(newKey)]) - ord('A')  # Add corresponding key character value
            chNum %= 26  # Wrap around if the sum exceeds 25
            ciphertext += chr(chNum + ord('A'))  # Convert back to a character and append to ciphertext
        return ciphertext  # Return the encrypted text

    def decrypt(self, ciphertext):
        newKey = ""  # Initialize the new key as an empty string

        # Generate a new key that matches the length of the ciphertext
        for i in range(len(ciphertext)):
            newKey += self.key[i % len(self.key)]

        # Sort the new key in reverse order
        newKeyOne = ""
        for i in range(len(self.key)):
            j = i
            while j < len(newKey):
                newKeyOne += newKey[j]  # Rearrange the new key in reverse order
                j += len(self.key)

        newKey = ""
        for i in range(len(newKeyOne) - 1, -1, -1):
            newKey += newKeyOne[i]  # Reverse the newKeyOne to form the final newKey

        plaintext = ""  # Initialize the plaintext as an empty string

        # Decrypt using the modified key
        for i in range(len(ciphertext)):
            chNum = ord(ciphertext[i]) - ord('A')  # Convert ciphertext character to 0-25 range
            chNum -= ord(newKey[i % len(newKey)]) - ord('A')  # Subtract corresponding key character value
            chNum %= 26  # Wrap around if the result is negative
            plaintext += chr(chNum + ord('A'))  # Convert back to a character and append to plaintext

        return plaintext  # Return the decrypted text


# Main code to demonstrate the Vignere Cipher and Improved Vignere Cipher
print("Vignere Cipher\n")
key = input("Enter key: ")  # Get the key from user input
key = key.upper().replace(" ", "")  # Convert key to uppercase and remove spaces
vignereCipher = VignereCipher(key)  # Create a VignereCipher object
text = input("Enter text to encrypt: ")  # Get the plaintext from user input
text = text.upper().replace(" ", "")  # Convert plaintext to uppercase and remove spaces
encryptedText = vignereCipher.encrypt(text)  # Encrypt the plaintext
print(f"\n\nEncrypted Text: {encryptedText}")  # Display the encrypted text
decryptedText = vignereCipher.decrypt(encryptedText)  # Decrypt the encrypted text
print(f"Decrypted Text: {decryptedText}")  # Display the decrypted text

print("\nImproved Vignere Cipher\n")
improvedVignereCipher = ImprovedVignereCipher(key)  # Create an ImprovedVignereCipher object
encryptedText = improvedVignereCipher.encrypt(text)  # Encrypt the plaintext using the improved cipher
print(f"Encrypted Text: {encryptedText}")  # Display the encrypted text from the improved cipher
decryptedText = improvedVignereCipher.decrypt(encryptedText)  # Decrypt the encrypted text from the improved cipher
print(f"Decrypted Text: {decryptedText}\n\n")  # Display the decrypted text from the improved cipher