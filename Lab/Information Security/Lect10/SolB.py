def encrypt_with_increment(plaintext):
    words = plaintext.split()  # Split the input by spaces
    encrypted_words = []

    for word_index, word in enumerate(words):
        encrypted_word = ""
        start_shift = word_index + 1  # Shift starts with 1 for first word, 2 for second, etc.

        for i, char in enumerate(word):
            shift = start_shift + i  # Increment shift based on position
            new_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            encrypted_word += new_char

        encrypted_words.append(encrypted_word)

    return " ".join(encrypted_words)

# Example usage
plaintext = "RAG BABY"
cipher_text = encrypt_with_increment(plaintext)
print(f"Encrypted Text: {cipher_text}")