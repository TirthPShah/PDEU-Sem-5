import random

butterLootSpots = ['Akrura Bapu', 'Devashrav Kaka', 'Devak Nana', 'Shursen Dada']

class Person:
    def __init__(self, name):
        self.name = name
        self.private_key = 0
        self.public_key = 0

class SecurityExchangeCompany:
    def __init__(self, prime, generator, noise):
        self.prime = prime
        self.generator = generator
        self.noise = noise  # Quirky noise factor

    def requestPublicKey(self, person):
        person.private_key = random.randint(1, 100)
        raw_public_key = pow(self.generator, person.private_key, self.prime)  # Generate raw public key
        # Add noise to the public key in a consistent way
        person.public_key = (raw_public_key + self.noise) % self.prime
        return person.public_key

    def computeSharedKey(self, person, public_key):
        # Compute shared key consistently
        # Here, we remove the noise from the public key to ensure the keys match
        public_key_adjusted = (public_key - self.noise + self.prime) % self.prime
        return pow(public_key_adjusted, person.private_key, self.prime)

class Channel:
    def __init__(self, person1, person2, sharedKey, prime, generator):
        self.person1 = person1
        self.person2 = person2
        self.sharedKey = sharedKey % 256
        self.prime = prime
        self.generator = generator

    def messagePassing(self, sender, receiver):
        message = [random.randint(1, 100)]
        temp = "Today's loot spot is " + random.choice(butterLootSpots) + "'s house."
        random.seed(self.sharedKey)
        for c in temp:
            message.append(ord(c) ^ self.sharedKey ^ random.randint(1, 100))
        message.append(random.randint(1, 100))
        print(f"Message sent by {sender.name} to {receiver.name}: {message}")
        return message

    def decryptMessage(self, message):
        decrypted_message = []
        random.seed(self.sharedKey)
        for c in message[1:-1]:
            decrypted_message.append(chr(c ^ self.sharedKey ^ random.randint(1, 100)))
        return "".join(decrypted_message)

def main():
    prime = 23  # A small prime number for simplicity
    generator = 5  # Generator value
    noise = 2  # Quirky noise factor

    # Initialize participants
    krishna = Person("Krishna")
    sudama = Person("Sudama")

    # Create the security exchange company
    sec = SecurityExchangeCompany(prime, generator, noise)

    # Exchange public keys
    krishna.public_key = sec.requestPublicKey(krishna)
    sudama.public_key = sec.requestPublicKey(sudama)

    print("\nKrishna's Public Key:", krishna.public_key)
    print("Sudama's Public Key:", sudama.public_key)

    # Compute shared keys with the corrected formula
    krishnaSudamaSharedKey = sec.computeSharedKey(krishna, sudama.public_key)
    sudamaKrishnaSharedKey = sec.computeSharedKey(sudama, krishna.public_key)

    print("\nKrishna-Sudama Shared Key:", krishnaSudamaSharedKey)
    print("Sudama-Krishna Shared Key:", sudamaKrishnaSharedKey)

    # Create a communication channel and exchange messages
    channel = Channel(krishna, sudama, krishnaSudamaSharedKey, prime, generator)

    message = channel.messagePassing(krishna, sudama)
    print("\nEavesdropped Message:", message)

    decrypted_message = channel.decryptMessage(message)
    print("\nDecrypted Message:", decrypted_message)

if __name__ == "__main__":
    main()
