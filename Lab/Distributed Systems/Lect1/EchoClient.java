//22BCP230

import java.io.BufferedReader;   // Import BufferedReader for reading text from input streams
import java.io.InputStreamReader; // Import InputStreamReader for reading bytes and decoding them into characters
import java.io.PrintWriter;      // Import PrintWriter for writing formatted text to an output stream
import java.net.Socket;          // Import Socket for creating a client socket connection to the server

public class EchoClient {

    private Socket clientSocket;  // Socket to represent the connection to the server
    private PrintWriter out;      // PrintWriter for sending text data to the server
    private BufferedReader in;    // BufferedReader for receiving text data from the server
    private boolean running;      // Flag to control the client’s running state

    public void startConnection(String ip, int port) {
        try {
            // Create a new socket to connect to the server at the specified IP address and port
            clientSocket = new Socket(ip, port);
            // Initialize the PrintWriter to send data to the server
            out = new PrintWriter(clientSocket.getOutputStream(), true);
            // Initialize the BufferedReader to receive data from the server
            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

            // Print the server's connection success message (assumed to be the first line received)
            System.out.println(in.readLine());

            running = true;  // Set the running flag to true to start processing

            // Thread to listen for incoming messages from the server
            Thread serverListenerThread = new Thread(() -> {
                String serverMessage;
                try {
                    // Continuously read messages from the server as long as the client is running
                    while (running && (serverMessage = in.readLine()) != null) {
                        System.out.println("\033[2K");  // Clear the current line in the console
                        System.out.println(serverMessage); // Print the received message from the server
                        System.out.print("Client: "); // Prompt the user for input
                    }
                } catch (Exception e) {
                    // Handle any exceptions that occur while reading from the server
                    System.out.println("Disconnected from server.");
                }
            });
            serverListenerThread.start(); // Start the thread to listen for server messages

            // Read user input from the console and send it to the server
            BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
            String userInput;
            while (running && (userInput = stdIn.readLine()) != null) {
                if (userInput.equals("exit()")) {
                    // If user input is "exit()", notify the server to shut down and stop the client
                    out.println("exit()");
                    running = false;
                    stopConnection(); // Close the connection
                    break; // Exit the loop
                } else {
                    // Move the cursor up one line to overwrite the prompt
                    System.out.print("\033[1A");
                    // Print the user's input prefixed with "Client: "
                    System.out.println("Client: " + userInput);
                    // Send the user input to the server
                    out.println(userInput);
                    // Prompt the user for new input
                    System.out.print("Client: ");
                }
            }

        } catch (Exception e) {
            // Handle any exceptions that occur during the connection setup or message exchange
            System.out.println("Error in client: " + e.getMessage());
            e.printStackTrace(); // Print the stack trace for debugging purposes
        }
    }

    public void stopConnection() {
        running = false; // Set the running flag to false to stop the client
        try {
            // Close the BufferedReader, PrintWriter, and Socket if they are not null
            if (in != null) in.close();
            if (out != null) out.close();
            if (clientSocket != null) clientSocket.close();
        } catch (Exception e) {
            // Handle any exceptions that occur while closing resources
            System.out.println("Error closing connection: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        // Create an instance of EchoClient and start the connection to the server at localhost on port 6666
        EchoClient client = new EchoClient();
        client.startConnection("localhost", 6666); // Change the IP and port as needed
    }
}
