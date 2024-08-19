import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class ChatClient {

    private Socket clientSocket;
    private PrintWriter out;
    private BufferedReader in;
    private boolean callSignSet = false;
    private String callSign = "Client";
    private String serverIp = "localhost";
    private int serverPort = 4221;
    private Thread serverListenerThread;

    public void startConnection(String ip, int port) throws IOException {
        clientSocket = new Socket(ip, port);
        out = new PrintWriter(clientSocket.getOutputStream(), true);
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        System.out.println("Connected to server at " + ip + ":" + port);
    }

    public void sendMessage(String msg) {
        if (out != null) {
            out.println(msg);
        }
    }

    public void stopConnection() {
        try {
            if (in != null) in.close();
            if (out != null) out.close();
            if (clientSocket != null) clientSocket.close();
        } catch (IOException e) {
            System.out.println("Error closing connection: " + e.getMessage());
        }
    }


    public void startServerListener() {
        serverListenerThread = new Thread(() -> {
            try {
                String serverMessage;
                while ((serverMessage = in.readLine()) != null) {
                    System.out.println("\033[2K");  // Clear the current line
                    System.out.println(serverMessage);
                    System.out.print(callSign + ": ");
                }
            } catch (IOException e) {
                System.out.println("Disconnected from server.");
            }
        });
        serverListenerThread.start();
    }

    public void run() {
        try {
            startConnection(serverIp, serverPort);
            startServerListener();  // Start listening to server messages

            BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
            String userInput;
            if (!callSignSet) {
                System.out.print("Enter Your Call Sign: ");
                callSign = stdIn.readLine();
                callSignSet = true;
                sendMessage(callSign);  // Send the call sign to the server
            }

            System.out.println("Type your messages (type '@exit' to quit, \n\033[26G'@list' to list all the available persons to chat, \n\033[26G'@broadcast' to send a message to all available persons, \n\033[26G'@CallSign' replace CallSign to the call sign of the person you want to do 1-1 chat):");
            System.out.print(callSign + ": ");

            while ((userInput = stdIn.readLine()) != null) {
                if ("@exit".equalsIgnoreCase(userInput)) {
                    sendMessage(userInput);
                    break;
                } else {
                    sendMessage(userInput);
                }
                System.out.print(callSign + ": ");
            }

            stopConnection();
            stdIn.close();
        } catch (IOException e) {
            System.out.println("Failed to connect to server: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        ChatClient client = new ChatClient();
        client.run();
    }
}
