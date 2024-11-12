import random

# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to find the nearest lower prime
def nearest_lower_prime(n):
    while n > 2:
        n -= 1
        if is_prime(n):
            return n
    return 2  # Smallest prime

# Function to find the nearest greater prime
def nearest_greater_prime(n):
    while True:
        n += 1
        if is_prime(n):
            return n

# Function to generate a random prime or adjust if it's not prime
def generate_random_prime(seed):
    random.seed(seed)  # Set the seed for reproducibility
    num = random.randint(50, 200)
    return num

# Function to compute the greatest common divisor (GCD)
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Function to compute the modular inverse using the Extended Euclidean Algorithm
def modinv(e, phi):
    # Initialize the variables for the extended Euclidean algorithm
    A1, A2, A3 = 1, 0, phi
    B1, B2, B3 = 0, 1, e

    # Perform the algorithm in a loop
    while B3 != 0 and B3 != 1:
        Q = A3 // B3  # Integer division
        # Update the variables
        T1, T2, T3 = A1 - Q * B1, A2 - Q * B2, A3 - Q * B3
        A1, A2, A3 = B1, B2, B3
        B1, B2, B3 = T1, T2, T3
    
    if B3 == 0:
        raise Exception("Modular inverse does not exist")
    
    # If we get here, B3 is 1, so the inverse exists and is B2
    return B2 % phi

# Function to generate RSA keys
def generate_rsa_keys(message):
    # Step 1: Use the ASCII value of the message as a seed for generating primes
    seed = ord(message)
    p = generate_random_prime(seed)
    q = generate_random_prime(seed + 1)  # Add a small offset to generate a second distinct prime

    p, q = min(p, q), max(p, q)  # Ensure p < q
    p, q = nearest_lower_prime(p), nearest_greater_prime(q)  # Adjust if not prime

    # Step 2: Compute n = p * q
    n = p * q
    
    # Step 3: Compute phi(n) = (p-1) * (q-1)
    phi = (p - 1) * (q - 1)
    
    # Step 4: Choose e such that 1 < e < phi and gcd(e, phi) = 1 (typically e = 65537)
    random.seed(seed + 2)  # Set the seed for reproducibility
    e = random.randint(2, phi - 1)

    e = nearest_lower_prime(e)  # Adjust e to the nearest lower prime

    if gcd(e, phi) != 1:
        raise ValueError("e and phi(n) are not coprime!")
    
    # Step 5: Compute the modular inverse of e mod phi (this is d)
    d = modinv(e, phi)
    
    # Public key is (e, n), private key is (d, n)
    return (e, n), (d, n), p, q

# RSA encryption function
def encrypt(plaintext, public_key):
    e, n = public_key
    # Convert plaintext to an integer using ord (assuming plaintext is a single character)
    plaintext_int = ord(plaintext)
    # Encrypt using ciphertext = plaintext^e mod n
    ciphertext = pow(plaintext_int, e, n)
    return ciphertext

# RSA decryption function
def decrypt(ciphertext, private_key):
    d, n = private_key
    # Decrypt using plaintext = ciphertext^d mod n
    plaintext_int = pow(ciphertext, d, n)
    # Convert integer back to a character
    plaintext = chr(plaintext_int)
    return plaintext

# Example usage
if __name__ == "__main__":
    # Message to encrypt
    message = 'B'  # Single character message
    
    # Generate public and private keys using the ASCII value of the message as seed
    public_key, private_key, p, q = generate_rsa_keys(message)
    
    # Print the public and private keys
    print(f"Public Key (e, n): {public_key}")
    print(f"Private Key (d, n): {private_key}")
    print(f"Generated primes p: {p}, q: {q}")
    
    # Encrypt the message
    ciphertext = encrypt(message, public_key)
    print(f"Ciphertext: {ciphertext}")
    
    # Decrypt the ciphertext
    decrypted_message = decrypt(ciphertext, private_key)
    print(f"Decrypted message: {decrypted_message}")
