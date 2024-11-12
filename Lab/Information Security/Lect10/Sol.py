def encrypt_combined(plaintext, key=None):
    encrypted_words = []
    smallest_char = min(plaintext.replace(" ", ""))  # Smallest char ignoring spaces

    words = plaintext.split()  # Split plaintext into words

    for word_index, word in enumerate(words):
        encrypted_word = ""
        
        # Determine the starting shift for each word
        start_shift = word_index + 1 if key is None else 0  # Incremental shift if no key

        # Prepare the key-based shift logic (if key is provided)
        extended_key = []
        if key:
            key_digits = [int(digit) for digit in str(key)]
            key_length = len(key_digits)

            # Pad word with smallest_char to make it a multiple of key length
            remainder = len(word) % key_length
            if remainder != 0:
                word += smallest_char * (key_length - remainder)

            # Extend the key to match the length of the padded word
            extended_key = [key_digits[i % key_length] for i in range(len(word))]

        # Encrypt each character of the word
        for i, char in enumerate(word):
            # Use key shift if provided, otherwise use incremental shift
            shift = extended_key[i] if key else start_shift + i
            new_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            encrypted_word += new_char

        encrypted_words.append(encrypted_word)

    # Join encrypted words with spaces
    return " ".join(encrypted_words)

# Example usage
plaintext1 = "GRONSFELD"
key = 1234
cipher_text1 = encrypt_combined(plaintext1, key)
print(f"Gronsfeld Encrypted Text: {cipher_text1}")

plaintext2 = "RAG BABY"
cipher_text2 = encrypt_combined(plaintext2)  # No key provided, uses incremental shift
print(f"Incremental Shift Encrypted Text: {cipher_text2}")