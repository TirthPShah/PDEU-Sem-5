import math

# First key generation 
class GCDUtil:
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


class KeyPairGenerator:
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
        gcd_util = GCDUtil()
        if self.is_prime(int(prime1)) and self.is_prime(int(prime2)):
            modulus = prime1 * prime2
            totient = (prime1 - 1) * (prime2 - 1)  # Calculate the totient function φ(n)
    
            # Now check for a number e in range 1 to φ(n) such that gcd(e, φ(n)) = 1
            exponent = gcd_util.find_coprime(totient)
    
            # Use extended Euclidean algorithm to find d such that (d * e) % φ(n) = 1
            gcd, private_key, _ = gcd_util.extended_gcd(exponent, totient)
            private_key = private_key % totient  # Ensure d is positive
            if private_key < 0:
                private_key += totient
                
            return exponent, private_key, modulus
        else:
            raise ValueError("Both numbers must be prime.")


# Encrypt with d (Private key) and it is called signature
class MessageSender:
    def encrypt(self, message, private_key, modulus):
        # Encrypt each character and return a list of encrypted values
        return [pow(char, private_key, modulus) for char in message]


# Verify With e (Public key) which is announced or receiver had it beforehand
class MessageReceiver:
    def decrypt(self, signature, exponent, modulus):
        # Decrypt each character and return the original message
        return ''.join(chr(pow(char, exponent, modulus)) for char in signature)


# Driver Code
keygen = KeyPairGenerator()
p = int(input("Enter first prime number (p): "))
q = int(input("Enter second prime number (q): "))
e, d, n = keygen.generate_keys(p, q)

# Sender encrypts message with private key d
plain_text = input("Enter message to encrypt: ")
# Convert the message to a list of ASCII values
plain_num = [ord(char) for char in plain_text]

sender = MessageSender()
signature = sender.encrypt(plain_num, d, n)
print(f"The signature generated to send to receiver is: {signature}")

# Receiver decrypts signature with public key e
receiver = MessageReceiver()
message = receiver.decrypt(signature, e, n)
print(f"Message and signature received by receiver: {message}")

# Check if the original message matches the decrypted message
if message == plain_text:
    print("Message is authentic") 
else:
    print("Message tampered")
