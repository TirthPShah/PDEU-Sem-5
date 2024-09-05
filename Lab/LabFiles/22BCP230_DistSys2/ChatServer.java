//22BCP230

import java.io.BufferedReader;    // Import BufferedReader for reading text from input streams
import java.io.IOException;      // Import IOException for handling input/output errors
import java.io.InputStreamReader; // Import InputStreamReader for reading bytes and decoding them into characters
import java.io.PrintWriter;      // Import PrintWriter for writing formatted text to an output stream
import java.net.ServerSocket;    // Import ServerSocket for creating a server socket
import java.net.Socket;          // Import Socket for handling client connections
import java.text.SimpleDateFormat; // Import SimpleDateFormat for formatting timestamps
import java.util.ArrayList;      // Import ArrayList for storing client handlers
import java.util.Date;           // Import Date for handling date and time
import java.util.HashMap;        // Import HashMap for storing call signs and client handlers
import java.util.concurrent.ExecutorService; // Import ExecutorService for managing a pool of threads
import java.util.concurrent.Executors;      // Import Executors for creating thread pools
import java.util.concurrent.TimeUnit;        // Import TimeUnit for handling time-based operations

public class ChatServer implements Runnable {

    private ServerSocket serverSocket;    // ServerSocket for listening for incoming client connections
    private ArrayList<ClientHandler> clients; // List to store active client handlers
    private HashMap<String, ClientHandler> clientMap; // Map to store call signs and their handlers
    private boolean done;                // Flag to indicate if the server should stop
    private ExecutorService pool;        // Thread pool for managing client handler threads

    public ChatServer(int port) {
        clients = new ArrayList<>();      // Initialize the list of clients
        clientMap = new HashMap<>();      // Initialize the map for call signs
        done = false;                    // Set done flag to false initially
    }

    @Override
    public void run() {
        try {
            serverSocket = new ServerSocket(4221); // Create a server socket to listen on port 4221
            pool = Executors.newCachedThreadPool(); // Create a cached thread pool for client handlers
            log("Server started on port 4221");   // Log that the server has started

            while (!done) { // Loop until the server is stopped
                Socket client = serverSocket.accept(); // Accept an incoming client connection
                ClientHandler clientThread = new ClientHandler(client); // Create a new ClientHandler for the client
                clients.add(clientThread); // Add the client handler to the list
                pool.execute(clientThread); // Execute the client handler in a separate thread
            }
        } catch (Exception e) {
            log("Error starting server: " + e.getMessage()); // Log any errors encountered while starting the server
            e.printStackTrace(); // Print stack trace for debugging
        } finally {
            shutServer(); // Ensure the server is shut down when done
        }
    }

    // Method to broadcast a message to all connected clients
    public void broadcast(String message) {
        for (ClientHandler client : clients) { // Iterate through all client handlers
            if (client != null) {
                client.sendMessage(message); // Send the message to each client
            }
        }
    }

    // Method to shut down the server
    public void shutServer() {
        done = true; // Set done flag to true to stop the server loop
        if (!serverSocket.isClosed()) { // Check if the server socket is not closed
            try {
                serverSocket.close(); // Close the server socket
            } catch (Exception e) {
                // Ignore the exception to avoid crashing the server
            }
        }
        pool.shutdown(); // Shutdown the thread pool
    }

    // Method to log messages with a timestamp
    private void log(String message) {
        String timestamp = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date()); // Get the current timestamp
        System.out.println("[" + timestamp + "] " + message); // Print the message with the timestamp
    }

    // Inner class to handle client timeouts
    class TimeoutHandler implements Runnable {
        private ClientHandler clientHandler; // Reference to the client handler being monitored
        private volatile boolean active;     // Flag to indicate if the timeout handler is active

        public TimeoutHandler(ClientHandler clientHandler) {
            this.clientHandler = clientHandler; // Initialize the client handler
            this.active = true; // Set active flag to true initially
        }

        @Override
        public void run() {
            try {
                while (active) { // Loop while the handler is active
                    TimeUnit.MINUTES.sleep(1); // Sleep for 1 minute
                    if (active) { // Check if still active after sleep
                        log("User " + clientHandler.getCallSign() + " has been inactive for 1 minute. Disconnecting..."); // Log inactivity
                        clientHandler.sendMessage("You have been inactive for 1 minute. Disconnecting... Exit and reconnect to chat again."); // Notify client
                        clientHandler.shutClient(); // Disconnect the client
                        break; // Exit the loop
                    }
                }
            } catch (InterruptedException e) {
                log("Timeout interrupted for user " + clientHandler.getCallSign()); // Log interruption
            }
        }

        // Method to reset the timeout handler
        public void reset() {
            active = false; // Deactivate the handler
            active = true;  // Reactivate the handler
        }
    }

    // Inner class to handle individual clients
    class ClientHandler implements Runnable {

        private BufferedReader in;          // BufferedReader for reading client input
        private PrintWriter out;            // PrintWriter for sending messages to the client
        private Socket client;              // Socket representing the client connection
        private String callSign;            // Call sign of the client
        private TimeoutHandler timeoutHandler; // Timeout handler for monitoring client inactivity

        public ClientHandler(Socket client) {
            this.client = client; // Initialize the client socket
            log("Client connected: " + client.getInetAddress()); // Log client connection
        }

        @Override
        public void run() {
            try {
                out = new PrintWriter(client.getOutputStream(), true); // Initialize PrintWriter
                in = new BufferedReader(new InputStreamReader(client.getInputStream())); // Initialize BufferedReader

                // Read call sign
                while (callSign == null) {
                    callSign = in.readLine(); // Read the call sign from client input
                }

                // Register the client with the call sign in the map
                synchronized (clientMap) {
                    clientMap.put(callSign, this); // Add client to the map
                }

                // Initialize and start the timeout handler
                timeoutHandler = new TimeoutHandler(this);
                pool.execute(timeoutHandler); // Start the timeout handler in a separate thread

                log("Broadcast: User " + callSign + " has joined the chat!!"); // Log new user joining
                broadcast("User " + callSign + " has joined the chat!!"); // Notify all clients

                String inputLine;
                while ((inputLine = in.readLine()) != null) { // Read messages from client
                    timeoutHandler.reset();  // Reset the timeout on any client activity
                    if (inputLine.equals("@exit")) { // Check for exit command
                        log("User " + callSign + " has left the chat!!"); // Log user leaving
                        broadcast("User " + callSign + " has left the chat!!"); // Notify all clients
                        shutClient(); // Disconnect the client
                        break; // Exit the loop
                    } else if (inputLine.startsWith("@broadcast")) { // Check for broadcast command
                        inputLine = inputLine.substring(10).trim(); // Extract the message
                        broadcast(callSign + ": " + inputLine); // Broadcast the message
                    } else if (inputLine.startsWith("@list")) { // Check for list command
                        out.println("Users in chat: " + clientMap.keySet()); // Send list of users to client
                    } else if (inputLine.startsWith("@")) { // Check for direct message command
                        String targetCallSign = inputLine.split(" ")[0].substring(1); // Extract target call sign
                        String message = inputLine.substring(targetCallSign.length() + 2); // Extract message
                        sendMessageToClient(targetCallSign, callSign + ": " + message); // Send message to target client
                    } else {
                        out.println("Invalid command. Use @broadcast or @callSign to send messages."); // Send error message
                    }
                }
            } catch (Exception e) {
                log("Error handling client: " + e.getMessage()); // Log any errors encountered
                e.printStackTrace(); // Print stack trace for debugging
            } finally {
                shutClient(); // Ensure client is disconnected when done
            }
        }

        // Method to send a message to a specific client
        private void sendMessageToClient(String targetCallSign, String message) {
            ClientHandler targetClient;
            synchronized (clientMap) {
                targetClient = clientMap.get(targetCallSign); // Get the target client handler
            }

            if (targetClient != null) {
                targetClient.sendMessage(message); // Send the message to the target client
            } else {
                sendMessage("User " + targetCallSign + " not found."); // Send error message if user not found
            }
        }

        // Method to disconnect the client
        public void shutClient() {
            try {
                synchronized (clientMap) {
                    clientMap.remove(callSign); // Remove the client from the map
                }
                clients.remove(this); // Remove the client handler from the list
                in.close(); // Close the BufferedReader
                out.close(); // Close the PrintWriter
                if (!client.isClosed()) {
                    client.close(); // Close the client socket
                }
            } catch (Exception e) {
                log("Error shutting down client: " + callSign); // Log any errors encountered
            }
        }

        // Method to send a message to the client
        public void sendMessage(String message) {
            out.println(message); // Send the message to the client
        }

        // Method to get the call sign of the client
        public String getCallSign() {
            return callSign; // Return the call sign
        }
    }

    // Main method to start the server
    public static void main(String[] args) {
        ChatServer server = new ChatServer(4221); // Create an instance of ChatServer
        server.run(); // Start the server
    }
}
