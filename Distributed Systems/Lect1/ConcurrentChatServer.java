import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class ConcurrentChatServer {

    private ArrayList<ServerThread> serverThreads = new ArrayList<>();
    private int port = 4444;

    public void startServer() {
        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Server started on port " + port);
            while (true) {
                Socket socket = serverSocket.accept();
                ServerThread serverThread = new ServerThread(socket, serverThreads);
                serverThreads.add(serverThread);
                serverThread.start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        ConcurrentChatServer server = new ConcurrentChatServer();
        server.startServer();
    }

    public class ServerThread extends Thread {

        private PrintWriter out;
        private BufferedReader in;
        private Socket socket;
        private ArrayList<ServerThread> serverThreads;

        public ServerThread(Socket socket, ArrayList<ServerThread> serverThreads) throws IOException {
            this.socket = socket;
            this.serverThreads = serverThreads;
            this.in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            this.out = new PrintWriter(socket.getOutputStream(), true);
        }

        @Override
        public void run() {
            try {
                String message;
                while ((message = in.readLine()) != null) {
                    if (message.equalsIgnoreCase("exit")) {
                        break;
                    }
                        for (ServerThread serverThread : serverThreads) {
                            serverThread.out.println(message);
                        }
                    System.out.println("Server received: " + message);
                }
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                try {
                    in.close();
                    out.close();
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
