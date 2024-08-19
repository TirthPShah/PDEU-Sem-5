import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ChatServer implements Runnable {

    private ServerSocket serverSocket;
    private ArrayList<ClientHandler> clients;
    private HashMap<String, ClientHandler> clientMap;  // Map to store call signs and their handlers
    private boolean done;
    private ExecutorService pool;

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
            log("Server started on port 4221");

            while (!done) {
                Socket client = serverSocket.accept();
                ClientHandler clientThread = new ClientHandler(client);
                clients.add(clientThread);
                pool.execute(clientThread);
            }
        } catch (Exception e) {
            log("Error starting server: " + e.getMessage());
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

    private void log(String message) {
        String timestamp = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
        System.out.println("[" + timestamp + "] " + message);
    }

    class TimeoutHandler implements Runnable {
        private ClientHandler clientHandler;
        private volatile boolean active;

        public TimeoutHandler(ClientHandler clientHandler) {
            this.clientHandler = clientHandler;
            this.active = true;
        }

        @Override
        public void run() {
            try {
                while (active) {
                    TimeUnit.MINUTES.sleep(1);
                    if (active) {
                        log("User " + clientHandler.getCallSign() + " has been inactive for 1 minute. Disconnecting...");
                        clientHandler.sendMessage("You have been inactive for 1 minute. Disconnecting... Exit and reconnect to chat again.");
                        clientHandler.shutClient();
                        break;
                    }
                }
            } catch (InterruptedException e) {
                log("Timeout interrupted for user " + clientHandler.getCallSign());
            }
        }

        public void reset() {
            active = false;
            active = true;  // Reset the activity flag to true
        }
    }

    class ClientHandler implements Runnable {

        private BufferedReader in;
        private PrintWriter out;
        private Socket client;
        private String callSign;
        private TimeoutHandler timeoutHandler;

        public ClientHandler(Socket client) {
            this.client = client;
            log("Client connected: " + client.getInetAddress());
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

                // Initialize and start the timeout handler
                timeoutHandler = new TimeoutHandler(this);
                pool.execute(timeoutHandler);

                log("Broadcast: User " + callSign + " has joined the chat!!");
                broadcast("User " + callSign + " has joined the chat!!");

                String inputLine;
                while ((inputLine = in.readLine()) != null) {
                    timeoutHandler.reset();  // Reset the timeout on any client activity
                    if (inputLine.equals("@exit")) {
                        log("User " + callSign + " has left the chat!!");
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
                log("Error handling client: " + e.getMessage());
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
                log("Error shutting down client: " + callSign);
            }
        }

        public void sendMessage(String message) {
            out.println(message);
        }

        public String getCallSign() {
            return callSign;
        }
    }

    public static void main(String[] args) {
        ChatServer server = new ChatServer(4221);
        server.run();
    }
}
