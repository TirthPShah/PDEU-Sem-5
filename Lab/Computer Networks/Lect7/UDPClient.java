import java.net.DatagramSocket;
import java.net.DatagramPacket;
import java.util.Scanner;
import java.net.InetAddress;

public class UDPClient {
    public static void main(String[] args) {
        
        DatagramSocket socket = null;
        Scanner scanner = new Scanner(System.in);

        try {

            String serverIP = args[0];
            int serverPort = Integer.parseInt(args[1]);
            socket = new DatagramSocket();


            while(true) {
                System.out.print("Enter message: ");
                String message = scanner.nextLine();

                byte[] sendingBuffer = new byte[1024];
                sendingBuffer = message.getBytes();
                DatagramPacket sendingPacket = new DatagramPacket(sendingBuffer, sendingBuffer.length, InetAddress.getByName(serverIP), serverPort);
                socket.send(sendingPacket);

                byte[] recievingBuffer = new byte[1024];
                DatagramPacket recievedPacket = new DatagramPacket(recievingBuffer, recievingBuffer.length);
                socket.receive(recievedPacket);

                String response = new String(recievedPacket.getData(), 0, recievedPacket.getLength());
                System.out.println("Server: " + response);

                if(message.equals("exit")) {
                    System.out.println("Client shutting down...");
                    break;
                }
            }
        } catch (Exception e) {
            System.err.println(e.getMessage());
        } finally {
            if(socket != null && !socket.isClosed()) {
                socket.close();
                scanner.close();
            }   
        }
    }
}