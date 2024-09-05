//22BCP230

import java.io.BufferedReader;    // Import BufferedReader for reading text from input streams
import java.io.IOException;      // Import IOException for handling input/output errors
import java.io.InputStreamReader; // Import InputStreamReader for reading bytes and decoding them into characters
import java.io.PrintWriter;      // Import PrintWriter for writing formatted text to an output stream
import java.net.Socket;          // Import Socket for handling client connections

public class ChatClient {

    private Socket clientSocket;      // Socket for the client to connect to the server
    private PrintWriter out;          // PrintWriter for sending text data to the server
    private BufferedReader in;        // BufferedReader for receiving text data from the server
    private boolean callSignSet = false; // Flag to check if the call sign has been set
    private String callSign = "Client"; // Default call sign for the client
    private String serverIp = "localhost"; // IP address of the server to connect to
    private int serverPort = 4221;       // Port number of the server to connect to
    private Thread serverListenerThread; // Thread to listen for messages from the server

    // Method to start a connection to the server
    public void startConnection(String ip, int port) throws IOException {
        clientSocket = new Socket(ip, port); // Create a new socket to connect to the server
        out = new PrintWriter(clientSocket.getOutputStream(), true); // Initialize PrintWriter for sending data
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream())); // Initialize BufferedReader for receiving data
        System.out.println("Connected to server at " + ip + ":" + port); // Print connection success message
    }

    // Method to send a message to the server
    public void sendMessage(String msg) {
        if (out != null) {
            out.println(msg); // Send the message to the server
        }
    }

    // Method to close the connection to the server
    public void stopConnection() {
        try {
            if (in != null) in.close(); // Close the BufferedReader
            if (out != null) out.close(); // Close the PrintWriter
            if (clientSocket != null) clientSocket.close(); // Close the Socket
        } catch (IOException e) {
            System.out.println("Error closing connection: " + e.getMessage()); // Print error message if closing fails
        }
    }

    // Method to start listening for messages from the server
    public void startServerListener() {
        serverListenerThread = new Thread(() -> {
            try {
                String serverMessage;
                while ((serverMessage = in.readLine()) != null) {
                    System.out.println("\033[2K");  // Clear the current line
                    System.out.println(serverMessage); // Print the message received from the server
                    System.out.print(callSign + ": "); // Print the prompt for user input
                }
            } catch (IOException e) {
                System.out.println("Disconnected from server."); // Print message if disconnected from server
            }
        });
        serverListenerThread.start(); // Start the thread to listen for server messages
    }

    // Main method to run the client application
    public void run() {
        try {
            startConnection(serverIp, serverPort); // Start connection to the server
            startServerListener();  // Start listening to server messages

            BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in)); // BufferedReader for reading user input
            String userInput;
            if (!callSignSet) {
                System.out.print("Enter Your Call Sign: "); // Prompt user to enter their call sign
                callSign = stdIn.readLine(); // Read the call sign from user input
                callSignSet = true; // Set the flag indicating that the call sign has been set
                sendMessage(callSign);  // Send the call sign to the server
            }

            // Print message explaining how to use the chat commands
            System.out.println("Type your messages (type '@exit' to quit, \n\033[26G'@list' to list all the available persons to chat, \n\033[26G'@broadcast' to send a message to all available persons, \n\033[26G'@CallSign' replace CallSign to the call sign of the person you want to do 1-1 chat):");
            System.out.print(callSign + ": "); // Print prompt for user input

            while ((userInput = stdIn.readLine()) != null) {
                if ("@exit".equalsIgnoreCase(userInput)) {
                    sendMessage(userInput); // Send exit command to the server
                    break; // Exit the loop and terminate the client
                } else {
                    sendMessage(userInput); // Send user input to the server
                }
                System.out.print(callSign + ": "); // Print prompt for user input
            }

            stopConnection(); // Close the connection to the server
            stdIn.close(); // Close the BufferedReader for user input
        } catch (IOException e) {
            System.out.println("Failed to connect to server: " + e.getMessage()); // Print error message if connection fails
        }
    }

    // Main method to start the client application
    public static void main(String[] args) {
        ChatClient client = new ChatClient(); // Create an instance of ChatClient
        client.run(); // Run the client application
    }
}
