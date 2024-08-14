import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ChatServer implements Runnable {

    private ServerSocket serverSocket;
    private ArrayList<ClientHandler> clients;
    private HashMap<String, ClientHandler> clientMap;  // Map to store call signs and their handlers
    private boolean done;
    private ExecutorService pool;
    private String callSign = "Server";

    public ChatServer(int port) {
        clients = new ArrayList<>();
        clientMap = new HashMap<>();
        done = false;
    }

    @Override
    public void run() {
        try {
            serverSocket = new ServerSocket(4221);
            pool = Executors.newCachedThreadPool();
            System.out.println("Server started on port 4221");

            while (!done) {
                Socket client = serverSocket.accept();
                ClientHandler clientThread = new ClientHandler(client);
                clients.add(clientThread);
                pool.execute(clientThread);
            }
        } catch (Exception e) {
            System.out.println("Error starting server: " + e.getMessage());
            e.printStackTrace();
        } finally {
            shutServer();
        }
    }

    public void broadcast(String message) {
        for (ClientHandler client : clients) {
            if (client != null) {
                client.sendMessage(message);
            }
        }
    }

    public void shutServer() {
        done = true;
        if (!serverSocket.isClosed()) {
            try {
                serverSocket.close();
            } catch (Exception e) {
                // Ignore the exception to avoid crashing the server
            }
        }
        pool.shutdown();
    }

    class ClientHandler implements Runnable {

        private BufferedReader in;
        private PrintWriter out;
        private Socket client;
        private String callSign;

        public ClientHandler(Socket client) {
            this.client = client;
            System.out.println("Client connected: " + client.getInetAddress());
        }

        @Override
        public void run() {
            try {
                out = new PrintWriter(client.getOutputStream(), true);
                in = new BufferedReader(new InputStreamReader(client.getInputStream()));

                // Read call sign
                while (callSign == null) {
                    callSign = in.readLine();
                }

                // Register the client with the call sign in the map
                synchronized (clientMap) {
                    clientMap.put(callSign, this);
                }

                System.out.println("Broadcast: User " + callSign + " has joined the chat!!");
                broadcast("User " + callSign + " has joined the chat!!");

                String inputLine;
                while ((inputLine = in.readLine()) != null) {
                    if (inputLine.equals("@exit")) {
                        System.out.println("User " + callSign + " has left the chat!!");
                        broadcast("User " + callSign + " has left the chat!!");
                        shutClient();
                        break;
                    } else if (inputLine.startsWith("@broadcast")) {
                        inputLine = inputLine.substring(10).trim();
                        broadcast(callSign + ": " + inputLine);
                    } else if (inputLine.startsWith("@list")) {
                        out.println("Users in chat: " + clientMap.keySet());
                    } else if (inputLine.startsWith("@")) {
                        String targetCallSign = inputLine.split(" ")[0].substring(1);
                        String message = inputLine.substring(targetCallSign.length() + 2);
                        sendMessageToClient(targetCallSign, callSign + ": " + message);
                    } else {
                        out.println("Invalid command. Use @broadcast or @callSign to send messages.");
                    }
                }
            } catch (Exception e) {
                System.out.println("Error handling client: " + e.getMessage());
                e.printStackTrace();
            } finally {
                shutClient();
            }
        }

        private void sendMessageToClient(String targetCallSign, String message) {
            ClientHandler targetClient;
            synchronized (clientMap) {
                targetClient = clientMap.get(targetCallSign);
            }

            if (targetClient != null) {
                targetClient.sendMessage(message);
            } else {
                sendMessage("User " + targetCallSign + " not found.");
            }
        }

        public void shutClient() {
            try {
                synchronized (clientMap) {
                    clientMap.remove(callSign);
                }
                clients.remove(this);
                in.close();
                out.close();
                if (!client.isClosed()) {
                    client.close();
                }
            } catch (Exception e) {
                System.out.println("Error shutting down client: " + callSign);
            }
        }

        public void sendMessage(String message) {
            out.println(message);
        }
    }

    public static void main(String[] args) {
        ChatServer server = new ChatServer(4221);
        server.run();
    }
}