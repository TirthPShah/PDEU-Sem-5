import java.net.DatagramSocket;
import java.net.DatagramPacket;

public class UDPServer {
    public static void main(String[] args) {

        DatagramSocket socket = null;

        try {

            socket = new DatagramSocket(Integer.parseInt(args[0]));
            System.out.println("Server started on port " + args[0]);

            while(true) {

                byte[] recievingBuffer = new byte[1024];
                DatagramPacket recievedPacket = new DatagramPacket(recievingBuffer, recievingBuffer.length);
                socket.receive(recievedPacket);

                String message = new String(recievedPacket.getData(), 0, recievedPacket.getLength());
                System.out.println("Client: " + message);

                byte[] sendingBuffer = new byte[1024];
                String response = "Server noticed your message: " + message;
                sendingBuffer = response.getBytes();
                DatagramPacket sendingPacket = new DatagramPacket(sendingBuffer, sendingBuffer.length, recievedPacket.getAddress(), recievedPacket.getPort());
                socket.send(sendingPacket);

                System.out.println("Responseded to client: " + response);

                if(message.equals("exit")) {
                    System.out.println("Server shutting down...");
                    break;
                }
            }

        } catch (Exception e) {
            System.err.println(e.getMessage());
        } finally {
            if(socket != null && !socket.isClosed()) {
                socket.close();
            }
        }
    }
}