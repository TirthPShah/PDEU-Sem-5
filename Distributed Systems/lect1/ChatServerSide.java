import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class ChatServerSide {

    // Private server socket
    ServerSocket serverSocket = null;

    Socket clientSocket = null;
    PrintWriter out = null;
    BufferedReader in = null;

    public void start(int port) throws IOException {
        serverSocket = new ServerSocket(port);
        System.out.println("Server started on port " + port);
        while (true) {
            clientSocket = serverSocket.accept();
            System.out.println("Accepted connection from " + clientSocket);
            out = new PrintWriter(clientSocket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream())); // Fixed line

            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                out.println(inputLine);
                if ("exit".equals(inputLine)) {
                    break;
                }
            }

            in.close();
            out.close();
            clientSocket.close();
        }

        // serverSocket.close(); // Move this line outside the loop to close it properly
    }

    public static void main(String[] args) {
        ChatServerSide server = new ChatServerSide();
        try {
            server.start(4444);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
