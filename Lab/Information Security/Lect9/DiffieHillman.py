# Diffie Hillman Key Exchange

import random

butterLootSpots = ['Akrura Bapu', 'Devashrav Kaka', 'Devak Nana', 'Shursen Dada']

class Person:

    def __init__(self, name):
        self.name = name
        self.private_key = 0

class SecurityExchangeCompany:

    def __init__(self, prime, generator):
        self.prime = prime
        self.generator = generator

    def requestPublicKey(self, person):
        person.private_key = random.randint(1, 100)
        return (self.generator ** person.private_key) % self.prime
    
    def computeSharedKey(self, person, publicKey):
        return (publicKey ** person.private_key) % self.prime

class Channel:

    def __init__(self, person1, person2, sharedKey):
        self.person1 = person1
        self.person2 = person2
        self.sharedKey = sharedKey % 256

    def messagePassing(self, sender, receiver):
        message = [random.randint(1, 100)]
        temp = "Today's loot spot is " + random.choice(butterLootSpots) + "'s house."
        for c in temp:
            message.append(ord(c) ^ self.sharedKey)
        message.append(random.randint(1, 100))
        print("Message sent by ", sender.name, " to ", receiver.name, ": ", message)
        return message

    def decryptMessage(self, message):
        # Start from index 1 to skip the first random integer
        decrypted_message = []
        for c in message[1:-1]:  # Skip the first and the last element
            decrypted_message.append(chr(c ^ self.sharedKey))  # Correctly decrypt each character
        return "".join(decrypted_message)  # Join the list into a string


def main():

    prime = 13147
    generator = 5

    krishna = Person("Krishna")
    sudama = Person("Sudama")
    pundirka = Person("Pundirka")
    balram = Person("Balram")

    sec = SecurityExchangeCompany(prime, generator)

    krishnaPublicKey = sec.requestPublicKey(krishna)
    sudamaPublicKey = sec.requestPublicKey(sudama)
    pundirkaPublicKey = sec.requestPublicKey(pundirka)
    balramPublicKey = sec.requestPublicKey(balram)

    print("\n\nKrishna Public Key: ", krishnaPublicKey)
    print("Sudama Public Key: ", sudamaPublicKey)
    print("Pundirka Public Key: ", pundirkaPublicKey)
    print("Balram Public Key: ", balramPublicKey)

    krishnaSudamaSharedKey = sec.computeSharedKey(krishna, sudamaPublicKey)
    pundirkaBalramSharedKey = sec.computeSharedKey(pundirka, balramPublicKey)
    sudamaBalramSharedKey = sec.computeSharedKey(sudama, balramPublicKey)
    krishnaBalramSharedKey = sec.computeSharedKey(krishna, balramPublicKey)

    print("\n-------- Eavesdropper don't know the shared keys -------", end="\n\n")

    print("Krishna-Sudama Shared Key: ", krishnaSudamaSharedKey)
    print("Pundirka-Balram Shared Key: ", pundirkaBalramSharedKey)
    print("Sudama-Balram Shared Key: ", sudamaBalramSharedKey)
    print("Krishna-Balram Shared Key: ", krishnaBalramSharedKey)


    print("\n\n--------------------------------------------\n\n")

    print("Channels available to eavesdrop:")
    print("1. Krishna-Sudama")
    krishnaSudamaChannel = Channel(krishna, sudama, krishnaSudamaSharedKey)
    print("2. Pundirka-Balram")
    pundirkaBalramChannel = Channel(pundirka, balram, pundirkaBalramSharedKey)
    print("3. Sudama-Balram")
    sudamaBalramChannel = Channel(sudama, balram, sudamaBalramSharedKey)
    print("4. Krishna-Balram")
    krishnaBalramChannel = Channel(krishna, balram, krishnaBalramSharedKey)



    choice = int(input("\nEnter your choice: "))

    print("\n\n--------------------------------------------\n\n")

    if choice == 1:
        print("Eavesdropper listening to Krishna-Sudama Conversational Channel")
        print("\nAvailable Informations: \n")

        print("Krishna Public Key: ", krishnaPublicKey)
        print("Sudama Public Key: ", sudamaPublicKey)
        print("Prime: ", prime)
        print("Generator: ", generator, end='\n')

        listened = krishnaSudamaChannel.messagePassing(krishna, sudama)
        print("\nListened Message: ", listened)

        print("\n\nEavesdropper can not decrypt the message as he don't know the shared key: \n\n")

        print("Decrypted Message: ", krishnaSudamaChannel.decryptMessage(listened))

    elif choice == 2:

        print("Eavesdropper listening to Pundirka-Balram Conversational Channel")
        print("\nAvailable Informations: \n")

        print("Pundirka Public Key: ", pundirkaPublicKey)
        print("Balram Public Key: ", balramPublicKey)
        print("Prime: ", prime)
        print("Generator: ", generator, end='\n')

        listened = pundirkaBalramChannel.messagePassing(pundirka, balram)
        print("\nListened Message: ", listened)

        print("\n\nEavesdropper can not decrypt the message as he don't know the shared key: \n\n")

        print("Decrypted Message: ", pundirkaBalramChannel.decryptMessage(listened))

    elif choice == 3:

        print("Eavesdropper listening to Sudama-Balram Conversational Channel")
        print("\nAvailable Informations: \n")

        print("Sudama Public Key: ", sudamaPublicKey)
        print("Balram Public Key: ", balramPublicKey)
        print("Prime: ", prime)
        print("Generator: ", generator, end='\n')

        listened = sudamaBalramChannel.messagePassing(sudama, balram)
        print("\nListened Message: ", listened)

        print("\n\nEavesdropper can not decrypt the message as he don't know the shared key: \n\n")

        print("Decrypted Message: ", sudamaBalramChannel.decryptMessage(listened))

    elif choice == 4:

        print("Eavesdropper listening to Krishna-Balram Conversational Channel")
        print("\nAvailable Informations: \n")

        print("Krishna Public Key: ", krishnaPublicKey)
        print("Balram Public Key: ", balramPublicKey)
        print("Prime: ", prime)
        print("Generator: ", generator, end='\n')

        listened = krishnaBalramChannel.messagePassing(krishna, balram)
        print("\nListened Message: ", listened)

        print("\n\nEavesdropper can not decrypt the message as he don't know the shared key: \n\n")

        print("Decrypted Message: ", krishnaBalramChannel.decryptMessage(listened))

    else:
        print("Exit")

    print("\n\n--------------------------------------------\n\n")

if __name__ == "__main__":
    main()