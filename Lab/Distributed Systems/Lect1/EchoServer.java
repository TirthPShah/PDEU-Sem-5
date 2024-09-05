//22BCP230

import java.io.BufferedReader;   // Import BufferedReader for reading text from input streams
import java.io.InputStreamReader; // Import InputStreamReader for reading bytes and decoding them into characters
import java.io.PrintWriter;      // Import PrintWriter for writing formatted text to an output stream
import java.net.ServerSocket;    // Import ServerSocket for creating a server socket that listens for incoming connections
import java.net.Socket;          // Import Socket for handling client connections

public class EchoServer {

    private ServerSocket serverSocket;  // ServerSocket to listen for incoming client connections
    private Socket clientSocket;        // Socket to represent the connection to the client
    private PrintWriter out;            // PrintWriter for sending text data to the client
    private BufferedReader in;          // BufferedReader for receiving text data from the client
    private boolean running;            // Flag to control the server's running state

    public void start(int port) {
        try {
            // Create a new ServerSocket to listen on the specified port
            serverSocket = new ServerSocket(port);
            System.out.println("Server started on port " + port); // Notify that the server has started

            // Wait for a client to connect
            clientSocket = serverSocket.accept();
            System.out.println("Client connected: " + clientSocket.getInetAddress()); // Notify of client connection

            // Initialize the PrintWriter and BufferedReader for communication with the client
            out = new PrintWriter(clientSocket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

            // Send a connection success message to the client
            out.println("Connected to the server successfully!");

            running = true; // Set the running flag to true to start processing

            // Thread for server to send messages to the client
            Thread serverInputThread = new Thread(() -> {
                BufferedReader serverInput = new BufferedReader(new InputStreamReader(System.in));
                String serverMessage;
                try {
                    // Continuously read messages from the server's standard input
                    while (running && (serverMessage = serverInput.readLine()) != null) {
                        out.println("Server: " + serverMessage); // Send the server's message to the client
                    }
                } catch (Exception e) {
                    // Handle any exceptions that occur while reading from the server input
                    System.out.println("Error sending message to client: " + e.getMessage());
                }
            });
            serverInputThread.start(); // Start the thread for server input

            // Echo client messages and check for exit command
            String clientMessage;
            while (running && (clientMessage = in.readLine()) != null) {
                if (clientMessage.equals("exit()")) {
                    // If the client sends the exit command, stop the server
                    System.out.println("Client requested to exit. Shutting down...");
                    running = false;
                    stop(); // Close resources and shut down the server
                } else {
                    // Print and echo the client's message
                    System.out.println("Client: " + clientMessage);
                    out.println("Echo: " + clientMessage); // Send the echoed message back to the client
                }
            }

        } catch (Exception e) {
            // Handle any exceptions that occur during the server setup or message exchange
            System.out.println("Error in server: " + e.getMessage());
            e.printStackTrace(); // Print the stack trace for debugging purposes
        } finally {
            stop(); // Ensure resources are closed in the finally block
        }
    }

    public void stop() {
        running = false; // Set the running flag to false to stop the server
        try {
            // Close the BufferedReader, PrintWriter, Socket, and ServerSocket if they are not null
            if (in != null) in.close();
            if (out != null) out.close();
            if (clientSocket != null) clientSocket.close();
            if (serverSocket != null) serverSocket.close();
        } catch (Exception e) {
            // Handle any exceptions that occur while closing resources
            System.out.println("Error closing server: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        // Create an instance of EchoServer and start it on port 6666
        EchoServer server = new EchoServer();
        server.start(6666); // Change the port as needed
    }
}
