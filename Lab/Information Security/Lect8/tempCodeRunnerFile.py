import math
import random

# First key generation 
class Key:
    def find_coprime(self, num):
        for i in range(2, num):
            if math.gcd(num, i) == 1:
                return i

    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = self.extended_gcd(b % a, a)
    
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y


class KeyGen:
    def is_prime(self, candidate):
        # First consider edge case:
        if candidate <= 1:
            return False
        else:
            # Calculating approx. square root.
            for i in range(2, int(math.sqrt(candidate) + 1)):
                if candidate % i == 0:
                    return False
            return True
        
    def generate_keys(self, prime1, prime2):
        backpack = Key()
        if self.is_prime(int(prime1)) and self.is_prime(int(prime2)):
            modulus = prime1 * prime2
            totient = (prime1 - 1) * (prime2 - 1)  # Calculate the totient function φ(n)
    
            # Now check for a number e in range 1 to φ(n) such that gcd(e, φ(n)) = 1
            exponent = backpack.find_coprime(totient)
    
            # Use extended Euclidean algorithm to find d such that (d * e) % φ(n) = 1
            gcd, private_key, _ = backpack.extended_gcd(exponent, totient)
            private_key = private_key % totient  # Ensure d is positive
            if private_key < 0:
                private_key += totient
                
            return exponent, private_key, modulus
        else:
            raise ValueError("Both numbers must be prime.")


# Second encrypt with d (Private key) and it is called signature
class Encryptor:
    def encrypt_message(self, msg, private_key, modulus):
        # Encrypt each character using random values seeded with p * q
        random.seed(modulus)  # Seed the random generator with modulus (p * q)
        encrypted_output = []
        for char in msg:
            # Generate a random modifier
            modifier = random.randint(1, 100)
            # Encrypt the character and apply the modifier
            encrypted_char = pow(char + modifier, private_key, modulus)
            encrypted_output.append(encrypted_char)
        return encrypted_output


# Fourth Verify With e (Public key) which is announced or receiver had it beforehand
class Decryptor:
    def decrypt_signature(self, encrypted_signature, public_key, modulus):
        # Decrypt each character and return the original message
        decrypted_output = []
        for char in encrypted_signature:
            # Decrypt the character
            decrypted_char = pow(char, public_key, modulus)
            decrypted_output.append(decrypted_char)  # Append the decrypted number
        return decrypted_output


# Driver Code
key_gen = KeyGen()
first_prime = int(input("Enter the First prime number for key generation: "))
second_prime = int(input("Enter the Second prime number for key generation: "))
public_key, private_key, modulus = key_gen.generate_keys(first_prime, second_prime)

# Encryptor encrypts message with private key
input_text = input("Enter Message to Encrypt: ")
# Convert the message to a list of ASCII values
ascii_values = [ord(char) for char in input_text]

encryptor = Encryptor()
signature = encryptor.encrypt_message(ascii_values, private_key, modulus)
print(f"The signature generated to send to receiver is: {signature}")
print("Sending Message & Signature to Receiver..............")

# Decryptor decrypts signature with public key
decryptor = Decryptor()
decrypted_signature = decryptor.decrypt_signature(signature, public_key, modulus)
# Convert the decrypted ASCII values back to characters
final_message = ''.join(chr(num) for num in decrypted_signature)
print(f"Message and Signature Received by Receiver: {final_message}")

# Check if the original message matches the decrypted message
if input_text == final_message:
    print("Verification Successful") 
else:
    print("Message Tampered")
