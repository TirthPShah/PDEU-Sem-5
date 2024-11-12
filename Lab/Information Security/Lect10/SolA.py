def encrypt_gronsfeld(plaintext, key):
    key = [int(digit) for digit in str(key)]
    key_length = len(key)
    
    # Find the smallest character in the plaintext
    smallest_char = min(plaintext)

    # Ensure the length of plaintext is a multiple of the key length
    remainder = len(plaintext) % key_length
    if remainder != 0:
        # Add filler characters (smallest_char) to make the length a multiple of key length
        plaintext += smallest_char * (key_length - remainder)

    # Extend the key to match the length of the (possibly extended) plaintext
    extended_key = []
    for i in range(len(plaintext)):
        extended_key.append(key[i % key_length])

    # Encrypt the plaintext using the extended key
    encrypted_text = ""
    for i, char in enumerate(plaintext):
        shift = extended_key[i]
        new_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        encrypted_text += new_char

    return encrypted_text

# Example usage
plaintext = "GRONSFELD"
key = 1234
cipher_text = encrypt_gronsfeld(plaintext, key)
print(f"Encrypted Text: {cipher_text}")