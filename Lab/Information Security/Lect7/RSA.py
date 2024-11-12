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
def generate_rsa_keys(p, q):
    # Step 1: Compute n = p * q
    n = p * q
    
    # Step 2: Compute phi(n) = (p-1) * (q-1)
    phi = (p - 1) * (q - 1)
    
    # Step 3: Choose e such that 1 < e < phi and gcd(e, phi) = 1 (typically e = 65537)
    e = 65537
    if gcd(e, phi) != 1:
        raise ValueError("e and phi(n) are not coprime!")
    
    # Step 4: Compute the modular inverse of e mod phi (this is d)
    d = modinv(e, phi)
    
    # Public key is (e, n), private key is (d, n)
    return (e, n), (d, n)

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
    # Choose two small prime numbers (in real RSA, p and q should be much larger)
    p = 61
    q = 53
    
    # Generate public and private keys
    public_key, private_key = generate_rsa_keys(p, q)

    print(f"Value of p: {p}")
    print(f"Value of q: {q}")
    
    # Print the public and private keys
    print(f"Public Key (e, n): {public_key}")
    print(f"Private Key (d, n): {private_key}")
    
    # Message to encrypt
    message = 'A'  # Single character message

    print(f"Message: {message}")
    
    # Encrypt the message
    ciphertext = encrypt(message, public_key)
    print(f"Ciphertext: {ciphertext}")
    
    # Decrypt the ciphertext
    decrypted_message = decrypt(ciphertext, private_key)
    print(f"Decrypted message: {decrypted_message}")