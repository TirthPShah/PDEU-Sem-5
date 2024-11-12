import java.net.ServerSocket;

public class SocketServer {

    public void start(int port) {
        try {
            ServerSocket server = new ServerSocket(port);
        } catch (Exception e) {
            System.out.println("Error starting server: " + e.getMessage());
        }
    }
    public static void main(String[] args) {
        
    }
}