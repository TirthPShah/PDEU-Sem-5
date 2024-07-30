import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class ConcurrentEchoClientSide {

    private Socket clientSocket;
    private PrintWriter out;
    private BufferedReader in;

    public void startConnection(String ip, int port) throws IOException {
        clientSocket = new Socket(ip, port);
        out = new PrintWriter(clientSocket.getOutputStream(), true);
        in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
    }

    public String sendMessage(String msg) throws IOException {
        out.println(msg);
        return in.readLine();
    }

    public void stopConnection() throws IOException {
        in.close();
        out.close();
        clientSocket.close();
    }

    public static void main(String[] args) {
        ConcurrentEchoClientSide client = new ConcurrentEchoClientSide();
        try {
            client.startConnection("127.0.0.1", 4444);

            BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));
            String userInput;
            System.out.println("Type your messages (type 'exit' to quit):");
            System.out.print("Client: ");

            while ((userInput = stdIn.readLine()) != "exit") {
                String response = client.sendMessage(userInput);
                System.out.println("Server response: " + response);
                if ("exit".equalsIgnoreCase(userInput)) {
                    break;
                }
                System.out.print("Client: ");
            }

            client.stopConnection();
            stdIn.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
