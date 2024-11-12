import zerorpc

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b

def main():
    server = zerorpc.Server(Calculator())
    server.bind("tcp://0.0.0.0:4242")  # Bind to a port
    print("Calculator server is running on tcp://0.0.0.0:4242")
    server.run()  # Start the server

if __name__ == "__main__":
    main()
