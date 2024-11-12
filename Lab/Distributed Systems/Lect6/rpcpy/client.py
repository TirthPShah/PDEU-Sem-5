import zerorpc

def main():
    client = zerorpc.Client()
    client.connect("tcp://127.0.0.1:4242")  # Connect to the server

    while True:
        print("\nAvailable operations:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")

        choice = int(input("Choose an operation (1-5): "))
        print("You chose: {}".format(choice))  # Debug print

        if choice == 5:
            print("Exiting...")
            break

        a = float(input("Enter the first number: "))
        b = float(input("Enter the second number: "))

        try:
            if choice == 1:
                result = client.add(a, b)
                print("Result: {} + {} = {}".format(a, b, result))
            elif choice == 2:
                result = client.subtract(a, b)
                print("Result: {} - {} = {}".format(a, b, result))
            elif choice == 3:
                result = client.multiply(a, b)
                print("Result: {} * {} = {}".format(a, b, result))
            elif choice == 4:
                result = client.divide(a, b)
                print("Result: {} / {} = {}".format(a, b, result))
            else:
                print("Invalid choice. Please choose a valid operation.")

        except zerorpc.exceptions.RemoteError as e:
            print("Error: {}".format(e))

if __name__ == "__main__":
    main()
