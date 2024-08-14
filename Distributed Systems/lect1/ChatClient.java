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

    public void startConnection(String ip, int port) throws IOException {
        clientSocket = new Socket(ip, port);
        out = new PrintWriter(clientSocket.getOutputStream(), true);
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
    }

    public void sendMessage(String msg) {
        out.println(msg);  // Send message without waiting for a response
    }

    public void stopConnection() throws IOException {
        in.close();
        out.close();
        clientSocket.close();
    }

    public void run() {
        
        try {
            startConnection("localhost", 4221);

            // Thread to handle incoming messages from the server
            new Thread(() -> {
                try {
                    String serverMessage;
                    while ((serverMessage = in.readLine()) != null) {

                        // Clear the current line and then print the server message
                        System.out.println("\033[2K");
                        System.out.println(serverMessage);
                        System.out.print(callSign + ": ");
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }).start();

            BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
            String userInput;
            System.out.print("Enter your call sign: ");
            callSign = stdIn.readLine();
            callSignSet = true;
            sendMessage(callSign);  // Send the call sign to the server

            System.out.println("Type your messages (type '@exit' to quit):");
            System.out.print(callSign + ": ");

            while ((userInput = stdIn.readLine()) != null) {
                sendMessage(userInput);
                if ("@exit".equalsIgnoreCase(userInput)) {
                    break;
                }
                System.out.print(callSign + ": ");
            }

            stopConnection();
            stdIn.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        ChatClient client = new ChatClient();
        client.run();
    }
}
